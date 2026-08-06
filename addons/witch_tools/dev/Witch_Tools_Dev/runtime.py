import bpy

from .state import MODE_CYCLE_ITEMS, MODE_SWITCHER_SEQUENCE, armature_hide_select_state, runtime_cache
from .utils_context import (
    active_mesh_for_panel,
    current_mode,
    current_tool_id,
    addon_preferences,
    ensure_view3d_override,
    is_weight_paint_tool,
    linked_armature,
    mode_set,
    normalize_mode,
    set_tool,
)


WM_STATE_DEFAULTS = {
    'wt_return_object_name': '',
    'wt_return_mode': 'OBJECT',
    'wt_return_workspace_name': '',
    'wt_temp_object_name': '',
    'wt_temp_mode': 'OBJECT',
    'wt_temp_workspace_name': '',
    'wt_last_mesh_name': '',
    'wt_last_switcher_mode': 'OBJECT',
}

MESH_SWITCHER_MODES = {'EDIT', 'UV_DATA', 'WEIGHT_PAINT', 'SCULPT', 'TEXTURE_PAINT', 'VERTEX_PAINT'}
PAINT_SWITCHER_MODES = {'WEIGHT_PAINT', 'SCULPT', 'TEXTURE_PAINT', 'VERTEX_PAINT'}


def ensure_wm_state(wm):
    for key, default in WM_STATE_DEFAULTS.items():
        if not hasattr(wm, key):
            setattr(wm, key, default)


def is_switcher_mode(mode):
    return normalize_mode(mode) in MODE_SWITCHER_SEQUENCE


def current_workspace_name(context):
    window = getattr(context, 'window', None)
    ws = getattr(window, 'workspace', None) if window else None
    return ws.name if ws else ''


def _restore_workspace(context, workspace_name):
    if not workspace_name:
        return False
    window = getattr(context, 'window', None)
    if window is None:
        return False
    ws = bpy.data.workspaces.get(workspace_name)
    if ws is None:
        return False
    try:
        window.workspace = ws
        return True
    except Exception:
        return False


def store_return_state(context):
    wm = context.window_manager
    ensure_wm_state(wm)
    obj = context.active_object
    wm.wt_return_object_name = obj.name if obj else ''
    wm.wt_return_mode = _effective_current_switcher_mode(context)
    wm.wt_return_workspace_name = current_workspace_name(context)


def remember_last_mesh(context, obj=None):
    wm = context.window_manager
    ensure_wm_state(wm)
    obj = obj or context.active_object
    if obj and obj.type == 'MESH':
        wm.wt_last_mesh_name = obj.name


def last_mesh(context):
    wm = context.window_manager
    ensure_wm_state(wm)
    obj = bpy.data.objects.get(wm.wt_last_mesh_name) if wm.wt_last_mesh_name else None
    if obj and obj.type == 'MESH':
        return obj
    return active_mesh_for_panel(context)


def remember_temp_state(context):
    wm = context.window_manager
    ensure_wm_state(wm)
    obj = context.active_object
    mode = _effective_current_switcher_mode(context)
    if obj and obj.type == 'MESH':
        remember_last_mesh(context, obj)
    if obj:
        wm.wt_temp_object_name = obj.name
        wm.wt_temp_mode = mode
        wm.wt_temp_workspace_name = current_workspace_name(context)


def _effective_current_switcher_mode(context):
    current = normalize_mode(current_mode(context))
    wm = context.window_manager
    ensure_wm_state(wm)
    last_switcher = normalize_mode(wm.wt_last_switcher_mode)
    if current == 'EDIT' and last_switcher == 'UV_DATA':
        return 'UV_DATA'
    return current


def remember_switcher_choice(context, mode):
    wm = context.window_manager
    ensure_wm_state(wm)
    wm.wt_last_switcher_mode = normalize_mode(mode)


def current_switcher_mode(context):
    return _effective_current_switcher_mode(context)


def cycle_sequence(context):
    prefs = addon_preferences(context)
    if prefs is None:
        return MODE_SWITCHER_SEQUENCE
    sequence = [mode for mode, prop_name, _label, _icon in MODE_CYCLE_ITEMS if getattr(prefs, prop_name, True)]
    return tuple(sequence) or MODE_SWITCHER_SEQUENCE


def next_switcher_mode(context):
    sequence = cycle_sequence(context)
    current = _effective_current_switcher_mode(context)
    wm = context.window_manager
    ensure_wm_state(wm)
    if current in sequence:
        base = current
    else:
        base = normalize_mode(wm.wt_last_switcher_mode)
        if base not in sequence:
            base = sequence[0]
    idx = sequence.index(base)
    return sequence[(idx + 1) % len(sequence)]



def _switch_to_workspace(context, workspace_names):
    window = getattr(context, 'window', None)
    if window is None:
        return False

    candidates = []
    for name in workspace_names:
        ws = bpy.data.workspaces.get(name)
        if ws is not None and ws not in candidates:
            candidates.append(ws)

    lowered = [name.lower() for name in workspace_names]
    for ws in bpy.data.workspaces:
        ws_name = ws.name.lower()
        if any(term in ws_name for term in lowered) or ('uv' in ws_name and 'edit' in ws_name):
            if ws not in candidates:
                candidates.append(ws)

    for ws in candidates:
        try:
            window.workspace = ws
            return True
        except Exception:
            pass
    return False


def _configure_uv_editor(context):
    screen = getattr(context, 'screen', None)
    if screen is None:
        return False

    for area in screen.areas:
        if area.type == 'IMAGE_EDITOR':
            try:
                area.ui_type = 'UV'
            except Exception:
                pass
            return True

    reusable_types = (
        'OUTLINER',
        'PROPERTIES',
        'DOPESHEET_EDITOR',
        'TIMELINE',
        'GRAPH_EDITOR',
        'NLA_EDITOR',
        'TEXT_EDITOR',
        'CONSOLE',
        'INFO',
        'SPREADSHEET',
    )
    fallback = None
    for area in screen.areas:
        if area.type in reusable_types:
            fallback = area
            break

    if fallback is None and len(screen.areas) > 1:
        for area in screen.areas:
            if area != getattr(context, 'area', None):
                fallback = area
                break

    if fallback is None:
        return False

    try:
        fallback.type = 'IMAGE_EDITOR'
        try:
            fallback.ui_type = 'UV'
        except Exception:
            pass
        return True
    except Exception:
        return False

def _set_vertex_select_mode(context, mesh):
    override = ensure_view3d_override(context, mesh)
    if override is None:
        return False
    try:
        with context.temp_override(**override):
            bpy.ops.mesh.select_mode(type='VERT')
        return True
    except Exception:
        return False


def select_all_pose_bones(context, armature_obj):
    override = ensure_view3d_override(context, armature_obj)
    if override is None:
        return False
    try:
        with context.temp_override(**override):
            bpy.ops.pose.select_all(action='SELECT')
        return True
    except Exception:
        return False


def hide_other_armatures(context, keep_armature):
    props = context.scene.witch_tools
    if not props.wtm_hide_other_armatures:
        return
    for obj in context.view_layer.objects:
        if obj.type == 'ARMATURE':
            obj.hide_viewport = obj != keep_armature


def best_mesh_for_switch(context):
    obj = context.active_object
    if obj and obj.type == 'MESH':
        return obj
    return last_mesh(context)


def _restore_mode(context, obj, mode, workspace_name=''):
    if obj is None:
        return False

    if mode in MESH_SWITCHER_MODES and obj.type != 'MESH':
        obj = best_mesh_for_switch(context)
        if obj is None:
            return False

    if mode == 'POSE':
        arm = obj if obj.type == 'ARMATURE' else linked_armature(obj)
        if arm is None or not mode_set(context, arm, 'POSE'):
            return False
        restore_weight_paint_locks()
        hide_other_armatures(context, arm)
        select_all_pose_bones(context, arm)
        set_tool(context, 'builtin.rotate')
        return True

    if mode == 'OBJECT':
        if not mode_set(context, obj, 'OBJECT'):
            return False
        restore_weight_paint_locks()
        if obj.type == 'MESH':
            remember_last_mesh(context, obj)
        return True

    if mode == 'EDIT':
        if not mode_set(context, obj, 'EDIT'):
            return False
        restore_weight_paint_locks()
        remember_last_mesh(context, obj)
        return True

    if mode == 'UV_DATA':
        if not _restore_workspace(context, workspace_name):
            _switch_to_workspace(context, ('UV Editing', 'UV'))
        _configure_uv_editor(context)
        if not mode_set(context, obj, 'EDIT'):
            return False
        _configure_uv_editor(context)
        restore_weight_paint_locks()
        remember_last_mesh(context, obj)
        return True

    if mode in PAINT_SWITCHER_MODES:
        if not mode_set(context, obj, mode):
            return False
        if mode == 'WEIGHT_PAINT':
            prepare_weight_paint_mode(context, obj, force_brush=True)
        else:
            restore_weight_paint_locks()
        remember_last_mesh(context, obj)
        return True

    return False


def restore_return_state(context):
    wm = context.window_manager
    ensure_wm_state(wm)
    obj = bpy.data.objects.get(wm.wt_return_object_name) if wm.wt_return_object_name else None
    obj = obj or context.active_object
    if obj is None:
        return False
    mode = normalize_mode(wm.wt_return_mode)
    return _restore_mode(context, obj, mode, wm.wt_return_workspace_name)


def restore_temp_state(context):
    wm = context.window_manager
    ensure_wm_state(wm)
    target_obj = bpy.data.objects.get(wm.wt_temp_object_name) if wm.wt_temp_object_name else None
    if target_obj is None:
        return False, 'No stored temporary mode'
    target_mode = normalize_mode(wm.wt_temp_mode)
    target_workspace = wm.wt_temp_workspace_name

    current_obj = context.active_object
    current_mode = _effective_current_switcher_mode(context)
    current_workspace = current_workspace_name(context)

    if not _restore_mode(context, target_obj, target_mode, target_workspace):
        return False, f'Could not switch back to {target_mode}'

    wm.wt_temp_object_name = current_obj.name if current_obj else ''
    wm.wt_temp_mode = current_mode
    wm.wt_temp_workspace_name = current_workspace

    if current_obj and current_obj.type == 'MESH':
        remember_last_mesh(context, current_obj)
    return True, None


def switch_mode(context, target_mode):
    current = _effective_current_switcher_mode(context)

    if target_mode in MODE_SWITCHER_SEQUENCE and current == target_mode and is_switcher_mode(target_mode):
        if restore_return_state(context):
            obj = context.active_object
            if obj and obj.type == 'MESH':
                remember_last_mesh(context, obj)
            return True, None

    if not is_switcher_mode(normalize_mode(current_mode(context))):
        store_return_state(context)
    remember_temp_state(context)

    if target_mode == 'POSE':
        source = context.active_object or last_mesh(context)
        mesh = best_mesh_for_switch(context)
        if mesh is not None:
            remember_last_mesh(context, mesh)
        arm = linked_armature(source)
        if arm is None and mesh is not None:
            arm = linked_armature(mesh)
        if arm is None:
            return False, 'No linked armature found'
        if not mode_set(context, arm, 'POSE'):
            return False, 'Could not switch to Pose Mode'
        restore_weight_paint_locks()
        hide_other_armatures(context, arm)
        select_all_pose_bones(context, arm)
        set_tool(context, 'builtin.rotate')
        remember_switcher_choice(context, 'POSE')
        return True, None

    if target_mode == 'OBJECT':
        obj = context.active_object
        if normalize_mode(current_mode(context)) == 'POSE':
            obj = last_mesh(context) or obj
        elif obj is None:
            obj = last_mesh(context)
        if obj is None:
            return False, 'No object found for Object Mode'
        if not mode_set(context, obj, 'OBJECT'):
            return False, 'Could not switch to Object Mode'
        restore_weight_paint_locks()
        if obj.type == 'MESH':
            remember_last_mesh(context, obj)
        remember_switcher_choice(context, 'OBJECT')
        return True, None

    mesh = best_mesh_for_switch(context)
    if mesh is None:
        return False, 'No mesh found'
    remember_last_mesh(context, mesh)

    if target_mode == 'EDIT':
        if not mode_set(context, mesh, 'EDIT'):
            return False, 'Could not switch to Edit Mode'
        restore_weight_paint_locks()
        remember_switcher_choice(context, 'EDIT')
        return True, None

    if target_mode == 'UV_DATA':
        switched_workspace = _switch_to_workspace(context, ('UV Editing', 'UV'))
        if not mode_set(context, mesh, 'EDIT'):
            return False, 'Could not switch to Edit Mode for UV editing'
        _set_vertex_select_mode(context, mesh)
        configured_editor = _configure_uv_editor(context)
        restore_weight_paint_locks()
        remember_switcher_choice(context, 'UV_DATA')
        if switched_workspace or configured_editor:
            return True, None
        return False, 'Could not find or create a UV editor/workspace'

    if target_mode in PAINT_SWITCHER_MODES:
        if not mode_set(context, mesh, target_mode):
            return False, f'Could not switch to {target_mode}'
        if target_mode == 'WEIGHT_PAINT':
            prepare_weight_paint_mode(context, mesh, force_brush=True)
        else:
            restore_weight_paint_locks()
        remember_switcher_choice(context, target_mode)
        return True, None

    return False, f'Unsupported mode: {target_mode}'


def lock_armature_for_weight_paint(obj, lock=True):
    arm = linked_armature(obj)
    if arm is None:
        return
    key = arm.name
    if lock:
        if key not in armature_hide_select_state:
            armature_hide_select_state[key] = bool(getattr(arm, 'hide_select', False))
        try:
            arm.hide_select = True
            arm.select_set(False)
        except Exception:
            pass
    elif key in armature_hide_select_state:
        previous = armature_hide_select_state.pop(key)
        try:
            arm.hide_select = previous
        except Exception:
            pass


def restore_weight_paint_locks():
    for name, previous in list(armature_hide_select_state.items()):
        arm = bpy.data.objects.get(name)
        if arm is None:
            continue
        try:
            arm.hide_select = previous
        except Exception:
            pass
    armature_hide_select_state.clear()


def apply_auto_weight_mirror(obj, props):
    if obj is None or obj.type != 'MESH' or not props.auto_enable_weight_paint_mirror:
        return
    try:
        obj.use_mesh_mirror_x = True
    except Exception:
        pass
    try:
        obj.data.use_mirror_vertex_groups = True
    except Exception:
        pass


def prepare_weight_paint_mode(context, obj, force_brush=False):
    props = context.scene.witch_tools
    if obj is None or obj.type != 'MESH':
        return
    apply_auto_weight_mirror(obj, props)
    tool_id = current_tool_id(context)
    brush_like = is_weight_paint_tool(tool_id)

    if not props.enable_pose_in_weight_paint:
        lock_armature_for_weight_paint(obj, True)
        if force_brush or not brush_like:
            set_tool(context, 'builtin_brush.Draw')
        return

    if brush_like:
        lock_armature_for_weight_paint(obj, True)
    else:
        lock_armature_for_weight_paint(obj, False)


def weight_paint_runtime_key(context):
    obj = context.active_object
    props = getattr(context.scene, 'witch_tools', None)
    return (
        getattr(context, 'mode', ''),
        obj.name if obj else '',
        current_tool_id(context),
        bool(getattr(props, 'auto_enable_weight_paint_mirror', False)) if props else False,
        bool(getattr(props, 'enable_pose_in_weight_paint', False)) if props else False,
    )


def sync_weight_paint_session(context):
    if context is None or getattr(context, 'scene', None) is None or not hasattr(context.scene, 'witch_tools'):
        return
    obj = context.active_object
    mode = getattr(context, 'mode', '')
    obj_mode = getattr(obj, 'mode', '') if obj else ''
    if obj and obj.type == 'MESH' and (mode == 'PAINT_WEIGHT' or obj_mode == 'WEIGHT_PAINT'):
        prepare_weight_paint_mode(context, obj)
    else:
        restore_weight_paint_locks()
