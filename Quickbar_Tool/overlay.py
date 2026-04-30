import bpy
from bpy.types import Operator

from .actions import execute_action
from .config import toggle_tool_open
from .draw import draw_overlay
from .icons import clear_cache
from .layout import (
    apply_mode_drop,
    apply_section_drop,
    build_layout,
    button_at,
    drop_mode_key,
    drop_section_key,
    resize_at,
)
from .utils import addon_preferences, tag_redraw_all


class Runtime:
    running = False
    handler = None
    dragging = False
    click_capture = False
    section_dragging = False
    section_drag_key = ''
    mode_dragging = False
    mode_drag_key = ''
    mode_press_action = ''
    mode_press_key = ''
    mode_press_x = 0
    mode_press_y = 0
    drag_offset_x = 0
    drag_offset_y = 0
    resizing = False
    resize_edge = ''
    resize_start_mouse_x = 0
    resize_start_mouse_y = 0
    resize_start_x = 0
    resize_start_w = 0
    resize_start_extra_h = 0
    hover = None
    mouse_x = -10000
    mouse_y = -10000
    cursor_forced = False


runtime = Runtime()


def draw_callback():
    draw_overlay(bpy.context, runtime)


def start_overlay(context):
    if runtime.running:
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
    runtime.click_capture = False
    runtime.section_dragging = False
    runtime.section_drag_key = ''
    runtime.mode_dragging = False
    runtime.mode_drag_key = ''
    runtime.mode_press_action = ''
    runtime.mode_press_key = ''
    runtime.resizing = False
    runtime.resize_edge = ''
    _restore_cursor(bpy.context)
    clear_cache()
    tag_redraw_all()


def _event_mouse_xy(event):
    mx = getattr(event, 'mouse_region_x', runtime.mouse_x)
    my = getattr(event, 'mouse_region_y', runtime.mouse_y)
    return mx, my


def _point_in_layout(layout, mx, my):
    return layout['x'] <= mx <= layout['x'] + layout['w'] and layout['y'] <= my <= layout['y'] + layout['h']


def _force_default_cursor(context):
    window = getattr(context, 'window', None)
    if not window or runtime.cursor_forced:
        return
    try:
        window.cursor_modal_set('DEFAULT')
        runtime.cursor_forced = True
    except Exception:
        runtime.cursor_forced = False


def _restore_cursor(context):
    window = getattr(context, 'window', None)
    if not window or not runtime.cursor_forced:
        return
    try:
        window.cursor_modal_restore()
    except Exception:
        pass
    runtime.cursor_forced = False


def _sync_cursor(context, layout, mx, my):
    active = (
        _point_in_layout(layout, mx, my)
        or runtime.dragging
        or runtime.resizing
        or runtime.section_dragging
        or runtime.mode_dragging
        or bool(runtime.mode_press_key)
    )
    if active:
        _force_default_cursor(context)
    else:
        _restore_cursor(context)


def _clear_mode_drag_state():
    runtime.mode_dragging = False
    runtime.mode_drag_key = ''
    runtime.mode_press_action = ''
    runtime.mode_press_key = ''
    runtime.click_capture = False


def _clear_section_drag_state():
    runtime.section_dragging = False
    runtime.section_drag_key = ''
    runtime.click_capture = False


def _clear_resize_state():
    runtime.resizing = False
    runtime.resize_edge = ''
    runtime.click_capture = False


class WQBAR_OT_show(Operator):
    bl_idname = 'witch_quickbar.show'
    bl_label = 'Show Witch Quickbar'
    bl_description = 'Show the floating Witch Quickbar quick-access bar.'
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        if runtime.running:
            return {'FINISHED'}
        start_overlay(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        return self.invoke(context, None)

    def modal(self, context, event):
        if not runtime.running:
            _restore_cursor(context)
            return {'CANCELLED'}
        if not (context.area and context.area.type == 'VIEW_3D' and context.region):
            _restore_cursor(context)
            return {'PASS_THROUGH'}

        mx, my = _event_mouse_xy(event)
        if getattr(event, 'mouse_region_x', None) is not None:
            runtime.mouse_x = mx
            runtime.mouse_y = my

        layout = build_layout(context)
        prefs = addon_preferences(context)
        if prefs is None:
            _restore_cursor(context)
            return {'PASS_THROUGH'}

        _sync_cursor(context, layout, mx, my)

        if runtime.dragging:
            return self._modal_dock_drag(context, event, mx, my, prefs)
        if runtime.resizing:
            return self._modal_resize(context, event, mx, my, prefs)
        if runtime.section_dragging:
            return self._modal_section_drag(event, layout, mx, my, prefs)
        if runtime.mode_dragging:
            return self._modal_mode_drag(event, layout, mx, my, prefs)
        if runtime.mode_press_key:
            return self._modal_mode_press(context, event, mx, my)

        hit = button_at(layout, mx, my) or resize_at(layout, mx, my)
        if event.type == 'MOUSEMOVE':
            if hit is not runtime.hover:
                runtime.hover = hit
                tag_redraw_all()
            return {'PASS_THROUGH'}

        if runtime.click_capture and event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            runtime.click_capture = False
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return self._handle_left_press(context, event, hit, mx, my, prefs)

        return {'PASS_THROUGH'}

    def _modal_dock_drag(self, context, event, mx, my, prefs):
        if event.type == 'MOUSEMOVE':
            prefs.dock_x = max(0, int(mx - runtime.drag_offset_x))
            prefs.dock_y = max(0, int(context.region.height - my - runtime.drag_offset_y))
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            runtime.dragging = False
            runtime.click_capture = False
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            runtime.dragging = False
            runtime.click_capture = False
            tag_redraw_all()
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def _modal_resize(self, context, event, mx, my, prefs):
        if event.type == 'MOUSEMOVE':
            if runtime.resize_edge == 'right':
                new_w = max(build_layout(context)['min_w'], runtime.resize_start_w + (mx - runtime.resize_start_mouse_x))
                prefs.dock_width = int(new_w)
            elif runtime.resize_edge == 'left':
                new_w = max(build_layout(context)['min_w'], runtime.resize_start_w - (mx - runtime.resize_start_mouse_x))
                right_edge = runtime.resize_start_x + runtime.resize_start_w
                prefs.dock_width = int(new_w)
                prefs.dock_x = max(0, int(right_edge - new_w))
            elif runtime.resize_edge == 'bottom':
                prefs.dock_height_extra = max(0, int(runtime.resize_start_extra_h + (runtime.resize_start_mouse_y - my)))
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            _clear_resize_state()
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            _clear_resize_state()
            tag_redraw_all()
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def _modal_section_drag(self, event, layout, mx, my, prefs):
        if event.type == 'MOUSEMOVE':
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            apply_section_drop(prefs, runtime.section_drag_key, drop_section_key(layout, mx, my))
            _clear_section_drag_state()
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            _clear_section_drag_state()
            tag_redraw_all()
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def _modal_mode_drag(self, event, layout, mx, my, prefs):
        if event.type == 'MOUSEMOVE':
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            apply_mode_drop(prefs, runtime.mode_drag_key, drop_mode_key(layout, mx, my))
            _clear_mode_drag_state()
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            _clear_mode_drag_state()
            tag_redraw_all()
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def _modal_mode_press(self, context, event, mx, my):
        if event.type == 'MOUSEMOVE':
            if abs(mx - runtime.mode_press_x) > 5 or abs(my - runtime.mode_press_y) > 5:
                runtime.mode_dragging = True
                runtime.mode_drag_key = runtime.mode_press_key
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            action = runtime.mode_press_action
            _clear_mode_drag_state()
            ok, msg = execute_action(context, action)
            if not ok and msg:
                self.report({'WARNING'}, msg)
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            _clear_mode_drag_state()
            tag_redraw_all()
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

    def _handle_left_press(self, context, event, hit, mx, my, prefs):
        if not hit:
            layout = build_layout(context)
            resize = resize_at(layout, mx, my)
            if resize and not prefs.locked:
                runtime.click_capture = True
                runtime.resizing = True
                runtime.resize_edge = resize.get('edge', '')
                runtime.resize_start_mouse_x = mx
                runtime.resize_start_mouse_y = my
                runtime.resize_start_x = prefs.dock_x
                runtime.resize_start_w = layout['w']
                runtime.resize_start_extra_h = getattr(prefs, 'dock_height_extra', 0)
                tag_redraw_all()
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}
        if hit.get('kind') == 'resize':
            if not prefs.locked:
                layout = build_layout(context)
                runtime.click_capture = True
                runtime.resizing = True
                runtime.resize_edge = hit.get('edge', '')
                runtime.resize_start_mouse_x = mx
                runtime.resize_start_mouse_y = my
                runtime.resize_start_x = prefs.dock_x
                runtime.resize_start_w = layout['w']
                runtime.resize_start_extra_h = getattr(prefs, 'dock_height_extra', 0)
                tag_redraw_all()
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}

        runtime.click_capture = True
        action = hit.get('action')

        if action == 'TOGGLE_LOCK':
            prefs.locked = not prefs.locked
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        if hit.get('group') == 'mode' and action:
            runtime.mode_press_action = action
            runtime.mode_press_key = hit.get('mode_key', '')
            runtime.mode_press_x = mx
            runtime.mode_press_y = my
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        if hit.get('kind') == 'drag':
            if not prefs.locked:
                runtime.dragging = True
                runtime.drag_offset_x = mx - prefs.dock_x
                runtime.drag_offset_y = context.region.height - my - prefs.dock_y
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        if action == 'TOGGLE_MORE_TOOLS':
            prefs.more_tools_open = not prefs.more_tools_open
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        if action and action.startswith('TOGGLE_TOOL:'):
            toggle_tool_open(prefs, action.split(':', 1)[1])
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        if action and action.startswith('DRAG_TOOL:'):
            runtime.section_dragging = True
            runtime.section_drag_key = action.split(':', 1)[1]
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        if hit.get('enabled', True) and action and action != 'NONE':
            ok, msg = execute_action(context, action)
            if not ok and msg:
                self.report({'WARNING'}, msg)
            tag_redraw_all()
            return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}


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
            return {'FINISHED'}
        if context.area and context.area.type == 'VIEW_3D':
            bpy.ops.witch_quickbar.show('INVOKE_DEFAULT')
        else:
            start_overlay(context)
        return {'FINISHED'}


class WQBAR_OT_reset_position(Operator):
    bl_idname = 'witch_quickbar.reset_position'
    bl_label = 'Reset Witch Quickbar Position'
    bl_description = 'Move Witch Quickbar back near the upper-left of the 3D View.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs:
            prefs.dock_x = 48
            prefs.dock_y = 36
        tag_redraw_all()
        return {'FINISHED'}


class WQBAR_OT_lock_position(Operator):
    bl_idname = 'witch_quickbar.lock_position'
    bl_label = 'Lock Witch Quickbar Position'
    bl_description = 'Toggle whether the floating Witch Quickbar can be dragged.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs:
            prefs.locked = not prefs.locked
        tag_redraw_all()
        return {'FINISHED'}


class WQBAR_OT_cycle_modes(Operator):
    bl_idname = 'witch_quickbar.cycle_modes'
    bl_label = 'Witch Quickbar Cycle Modes'
    bl_description = 'Cycle through the visible Witch Quickbar mode order.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ok, msg = execute_action(context, 'MODE:CYCLE')
        if ok:
            tag_redraw_all()
            return {'FINISHED'}
        self.report({'WARNING'}, msg or 'Could not cycle modes')
        return {'CANCELLED'}


class WQBAR_OT_last_mode(Operator):
    bl_idname = 'witch_quickbar.last_mode'
    bl_label = 'Witch Quickbar Last Mode Used'
    bl_description = 'Return to the last mode used through Witch Quickbar.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ok, msg = execute_action(context, 'MODE:RETURN')
        if ok:
            tag_redraw_all()
            return {'FINISHED'}
        self.report({'WARNING'}, msg or 'No last mode available')
        return {'CANCELLED'}


CLASSES = (
    WQBAR_OT_show,
    WQBAR_OT_hide,
    WQBAR_OT_toggle,
    WQBAR_OT_reset_position,
    WQBAR_OT_lock_position,
    WQBAR_OT_cycle_modes,
    WQBAR_OT_last_mode,
)
