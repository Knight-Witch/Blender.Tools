import math

import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import GizmoGroup, Operator
from mathutils import Matrix

from .actions import execute_action
from .config import MODE_BUTTON_MAP
from .layout import apply_mode_drop, apply_section_drop, build_layout, drop_mode_key, drop_section_key, restore_from_launcher
from .overlay import runtime
from .utils import addon_preferences, tag_redraw_all


def _execute(operator, context, action):
    ok, msg = execute_action(context, action)
    if ok:
        tag_redraw_all()
        return {'FINISHED'}
    operator.report({'WARNING'}, msg or 'Action failed')
    tag_redraw_all()
    return {'CANCELLED'}

MAX_GIZMOS = 256
TILE_SIZE = 24


def _copy_item(item):
    return dict(item)


def _tile_rect(item, tile_size=TILE_SIZE):
    x, y, w, h = item['x'], item['y'], item['w'], item['h']
    if w <= tile_size * 1.35 and h <= tile_size * 1.35:
        yield _copy_item(item)
        return
    cols = max(1, math.ceil(w / tile_size))
    rows = max(1, math.ceil(h / tile_size))
    cell_w = w / cols
    cell_h = h / rows
    for row in range(rows):
        for col in range(cols):
            tile = _copy_item(item)
            tile['x'] = x + col * cell_w
            tile['y'] = y + row * cell_h
            tile['w'] = cell_w
            tile['h'] = cell_h
            yield tile


def gizmo_items_from_layout(layout):
    items = []

    if layout.get('display_state') == 'CLOSED':
        for button in layout.get('buttons', []):
            items.append(dict(button))
        return items[:MAX_GIZMOS]

    for button in layout.get('buttons', []):
        if button.get('style') == 'drag_zone':
            continue
        if button.get('w', 0) > button.get('h', 0) * 1.35:
            for tile in _tile_rect(button):
                items.append(tile)
        else:
            items.append(dict(button))

    for handle in layout.get('resize_handles', []):
        for tile in _tile_rect(handle, tile_size=18):
            items.append(tile)

    for button in layout.get('buttons', []):
        if button.get('style') == 'drag_zone':
            for tile in _tile_rect(button):
                items.append(tile)

    drag = dict(layout['drag'])
    drag['action'] = 'DRAG_DOCK'
    drag['tooltip'] = ''

    titlebar_buttons = [item for item in layout.get('buttons', []) if item.get('group') == 'titlebar']
    left = drag['x'] + 4
    right = drag['x'] + drag['w'] - 4
    if titlebar_buttons:
        center_x = drag['x'] + drag['w'] / 2
        left_items = [item for item in titlebar_buttons if item['x'] + item['w'] / 2 <= center_x]
        right_items = [item for item in titlebar_buttons if item['x'] + item['w'] / 2 > center_x]
        if left_items:
            left = max(left, max(item['x'] + item['w'] for item in left_items) + 6)
        if right_items:
            right = min(right, min(item['x'] for item in right_items) - 6)
    if right > left + 12:
        drag['x'] = left
        drag['w'] = right - left
        for tile in _tile_rect(drag):
            items.append(tile)

    return items[:MAX_GIZMOS]


def _set_matrix(gizmo, item):
    cx = item['x'] + item['w'] / 2
    cy = item['y'] + item['h'] / 2
    gizmo.matrix_basis = Matrix.Translation((cx, cy, 0.0))
    gizmo.scale_basis = max(2.0, max(item['w'], item['h']) * 0.50)


def _set_invisible_style(gizmo, tooltip=''):
    try:
        gizmo.icon = 'BLANK1'
    except Exception:
        pass
    try:
        gizmo.draw_options = {'BACKDROP'}
    except Exception:
        pass
    gizmo.color = (0.0, 0.0, 0.0)
    gizmo.color_highlight = (0.0, 0.0, 0.0)
    gizmo.alpha = 0.001
    gizmo.alpha_highlight = 0.001
    try:
        gizmo.use_tooltip = bool(tooltip)
        gizmo.name = tooltip or ''
    except Exception:
        pass


def _target_operator_for_item(gizmo, item):
    action = item.get('action', '')
    if not item.get('enabled', True):
        gizmo.target_set_operator('witch_quickbar.noop')
        return

    if item.get('kind') == 'resize':
        props = gizmo.target_set_operator('witch_quickbar.resize_handle')
        props.edge = item.get('edge', '')
        return

    if item.get('kind') == 'drag' or action == 'DRAG_DOCK':
        gizmo.target_set_operator('witch_quickbar.drag_dock')
        return

    if item.get('group') == 'mode' and action.startswith('MODE:'):
        props = gizmo.target_set_operator('witch_quickbar.mode_button')
        props.action = action
        props.mode_key = item.get('mode_key', '')
        return

    if action == 'LAUNCHER_BUTTON':
        gizmo.target_set_operator('witch_quickbar.launcher_button')
        return

    if action.startswith('DRAG_TOOL:'):
        props = gizmo.target_set_operator('witch_quickbar.drag_section')
        props.tool_key = action.split(':', 1)[1]
        return

    if action.startswith('ROTATE:'):
        props = gizmo.target_set_operator('witch_quickbar.rotate_axis')
        props.axis = action.split(':', 1)[1]
        return

    if action.startswith('ORIGIN:'):
        props = gizmo.target_set_operator('witch_quickbar.origin_set')
        props.origin_type = action.split(':', 1)[1]
        return

    if action.startswith('SNAP:'):
        props = gizmo.target_set_operator('witch_quickbar.snap')
        props.snap_action = action.split(':', 1)[1]
        return

    if action == 'MIRROR_OBJECTS':
        gizmo.target_set_operator('witch_quickbar.mirror_selected')
        return

    if action.startswith('ASSIGN_SHORTCUT:'):
        props = gizmo.target_set_operator('witch_quickbar.assign_shortcut')
        props.target = action.split(':', 1)[1]
        return

    if action.startswith('CLEAR_SHORTCUT:'):
        props = gizmo.target_set_operator('witch_quickbar.clear_shortcut')
        props.target = action.split(':', 1)[1]
        return

    if action:
        props = gizmo.target_set_operator('witch_quickbar.ui_action')
        props.action = action
        return

    gizmo.target_set_operator('witch_quickbar.noop')


class WQBAR_GGT_quickbar_buttons(GizmoGroup):
    bl_idname = 'WQBAR_GGT_quickbar_buttons'
    bl_label = 'Witch Quickbar Buttons'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        return bool(runtime.running and context.area and context.area.type == 'VIEW_3D')

    def setup(self, context):
        self._slots = []
        for _index in range(MAX_GIZMOS):
            gizmo = self.gizmos.new('GIZMO_GT_button_2d')
            _set_invisible_style(gizmo)
            gizmo.target_set_operator('witch_quickbar.noop')
            self._slots.append(gizmo)

    def draw_prepare(self, context):
        try:
            layout = build_layout(context)
            items = gizmo_items_from_layout(layout)
        except Exception:
            items = []
        runtime.gizmo_items = items
        for index, gizmo in enumerate(self._slots):
            if index < len(items):
                item = items[index]
                _set_matrix(gizmo, item)
                _set_invisible_style(gizmo, item.get('tooltip', ''))
                _target_operator_for_item(gizmo, item)
                try:
                    gizmo.hide = False
                except Exception:
                    pass
            else:
                gizmo.matrix_basis = Matrix.Translation((-10000.0, -10000.0, 0.0))
                gizmo.scale_basis = 0.001
                try:
                    gizmo.hide = True
                except Exception:
                    pass


class WQBAR_OT_launcher_button(Operator):
    bl_idname = 'witch_quickbar.launcher_button'
    bl_label = 'Open Witch Quickbar Launcher'
    bl_description = 'Open Witch Quickbar, or drag the launcher button.'
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            return {'CANCELLED'}
        runtime.launcher_dragging = False
        runtime.mouse_x = event.mouse_region_x
        runtime.mouse_y = event.mouse_region_y
        self._start_x = event.mouse_region_x
        self._start_y = event.mouse_region_y
        self._start_launcher_x = prefs.launcher_x
        self._start_launcher_y = prefs.launcher_y
        context.window_manager.modal_handler_add(self)
        tag_redraw_all()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            runtime.launcher_dragging = False
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            runtime.mouse_x = event.mouse_region_x
            runtime.mouse_y = event.mouse_region_y
            dx = event.mouse_region_x - self._start_x
            dy = event.mouse_region_y - self._start_y
            if abs(dx) > 5 or abs(dy) > 5:
                runtime.launcher_dragging = True
            if runtime.launcher_dragging:
                prefs.launcher_x = max(0, int(self._start_launcher_x + dx))
                prefs.launcher_y = max(0, int(self._start_launcher_y + dy))
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            if not runtime.launcher_dragging:
                restore_from_launcher(prefs)
            runtime.launcher_dragging = False
            tag_redraw_all()
            return {'FINISHED'}
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            runtime.launcher_dragging = False
            tag_redraw_all()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


class WQBAR_OT_drag_dock(Operator):
    bl_idname = 'witch_quickbar.drag_dock'
    bl_label = 'Drag Witch Quickbar'
    bl_description = ''
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        prefs = addon_preferences(context)
        if not prefs or prefs.locked:
            return {'CANCELLED'}
        runtime.dragging = True
        runtime.mouse_x = event.mouse_region_x
        runtime.mouse_y = event.mouse_region_y
        self._offset_x = event.mouse_region_x - prefs.dock_x
        self._offset_y = context.region.height - event.mouse_region_y - prefs.dock_y
        context.window_manager.modal_handler_add(self)
        tag_redraw_all()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            runtime.dragging = False
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            runtime.mouse_x = event.mouse_region_x
            runtime.mouse_y = event.mouse_region_y
            prefs.dock_x = max(0, int(event.mouse_region_x - self._offset_x))
            prefs.dock_y = max(0, int(context.region.height - event.mouse_region_y - self._offset_y))
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            runtime.dragging = False
            tag_redraw_all()
            return {'FINISHED'}
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            runtime.dragging = False
            tag_redraw_all()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


class WQBAR_OT_resize_handle(Operator):
    bl_idname = 'witch_quickbar.resize_handle'
    bl_label = 'Resize Witch Quickbar'
    bl_description = ''
    bl_options = {'REGISTER'}

    edge: EnumProperty(
        name='Edge',
        items=(('left', 'Left', ''), ('right', 'Right', ''), ('bottom', 'Bottom', '')),
        default='right',
    )

    def invoke(self, context, event):
        prefs = addon_preferences(context)
        if not prefs or prefs.locked:
            return {'CANCELLED'}
        layout = build_layout(context)
        runtime.resizing = True
        runtime.resize_edge = self.edge
        runtime.mouse_x = event.mouse_region_x
        runtime.mouse_y = event.mouse_region_y
        self._start_mouse_x = event.mouse_region_x
        self._start_mouse_y = event.mouse_region_y
        self._start_x = prefs.dock_x
        self._start_w = layout['w']
        self._start_min_w = layout['min_w']
        self._start_extra_h = getattr(prefs, 'dock_height_extra', 0)
        context.window_manager.modal_handler_add(self)
        tag_redraw_all()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            runtime.resizing = False
            runtime.resize_edge = ''
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            runtime.mouse_x = event.mouse_region_x
            runtime.mouse_y = event.mouse_region_y
            if self.edge == 'right':
                prefs.dock_width = int(max(self._start_min_w, self._start_w + (event.mouse_region_x - self._start_mouse_x)))
            elif self.edge == 'left':
                new_w = max(self._start_min_w, self._start_w - (event.mouse_region_x - self._start_mouse_x))
                right_edge = self._start_x + self._start_w
                prefs.dock_width = int(new_w)
                prefs.dock_x = max(0, int(right_edge - new_w))
            elif self.edge == 'bottom':
                prefs.dock_height_extra = max(0, int(self._start_extra_h + (self._start_mouse_y - event.mouse_region_y)))
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            runtime.resizing = False
            runtime.resize_edge = ''
            tag_redraw_all()
            return {'FINISHED'}
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            runtime.resizing = False
            runtime.resize_edge = ''
            tag_redraw_all()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


class WQBAR_OT_drag_section(Operator):
    bl_idname = 'witch_quickbar.drag_section'
    bl_label = 'Reorder Witch Quickbar Section'
    bl_description = ''
    bl_options = {'REGISTER'}

    tool_key: StringProperty(default='')

    def invoke(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            return {'CANCELLED'}
        runtime.section_dragging = True
        runtime.section_drag_key = self.tool_key
        runtime.mouse_x = event.mouse_region_x
        runtime.mouse_y = event.mouse_region_y
        context.window_manager.modal_handler_add(self)
        tag_redraw_all()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            runtime.section_dragging = False
            runtime.section_drag_key = ''
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            runtime.mouse_x = event.mouse_region_x
            runtime.mouse_y = event.mouse_region_y
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            layout = build_layout(context)
            apply_section_drop(prefs, runtime.section_drag_key, drop_section_key(layout, event.mouse_region_x, event.mouse_region_y))
            runtime.section_dragging = False
            runtime.section_drag_key = ''
            tag_redraw_all()
            return {'FINISHED'}
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            runtime.section_dragging = False
            runtime.section_drag_key = ''
            tag_redraw_all()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


class WQBAR_OT_mode_button(Operator):
    bl_idname = 'witch_quickbar.mode_button'
    bl_label = 'Witch Quickbar Mode Button'
    bl_description = 'Switch modes.'
    bl_options = {'REGISTER'}

    action: StringProperty(default='')
    mode_key: StringProperty(default='')

    @classmethod
    def description(cls, context, properties):
        key = getattr(properties, 'mode_key', '')
        item = MODE_BUTTON_MAP.get(key)
        if item:
            return item[2]
        return 'Switch modes'

    def invoke(self, context, event):
        runtime.mode_dragging = False
        runtime.mode_drag_key = self.mode_key
        runtime.mouse_x = event.mouse_region_x
        runtime.mouse_y = event.mouse_region_y
        self._start_x = event.mouse_region_x
        self._start_y = event.mouse_region_y
        context.window_manager.modal_handler_add(self)
        tag_redraw_all()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        prefs = addon_preferences(context)
        if not prefs:
            runtime.mode_dragging = False
            runtime.mode_drag_key = ''
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            runtime.mouse_x = event.mouse_region_x
            runtime.mouse_y = event.mouse_region_y
            if abs(event.mouse_region_x - self._start_x) > 5 or abs(event.mouse_region_y - self._start_y) > 5:
                runtime.mode_dragging = True
            tag_redraw_all()
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            if runtime.mode_dragging:
                layout = build_layout(context)
                apply_mode_drop(prefs, self.mode_key, drop_mode_key(layout, event.mouse_region_x, event.mouse_region_y))
                runtime.mode_dragging = False
                runtime.mode_drag_key = ''
                tag_redraw_all()
                return {'FINISHED'}
            runtime.mode_dragging = False
            runtime.mode_drag_key = ''
            runtime.mouse_x = -10000
            runtime.mouse_y = -10000
            tag_redraw_all()
            return _execute(self, context, self.action)
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            runtime.mode_dragging = False
            runtime.mode_drag_key = ''
            tag_redraw_all()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}


CLASSES = (
    WQBAR_GGT_quickbar_buttons,
    WQBAR_OT_launcher_button,
    WQBAR_OT_drag_dock,
    WQBAR_OT_resize_handle,
    WQBAR_OT_drag_section,
    WQBAR_OT_mode_button,
)
