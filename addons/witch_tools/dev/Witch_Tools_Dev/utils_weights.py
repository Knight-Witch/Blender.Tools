import bmesh
import bpy
import re

from .utils_context import linked_armature, mode_set


def get_edit_mesh_objects(context):
    return [obj for obj in context.objects_in_mode_unique_data if obj.type == 'MESH']


def get_bmesh(obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    return bm


def selected_verts(bm):
    return [v for v in bm.verts if v.select]


def selected_verts_in_order(bm):
    ordered = []
    seen = set()
    for elem in bm.select_history:
        if isinstance(elem, bmesh.types.BMVert) and elem.select and elem.index not in seen:
            ordered.append(elem)
            seen.add(elem.index)
    for vert in bm.verts:
        if vert.select and vert.index not in seen:
            ordered.append(vert)
            seen.add(vert.index)
    return ordered


def selected_mesh_info(context):
    info = {}
    for obj in get_edit_mesh_objects(context):
        bm = get_bmesh(obj)
        sel = selected_verts(bm)
        if sel:
            info[obj] = {
                'bm': bm,
                'selected': sel,
                'ordered': selected_verts_in_order(bm),
            }
    return info


def sync_edit_meshes(context):
    for obj in get_edit_mesh_objects(context):
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)


def base_name(name):
    return re.sub(r'\.\d{3}$', '', name)


def transfer_weights(source_obj, target_obj):
    if source_obj is None or target_obj is None:
        return False, 'Source or target is missing'
    if source_obj == target_obj:
        return False, f'Source and target are the same object: {source_obj.name}'
    if source_obj.type != 'MESH' or target_obj.type != 'MESH':
        return False, 'Source and target must both be mesh objects'

    context = bpy.context
    view_layer = context.view_layer
    prev_active = view_layer.objects.active
    prev_selected = list(context.selected_objects)
    prev_mode = context.mode

    try:
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        for obj in list(context.selected_objects):
            obj.select_set(False)
        target_obj.select_set(True)
        view_layer.objects.active = target_obj

        mod = target_obj.modifiers.new(name='WT_TMP_DataTransfer', type='DATA_TRANSFER')
        mod.object = source_obj
        mod.use_vert_data = True
        mod.data_types_verts = {'VGROUP_WEIGHTS'}
        mod.vert_mapping = 'POLYINTERP_NEAREST'
        mod.layers_vgroup_select_src = 'ALL'
        mod.layers_vgroup_select_dst = 'NAME'
        mod.mix_mode = 'REPLACE'
        mod.mix_factor = 1.0
        bpy.ops.object.modifier_apply(modifier=mod.name)
        return True, f'{source_obj.name} -> {target_obj.name}'
    except Exception as exc:
        return False, f'{target_obj.name}: {exc}'
    finally:
        for obj in list(context.selected_objects):
            obj.select_set(False)
        for obj in prev_selected:
            if obj.name in bpy.data.objects:
                obj.select_set(True)
        if prev_active and prev_active.name in bpy.data.objects:
            view_layer.objects.active = prev_active
        try:
            if prev_active and prev_active.name in bpy.data.objects:
                if prev_mode == 'EDIT_MESH' and prev_active.type == 'MESH':
                    mode_set(context, prev_active, 'EDIT')
                elif prev_mode == 'PAINT_WEIGHT' and prev_active.type == 'MESH':
                    mode_set(context, prev_active, 'WEIGHT_PAINT')
                elif prev_mode == 'POSE' and linked_armature(prev_active):
                    arm = prev_active if prev_active.type == 'ARMATURE' else linked_armature(prev_active)
                    mode_set(context, arm, 'POSE')
        except Exception:
            pass


def mesh_pool_from_collection(collection, exclude_obj=None):
    if collection is None:
        return []
    result = []
    seen = set()
    for obj in collection.all_objects:
        if obj.type != 'MESH' or obj == exclude_obj or obj.name in seen:
            continue
        result.append(obj)
        seen.add(obj.name)
    return result


def mesh_pool_from_armature(armature, exclude_obj=None):
    if armature is None or armature.type != 'ARMATURE':
        return []
    result = []
    seen = set()
    for obj in bpy.data.objects:
        if obj.type != 'MESH' or obj == exclude_obj or obj.name in seen:
            continue
        if linked_armature(obj) != armature:
            continue
        result.append(obj)
        seen.add(obj.name)
    return result


def find_best_source_for_target(target_obj, source_pool):
    target_base = base_name(target_obj.name)
    matches = [obj for obj in source_pool if obj.type == 'MESH' and obj != target_obj and base_name(obj.name) == target_base]
    if not matches:
        return None
    exact = [obj for obj in matches if obj.name == target_base]
    if exact:
        return exact[0]
    bare = [obj for obj in matches if base_name(obj.name) == obj.name]
    if bare:
        return bare[0]
    return sorted(matches, key=lambda obj: obj.name)[0]


def weighted_group_names(mesh_obj):
    names = set()
    for vertex in mesh_obj.data.vertices:
        for group in vertex.groups:
            if group.weight > 0:
                vg = mesh_obj.vertex_groups[group.group]
                names.add(vg.name)
    return names


def armature_check_from_object(obj):
    if obj is None:
        return False, 'No active mesh or armature selected', ''
    arm = linked_armature(obj)
    if obj.type == 'ARMATURE':
        arm = obj
        meshes = [child for child in obj.children if child.type == 'MESH']
    elif obj.type == 'MESH':
        meshes = [obj]
    else:
        meshes = []

    if arm is None:
        return False, 'No linked armature found', ''
    if not meshes:
        return False, 'No linked mesh objects found', ''

    bone_names = {bone.name for bone in arm.data.bones}
    missing = {}
    for mesh in meshes:
        missing_names = sorted(name for name in weighted_group_names(mesh) if name not in bone_names)
        if missing_names:
            missing[mesh.name] = missing_names

    if missing:
        detail_lines = []
        total = 0
        for mesh_name, names in missing.items():
            total += len(names)
            detail_lines.append(f'{mesh_name}: {", ".join(names[:12])}')
        return True, f'Partial / outdated armature likely: {total} weighted groups have no matching bone', '\n'.join(detail_lines)

    return False, 'Current armature looks complete for the checked weighted groups', ''
