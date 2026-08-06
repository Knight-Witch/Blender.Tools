import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector

from .utils_head import (
    boundary_loops_from_bmesh,
    centroid,
    closest_vert_pair,
    object_world_avg_x,
    ordered_loop_verts,
    recalc_normals_edit_object,
)


def _get_bone_variants(bone_name):
    if bone_name.endswith('_l'):
        return [bone_name, bone_name[:-2] + '_r']
    if bone_name.endswith('_m') or ('_l' not in bone_name and '_r' not in bone_name):
        return [bone_name]
    return [bone_name]


BONES_FROM_CURSOR = [
    'piercing_brow_a_l', 'piercing_brow_b_l', 'piercing_tragus_a_l', 'piercing_helix_b_l',
    'piercing_helix_a_l', 'piercing_lobe_b_l', 'piercing_lobe_a_l', 'beard_philtrum_m',
    'adams_apple', 'gullet', 'piercing_bridge_a_l', 'beard_ear_l', 'beard_smileline1_l',
    'beard_smileline2_l', 'beard_smileline3_l', 'beard_upper_lip1_l', 'beard_upper_lip2_l',
    'beard_lower_lip1_l', 'beard_lower_lip2_l', 'beard_labiomental_l', 'beard_philtrum_l',
    'beard_lower_lip_m', 'beard_labiomental_m', 'beard_chin_l', 'beard_jaw_m',
]
BONES_X_AXIS = ['beard_jaw_l', 'beard_jaw_base_l', 'beard_cheek_l', 'piercing_nostril_a_l']
BONES_Y_AXIS = ['beard_upper_lip_m']



def _raycast_to_mesh(origin, direction, target_mesh, max_distance=10.0):
    matrix_world = target_mesh.matrix_world
    matrix_inv = matrix_world.inverted()
    origin_local = matrix_inv @ origin
    direction_local = matrix_inv.to_3x3() @ direction
    direction_local.normalize()
    hit, location, normal, _face_index = target_mesh.ray_cast(origin_local, direction_local, distance=max_distance)
    if hit:
        return matrix_world @ location, matrix_world.to_3x3() @ normal
    return None, None



def _closest_point_on_mesh(point, target_mesh):
    matrix_world = target_mesh.matrix_world
    matrix_inv = matrix_world.inverted()
    point_local = matrix_inv @ point
    hit, location, normal, _face_index = target_mesh.closest_point_on_mesh(point_local)
    if hit:
        return matrix_world @ location, matrix_world.to_3x3() @ normal
    return None, None


class WT_OT_snap_ear_to_head(Operator):
    bl_idname = 'witch_tools.snap_ear_to_head'
    bl_label = 'Snap Ear to Head'
    bl_description = 'Snap ear opening boundary loops to the matching head opening and recalculate normals.'
    bl_options = {'REGISTER', 'UNDO'}

    fix_normals: bpy.props.BoolProperty(name='Fix Normals', default=True)

    def execute(self, context):
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected_meshes) < 2:
            self.report({'ERROR'}, 'Select at least a head mesh and one ear mesh')
            return {'CANCELLED'}

        head_obj = None
        ear_objs = []
        for obj in selected_meshes:
            vert_count = len(obj.data.vertices)
            if 3200 <= vert_count <= 3300:
                head_obj = obj
            elif 350 <= vert_count <= 800:
                ear_objs.append(obj)

        if head_obj is None or not ear_objs:
            self.report({'ERROR'}, 'Could not detect head / ear meshes from the selection')
            return {'CANCELLED'}

        bm_head = bmesh.new()
        bm_head.from_mesh(head_obj.data)
        bm_head.verts.ensure_lookup_table()
        bm_head.edges.ensure_lookup_table()

        head_ear_loops = []
        for loop in boundary_loops_from_bmesh(bm_head):
            verts = ordered_loop_verts(loop)
            if len(verts) == 20:
                head_ear_loops.append((verts, object_world_avg_x(head_obj, verts)))
        head_ear_loops.sort(key=lambda item: item[1])
        if len(head_ear_loops) != 2:
            bm_head.free()
            self.report({'ERROR'}, 'Expected 2 head ear-opening loops with 20 vertices each')
            return {'CANCELLED'}

        snapped = 0
        for ear_obj in ear_objs:
            bm_ear = bmesh.new()
            bm_ear.from_mesh(ear_obj.data)
            bm_ear.verts.ensure_lookup_table()
            bm_ear.edges.ensure_lookup_table()

            ear_openings = []
            all_boundary_verts = set()
            for loop in boundary_loops_from_bmesh(bm_ear):
                verts = ordered_loop_verts(loop)
                if len(verts) == 20:
                    ear_openings.append((verts, object_world_avg_x(ear_obj, verts)))
                    all_boundary_verts.update(verts)

            for ear_loop_verts, ear_avg_x in ear_openings:
                original_centroid = centroid(ear_loop_verts)
                matching_head_loop = min(head_ear_loops, key=lambda item: abs(ear_avg_x - item[1]))[0]
                ear_start_idx, head_start_idx, _dist = closest_vert_pair(ear_loop_verts, matching_head_loop, ear_obj, head_obj)
                if ear_start_idx is None:
                    continue

                ear_next_idx = (ear_start_idx + 1) % len(ear_loop_verts)
                head_next_forward = (head_start_idx + 1) % len(matching_head_loop)
                head_next_backward = (head_start_idx - 1) % len(matching_head_loop)
                ear_next_co = ear_obj.matrix_world @ ear_loop_verts[ear_next_idx].co
                head_forward_co = head_obj.matrix_world @ matching_head_loop[head_next_forward].co
                head_backward_co = head_obj.matrix_world @ matching_head_loop[head_next_backward].co
                head_direction = 1 if (ear_next_co - head_forward_co).length < (ear_next_co - head_backward_co).length else -1

                for i in range(len(ear_loop_verts)):
                    eidx = (ear_start_idx + i) % len(ear_loop_verts)
                    hidx = (head_start_idx + (i * head_direction)) % len(matching_head_loop)
                    head_world_co = head_obj.matrix_world @ matching_head_loop[hidx].co
                    ear_loop_verts[eidx].co = ear_obj.matrix_world.inverted() @ head_world_co

                move = centroid(ear_loop_verts) - original_centroid
                non_seam_verts = [v for v in bm_ear.verts if v not in all_boundary_verts]
                if len(ear_openings) > 1:
                    this_side_verts = []
                    for vert in non_seam_verts:
                        world_x = (ear_obj.matrix_world @ vert.co).x
                        if (world_x < 0 and ear_avg_x < 0) or (world_x >= 0 and ear_avg_x >= 0):
                            this_side_verts.append(vert)
                else:
                    this_side_verts = non_seam_verts
                for vert in this_side_verts:
                    vert.co += move
                snapped += 1

            bm_ear.to_mesh(ear_obj.data)
            ear_obj.data.update()
            bm_ear.free()
            if self.fix_normals:
                recalc_normals_edit_object(context, ear_obj)

        bm_head.free()
        if not snapped:
            self.report({'ERROR'}, 'No ear loops were snapped')
            return {'CANCELLED'}
        self.report({'INFO'}, f'Snapped {snapped} ear loop(s)')
        return {'FINISHED'}


class WT_OT_snap_all_head_bones(Operator):
    bl_idname = 'witch_tools.snap_all_head_bones'
    bl_label = 'Snap All Bones'
    bl_description = 'Snap beard and piercing bones onto the reference head mesh.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        armature_obj = props.head_target_armature
        mesh_obj = props.head_target_mesh
        offset_distance = props.head_offset_distance

        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, 'Pick a valid armature in Head Tools')
            return {'CANCELLED'}
        if not mesh_obj or mesh_obj.type != 'MESH':
            self.report({'ERROR'}, 'Pick a valid reference mesh in Head Tools')
            return {'CANCELLED'}

        original_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')
        armature = armature_obj.data
        bones_moved = 0

        if 'Head_M' in armature.edit_bones:
            cursor_location = armature_obj.matrix_world @ armature.edit_bones['Head_M'].head
            context.scene.cursor.location = cursor_location
        else:
            cursor_location = context.scene.cursor.location.copy()

        base_bones = ['Head_M', 'gesture_base', 'gesture_01', 'wrinkle_base', 'wrinkle_01', 'wrinkle_02', 'wrinkle_03', 'piercing_base', 'beard_base']
        bpy.ops.armature.select_all(action='DESELECT')
        for name in base_bones:
            bone = armature.edit_bones.get(name)
            if bone:
                bone.select = bone.select_head = bone.select_tail = True
        try:
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        except Exception:
            pass
        bpy.ops.armature.select_all(action='DESELECT')

        for bone_name in BONES_FROM_CURSOR:
            for variant in _get_bone_variants(bone_name):
                bone = armature.edit_bones.get(variant)
                if not bone:
                    continue
                bone_world = armature_obj.matrix_world @ bone.head
                hit_location, hit_normal = _closest_point_on_mesh(bone_world, mesh_obj)
                if hit_location:
                    final = hit_location + hit_normal * offset_distance
                    local = armature_obj.matrix_world.inverted() @ final
                    offset = bone.tail - bone.head
                    bone.head = local
                    bone.tail = local + offset
                    bones_moved += 1

        for bone_name in BONES_X_AXIS:
            for variant in _get_bone_variants(bone_name):
                bone = armature.edit_bones.get(variant)
                if not bone:
                    continue
                bone_world = armature_obj.matrix_world @ bone.head
                direction = Vector((-1 if bone_world.x > 0 else 1, 0, 0))
                hit_location, hit_normal = _raycast_to_mesh(bone_world, direction, mesh_obj, max_distance=1.0)
                if hit_location:
                    final = hit_location + hit_normal * offset_distance
                    local = armature_obj.matrix_world.inverted() @ final
                    offset = bone.tail - bone.head
                    bone.head = local
                    bone.tail = local + offset
                    bones_moved += 1

        for bone_name in BONES_Y_AXIS:
            for variant in _get_bone_variants(bone_name):
                bone = armature.edit_bones.get(variant)
                if not bone:
                    continue
                bone_world = armature_obj.matrix_world @ bone.head
                direction = Vector((0, -1 if bone_world.y > 0 else 1, 0))
                hit_location, hit_normal = _raycast_to_mesh(bone_world, direction, mesh_obj, max_distance=1.0)
                if hit_location:
                    final = hit_location + hit_normal * offset_distance
                    local = armature_obj.matrix_world.inverted() @ final
                    offset = bone.tail - bone.head
                    bone.head = local
                    bone.tail = local + offset
                    bones_moved += 1

        bpy.ops.object.mode_set(mode='OBJECT')
        if original_mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode=original_mode)
            except Exception:
                pass

        self.report({'INFO'}, f'Snapped {bones_moved} head helper bone(s)')
        return {'FINISHED'}


CLASSES = (
    WT_OT_snap_ear_to_head,
    WT_OT_snap_all_head_bones,
)
