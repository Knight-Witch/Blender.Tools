import bpy
import bmesh
import math
import os
import random
import struct
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

# Match the standard 3D Print Toolbox defaults that the integrated UI intentionally hides.
THRESHOLD_ZERO = 0.0001
ANGLE_DISTORT = math.radians(5.0)
THICKNESS_MIN = 0.001
ANGLE_SHARP = math.radians(160.0)
ANGLE_OVERHANG = math.radians(45.0)


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


def _bm_from_object(obj, transform=False, triangulate=False):
    """Copy mesh data using the same object/edit and transform semantics as 3D Print Toolbox."""
    me = obj.data
    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(me).copy()
    else:
        bm = bmesh.new()
        bm.from_mesh(me)

    if transform:
        matrix = obj.matrix_world.copy()
        if not matrix.is_identity:
            bm.transform(matrix)
            matrix.translation.zero()
            if not matrix.is_identity:
                bm.normal_update()

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces[:])

    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    return bm


def _count_shells(bm):
    if bm.faces:
        unseen = set(bm.faces)
        count = 0
        while unseen:
            count += 1
            seed = unseen.pop()
            queue = deque([seed])
            while queue:
                face = queue.popleft()
                for edge in face.edges:
                    for other in edge.link_faces:
                        if other in unseen:
                            unseen.remove(other)
                            queue.append(other)
        return count
    if bm.edges:
        unseen = set(bm.verts)
        count = 0
        while unseen:
            count += 1
            seed = unseen.pop()
            queue = deque([seed])
            while queue:
                vert = queue.popleft()
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    if other in unseen:
                        unseen.remove(other)
                        queue.append(other)
        return count
    return len(bm.verts)


def _count_intersections(obj):
    """Match 3D Print Toolbox self-intersection BVH semantics."""
    if not obj.data.polygons:
        return 0
    bm = _bm_from_object(obj, transform=False, triangulate=False)
    try:
        tree = BVHTree.FromBMesh(bm, epsilon=0.00001)
        if tree is None:
            return 0
        overlap = tree.overlap(tree)
        return len({index for pair in overlap for index in pair})
    finally:
        bm.free()


def _face_is_distorted(face, threshold):
    normal = face.normal
    angle_fn = normal.angle
    for loop in face.loops:
        loop_normal = loop.calc_normal()
        if loop_normal.dot(normal) < 0.0:
            loop_normal.negate()
        if angle_fn(loop_normal, 1000.0) > threshold:
            return True
    return False


def _count_nonflat_faces(obj, threshold=ANGLE_DISTORT):
    bm = _bm_from_object(obj, transform=True, triangulate=False)
    try:
        bm.normal_update()
        return sum(1 for face in bm.faces if _face_is_distorted(face, threshold))
    finally:
        bm.free()


def _face_points_random(face, num_points=1, margin=0.05):
    """Deterministic interior samples matching the 3D Print Toolbox thickness check."""
    rng = random.Random(face.index)
    uniform_args = (margin, 1.0 - margin)
    vecs = [vert.co for vert in face.verts]
    for _ in range(num_points):
        u1 = rng.uniform(*uniform_args)
        u2 = rng.uniform(*uniform_args)
        if u1 + u2 > 1.0:
            u1 = 1.0 - u1
            u2 = 1.0 - u2
        side1 = vecs[1] - vecs[0]
        side2 = vecs[2] - vecs[0]
        yield vecs[0] + u1 * side1 + u2 * side2


def _count_thin_faces(obj, thickness=THICKNESS_MIN):
    """Match the 3D Print Toolbox six-sample, backwards ray thickness test."""
    bm = _bm_from_object(obj, transform=True, triangulate=False)
    context = bpy.context
    layer = context.view_layer
    scene_collection = context.layer_collection.collection
    me_tmp = None
    obj_tmp = None

    try:
        face_index_map_org = {face: index for index, face in enumerate(bm.faces)}
        result = bmesh.ops.triangulate(bm, faces=bm.faces[:])
        face_map = result.get('face_map', {})
        bm.faces.ensure_lookup_table()
        bm.normal_update()

        me_tmp = bpy.data.meshes.new(name='~wt_print3d_temp~')
        bm.to_mesh(me_tmp)
        obj_tmp = bpy.data.objects.new(name=me_tmp.name, object_data=me_tmp)
        scene_collection.objects.link(obj_tmp)
        layer.update()

        ray_cast = obj_tmp.ray_cast
        eps_bias = 0.0001
        faces_error = set()
        bm_faces_new = bm.faces[:]

        for face in bm_faces_new:
            normal = face.normal
            no_start = normal * eps_bias
            no_end = normal * thickness
            for point in _face_points_random(face, num_points=6):
                point_a = point - no_start
                point_b = point - no_end
                direction = point_b - point_a
                if direction.length == 0.0:
                    continue
                hit, _co, _normal, index = ray_cast(point_a, direction, distance=direction.length)
                if hit and 0 <= index < len(bm_faces_new):
                    for face_iter in (face, bm_faces_new[index]):
                        original = face_map.get(face_iter, face_iter)
                        original_index = face_index_map_org.get(original)
                        if original_index is not None:
                            faces_error.add(original_index)

        return len(faces_error)
    finally:
        bm.free()
        if obj_tmp is not None:
            try:
                if obj_tmp.name in scene_collection.objects:
                    scene_collection.objects.unlink(obj_tmp)
            except Exception:
                pass
            try:
                bpy.data.objects.remove(obj_tmp)
            except Exception:
                pass
        if me_tmp is not None:
            try:
                bpy.data.meshes.remove(me_tmp)
            except Exception:
                pass
        try:
            layer.update()
        except Exception:
            pass


def _count_sharp_edges(obj, threshold=ANGLE_SHARP):
    bm = _bm_from_object(obj, transform=True, triangulate=False)
    try:
        bm.normal_update()
        return sum(
            1 for edge in bm.edges
            if edge.is_manifold and edge.calc_face_angle_signed() > threshold
        )
    finally:
        bm.free()


def _count_overhang_faces(obj, threshold=ANGLE_OVERHANG):
    angle_overhang = (math.pi / 2.0) - threshold
    if angle_overhang == math.pi:
        return 0

    bm = _bm_from_object(obj, transform=True, triangulate=False)
    try:
        bm.normal_update()
        z_down = Vector((0.0, 0.0, -1.0))
        z_down_angle = z_down.angle
        return sum(
            1 for face in bm.faces
            if z_down_angle(face.normal, 4.0) < angle_overhang
        )
    finally:
        bm.free()


def _try_blender_stl_export(filepath):
    """Try Blender's native/current STL operator, then the legacy add-on operator."""
    errors = []

    try:
        native = getattr(bpy.ops.wm, 'stl_export', None)
        if native is not None and native.poll():
            result = native(
                filepath=filepath,
                check_existing=False,
                export_selected_objects=True,
                apply_modifiers=True,
            )
            if 'FINISHED' in result and os.path.isfile(filepath) and os.path.getsize(filepath) >= 84:
                return True, 'Blender native STL exporter'
            errors.append(f'native returned {sorted(result)}')
        else:
            errors.append('native STL exporter unavailable in current context')
    except Exception as exc:
        errors.append(f'native STL exporter: {exc}')

    try:
        legacy = getattr(bpy.ops.export_mesh, 'stl', None)
        if legacy is not None and legacy.poll():
            result = legacy(
                filepath=filepath,
                check_existing=False,
                use_selection=True,
                use_mesh_modifiers=True,
            )
            if 'FINISHED' in result and os.path.isfile(filepath) and os.path.getsize(filepath) >= 84:
                return True, 'Blender legacy STL exporter'
            errors.append(f'legacy returned {sorted(result)}')
        else:
            errors.append('legacy STL exporter unavailable in current context')
    except Exception as exc:
        errors.append(f'legacy STL exporter: {exc}')

    return False, '; '.join(errors)


def _write_binary_stl_fallback(context, filepath, selected_objects):
    """Write selected evaluated meshes directly as one binary STL if Blender's exporter fails."""
    temp_path = filepath + '.wt_tmp'
    depsgraph = context.evaluated_depsgraph_get()
    triangle_count = 0

    try:
        with open(temp_path, 'wb') as handle:
            header = b'Witch Tools STL fallback export'
            handle.write(header[:80].ljust(80, b'\0'))
            handle.write(struct.pack('<I', 0))

            for obj in selected_objects:
                if obj.mode == 'EDIT':
                    obj.update_from_editmode()

                obj_eval = obj.evaluated_get(depsgraph)
                mesh = None
                try:
                    mesh = obj_eval.to_mesh()
                    if mesh is None:
                        continue
                    mesh.calc_loop_triangles()
                    matrix = obj_eval.matrix_world.copy()
                    reverse_winding = matrix.is_negative
                    vertices = mesh.vertices

                    for tri in mesh.loop_triangles:
                        v0, v1, v2 = (matrix @ vertices[index].co for index in tri.vertices)
                        if reverse_winding:
                            v1, v2 = v2, v1

                        normal = (v1 - v0).cross(v2 - v0)
                        if normal.length_squared:
                            normal.normalize()
                        else:
                            normal = Vector((0.0, 0.0, 0.0))

                        handle.write(struct.pack(
                            '<12fH',
                            normal.x, normal.y, normal.z,
                            v0.x, v0.y, v0.z,
                            v1.x, v1.y, v1.z,
                            v2.x, v2.y, v2.z,
                            0,
                        ))
                        triangle_count += 1
                finally:
                    if mesh is not None:
                        obj_eval.to_mesh_clear()

            if triangle_count == 0:
                raise RuntimeError('Selected mesh objects contain no exportable triangles')
            if triangle_count >= 2 ** 32:
                raise RuntimeError('STL triangle count exceeds the binary STL format limit')

            handle.seek(80)
            handle.write(struct.pack('<I', triangle_count))

        os.replace(temp_path, filepath)
        return triangle_count
    except Exception:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
        raise


class WT_OT_print3d_analyze(Operator):
    bl_idname = 'witch_tools.print3d_analyze'
    bl_label = 'Check All'
    bl_options = {'REGISTER'}
    bl_description = 'Run 3D Print Toolbox-equivalent mesh checks and refresh the Results box'

    @classmethod
    def poll(cls, context):
        return _mesh_object(context) is not None

    def execute(self, context):
        obj = _mesh_object(context)
        props = context.scene.wt_print3d
        if context.mode == 'EDIT_MESH':
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)

        bm = _bm_from_object(obj, transform=False, triangulate=False)
        try:
            props.non_manifold_edges = sum(1 for edge in bm.edges if not edge.is_manifold)
            props.bad_contiguous_edges = sum(
                1 for edge in bm.edges if edge.is_manifold and not edge.is_contiguous
            )
            props.shells = _count_shells(bm)
            props.zero_faces = sum(1 for face in bm.faces if face.calc_area() <= THRESHOLD_ZERO)
            props.zero_edges = sum(1 for edge in bm.edges if edge.calc_length() <= THRESHOLD_ZERO)
        finally:
            bm.free()

        props.intersect_faces = _count_intersections(obj)
        props.non_flat_faces = _count_nonflat_faces(obj, ANGLE_DISTORT)
        props.thin_faces = _count_thin_faces(obj, THICKNESS_MIN)
        props.sharp_edges = _count_sharp_edges(obj, ANGLE_SHARP)
        props.overhang_faces = _count_overhang_faces(obj, ANGLE_OVERHANG)
        props.last_analyzed_object = obj.name
        return {'FINISHED'}


class WT_OT_print3d_make_manifold(Operator):
    bl_idname = 'witch_tools.print3d_make_manifold'
    bl_label = 'Make Manifold'
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Merge doubles, remove degenerate/loose geometry, fill boundary holes, and recalculate normals outside'

    @classmethod
    def poll(cls, context):
        return _mesh_object(context) is not None

    def execute(self, context):
        obj = _mesh_object(context)
        prev_mode = context.mode
        try:
            if context.mode != 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=0.0001)
            bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)
            bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(type='EDGE')
            bpy.ops.mesh.select_non_manifold(
                extend=False,
                use_wire=False,
                use_boundary=True,
                use_multi_face=False,
                use_non_contiguous=False,
                use_verts=False,
            )
            try:
                bpy.ops.mesh.fill_holes(sides=0)
            except Exception:
                pass
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)
        except Exception as exc:
            self.report({'ERROR'}, f'Make Manifold failed: {exc}')
            return {'CANCELLED'}
        finally:
            try:
                if prev_mode == 'OBJECT' and context.mode == 'EDIT_MESH':
                    bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass
        return {'FINISHED'}


class WT_OT_print3d_export_stl(Operator):
    bl_idname = 'witch_tools.print3d_export_stl'
    bl_label = 'Export STL'
    bl_options = {'REGISTER'}
    bl_description = 'Export selected mesh objects as one STL to the chosen folder'

    @classmethod
    def poll(cls, context):
        return any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        props = context.scene.wt_print3d
        folder = bpy.path.abspath(props.export_directory or '//').strip()
        if not folder:
            self.report({'ERROR'}, 'Choose an export folder first')
            return {'CANCELLED'}

        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as exc:
            self.report({'ERROR'}, f'Cannot create export folder: {exc}')
            return {'CANCELLED'}

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected:
            self.report({'ERROR'}, 'Select at least one mesh object to export')
            return {'CANCELLED'}

        active = context.active_object if context.active_object in selected else selected[0]
        filename = bpy.path.clean_name(active.name if len(selected) == 1 else f'{active.name}_selection') + '.stl'
        filepath = os.path.join(folder, filename)

        native_ok, native_detail = _try_blender_stl_export(filepath)
        if native_ok:
            self.report({'INFO'}, f'Exported STL: {filepath}')
            return {'FINISHED'}

        try:
            triangle_count = _write_binary_stl_fallback(context, filepath, selected)
        except Exception as exc:
            self.report({'ERROR'}, f'STL export failed: {exc}. Blender exporter: {native_detail}')
            return {'CANCELLED'}

        self.report(
            {'INFO'},
            f'Exported STL: {filepath} ({triangle_count} triangles; Witch Tools fallback writer)',
        )
        return {'FINISHED'}


CLASSES = (
    WTPrint3DProperties,
    WT_OT_print3d_analyze,
    WT_OT_print3d_make_manifold,
    WT_OT_print3d_export_stl,
)


def register_props():
    bpy.types.Scene.wt_print3d = PointerProperty(type=WTPrint3DProperties)


def unregister_props():
    if hasattr(bpy.types.Scene, 'wt_print3d'):
        delattr(bpy.types.Scene, 'wt_print3d')
