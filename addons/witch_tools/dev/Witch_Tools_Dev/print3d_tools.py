import bpy
import bmesh
import math
import os
from collections import deque
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy.types import Operator, PropertyGroup
from bpy.props import IntProperty, StringProperty, PointerProperty


RESULT_FIELDS = (
    ('non_manifold_edges', 'Non-manifold Edges'),
    ('bad_contiguous_edges', 'Bad Contiguous Edges'),
    ('intersect_faces', 'Intersect Faces'),
    ('shells', 'Shells'),
    ('zero_faces', 'Zero Faces'),
    ('zero_edges', 'Zero Edges'),
    ('non_flat_faces', 'Non-flat Faces'),
    ('thin_faces', 'Thin Faces'),
    ('sharp_edges', 'Sharp Edges'),
    ('overhang_faces', 'Overhang Faces'),
)


class WTPrint3DProperties(PropertyGroup):
    export_directory: StringProperty(name='Export Folder', subtype='DIR_PATH', default='//')
    non_manifold_edges: IntProperty(default=0, min=0)
    bad_contiguous_edges: IntProperty(default=0, min=0)
    intersect_faces: IntProperty(default=0, min=0)
    shells: IntProperty(default=0, min=0)
    zero_faces: IntProperty(default=0, min=0)
    zero_edges: IntProperty(default=0, min=0)
    non_flat_faces: IntProperty(default=0, min=0)
    thin_faces: IntProperty(default=0, min=0)
    sharp_edges: IntProperty(default=0, min=0)
    overhang_faces: IntProperty(default=0, min=0)
    last_analyzed_object: StringProperty(default='')


def _mesh_object(context):
    obj = context.active_object
    return obj if obj and obj.type == 'MESH' else None


def _bm_from_object(obj):
    bm = bmesh.new(); bm.from_mesh(obj.data); bm.normal_update()
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    return bm


def _count_shells(bm):
    if bm.faces:
        unseen = set(bm.faces); count = 0
        while unseen:
            count += 1; seed = unseen.pop(); q = deque([seed])
            while q:
                face = q.popleft()
                for edge in face.edges:
                    for other in edge.link_faces:
                        if other in unseen: unseen.remove(other); q.append(other)
        return count
    if bm.edges:
        unseen = set(bm.verts); count = 0
        while unseen:
            count += 1; seed = unseen.pop(); q = deque([seed])
            while q:
                vert = q.popleft()
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    if other in unseen: unseen.remove(other); q.append(other)
        return count
    return len(bm.verts)


def _count_intersections(bm):
    if not bm.faces: return 0
    tree = BVHTree.FromBMesh(bm, epsilon=1e-7)
    if tree is None: return 0
    bad = set()
    for a, b in tree.overlap(tree):
        if a == b or a >= len(bm.faces) or b >= len(bm.faces): continue
        fa, fb = bm.faces[a], bm.faces[b]
        if any(v in fb.verts for v in fa.verts): continue
        bad.add(a); bad.add(b)
    return len(bad)


def _count_nonflat_faces(bm, threshold=math.radians(5.0)):
    bad = 0
    for face in bm.faces:
        if len(face.verts) <= 3: continue
        no = face.normal.normalized() if face.normal.length else Vector((0,0,1)); distorted = False
        for loop in face.loops:
            ln = loop.calc_normal()
            if not ln.length: continue
            if ln.dot(no) < 0: ln.negate()
            try:
                if no.angle(ln) > threshold: distorted = True; break
            except ValueError: pass
        if distorted: bad += 1
    return bad


def _count_thin_faces(bm, minimum=0.001):
    if not bm.faces: return 0
    tree = BVHTree.FromBMesh(bm, epsilon=1e-7)
    if tree is None: return 0
    bad = 0; eps = 1e-6
    for face in bm.faces:
        if not face.normal.length: continue
        center = face.calc_center_median(); normal = face.normal.normalized(); found = False
        for direction in (normal, -normal):
            hit = tree.ray_cast(center + direction * eps, direction, minimum)
            if hit and hit[0] is not None and hit[3] is not None and hit[3] != face.index and hit[2] is not None and hit[2] <= minimum:
                found = True; break
        if found: bad += 1
    return bad


class WT_OT_print3d_analyze(Operator):
    bl_idname = 'witch_tools.print3d_analyze'; bl_label = 'Check All'; bl_options = {'REGISTER'}
    bl_description = 'Run the print-focused mesh checks and refresh the Results box'
    @classmethod
    def poll(cls, context): return _mesh_object(context) is not None
    def execute(self, context):
        obj = _mesh_object(context); props = context.scene.wt_print3d
        if context.mode == 'EDIT_MESH': bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)
        bm = _bm_from_object(obj)
        try:
            props.non_manifold_edges = sum(1 for e in bm.edges if not e.is_manifold)
            props.bad_contiguous_edges = sum(1 for e in bm.edges if e.is_manifold and not e.is_contiguous)
            props.intersect_faces = _count_intersections(bm)
            props.shells = _count_shells(bm)
            props.zero_faces = sum(1 for f in bm.faces if f.calc_area() <= 1e-12)
            props.zero_edges = sum(1 for e in bm.edges if e.calc_length() <= 1e-7)
            props.non_flat_faces = _count_nonflat_faces(bm)
            props.thin_faces = _count_thin_faces(bm, 0.001)
            props.sharp_edges = sum(1 for e in bm.edges if len(e.link_faces) == 2 and e.calc_face_angle(0.0) >= math.radians(160.0))
            up = Vector((0.0,0.0,1.0)); limit = math.radians(135.0)
            props.overhang_faces = sum(1 for f in bm.faces if f.normal.length and f.normal.angle(up) > limit)
            props.last_analyzed_object = obj.name
        finally: bm.free()
        return {'FINISHED'}


class WT_OT_print3d_make_manifold(Operator):
    bl_idname = 'witch_tools.print3d_make_manifold'; bl_label = 'Make Manifold'; bl_options = {'REGISTER','UNDO'}
    bl_description = 'Merge doubles, remove degenerate/loose geometry, fill boundary holes, and recalculate normals outside'
    @classmethod
    def poll(cls, context): return _mesh_object(context) is not None
    def execute(self, context):
        obj = _mesh_object(context); prev_mode = context.mode
        try:
            if context.mode != 'EDIT_MESH': bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles(threshold=0.0001)
            bpy.ops.mesh.dissolve_degenerate(threshold=0.0001); bpy.ops.mesh.delete_loose(use_verts=True,use_edges=True,use_faces=True)
            bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_mode(type='EDGE')
            bpy.ops.mesh.select_non_manifold(extend=False,use_wire=False,use_boundary=True,use_multi_face=False,use_non_contiguous=False,use_verts=False)
            try: bpy.ops.mesh.fill_holes(sides=0)
            except Exception: pass
            bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.normals_make_consistent(inside=False)
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)
        except Exception as exc:
            self.report({'ERROR'}, f'Make Manifold failed: {exc}'); return {'CANCELLED'}
        finally:
            try:
                if prev_mode == 'OBJECT' and context.mode == 'EDIT_MESH': bpy.ops.object.mode_set(mode='OBJECT')
            except Exception: pass
        return {'FINISHED'}


class WT_OT_print3d_export_stl(Operator):
    bl_idname = 'witch_tools.print3d_export_stl'; bl_label = 'Export STL'; bl_options = {'REGISTER'}
    bl_description = 'Export selected mesh objects as one STL to the chosen folder'
    @classmethod
    def poll(cls, context): return any(o.type == 'MESH' for o in context.selected_objects)
    def execute(self, context):
        props = context.scene.wt_print3d; folder = bpy.path.abspath(props.export_directory or '//')
        try: os.makedirs(folder, exist_ok=True)
        except Exception as exc: self.report({'ERROR'}, f'Cannot create export folder: {exc}'); return {'CANCELLED'}
        selected = [o for o in context.selected_objects if o.type == 'MESH']; active = context.active_object if context.active_object in selected else selected[0]
        filename = bpy.path.clean_name(active.name if len(selected) == 1 else f'{active.name}_selection') + '.stl'; filepath = os.path.join(folder, filename)
        try:
            if hasattr(bpy.ops.wm, 'stl_export'): bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True)
            else: bpy.ops.export_mesh.stl(filepath=filepath, use_selection=True)
        except Exception as exc: self.report({'ERROR'}, f'STL export failed: {exc}'); return {'CANCELLED'}
        self.report({'INFO'}, f'Exported {filename}'); return {'FINISHED'}


CLASSES = (WTPrint3DProperties, WT_OT_print3d_analyze, WT_OT_print3d_make_manifold, WT_OT_print3d_export_stl)


def register_props(): bpy.types.Scene.wt_print3d = PointerProperty(type=WTPrint3DProperties)
def unregister_props():
    if hasattr(bpy.types.Scene, 'wt_print3d'): del bpy.types.Scene.wt_print3d
