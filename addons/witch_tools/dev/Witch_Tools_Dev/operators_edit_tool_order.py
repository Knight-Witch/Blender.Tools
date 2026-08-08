from bpy.props import IntProperty, StringProperty
from bpy.types import Operator

from .utils_context import addon_preferences


DEFAULT_EDIT_TOOL_ORDER = (
    'COORDINATE_COPY',
    'PLANAR_EDIT',
    'VERTEX_SNAP',
    'OBJECT_SNAP',
    'INJECT_NEW',
    'MAGIC_BRANCH',
    'EDGE_DOCTOR',
    'VERTEX_LOCKS',
    'SELECTION_SLOTS',
)

EDIT_TOOL_LABELS = {
    'COORDINATE_COPY': 'Coordinate Copy',
    'PLANAR_EDIT': 'Planar Edit',
    'VERTEX_SNAP': 'Vertex Snap',
    'OBJECT_SNAP': 'Object Snap',
    'INJECT_NEW': 'Inject New',
    'MAGIC_BRANCH': 'Magic Branch',
    'EDGE_DOCTOR': 'Edge Doctor',
    'VERTEX_LOCKS': 'Vertex Lock',
    'SELECTION_SLOTS': 'Selection Slots',
}


def parse_edit_tool_order(value):
    incoming = [item.strip() for item in str(value or '').split(',') if item.strip()]
    result = []
    for item in incoming:
        if item in EDIT_TOOL_LABELS and item not in result:
            result.append(item)
    for item in DEFAULT_EDIT_TOOL_ORDER:
        if item not in result:
            result.append(item)
    return result


def save_edit_tool_order(prefs, order):
    prefs.edit_tool_order = ','.join(parse_edit_tool_order(','.join(order)))


def _redraw(context):
    wm = getattr(context, 'window_manager', None)
    if wm is None:
        return
    for window in wm.windows:
        if window.screen is None:
            continue
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


class WITCHTOOLS_OT_edit_tool_move(Operator):
    bl_idname = 'witch_tools.edit_tool_move'
    bl_label = 'Move Edit Tool'
    bl_description = 'Move this Edit Tools section up or down in your saved custom order.'
    bl_options = {'INTERNAL'}

    tool_id: StringProperty()
    direction: IntProperty(default=0)

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs is None:
            return {'CANCELLED'}
        order = parse_edit_tool_order(prefs.edit_tool_order)
        if self.tool_id not in order or self.direction == 0:
            return {'CANCELLED'}
        index = order.index(self.tool_id)
        target = max(0, min(len(order) - 1, index + (1 if self.direction > 0 else -1)))
        if target == index:
            return {'FINISHED'}
        order[index], order[target] = order[target], order[index]
        save_edit_tool_order(prefs, order)
        _redraw(context)
        return {'FINISHED'}


class WITCHTOOLS_OT_edit_tool_reset_order(Operator):
    bl_idname = 'witch_tools.edit_tool_reset_order'
    bl_label = 'Reset Edit Tool Order'
    bl_description = 'Restore the default Witch Tools Edit Tools section order.'
    bl_options = {'INTERNAL'}

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs is None:
            return {'CANCELLED'}
        save_edit_tool_order(prefs, DEFAULT_EDIT_TOOL_ORDER)
        _redraw(context)
        return {'FINISHED'}


class WITCHTOOLS_OT_edit_tool_drag_reorder(Operator):
    bl_idname = 'witch_tools.edit_tool_drag_reorder'
    bl_label = 'Drag to Reorder Edit Tool'
    bl_description = 'Drag this handle up or down while Reorder Tools mode is enabled. Release to drop; Esc restores the prior order.'
    bl_options = {'INTERNAL', 'BLOCKING'}

    tool_id: StringProperty()
    _start_y = 0
    _start_index = 0
    _original = None
    _last_target = None

    def invoke(self, context, event):
        prefs = addon_preferences(context)
        if prefs is None or not getattr(prefs, 'edit_tool_reorder_mode', False):
            return {'CANCELLED'}
        order = parse_edit_tool_order(prefs.edit_tool_order)
        if self.tool_id not in order:
            return {'CANCELLED'}
        self._original = list(order)
        self._start_index = order.index(self.tool_id)
        self._start_y = event.mouse_y
        self._last_target = self._start_index
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        prefs = addon_preferences(context)
        if prefs is None:
            return {'CANCELLED'}
        if event.type == 'ESC' and event.value == 'PRESS':
            save_edit_tool_order(prefs, self._original)
            _redraw(context)
            return {'CANCELLED'}
        if event.type == 'MOUSEMOVE':
            steps = int(round((self._start_y - event.mouse_y) / 27.0))
            target = max(0, min(len(self._original) - 1, self._start_index + steps))
            if target != self._last_target:
                order = [item for item in self._original if item != self.tool_id]
                order.insert(target, self.tool_id)
                save_edit_tool_order(prefs, order)
                self._last_target = target
                _redraw(context)
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            _redraw(context)
            return {'FINISHED'}
        return {'RUNNING_MODAL'}


CLASSES = (
    WITCHTOOLS_OT_edit_tool_move,
    WITCHTOOLS_OT_edit_tool_reset_order,
    WITCHTOOLS_OT_edit_tool_drag_reorder,
)
