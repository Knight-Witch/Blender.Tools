import bpy
from bpy.props import StringProperty
from bpy.types import Operator

from .config import (
    MODE_SEQUENCE,
    UPDATE_URL,
    cycle_enabled_modes,
    save_cycle_enabled_modes,
)
from .state import ADDON_PACKAGE, addon_keymaps
from .utils import addon_preferences, tag_redraw_all

SHORTCUT_TARGETS = {
    'cycle': {
        'label': 'Cycle Modes',
        'operator': 'witch_quickbar.cycle_modes',
        'prefix': 'cycle_shortcut',
    },
    'last': {
        'label': 'Last Mode Used',
        'operator': 'witch_quickbar.last_mode',
        'prefix': 'last_shortcut',
    },
}

IGNORED_CAPTURE_EVENTS = {
    'MOUSEMOVE',
    'INBETWEEN_MOUSEMOVE',
    'TIMER',
    'TIMER0',
    'TIMER1',
    'TIMER2',
    'TIMER_JOBS',
    'TIMER_AUTOSAVE',
    'TIMER_REPORT',
    'WINDOW_DEACTIVATE',
}

MODIFIER_ONLY_EVENTS = {
    'LEFT_SHIFT',
    'RIGHT_SHIFT',
    'LEFT_CTRL',
    'RIGHT_CTRL',
    'LEFT_ALT',
    'RIGHT_ALT',
    'OSKEY',
}


def _target_data(target):
    return SHORTCUT_TARGETS.get(target)


def _field(target, suffix):
    data = _target_data(target)
    return f"{data['prefix']}_{suffix}" if data else ''


def _keyconfig():
    wm = bpy.context.window_manager if bpy.context else None
    return wm.keyconfigs.addon if wm and wm.keyconfigs else None


def _remove_keymaps_for_operator(operator_id):
    kc = _keyconfig()
    if not kc:
        return
    for km in kc.keymaps:
        for kmi in list(km.keymap_items):
            if kmi.idname == operator_id:
                try:
                    km.keymap_items.remove(kmi)
                except Exception:
                    pass
    addon_keymaps[:] = [(km, kmi) for km, kmi in addon_keymaps if getattr(kmi, 'idname', '') != operator_id]


def _remove_all_keymaps():
    for data in SHORTCUT_TARGETS.values():
        _remove_keymaps_for_operator(data['operator'])
    addon_keymaps.clear()


def _create_keymap_item(target, context=None):
    data = _target_data(target)
    prefs = addon_preferences(context or bpy.context)
    kc = _keyconfig()
    if not data or not prefs or not kc:
        return None

    key_type = getattr(prefs, _field(target, 'type'), '')
    if not key_type:
        return None

    key_value = getattr(prefs, _field(target, 'value'), 'PRESS') or 'PRESS'
    ctrl = bool(getattr(prefs, _field(target, 'ctrl'), False))
    shift = bool(getattr(prefs, _field(target, 'shift'), False))
    alt = bool(getattr(prefs, _field(target, 'alt'), False))
    oskey = bool(getattr(prefs, _field(target, 'oskey'), False))

    try:
        km = kc.keymaps.get('3D View') or kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(data['operator'], key_type, key_value, ctrl=ctrl, shift=shift, alt=alt, oskey=oskey)
        addon_keymaps.append((km, kmi))
        return kmi
    except Exception:
        return None


def rebuild_shortcut(target=None, context=None):
    if target in SHORTCUT_TARGETS:
        _remove_keymaps_for_operator(SHORTCUT_TARGETS[target]['operator'])
        return _create_keymap_item(target, context)
    _remove_all_keymaps()
    for key in SHORTCUT_TARGETS:
        _create_keymap_item(key, context)
    return None


def unregister_keymaps():
    _remove_all_keymaps()


def register_keymaps():
    rebuild_shortcut(None, bpy.context)


def shortcut_label(context, target):
    data = _target_data(target)
    prefs = addon_preferences(context)
    if not data or not prefs:
        return 'Unassigned'

    key_type = getattr(prefs, _field(target, 'type'), '')
    if not key_type:
        return 'Unassigned'

    parts = []
    if getattr(prefs, _field(target, 'ctrl'), False):
        parts.append('Ctrl')
    if getattr(prefs, _field(target, 'shift'), False):
        parts.append('Shift')
    if getattr(prefs, _field(target, 'alt'), False):
        parts.append('Alt')
    if getattr(prefs, _field(target, 'oskey'), False):
        parts.append('OS')
    parts.append(key_type.replace('_', ' ').title())
    return ' + '.join(parts)


def assign_shortcut_from_event(context, target, event):
    prefs = addon_preferences(context)
    data = _target_data(target)
    if not prefs or not data:
        return False

    setattr(prefs, _field(target, 'type'), event.type)
    setattr(prefs, _field(target, 'value'), event.value or 'PRESS')
    setattr(prefs, _field(target, 'ctrl'), bool(event.ctrl))
    setattr(prefs, _field(target, 'shift'), bool(event.shift))
    setattr(prefs, _field(target, 'alt'), bool(event.alt))
    setattr(prefs, _field(target, 'oskey'), bool(event.oskey))
    rebuild_shortcut(target, context)
    tag_redraw_all()
    return True


def clear_shortcut(context, target):
    prefs = addon_preferences(context)
    data = _target_data(target)
    if not prefs or not data:
        return False
    setattr(prefs, _field(target, 'type'), '')
    setattr(prefs, _field(target, 'value'), 'PRESS')
    setattr(prefs, _field(target, 'ctrl'), False)
    setattr(prefs, _field(target, 'shift'), False)
    setattr(prefs, _field(target, 'alt'), False)
    setattr(prefs, _field(target, 'oskey'), False)
    rebuild_shortcut(target, context)
    tag_redraw_all()
    return True


class WQBAR_OT_assign_shortcut(Operator):
    bl_idname = 'witch_quickbar.assign_shortcut'
    bl_label = 'Assign Witch Quickbar Shortcut'
    bl_description = 'Assign a keyboard shortcut to a Witch Quickbar action.'
    bl_options = {'REGISTER'}

    target: StringProperty(default='cycle')

    def invoke(self, context, event):
        data = _target_data(self.target)
        if not data:
            self.report({'WARNING'}, 'Unknown shortcut target')
            return {'CANCELLED'}
        self.report({'INFO'}, f"Press a shortcut for {data['label']} or Esc to cancel")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'ESC' and event.value == 'PRESS':
            self.report({'INFO'}, 'Shortcut assignment cancelled')
            return {'CANCELLED'}
        if event.type in IGNORED_CAPTURE_EVENTS:
            return {'RUNNING_MODAL'}
        if event.value != 'PRESS':
            return {'RUNNING_MODAL'}
        if event.type in MODIFIER_ONLY_EVENTS:
            return {'RUNNING_MODAL'}

        if assign_shortcut_from_event(context, self.target, event):
            data = _target_data(self.target)
            self.report({'INFO'}, f"{data['label']} shortcut: {shortcut_label(context, self.target)}")
            return {'FINISHED'}
        self.report({'WARNING'}, 'Could not assign shortcut')
        return {'CANCELLED'}


class WQBAR_OT_clear_shortcut(Operator):
    bl_idname = 'witch_quickbar.clear_shortcut'
    bl_label = 'Clear Witch Quickbar Shortcut'
    bl_description = 'Clear a Witch Quickbar shortcut.'
    bl_options = {'REGISTER'}

    target: StringProperty(default='cycle')

    def execute(self, context):
        data = _target_data(self.target)
        if not data:
            self.report({'WARNING'}, 'Unknown shortcut target')
            return {'CANCELLED'}
        if clear_shortcut(context, self.target):
            self.report({'INFO'}, f"Cleared {data['label']} shortcut")
            return {'FINISHED'}
        self.report({'WARNING'}, 'Could not clear shortcut')
        return {'CANCELLED'}


class WQBAR_OT_toggle_cycle_mode(Operator):
    bl_idname = 'witch_quickbar.toggle_cycle_mode'
    bl_label = 'Toggle Cycle Mode'
    bl_description = 'Include or exclude this mode from Cycle Modes.'
    bl_options = {'REGISTER'}

    mode_key: StringProperty(default='')

    def execute(self, context):
        prefs = addon_preferences(context)
        if not prefs or self.mode_key not in MODE_SEQUENCE:
            self.report({'WARNING'}, 'Unknown cycle mode')
            return {'CANCELLED'}
        enabled = cycle_enabled_modes(prefs)
        if self.mode_key in enabled:
            if len(enabled) <= 1:
                self.report({'WARNING'}, 'At least one mode must stay enabled for cycling')
                return {'CANCELLED'}
            enabled.remove(self.mode_key)
        else:
            enabled.append(self.mode_key)
        save_cycle_enabled_modes(prefs, enabled)
        tag_redraw_all()
        return {'FINISHED'}


class WQBAR_OT_open_preferences(Operator):
    bl_idname = 'witch_quickbar.open_preferences'
    bl_label = 'Open Witch Quickbar Preferences'
    bl_description = 'Open Blender Preferences to the Witch Quickbar add-on entry.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        except Exception:
            pass

        def _show_addon():
            try:
                bpy.context.preferences.active_section = 'ADDONS'
                try:
                    bpy.ops.preferences.addon_show(module=ADDON_PACKAGE)
                except Exception:
                    pass
            except Exception:
                pass
            return None

        try:
            bpy.app.timers.register(_show_addon, first_interval=0.15)
        except Exception:
            _show_addon()
        return {'FINISHED'}


class WQBAR_OT_check_updates(Operator):
    bl_idname = 'witch_quickbar.check_updates'
    bl_label = 'Check for Witch Quickbar Updates'
    bl_description = 'Open the Witch Quickbar GitHub update repository.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            bpy.ops.wm.url_open(url=UPDATE_URL)
            return {'FINISHED'}
        except Exception:
            self.report({'WARNING'}, 'Could not open update URL')
            return {'CANCELLED'}


CLASSES = (
    WQBAR_OT_assign_shortcut,
    WQBAR_OT_clear_shortcut,
    WQBAR_OT_toggle_cycle_mode,
    WQBAR_OT_open_preferences,
    WQBAR_OT_check_updates,
)
