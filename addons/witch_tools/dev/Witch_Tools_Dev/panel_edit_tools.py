from bpy.types import Panel

from .operators_edit_tool_order import EDIT_TOOL_LABELS, parse_edit_tool_order
from .panel_base import WTHeaderPanelMixin
from .panel_edit_sections import draw_edge_doctor, draw_object_snap, draw_selection_slots, draw_vertex_locks, draw_vertex_snap
from .panel_precision_edit import draw_coordinate_copy, draw_inject_new, draw_magic_branch, draw_planar_edit
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .utils_context import ui_state_owner


class VIEW3D_PT_wt_edit_tools(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_edit_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['EDIT_TOOLS']
    panel_title = 'Edit Tools'
    panel_icon = 'EDITMODE_HLT'
    bl_options = {'DEFAULT_CLOSED'}
    bl_description = 'Precision placement, snapping, drag-and-drop topology building, Edge Doctor repair, saved selections, and protected edit tools.'

    def _draw_reorder(self, layout, ui):
        box = layout.box()
        header = box.row(align=True)
        header.label(text='Reorder Edit Tools', icon='SORTSIZE')
        header.prop(ui, 'edit_tool_reorder_mode', text='Done', icon='CHECKMARK', toggle=True)
        order = parse_edit_tool_order(ui.edit_tool_order)
        for index, tool_id in enumerate(order):
            row = box.row(align=True)
            drag = row.operator('witch_tools.edit_tool_drag_reorder', text='', icon='SORTSIZE')
            drag.tool_id = tool_id
            row.label(text=EDIT_TOOL_LABELS.get(tool_id, tool_id))
            up = row.row(align=True)
            up.ui_units_x = 1.0
            up.enabled = index > 0
            op = up.operator('witch_tools.edit_tool_move', text='', icon='TRIA_UP')
            op.tool_id = tool_id
            op.direction = -1
            down = row.row(align=True)
            down.ui_units_x = 1.0
            down.enabled = index < len(order) - 1
            op = down.operator('witch_tools.edit_tool_move', text='', icon='TRIA_DOWN')
            op.tool_id = tool_id
            op.direction = 1
        reset = box.row()
        reset.operator('witch_tools.edit_tool_reset_order', text='Reset Default Order', icon='LOOP_BACK')
        hint = box.row()
        hint.scale_y = 0.65
        hint.label(text='Drag the grip to move a compact row; arrows are a precise fallback.')

    def draw(self, context):
        props = context.scene.witch_tools
        precision = context.scene.wt_precision_edit
        ui = ui_state_owner(context)
        layout = self.layout

        if getattr(ui, 'ui_minimal_mode', False):
            return

        controls = layout.row(align=True)
        controls.prop(ui, 'edit_tool_reorder_mode', text='Reorder Tools', icon='SORTSIZE', toggle=True)
        if getattr(ui, 'edit_tool_reorder_mode', False):
            self._draw_reorder(layout, ui)
            return

        drawers = {
            'COORDINATE_COPY': lambda: draw_coordinate_copy(layout, context, precision),
            'PLANAR_EDIT': lambda: draw_planar_edit(layout, context, precision),
            'VERTEX_SNAP': lambda: draw_vertex_snap(layout, context, props, ui),
            'OBJECT_SNAP': lambda: draw_object_snap(layout, context, props, ui),
            'INJECT_NEW': lambda: draw_inject_new(layout, context, precision, props),
            'MAGIC_BRANCH': lambda: draw_magic_branch(layout, context, precision),
            'EDGE_DOCTOR': lambda: draw_edge_doctor(layout, context, props, ui),
            'VERTEX_LOCKS': lambda: draw_vertex_locks(layout, context, props, ui),
            'SELECTION_SLOTS': lambda: draw_selection_slots(layout, context, props, ui),
        }
        for tool_id in parse_edit_tool_order(ui.edit_tool_order):
            drawer = drawers.get(tool_id)
            if drawer is not None:
                drawer()


PANELS = (VIEW3D_PT_wt_edit_tools,)
