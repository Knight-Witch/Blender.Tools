from bpy.types import Panel

from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .ui_helpers import draw_inline_label_prop, draw_section_toggle
from .utils_context import ui_state_owner


class VIEW3D_PT_wt_modifier_tool(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_modifier_tool'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['MODIFIER_TOOL']
    panel_title = 'Quick Modifiers'
    panel_icon = 'MODIFIER'
    bl_options = {'DEFAULT_CLOSED'}
    bl_description = 'Shrinkwrap setup plus batch object transforms.'

    def draw(self, context):
        props = context.scene.witch_tools
        ui = ui_state_owner(context)
        layout = self.layout

        if getattr(ui, 'ui_minimal_mode', False):
            return

        shrink = layout.box()
        if draw_section_toggle(shrink, ui, 'show_modifier_shrinkwrap', 'Shrinkwrap', section_icon='MOD_SHRINKWRAP'):
            draw_inline_label_prop(shrink, 'Target', props, 'shrinkwrap_target', icon='MOD_SHRINKWRAP', label_units=3.2, field_units=6.0)
            shrink.prop(props, 'shrinkwrap_apply_to_selected', text='Use Selected Meshes')

            row = shrink.row(align=True)
            left = row.row(align=True)
            left.scale_x = 0.92
            left.label(text='Method')
            left.prop(props, 'shrinkwrap_wrap_method', text='')
            spacer = row.row(align=True)
            spacer.ui_units_x = 0.45
            spacer.label(text='')
            right = row.row(align=True)
            right.scale_x = 0.92
            right.label(text='Snap')
            right.prop(props, 'shrinkwrap_wrap_mode', text='')

            row = shrink.row(align=True)
            left = row.row(align=True)
            left.scale_x = 0.92
            left.label(text='Offset')
            offset_field = left.row(align=True)
            offset_field.ui_units_x = 5.2
            offset_field.prop(props, 'shrinkwrap_offset', text='')
            spacer = row.row(align=True)
            spacer.ui_units_x = 0.45
            spacer.label(text='')
            right = row.row(align=True)
            right.scale_x = 0.92
            right.label(text='Vertex Group')
            group_field = right.row(align=True)
            group_field.ui_units_x = 5.5
            group_field.prop(props, 'shrinkwrap_vertex_group', text='')

            row = shrink.row(align=True)
            row.operator('witch_tools.add_shrinkwrap_modifier', text='Add / Update')
            row.operator('witch_tools.apply_shrinkwrap_modifier', text='Apply')

        batch = layout.box()
        if draw_section_toggle(batch, ui, 'show_modifier_batch_tools', 'Batch Object Tools', section_icon='OBJECT_DATAMODE'):
            draw_inline_label_prop(batch, 'Scale', props, 'scale_value', label_units=2.4, field_units=6.4)

            rotate = batch.row(align=True)
            rotate.label(text='Rotate')
            for use_prop, value_prop, axis in (
                ('batch_rotate_use_x', 'batch_rotate_x_degrees', 'X'),
                ('batch_rotate_use_y', 'batch_rotate_y_degrees', 'Y'),
                ('batch_rotate_use_z', 'batch_rotate_z_degrees', 'Z'),
            ):
                block = rotate.row(align=True)
                toggle = block.row(align=True)
                toggle.ui_units_x = 1.15
                toggle.prop(props, use_prop, text=axis, toggle=True)
                field = block.row(align=True)
                field.ui_units_x = 2.9
                field.prop(props, value_prop, text='')

            batch.operator('witch_tools.apply_batch_rotation', text='Apply')
            batch.prop(props, 'batch_auto_apply_rotation')
            batch.prop(props, 'apply_transforms')
            batch.prop(props, 'remove_modifiers')
            row = batch.row(align=True)
            row.operator('witch_tools.batch_apply_tools', text='Apply To Selected')
            row.operator('witch_tools.apply_all_transforms', text='Apply All Transforms')


PANELS = (VIEW3D_PT_wt_modifier_tool,)
