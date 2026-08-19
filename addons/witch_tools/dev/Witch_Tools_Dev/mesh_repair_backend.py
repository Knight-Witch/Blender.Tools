import bpy
import bmesh
import math
from collections import deque
from mathutils.bvhtree import BVHTree


def _remove_spikes(bm, angle_limit):
    verts = set()
    for v in bm.verts:
        if len(v.link_faces) < 3:
            continue
        faces = [f for f in v.link_faces if f.normal.length]
        if any(a.normal.angle(b.normal) > angle_limit for i, a in enumerate(faces) for b in faces[i+1:]):
            verts.add(v)
    count = len(verts)
    if verts:
        bmesh.ops.dissolve_verts(bm, verts=list(verts), use_face_split=False, use_boundary_tear=False)
    return count


def _smooth_intersections(bm, angle_limit):
    verts = set()
    for f in bm.faces:
        if not f.normal.length:
            verts.update(f.verts)
    for e in bm.edges:
        if len(e.link_faces) > 2:
            verts.update(e.verts)
        elif len(e.link_faces) == 2:
            a, b = e.link_faces
            if a.normal.length and b.normal.length and a.normal.angle(b.normal) > angle_limit:
                verts.update(e.verts)
    count = len(verts)
    if verts:
        bmesh.ops.dissolve_verts(bm, verts=list(verts), use_face_split=False, use_boundary_tear=False)
    return count


def _face_components(bm):
    unseen = set(bm.faces)
    comps = []
    while unseen:
        seed = unseen.pop(); comp = [seed]; q = deque([seed])
        while q:
            f = q.popleft()
            for e in f.edges:
                for n in e.link_faces:
                    if n in unseen:
                        unseen.remove(n); comp.append(n); q.append(n)
        comps.append(comp)
    return comps


def _remove_small_shells(bm, threshold):
    total = max(1, len(bm.faces)); removed = 0
    for comp in _face_components(bm):
        if len(comp) < total * threshold:
            removed += 1
            bmesh.ops.delete(bm, geom=list(comp), context='FACES')
    loose_edges = [e for e in bm.edges if not e.link_faces]
    edge_count = len(loose_edges)
    if loose_edges: bmesh.ops.delete(bm, geom=loose_edges, context='EDGES')
    loose_verts = [v for v in bm.verts if not v.link_edges]
    vert_count = len(loose_verts)
    if loose_verts: bmesh.ops.delete(bm, geom=loose_verts, context='VERTS')
    return removed, edge_count, vert_count


def _fill_holes(bm):
    boundary = [e for e in bm.edges if len(e.link_faces) == 1]
    if not boundary:
        return 0
    unseen = set(boundary); holes = 0
    while unseen:
        holes += 1
        seed = unseen.pop(); q = deque(seed.verts); visited = set(seed.verts)
        while q:
            v = q.popleft()
            for e in list(unseen):
                if v in e.verts:
                    unseen.remove(e)
                    for ov in e.verts:
                        if ov not in visited:
                            visited.add(ov); q.append(ov)
    bmesh.ops.holes_fill(bm, edges=boundary, sides=0)
    return holes


def _union_overlapping_components(context, obj):
    bm = bmesh.new(); bm.from_mesh(obj.data); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    comps = _face_components(bm)
    if len(comps) < 2:
        bm.free(); return 0
    verts = [v.co.copy() for v in bm.verts]
    overlaps = 0
    for i, comp_a in enumerate(comps):
        tree_a = BVHTree.FromPolygons(verts, [[v.index for v in f.verts] for f in comp_a], all_triangles=False)
        for comp_b in comps[i+1:]:
            tree_b = BVHTree.FromPolygons(verts, [[v.index for v in f.verts] for f in comp_b], all_triangles=False)
            if tree_a and tree_b and tree_a.overlap(tree_b):
                overlaps += 1
    bm.free()
    if overlaps:
        mod = obj.modifiers.new(name='WT Intersect Volumes', type='REMESH')
        mod.mode = 'VOXEL'
        span = max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z, 0.001)
        mod.voxel_size = span / 500.0
        context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return overlaps


class LocalFaceNormal(bpy.types.Operator):
    bl_idname = 'witch_tools.mr_local_face_normal'
    bl_label = 'Unify/Flip Face Normal'
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, context): return bool(context.object and context.mode == 'EDIT_MESH')
    def execute(self, context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        selected = [f for f in bm.faces if f.select]
        before = [f.normal.copy() for f in selected]
        bpy.ops.mesh.normals_make_consistent(inside=False)
        if selected and not any(a != b.normal for a, b in zip(before, selected)):
            bpy.ops.mesh.flip_normals()
        bmesh.update_edit_mesh(context.active_object.data)
        return {'FINISHED'}


class RemeshLocalV2(bpy.types.Operator):
    bl_idname = 'witch_tools.mr_remesh_local'; bl_label = 'Remesh Selection'; bl_options = {'REGISTER','UNDO'}
    @classmethod
    def poll(cls, context): return bool(context.object and context.mode == 'EDIT_MESH')
    def execute(self, context):
        bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0, ngon=False, quadcorner='STRAIGHT_CUT')
        bpy.ops.mesh.vertices_smooth_laplacian(repeat=10, lambda_factor=1.0, lambda_border=1e-7, preserve_volume=False)
        bpy.ops.mesh.decimate(ratio=0.3)
        return {'FINISHED'}


class SmoothLocalV2(bpy.types.Operator):
    bl_idname = 'witch_tools.mr_smooth_local'; bl_label = 'Smooth Selection'; bl_options = {'REGISTER','UNDO'}
    @classmethod
    def poll(cls, context): return bool(context.object and context.mode == 'EDIT_MESH')
    def execute(self, context): bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=5); return {'FINISHED'}


class ReduceLocal(bpy.types.Operator):
    bl_idname = 'witch_tools.mr_reduce_local'; bl_label = 'Reduce Selection'; bl_options = {'REGISTER','UNDO'}
    @classmethod
    def poll(cls, context): return bool(context.object and context.mode == 'EDIT_MESH')
    def execute(self, context): bpy.ops.mesh.decimate(ratio=0.5); return {'FINISHED'}


class RefineLocal(bpy.types.Operator):
    bl_idname = 'witch_tools.mr_refine_local'; bl_label = 'Refine Selection'; bl_options = {'REGISTER','UNDO'}
    @classmethod
    def poll(cls, context): return bool(context.object and context.mode == 'EDIT_MESH')
    def execute(self, context):
        mode = tuple(context.tool_settings.mesh_select_mode)
        context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_less()
        bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0, ngon=False, quadcorner='STRAIGHT_CUT')
        bpy.ops.mesh.vertices_smooth_laplacian(repeat=10, lambda_factor=1.0, lambda_border=1e-7, preserve_volume=False)
        bpy.ops.mesh.select_more()
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        context.tool_settings.mesh_select_mode = mode
        return {'FINISHED'}


class FixMeshGlobal(bpy.types.Operator):
    bl_idname = 'witch_tools.mr_auto_fix'; bl_label = 'Auto Fix'; bl_options = {'REGISTER','UNDO'}
    @classmethod
    def poll(cls, context): return bool(context.active_object and context.active_object.type == 'MESH')
    def execute(self, context):
        props = context.scene.meshfixtool_properties
        obj = context.active_object
        prev_mode = context.mode
        props.meshfixing = True
        try:
            if context.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles()
            full = props.tri_boolean or props.quad_boolean
            if full: bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            if props.face_normal_boolean: bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            bm = bmesh.new(); bm.from_mesh(obj.data); bm.normal_update()
            n_spike = _remove_spikes(bm, math.radians(180.0 - props.spikes_angle_limit)) if full and props.spikes_boolean else 0
            n_inter = _smooth_intersections(bm, math.radians(180.0 - props.intersection_angle_limit)) if full and props.intersection_boolean else 0
            shell_count = edge_count = vert_count = 0
            if props.minor_parts_boolean:
                shell_count, edge_count, vert_count = _remove_small_shells(bm, props.minor_parts_threshold / 100.0)
            holes = _fill_holes(bm) if full and props.holes_boolean else 0
            bm.to_mesh(obj.data); obj.data.update(); bm.free()
            volumes = _union_overlapping_components(context, obj) if full and props.volume_intersection_boolean else 0
            bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles()
            if full:
                bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
                if props.quad_boolean:
                    bpy.ops.mesh.tris_convert_to_quads(face_threshold=0.698132, shape_threshold=0.698132, uvs=False, vcols=False, seam=False, sharp=False, materials=False)
            bpy.ops.mesh.select_all(action='DESELECT')
            props.sum_vertices = n_spike + n_inter + vert_count
            props.sum_edges = edge_count
            props.sum_faces = shell_count
            props.sum_holes = holes
            props.sum_volumes = volumes
        except Exception as exc:
            self.report({'ERROR'}, f'Auto Fix failed: {exc}')
            return {'CANCELLED'}
        finally:
            props.meshfixing = False
            try:
                target = 'EDIT' if prev_mode == 'EDIT_MESH' else 'OBJECT'
                if context.object and context.object.mode != target: bpy.ops.object.mode_set(mode=target)
            except Exception: pass
        return {'FINISHED'}


CLASSES = (LocalFaceNormal, RemeshLocalV2, FixMeshGlobal, SmoothLocalV2, ReduceLocal, RefineLocal)
