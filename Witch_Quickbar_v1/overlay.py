import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator

from .actions import execute_action
from .draw import draw_overlay
from .icons import clear_cache
from .layout import close_to_launcher, main_toggle_display, maximize_display, set_display_state, DISPLAY_FULL, DISPLAY_MINIMIZED
from .utils import addon_preferences, tag_redraw_all


class Runtime:
    running = False
    handler = None
    dragging = False
    section_dragging = False
    section_drag_key = ''
    mode_dragging = False
    mode_drag_key = ''
    resizing = False
    resize_edge = ''
    mouse_x = -10000
    mouse_y = -10000
    gizmo_items = []
    launcher_dragging = False


runtime = Runtime()


def draw_callback():
    draw_overlay(bpy.context, runtime)


def start_overlay(context):
    if runtime.running:
        tag_redraw_all()
        return True
    runtime.handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback, (), 'WINDOW', 'POST_PIXEL')
    runtime.running = True
    tag_redraw_all()
    return True


def stop_overlay():
    if runtime.handler is not None:
        try:
            bpy.types.SpaceView3D.draw_handler_remove(runtime.handler, 'WINDOW')
        except Exception:
            pass
    runtime.handler = None
    runtime.running = False
    runtime.dragging = False
    runtime.section_dragging = False
    runtime.section_drag_key = ''
    runtime.mode_dragging = False
    runtime.mode_drag_key = ''
    runtime.resizing = False
    runtime.resize_edge = ''
    runtime.gizmo_items = []
    runtime.launcher_dragging = False
    clear_cache()
    tag_redraw_all()


def _report_result(operator, ok, msg):
    if ok:
        tag_redraw_all()
        return {'FINISHED'}
    operator.report({'WARNING'}, msg or 'Action failed')
    tag_redraw_all()
    return {'CANCELLED'}


def _execute(operator, context, action):
    ok, msg = execute_action(context, action)
    return _report_result(operator, ok, msg)


class WQBAR_OT_show(Operator):
    bl_idname = 'witch_quickbar.show'
    bl_label = 'Show Witch Quickbar'
    bl_description = 'Show the floating Witch Quickbar quick-access bar.'
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        start_overlay(context)
        return {'FINISHED'}

    def execute(self, context):
        start_overlay(context)
        return {'FINISHED'}


class WQBAR_OT_hide(Operator):
    bl_idname = 'witch_quickbar.hide'
    bl_label = 'Hide Witch Quickbar'
    bl_description = 'Hide the floating Witch Quickbar quick-access bar.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        stop_overlay()
        return {'FINISHED'}


class WQBAR_OT_toggle(Operator):
    bl_idname = 'witch_quickbar.toggle'
    bl_label = 'Toggle Witch Quickbar'
    bl_description = 'Show or hide the floating Witch Quickbar quick-access bar.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        if runtime.running:
            stop_overlay()
        else:
            start_overlay(context)
        return {'FINISHED'}


class WQBAR_OT_toggle_display_state(Operator):
    bl_idname = 'witch_quickbar.toggle_display_state'
    bl_label = 'Witch Quickbar Open/Close'
    bl_description = 'Cycle Witch Quickbar between open, minimized, and launcher states.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs:
            main_toggle_display(prefs)
        tag_redraw_all()
        return {'FINISHED'}


class WQBAR_OT_maximize_display_state(Operator):
    bl_idname = 'witch_quickbar.maximize_display_state'
    bl_label = 'Witch Quickbar Maximize Open/Close'
    bl_description = 'Open Witch Quickbar to full view, or expand all sections when already maximized.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs:
            maximize_display(prefs, expand_all_if_full=True)
        tag_redraw_all()
        return {'FINISHED'}


class WQBAR_OT_reset_position(Operator):
    bl_idname = 'witch_quickbar.reset_position'
    bl_label = 'Reset Witch Quickbar Position'
    bl_description = 'Move Witch Quickbar back near the upper-left of the 3D View.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs:
            prefs.dock_x = 48
            prefs.dock_y = 36
            prefs.dock_width = 0
            prefs.dock_height_extra = 0
        tag_redraw_all()
        return {'FINISHED'}


class WQBAR_OT_lock_position(Operator):
    bl_idname = 'witch_quickbar.lock_position'
    bl_label = 'Lock Witch Quickbar Position'
    bl_description = 'Toggle whether the floating Witch Quickbar can be dragged or resized.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs:
            prefs.locked = not prefs.locked
        tag_redraw_all()
        return {'FINISHED'}



def _cycle_quickbar_scale(prefs):
    presets = (0.85, 1.0, 1.15, 1.30, 1.45)
    current = float(getattr(prefs, 'dock_scale', 1.0) or 1.0)
    closest = min(range(len(presets)), key=lambda i: abs(presets[i] - current))
    if current < presets[closest] - 0.01:
        next_value = presets[closest]
    else:
        next_value = presets[(closest + 1) % len(presets)]
    prefs.dock_scale = next_value


class WQBAR_OT_ui_action(Operator):
    bl_idname = 'witch_quickbar.ui_action'
    bl_label = 'Witch Quickbar UI Action'
    bl_description = ''
    bl_options = {'REGISTER'}

    action: StringProperty(default='')

    @classmethod
    def description(cls, context, properties):
        action = getattr(properties, 'action', '')
        descriptions = {
            'TOGGLE_LOCK': 'Lock/unlock dock position',
            'TOGGLE_MORE_TOOLS': 'Show/Hide More Tools',
            'ROTATE_TOGGLE': 'Toggle 90° / 180°',
            'MIRROR_PIVOT:CURSOR': 'Cursor',
            'MIRROR_PIVOT:WORLD': 'World',
            'TOGGLE_FOOTER_SETTINGS': 'Hotkeys',
            'OPEN_PREFERENCES': 'Settings',
            'CHECK_UPDATES': 'Check for updates',
            'CYCLE_SCALE': 'Scale quickbar',
            'DISPLAY_MINIMIZE': 'Minimize to Mode bar',
            'DISPLAY_MAXIMIZE': 'Maximize Quickbar',
            'DISPLAY_CLOSE': 'Close to launcher',
        }
        if action.startswith('TOGGLE_TOOL:'):
            return ''
        return descriptions.get(action, '')

    def execute(self, context):
        prefs = addon_preferences(context)
        action = self.action
        if prefs is None:
            return {'CANCELLED'}
        if action == 'TOGGLE_LOCK':
            prefs.locked = not prefs.locked
            tag_redraw_all()
            return {'FINISHED'}
        if action == 'TOGGLE_MORE_TOOLS':
            prefs.more_tools_open = not prefs.more_tools_open
            tag_redraw_all()
            return {'FINISHED'}
        if action == 'TOGGLE_FOOTER_SETTINGS':
            prefs.footer_settings_open = not getattr(prefs, 'footer_settings_open', False)
            tag_redraw_all()
            return {'FINISHED'}
        if action == 'CYCLE_SCALE':
            _cycle_quickbar_scale(prefs)
            tag_redraw_all()
            return {'FINISHED'}
        if action == 'DISPLAY_MINIMIZE':
            set_display_state(prefs, DISPLAY_MINIMIZED)
            tag_redraw_all()
            return {'FINISHED'}
        if action == 'DISPLAY_MAXIMIZE':
            maximize_display(prefs, expand_all_if_full=True)
            tag_redraw_all()
            return {'FINISHED'}
        if action == 'DISPLAY_CLOSE':
            close_to_launcher(prefs)
            tag_redraw_all()
            return {'FINISHED'}
        if action.startswith('TOGGLE_TOOL:'):
            from .config import toggle_tool_open
            toggle_tool_open(prefs, action.split(':', 1)[1])
            tag_redraw_all()
            return {'FINISHED'}
        return _execute(self, context, action)


class WQBAR_OT_rotate_axis(Operator):
    bl_idname = 'witch_quickbar.rotate_axis'
    bl_label = 'Witch Quickbar Rotate'
    bl_description = 'Rotate the current selection around an axis.'
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name='Axis',
        items=(('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')),
        default='X',
    )

    def execute(self, context):
        return _execute(self, context, f'ROTATE:{self.axis}')


class WQBAR_OT_origin_set(Operator):
    bl_idname = 'witch_quickbar.origin_set'
    bl_label = 'Witch Quickbar Set Origin'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    origin_type: EnumProperty(
        name='Origin Type',
        items=(('GEOMETRY', 'Geometry', ''), ('CURSOR', 'Cursor', '')),
        default='GEOMETRY',
    )

    @classmethod
    def description(cls, context, properties):
        origin_type = getattr(properties, 'origin_type', '')
        if origin_type == 'GEOMETRY':
            return 'Origin to geometry'
        if origin_type == 'CURSOR':
            return 'Origin to cursor'
        return ''

    def execute(self, context):
        return _execute(self, context, f'ORIGIN:{self.origin_type}')


class WQBAR_OT_snap(Operator):
    bl_idname = 'witch_quickbar.snap'
    bl_label = 'Witch Quickbar Snap'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    snap_action: EnumProperty(
        name='Snap Action',
        items=(
            ('CURSOR_TO_SELECTED', 'Cursor to Selected', ''),
            ('CURSOR_TO_GRID', 'Cursor to Grid', ''),
            ('SELECTION_TO_CURSOR', 'Selection to Cursor', ''),
            ('SELECTION_TO_GRID', 'Selection to Grid', ''),
        ),
        default='CURSOR_TO_SELECTED',
    )

    @classmethod
    def description(cls, context, properties):
        labels = {
            'CURSOR_TO_SELECTED': 'Cursor to selected',
            'CURSOR_TO_GRID': 'Cursor to grid',
            'SELECTION_TO_CURSOR': 'Selected to cursor',
            'SELECTION_TO_GRID': 'Selected to grid',
        }
        return labels.get(getattr(properties, 'snap_action', ''), '')

    def execute(self, context):
        return _execute(self, context, f'SNAP:{self.snap_action}')


class WQBAR_OT_mirror_selected(Operator):
    bl_idname = 'witch_quickbar.mirror_selected'
    bl_label = 'Witch Quickbar Mirror Selected Objects'
    bl_description = 'Duplicate selected mesh objects and mirror the duplicates on X.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return _execute(self, context, 'MIRROR_OBJECTS')


class WQBAR_OT_cycle_modes(Operator):
    bl_idname = 'witch_quickbar.cycle_modes'
    bl_label = 'Witch Quickbar Cycle Modes'
    bl_description = 'Cycle through the visible Witch Quickbar mode order.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        return _execute(self, context, 'MODE:CYCLE')


class WQBAR_OT_last_mode(Operator):
    bl_idname = 'witch_quickbar.last_mode'
    bl_label = 'Witch Quickbar Last Mode Used'
    bl_description = 'Return to the last mode used through Witch Quickbar.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        return _execute(self, context, 'MODE:RETURN')


class WQBAR_OT_noop(Operator):
    bl_idname = 'witch_quickbar.noop'
    bl_label = 'Witch Quickbar Disabled Control'
    bl_description = 'This control is not available in the current context.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'CANCELLED'}



CLASSES = (
    WQBAR_OT_show,
    WQBAR_OT_hide,
    WQBAR_OT_toggle,
    WQBAR_OT_toggle_display_state,
    WQBAR_OT_maximize_display_state,
    WQBAR_OT_reset_position,
    WQBAR_OT_lock_position,
    WQBAR_OT_ui_action,
    WQBAR_OT_rotate_axis,
    WQBAR_OT_origin_set,
    WQBAR_OT_snap,
    WQBAR_OT_mirror_selected,
    WQBAR_OT_cycle_modes,
    WQBAR_OT_last_mode,
    WQBAR_OT_noop,
)
