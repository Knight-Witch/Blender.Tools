bl_info = {
    'name': 'Witch Quickbar v1.0.0',
    'author': 'Knight Witch',
    'version': (1, 0, 0),
    'blender': (4, 5, 0),
    'location': '3D View > Floating Quickbar; 3D View > Sidebar > Witch Quickbar',
    'description': 'A compact floating quick-access bar for mode switching, rotate, mirror, origin, cursor, and snapping actions.',
    'category': '3D View',
}

import bpy
from bpy.props import StringProperty

from .preferences import WQBAR_Preferences
from .overlay import CLASSES as OVERLAY_CLASSES, stop_overlay
from .panels import CLASSES as PANEL_CLASSES
from .keymaps import CLASSES as KEYMAP_CLASSES, register_keymaps, unregister_keymaps
from .actions import WM_DEFAULTS

CLASSES = (WQBAR_Preferences,) + OVERLAY_CLASSES + KEYMAP_CLASSES + PANEL_CLASSES


def _auto_start():
    try:
        addon = bpy.context.preferences.addons.get(__package__)
        prefs = addon.preferences if addon else None
        if not prefs or not prefs.auto_start:
            return None
        window = bpy.context.window
        screen = window.screen if window else None
        if not screen:
            return 0.5
        for area in screen.areas:
            if area.type != 'VIEW_3D':
                continue
            region = next((r for r in area.regions if r.type == 'WINDOW'), None)
            if not region:
                continue
            with bpy.context.temp_override(window=window, screen=screen, area=area, region=region):
                bpy.ops.witch_quickbar.show('INVOKE_DEFAULT')
            return None
    except Exception:
        return 0.5
    return None


def _migrate_preferences():
    try:
        addon = bpy.context.preferences.addons.get(__package__)
        prefs = addon.preferences if addon else None
        if not prefs:
            return
        if getattr(prefs, 'tool_order', '') == 'rotate,mirror,origin':
            prefs.tool_order = 'rotate,origin,mirror'
    except Exception:
        pass


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    _migrate_preferences()
    for key, default in WM_DEFAULTS.items():
        if not hasattr(bpy.types.WindowManager, key):
            setattr(bpy.types.WindowManager, key, StringProperty(default=default))
    try:
        register_keymaps()
    except Exception:
        pass
    try:
        bpy.app.timers.register(_auto_start, first_interval=0.5)
    except Exception:
        pass


def unregister():
    stop_overlay()
    try:
        unregister_keymaps()
    except Exception:
        pass
    for key in WM_DEFAULTS.keys():
        if hasattr(bpy.types.WindowManager, key):
            delattr(bpy.types.WindowManager, key)
    for cls in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass


if __name__ == '__main__':
    register()
