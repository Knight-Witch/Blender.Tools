import math

import bpy

from .config import MODE_SEQUENCE, cycle_mode_order, mode_order
from .utils import (
    addon_preferences,
    current_mode,
    linked_armature,
    normalize_mode,
    set_mode,
    view3d_override,
)


WM_DEFAULTS = {
    'witch_quickbar_previous_object_name': '',
    'witch_quickbar_previous_mode': 'OBJECT',
    'witch_quickbar_previous_target': 'OBJECT',
    'witch_quickbar_last_mesh_name': '',
    'witch_quickbar_last_switcher_target': 'OBJECT',
    'witch_quickbar_rotation_degrees': '90',
}


def ensure_wm_state(wm):
    for key, value in WM_DEFAULTS.items():
        if not hasattr(wm, key):
            setattr(wm, key, value)


def remember_last_mesh(context, obj=None):
    ensure_wm_state(context.window_manager)
    obj = obj or context.active_object
    if obj and obj.type == 'MESH':
        context.window_manager.witch_quickbar_last_mesh_name = obj.name


def last_mesh(context):
    ensure_wm_state(context.window_manager)
    name = context.window_manager.witch_quickbar_last_mesh_name
    obj = bpy.data.objects.get(name) if name else None
    if obj and obj.type == 'MESH':
        return obj
    obj = context.active_object
    if obj and obj.type == 'MESH':
        return obj
    return None


def best_mesh_for_switch(context):
    obj = context.active_object
    if obj and obj.type == 'MESH':
        return obj
    return last_mesh(context)


def store_previous_mode(context):
    ensure_wm_state(context.window_manager)
    obj = context.active_object
    wm = context.window_manager
    wm.witch_quickbar_previous_object_name = obj.name if obj else ''
    wm.witch_quickbar_previous_mode = current_mode(context)
    wm.witch_quickbar_previous_target = normalize_mode(wm.witch_quickbar_last_switcher_target)
    if obj and obj.type == 'MESH':
        remember_last_mesh(context, obj)


def remember_switcher_choice(context, target):
    ensure_wm_state(context.window_manager)
    context.window_manager.witch_quickbar_last_switcher_target = target


def last_switcher_choice(context):
    ensure_wm_state(context.window_manager)
    target = context.window_manager.witch_quickbar_last_switcher_target
    return target if target in MODE_SEQUENCE else 'OBJECT'


def cycle_mode_candidates(context):
    prefs = addon_preferences(context)
    enabled_order = cycle_mode_order(prefs)
    if not enabled_order:
        return []

    all_order = [key for key in mode_order(prefs) if key in MODE_SEQUENCE]
    if not all_order:
        return enabled_order

    last_target = last_switcher_choice(context)
    current_target = current_mode(context)
    if current_target == 'EDIT' and last_target == 'UV_DATA':
        current_target = 'UV_DATA'

    if last_target in all_order:
        start_key = last_target
    elif current_target in all_order:
        start_key = current_target
    else:
        start_key = ''

    if start_key in all_order:
        start_index = all_order.index(start_key)
        search_order = all_order[start_index + 1:] + all_order[:start_index + 1]
    else:
        search_order = all_order

    enabled = set(enabled_order)
    return [key for key in search_order if key in enabled]


def next_switcher_mode(context):
    candidates = cycle_mode_candidates(context)
    return candidates[0] if candidates else ''


def set_vertex_select_mode(context, mesh):
    override = view3d_override(context, mesh)
    if override is None:
        return False
    try:
        with context.temp_override(**override):
            bpy.ops.mesh.select_mode(type='VERT')
        return True
    except Exception:
        return False


def select_all_pose_bones(context, armature):
    override = view3d_override(context, armature)
    if override is None:
        return False
    try:
        with context.temp_override(**override):
            bpy.ops.pose.select_all(action='SELECT')
        return True
    except Exception:
        return False


def restore_previous_mode(context):
    ensure_wm_state(context.window_manager)
    wm = context.window_manager
    obj = bpy.data.objects.get(wm.witch_quickbar_previous_object_name) if wm.witch_quickbar_previous_object_name else None
    obj = obj or context.active_object
    mode = normalize_mode(wm.witch_quickbar_previous_mode)
    target = wm.witch_quickbar_previous_target if wm.witch_quickbar_previous_target in MODE_SEQUENCE else mode
    if obj is None:
        return False, 'No previous mode stored'
    store_previous_mode(context)
    if mode == 'POSE':
        arm = obj if obj.type == 'ARMATURE' else linked_armature(obj)
        if arm is None:
            return False, 'No linked armature found'
        if not set_mode(context, arm, 'POSE'):
            return False, 'Could not switch to Pose Mode'
        select_all_pose_bones(context, arm)
    else:
        if mode in {'EDIT', 'WEIGHT_PAINT', 'SCULPT', 'TEXTURE_PAINT', 'VERTEX_PAINT'} and obj.type != 'MESH':
            obj = best_mesh_for_switch(context)
        if mode in {'EDIT', 'WEIGHT_PAINT', 'SCULPT', 'TEXTURE_PAINT', 'VERTEX_PAINT'} and obj is None:
            return False, 'No mesh found'
        if not set_mode(context, obj, mode):
            return False, f'Could not switch to {mode}'
        if mode == 'EDIT':
            set_vertex_select_mode(context, obj)
    if obj and obj.type == 'MESH':
        remember_last_mesh(context, obj)
    remember_switcher_choice(context, target if target in MODE_SEQUENCE else mode)
    return True, ''


def switch_mode(context, target_mode):
    ensure_wm_state(context.window_manager)
    if target_mode == 'CYCLE':
        candidates = cycle_mode_candidates(context)
        if not candidates:
            return False, 'No modes are enabled for cycling'
        failures = []
        for candidate in candidates:
            ok, msg = switch_mode(context, candidate)
            if ok:
                return True, ''
            if msg:
                failures.append(f'{candidate}: {msg}')
        detail = f" ({'; '.join(failures)})" if failures else ''
        return False, f'Could not cycle to any enabled mode{detail}'
    if target_mode == 'RETURN':
        return restore_previous_mode(context)
    if target_mode not in MODE_SEQUENCE:
        return False, f'Unsupported mode: {target_mode}'

    store_previous_mode(context)

    if target_mode == 'POSE':
        source = context.active_object or last_mesh(context)
        mesh = best_mesh_for_switch(context)
        if mesh:
            remember_last_mesh(context, mesh)
        armature = linked_armature(source) or linked_armature(mesh)
        if armature is None:
            return False, 'No linked armature found'
        if not set_mode(context, armature, 'POSE'):
            return False, 'Could not switch to Pose Mode'
        select_all_pose_bones(context, armature)
        try:
            override = view3d_override(context, armature)
            if override:
                with context.temp_override(**override):
                    bpy.ops.wm.tool_set_by_id(name='builtin.rotate')
        except Exception:
            pass
        remember_switcher_choice(context, 'POSE')
        return True, ''

    if target_mode == 'OBJECT':
        obj = context.active_object or last_mesh(context)
        if obj is None:
            return False, 'No object found'
        if not set_mode(context, obj, 'OBJECT'):
            return False, 'Could not switch to Object Mode'
        if obj.type == 'MESH':
            remember_last_mesh(context, obj)
        remember_switcher_choice(context, 'OBJECT')
        return True, ''

    mesh = best_mesh_for_switch(context)
    if mesh is None:
        return False, 'No mesh found'
    remember_last_mesh(context, mesh)

    if target_mode == 'UV_DATA':
        if not set_mode(context, mesh, 'EDIT'):
            return False, 'Could not switch to UV Data / Edit Mode'
        set_vertex_select_mode(context, mesh)
        remember_switcher_choice(context, 'UV_DATA')
        return True, ''

    if target_mode == 'EDIT':
        if not set_mode(context, mesh, 'EDIT'):
            return False, 'Could not switch to Edit Mode'
        remember_switcher_choice(context, 'EDIT')
        return True, ''

    if target_mode in {'WEIGHT_PAINT', 'SCULPT', 'TEXTURE_PAINT', 'VERTEX_PAINT'}:
        if not set_mode(context, mesh, target_mode):
            return False, f'Could not switch to {target_mode}'
        remember_switcher_choice(context, target_mode)
        return True, ''

    return False, f'Unsupported mode: {target_mode}'


def rotation_degrees(context):
    ensure_wm_state(context.window_manager)
    try:
        return int(context.window_manager.witch_quickbar_rotation_degrees)
    except Exception:
        return 90


def toggle_rotation_degrees(context):
    ensure_wm_state(context.window_manager)
    context.window_manager.witch_quickbar_rotation_degrees = '180' if rotation_degrees(context) == 90 else '90'
    return True, ''


def rotate_selection(context, axis):
    mode = normalize_mode(getattr(context, 'mode', 'OBJECT'))
    if mode not in {'OBJECT', 'EDIT'}:
        return False, 'Rotate is only available in Object and Edit Mode'
    override = view3d_override(context, context.active_object)
    if override is None:
        return False, 'No 3D View context found'
    angle = math.radians(rotation_degrees(context))
    constraints = (axis == 'X', axis == 'Y', axis == 'Z')
    try:
        with context.temp_override(**override):
            bpy.ops.transform.rotate(
                value=angle,
                orient_axis=axis,
                orient_type='GLOBAL',
                constraint_axis=constraints,
            )
        return True, ''
    except Exception as exc:
        return False, str(exc)


def mode_for_restore(context):
    obj = context.active_object
    if not obj:
        return 'OBJECT'
    return normalize_mode(obj.mode)


def restore_mode(context, obj, mode):
    if obj is None:
        return
    if mode == 'EDIT' and obj.type == 'MESH':
        set_mode(context, obj, 'EDIT')
    elif mode == 'POSE' and obj.type == 'ARMATURE':
        set_mode(context, obj, 'POSE')
    elif mode == 'WEIGHT_PAINT' and obj.type == 'MESH':
        set_mode(context, obj, 'WEIGHT_PAINT')
    elif mode == 'SCULPT' and obj.type == 'MESH':
        set_mode(context, obj, 'SCULPT')
    elif mode == 'TEXTURE_PAINT' and obj.type == 'MESH':
        set_mode(context, obj, 'TEXTURE_PAINT')
    elif mode == 'VERTEX_PAINT' and obj.type == 'MESH':
        set_mode(context, obj, 'VERTEX_PAINT')


def set_origin(context, origin_type):
    obj = context.active_object
    if obj is None:
        return False, 'No active object'
    previous_obj = obj
    previous_mode = mode_for_restore(context)
    try:
        if previous_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass
    override = view3d_override(context, previous_obj)
    if override is None:
        return False, 'No 3D View context found'
    try:
        with context.temp_override(**override):
            if origin_type == 'GEOMETRY':
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            elif origin_type == 'CURSOR':
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            else:
                return False, f'Unsupported origin type: {origin_type}'
        restore_mode(context, previous_obj, previous_mode)
        return True, ''
    except Exception as exc:
        restore_mode(context, previous_obj, previous_mode)
        return False, str(exc)


def view3d_snap(context, snap_action):
    override = view3d_override(context, context.active_object)
    if override is None:
        return False, 'No 3D View context found'
    try:
        with context.temp_override(**override):
            if snap_action == 'CURSOR_TO_SELECTED':
                bpy.ops.view3d.snap_cursor_to_selected()
            elif snap_action == 'CURSOR_TO_GRID':
                bpy.ops.view3d.snap_cursor_to_grid()
            elif snap_action == 'SELECTION_TO_CURSOR':
                bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
            elif snap_action == 'SELECTION_TO_GRID':
                bpy.ops.view3d.snap_selected_to_grid()
            else:
                return False, f'Unsupported snap action: {snap_action}'
        return True, ''
    except Exception as exc:
        return False, str(exc)



def mirror_pivot_mode(context):
    prefs = addon_preferences(context)
    mode = getattr(prefs, 'mirror_pivot_mode', 'CURSOR') if prefs else 'CURSOR'
    return mode if mode in {'CURSOR', 'WORLD'} else 'CURSOR'


def set_mirror_pivot_mode(context, pivot_mode):
    if pivot_mode not in {'CURSOR', 'WORLD'}:
        return False, f'Unsupported mirror pivot: {pivot_mode}'
    prefs = addon_preferences(context)
    if prefs is None:
        return False, 'Quickbar preferences unavailable'
    prefs.mirror_pivot_mode = pivot_mode
    return True, ''


def _selected_mesh_objects(context):
    return [obj for obj in context.selected_objects if obj and obj.type == 'MESH']


def _select_objects(context, objects, active=None):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    if active or objects:
        context.view_layer.objects.active = active or objects[0]


def _apply_transforms_to_objects(context, objects):
    if not objects:
        return
    _select_objects(context, objects, objects[0])
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def _set_objects_origin_to_location(context, objects, location):
    cursor = context.scene.cursor
    cursor.location = location
    for obj in objects:
        _select_objects(context, [obj], obj)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')


def _recalculate_normals_outside(context, objects):
    for obj in objects:
        if obj.type != 'MESH':
            continue
        try:
            _select_objects(context, [obj], obj)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass


def mirror_selected_objects(context):
    if normalize_mode(getattr(context, 'mode', 'OBJECT')) != 'OBJECT':
        return False, 'Mirror Objects is only available in Object Mode'

    objects = _selected_mesh_objects(context)
    if not objects:
        return False, 'Select at least one mesh object to mirror'

    override = view3d_override(context, objects[0])
    if override is None:
        return False, 'No 3D View context found'

    pivot_mode = mirror_pivot_mode(context)
    cursor = context.scene.cursor
    cursor_location = cursor.location.copy()
    cursor_rotation = cursor.rotation_euler.copy()
    pivot = cursor_location.copy()
    if pivot_mode == 'WORLD':
        pivot.x = 0.0
        pivot.y = 0.0
        pivot.z = 0.0

    source_names = {obj.name for obj in objects}

    try:
        with context.temp_override(**override):
            bpy.ops.object.mode_set(mode='OBJECT')
            _apply_transforms_to_objects(context, objects)
            _set_objects_origin_to_location(context, objects, pivot)
            _apply_transforms_to_objects(context, objects)
            _set_objects_origin_to_location(context, objects, pivot)
            _select_objects(context, objects, objects[0])
            bpy.ops.object.duplicate(linked=False)
            duplicates = [obj for obj in context.selected_objects if obj.type == 'MESH' and obj.name not in source_names]
            if not duplicates:
                duplicates = [obj for obj in context.selected_objects if obj.type == 'MESH' and obj not in objects]
            if not duplicates:
                return False, 'Duplicate operation did not create mirrored objects'
            _select_objects(context, duplicates, duplicates[0])
            for obj in duplicates:
                obj.scale.x *= -1.0
            _apply_transforms_to_objects(context, duplicates)
            _recalculate_normals_outside(context, duplicates)
            _select_objects(context, duplicates, duplicates[0])
        return True, f'Mirrored {len(duplicates)} object(s)'
    except Exception as exc:
        return False, str(exc)
    finally:
        cursor.location = cursor_location
        cursor.rotation_euler = cursor_rotation

def execute_action(context, action):
    if action == 'OPEN_PREFERENCES':
        try:
            bpy.ops.witch_quickbar.open_preferences('INVOKE_DEFAULT')
            return True, ''
        except Exception as exc:
            return False, str(exc)
    if action == 'CHECK_UPDATES':
        try:
            bpy.ops.witch_quickbar.check_updates('INVOKE_DEFAULT')
            return True, ''
        except Exception as exc:
            return False, str(exc)
    if action.startswith('MODE:'):
        return switch_mode(context, action.split(':', 1)[1])
    if action == 'ROTATE_TOGGLE':
        return toggle_rotation_degrees(context)
    if action.startswith('ROTATE:'):
        return rotate_selection(context, action.split(':', 1)[1])
    if action.startswith('ORIGIN:'):
        return set_origin(context, action.split(':', 1)[1])
    if action.startswith('SNAP:'):
        return view3d_snap(context, action.split(':', 1)[1])
    if action.startswith('MIRROR_PIVOT:'):
        return set_mirror_pivot_mode(context, action.split(':', 1)[1])
    if action == 'MIRROR_OBJECTS':
        return mirror_selected_objects(context)
    return False, f'Unknown action: {action}'
