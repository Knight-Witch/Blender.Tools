bl_info = {
    'name': 'Witch Quickbar v1.0.2',
    'author': 'Knight Witch',
    'version': (1, 0, 2),
    'blender': (4, 5, 0),
    'location': '3D View > Floating Quickbar',
    'description': 'A compact floating quick-access bar for mode switching, rotate, mirror, origin, cursor, and snapping actions.',
    'category': '3D View',
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import StringProperty

from .preferences import WQBAR_Preferences
from .overlay import CLASSES as OVERLAY_CLASSES, runtime, stop_overlay
from .input_gizmos import CLASSES as GIZMO_CLASSES
from .keymaps import CLASSES as KEYMAP_CLASSES, register_keymaps, unregister_keymaps
from .actions import WM_DEFAULTS

CLASSES = (WQBAR_Preferences,) + OVERLAY_CLASSES + GIZMO_CLASSES + KEYMAP_CLASSES


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


def _schedule_auto_start(delay=0.5):
    try:
        if hasattr(bpy.app.timers, 'is_registered') and bpy.app.timers.is_registered(_auto_start):
            return
    except Exception:
        pass
    try:
        bpy.app.timers.register(_auto_start, first_interval=delay)
    except Exception:
        pass


def _should_restart_after_file_change():
    try:
        addon = bpy.context.preferences.addons.get(__package__)
        prefs = addon.preferences if addon else None
        return bool(runtime.running or (prefs and prefs.auto_start))
    except Exception:
        return bool(runtime.running)


@persistent
def _wqbar_file_change_post(_dummy):
    should_restart = _should_restart_after_file_change()
    stop_overlay()
    if should_restart:
        _schedule_auto_start(0.6)

@persistent
def _wqbar_undo_redo_post(_dummy):
    try:
        from .utils import tag_redraw_all
        tag_redraw_all()
    except Exception:
        pass


def _append_handler(handler_name, callback):
    handlers = getattr(bpy.app.handlers, handler_name, None)
    if handlers is None:
        return
    if callback not in handlers:
        handlers.append(callback)


def _remove_handler(handler_name, callback):
    handlers = getattr(bpy.app.handlers, handler_name, None)
    if handlers is None:
        return
    while callback in handlers:
        handlers.remove(callback)


def _register_file_handlers():
    _append_handler('load_post', _wqbar_file_change_post)
    _append_handler('load_factory_startup_post', _wqbar_file_change_post)
    _append_handler('undo_post', _wqbar_undo_redo_post)
    _append_handler('redo_post', _wqbar_undo_redo_post)


def _unregister_file_handlers():
    _remove_handler('load_post', _wqbar_file_change_post)
    _remove_handler('load_factory_startup_post', _wqbar_file_change_post)
    _remove_handler('undo_post', _wqbar_undo_redo_post)
    _remove_handler('redo_post', _wqbar_undo_redo_post)


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
    _register_file_handlers()
    _schedule_auto_start(0.5)


def unregister():
    _unregister_file_handlers()
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
