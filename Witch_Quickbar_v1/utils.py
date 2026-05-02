import bpy

from .state import ADDON_PACKAGE


def addon_preferences(context=None):
    context = context or bpy.context
    addon = context.preferences.addons.get(ADDON_PACKAGE)
    return addon.preferences if addon else None


def tag_redraw_all():
    wm = bpy.context.window_manager if bpy.context else None
    if not wm:
        return
    for window in wm.windows:
        screen = window.screen
        if not screen:
            continue
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def view3d_override(context, active_obj=None):
    window = context.window
    screen = context.screen
    if not window or not screen:
        return None
    areas = []
    if context.area and context.area.type == 'VIEW_3D':
        areas.append(context.area)
    areas.extend(area for area in screen.areas if area.type == 'VIEW_3D' and area not in areas)
    for area in areas:
        region = next((r for r in area.regions if r.type == 'WINDOW'), None)
        if not region:
            continue
        space = area.spaces.active if area.spaces else None
        override = {
            'window': window,
            'screen': screen,
            'area': area,
            'region': region,
            'scene': context.scene,
            'view_layer': context.view_layer,
        }
        if space:
            override['space_data'] = space
            if getattr(space, 'region_3d', None):
                override['region_data'] = space.region_3d
        if active_obj is not None:
            override['active_object'] = active_obj
            override['object'] = active_obj
        return override
    return None


def normalize_mode(mode):
    if mode in {'EDIT', 'EDIT_MESH'}:
        return 'EDIT'
    if mode in {'PAINT_WEIGHT', 'WEIGHT_PAINT'}:
        return 'WEIGHT_PAINT'
    if mode in {'PAINT_TEXTURE', 'TEXTURE_PAINT'}:
        return 'TEXTURE_PAINT'
    if mode in {'PAINT_VERTEX', 'VERTEX_PAINT'}:
        return 'VERTEX_PAINT'
    if mode in {'SCULPT'}:
        return 'SCULPT'
    if mode in {'POSE'}:
        return 'POSE'
    return mode or 'OBJECT'


def current_mode(context):
    obj = context.active_object
    if obj:
        return normalize_mode(getattr(obj, 'mode', None))
    return normalize_mode(getattr(context, 'mode', None))


def set_active_only(context, obj):
    if obj is None:
        return False
    try:
        if normalize_mode(context.mode) != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass
    try:
        for item in list(context.selected_objects):
            item.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return True
    except Exception:
        return False


def set_mode(context, obj, mode):
    if obj is None:
        return False
    previous = current_mode(context)
    if previous != 'OBJECT':
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass
    if not set_active_only(context, obj):
        return False
    override = view3d_override(context, obj)
    if override is None:
        return False
    actual = 'EDIT' if mode in {'EDIT', 'UV_DATA'} else mode
    try:
        with context.temp_override(**override):
            bpy.ops.object.mode_set(mode=actual)
        return True
    except Exception:
        return False


def linked_armature(obj):
    if obj is None:
        return None
    if obj.type == 'ARMATURE':
        return obj
    for mod in getattr(obj, 'modifiers', []):
        if mod.type == 'ARMATURE' and mod.object:
            return mod.object
    if obj.parent and obj.parent.type == 'ARMATURE':
        return obj.parent
    return None
