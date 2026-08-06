from bpy.types import Panel

from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .utils_context import active_mesh_for_panel, ui_state_owner


class VIEW3D_PT_wt_auto_mirror(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_auto_mirror'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['AUTO_MIRROR']
    panel_title = 'Auto Mirror'
    panel_icon = 'MOD_MIRROR'
    bl_options = {'DEFAULT_CLOSED'}
    bl_description = 'Compact mirror toggles for the active mesh. Auto Weight turns weight-paint X mirroring on when you enter Weight Paint mode.'

    def draw(self, context):
        props = context.scene.witch_tools
        if getattr(ui_state_owner(context), 'ui_minimal_mode', False):
            return
        obj = active_mesh_for_panel(context)
        box = self.layout.box()
        if obj is None:
            box.label(text='Active mesh required')
            return

        row = box.row(align=True)
        row.alignment = 'LEFT'

        edit_icon = row.row(align=True)
        edit_icon.ui_units_x = 0.75
        edit_icon.alignment = 'CENTER'
        edit_icon.label(text='', icon='EDITMODE_HLT')

        edit_gap = row.row(align=True)
        edit_gap.ui_units_x = 0.8
        edit_gap.label(text='')

        edit_buttons = row.row(align=True)
        edit_buttons.alignment = 'LEFT'
        edit_x = edit_buttons.row(align=True)
        edit_x.ui_units_x = 1.05
        edit_x.operator('witch_tools.toggle_edit_x_mirror', text='X', depress=bool(getattr(obj.data, 'use_mirror_x', False)))
        edit_topo = edit_buttons.row(align=True)
        edit_topo.ui_units_x = 1.05
        edit_topo.operator('witch_tools.toggle_topology_mirror', text='', icon='MESH_GRID', depress=bool(getattr(obj.data, 'use_mirror_topology', False)))

        divider_pre_gap = row.row(align=True)
        divider_pre_gap.ui_units_x = 0.55
        divider_pre_gap.label(text='')

        divider = row.row(align=True)
        divider.ui_units_x = 0.5
        divider.alignment = 'CENTER'
        divider.label(text='|')

        divider_post_gap = row.row(align=True)
        divider_post_gap.ui_units_x = 0.55
        divider_post_gap.label(text='')

        paint_icon = row.row(align=True)
        paint_icon.ui_units_x = 0.75
        paint_icon.alignment = 'CENTER'
        paint_icon.label(text='', icon='WPAINT_HLT')

        paint_gap = row.row(align=True)
        paint_gap.ui_units_x = 0.8
        paint_gap.label(text='')

        paint_buttons = row.row(align=True)
        paint_buttons.alignment = 'LEFT'
        paint_x = paint_buttons.row(align=True)
        paint_x.ui_units_x = 1.05
        paint_x.operator('witch_tools.toggle_weight_x_mirror', text='X', depress=bool(getattr(obj, 'use_mesh_mirror_x', False)))
        paint_groups = paint_buttons.row(align=True)
        paint_groups.ui_units_x = 1.05
        paint_groups.operator('witch_tools.toggle_mirror_vertex_groups', text='', icon='GROUP_VERTEX', depress=bool(getattr(obj.data, 'use_mirror_vertex_groups', False)))
        paint_auto = paint_buttons.row(align=True)
        paint_auto.ui_units_x = 2.35
        paint_auto.operator('witch_tools.toggle_auto_weight_mirror', text='Auto', icon='WPAINT_HLT', depress=props.auto_enable_weight_paint_mirror)


PANELS = (VIEW3D_PT_wt_auto_mirror,)
