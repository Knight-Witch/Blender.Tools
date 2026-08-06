import bpy

from .state import addon_keymaps


def _ensure_keymap(name, space_type):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is None:
        return None
    return kc.keymaps.new(name=name, space_type=space_type)


def add_keymap_once(km_name, space_type, idname, key, value='PRESS', shift=False, ctrl=False, alt=False):
    km = _ensure_keymap(km_name, space_type)
    if km is None:
        return None, None
    for existing_km, existing_kmi in addon_keymaps:
        if (
            existing_km.name == km_name and
            existing_km.space_type == space_type and
            existing_kmi.idname == idname and
            existing_kmi.type == key and
            existing_kmi.value == value and
            existing_kmi.shift == shift and
            existing_kmi.ctrl == ctrl and
            existing_kmi.alt == alt
        ):
            return existing_km, existing_kmi
    kmi = km.keymap_items.new(idname, type=key, value=value, shift=shift, ctrl=ctrl, alt=alt)
    addon_keymaps.append((km, kmi))
    return km, kmi


def unregister_keymaps():
    for km, kmi in list(addon_keymaps):
        try:
            km.keymap_items.remove(kmi)
        except Exception:
            pass
    addon_keymaps.clear()


def register_default_keymaps():
    defaults = [
        ('Mesh', 'EMPTY', 'mesh.vertex_snap_global', 'V', 'PRESS', True, True, False),
        ('3D View', 'VIEW_3D', 'wtm.switch_edit_mode', 'Q', 'PRESS', True, False, False),
        ('3D View', 'VIEW_3D', 'wtm.switch_object_mode', 'W', 'PRESS', True, False, False),
        ('3D View', 'VIEW_3D', 'wtm.toggle_weight_paint', 'E', 'PRESS', True, False, False),
        ('3D View', 'VIEW_3D', 'wtm.toggle_pose_mode', 'R', 'PRESS', True, False, False),
        ('3D View', 'VIEW_3D', 'wtm.cycle_mode_switcher', 'TAB', 'PRESS', False, False, False),
        ('3D View', 'VIEW_3D', 'wtm.return_temp_mode', 'BUTTON5MOUSE', 'PRESS', False, False, False),
        ('Image', 'IMAGE_EDITOR', 'wtm.switch_edit_mode', 'Q', 'PRESS', True, False, False),
        ('Image', 'IMAGE_EDITOR', 'wtm.switch_object_mode', 'W', 'PRESS', True, False, False),
        ('Image', 'IMAGE_EDITOR', 'wtm.toggle_weight_paint', 'E', 'PRESS', True, False, False),
        ('Image', 'IMAGE_EDITOR', 'wtm.toggle_pose_mode', 'R', 'PRESS', True, False, False),
        ('Image', 'IMAGE_EDITOR', 'wtm.cycle_mode_switcher', 'TAB', 'PRESS', False, False, False),
        ('Image', 'IMAGE_EDITOR', 'wtm.return_temp_mode', 'BUTTON5MOUSE', 'PRESS', False, False, False),
        ('Window', 'EMPTY', 'witch_tools.toggle_minimal_view', 'TAB', 'PRESS', False, True, True),
    ]
    for km_name, space_type, idname, key, value, shift, ctrl, alt in defaults:
        add_keymap_once(km_name, space_type, idname, key, value=value, shift=shift, ctrl=ctrl, alt=alt)


def _format_shortcut(kmi):
    parts = []
    if kmi.ctrl:
        parts.append('Ctrl')
    if kmi.shift:
        parts.append('Shift')
    if kmi.alt:
        parts.append('Alt')
    parts.append(kmi.type)
    return '+'.join(parts)


def find_shortcut_text(operator_id):
    wm = bpy.context.window_manager
    seen = set()
    for keyconfig in (wm.keyconfigs.user, wm.keyconfigs.addon, wm.keyconfigs.default):
        if keyconfig is None:
            continue
        for km in keyconfig.keymaps:
            for kmi in km.keymap_items:
                if not kmi.active or kmi.idname != operator_id:
                    continue
                key = (km.name, kmi.idname, kmi.type, kmi.shift, kmi.ctrl, kmi.alt)
                if key in seen:
                    continue
                seen.add(key)
                return _format_shortcut(kmi)
    return None
