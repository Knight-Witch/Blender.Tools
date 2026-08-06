import bpy

from .state import ADDON_PACKAGE


PAINT_TOOL_IDS = {
    'builtin_brush.Draw',
    'builtin_brush.Blur',
    'builtin_brush.Average',
    'builtin_brush.Smear',
    'builtin.gradient',
    'builtin.sample_weight',
}


def addon_preferences(context=None):
    context = context or bpy.context
    addon = context.preferences.addons.get(ADDON_PACKAGE)
    return addon.preferences if addon else None


def prefs_mirror_tolerance():
    prefs = addon_preferences()
    return prefs.mirror_tolerance if prefs else 0.0005


def active_mesh_for_panel(context):
    obj = context.active_object
    if obj and obj.type == 'MESH':
        return obj
    if obj and obj.type == 'ARMATURE':
        for child in obj.children:
            if child.type == 'MESH':
                return child
    return None


def linked_armature(obj):
    if obj is None:
        return None
    if obj.type == 'ARMATURE':
        return obj
    for mod in obj.modifiers:
        if mod.type == 'ARMATURE' and mod.object:
            return mod.object
    if obj.parent and obj.parent.type == 'ARMATURE':
        return obj.parent
    return None


def ensure_view3d_override(context, active_obj=None):
    window = context.window
    screen = context.screen
    areas = [context.area] if context.area and context.area.type == 'VIEW_3D' else []
    areas += [area for area in screen.areas if area.type == 'VIEW_3D' and area is not context.area]
    for area in areas:
        if area is None or area.type != 'VIEW_3D':
            continue
        region = next((r for r in area.regions if r.type == 'WINDOW'), None)
        if region is None:
            continue
        override = {
            'window': window,
            'screen': screen,
            'area': area,
            'region': region,
            'scene': context.scene,
            'view_layer': context.view_layer,
        }
        if active_obj is not None:
            override['active_object'] = active_obj
            override['object'] = active_obj
        return override
    return None


def set_active_only(context, obj):
    if obj is None:
        return False
    try:
        for item in list(context.selected_objects):
            item.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return True
    except Exception:
        return False


def mode_set(context, obj, mode):
    if obj is None or not set_active_only(context, obj):
        return False
    override = ensure_view3d_override(context, obj)
    if override is None:
        return False
    try:
        with context.temp_override(**override):
            bpy.ops.object.mode_set(mode=mode)
        return True
    except Exception:
        return False


def current_mode(context):
    obj = context.active_object
    if obj is None:
        return 'OBJECT'
    return obj.mode


def normalize_mode(mode):
    if mode in {'EDIT_MESH', 'EDIT'}:
        return 'EDIT'
    return mode or 'OBJECT'


def current_tool_id(context):
    try:
        workspace = context.workspace
        tool = workspace.tools.from_space_view3d_mode(context.mode or 'OBJECT', create=False)
        return tool.idname if tool else ''
    except Exception:
        return ''


def is_weight_paint_tool(tool_id):
    return bool(tool_id) and (tool_id in PAINT_TOOL_IDS or tool_id.startswith('builtin_brush.'))


def set_tool(context, tool_id):
    override = ensure_view3d_override(context)
    if override is None:
        return False
    try:
        with context.temp_override(**override):
            bpy.ops.wm.tool_set_by_id(name=tool_id)
        return True
    except Exception:
        return False


def ui_state_owner(context=None):
    context = context or bpy.context
    prefs = addon_preferences(context)
    if prefs is not None:
        return prefs
    scene = getattr(context, 'scene', None)
    return getattr(scene, 'witch_tools', None) if scene else None
