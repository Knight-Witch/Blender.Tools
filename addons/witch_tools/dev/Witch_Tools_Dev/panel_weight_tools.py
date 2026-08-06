from bpy.types import Panel

from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .ui_helpers import draw_centered_disclosure, draw_help_title, draw_inline_label_prop, draw_section_toggle, draw_wrapped_text
from .utils_context import ui_state_owner


def _group_list_rows(count):
    if count <= 0:
        return 1
    if count == 1:
        return 2
    return 3


class VIEW3D_PT_wt_weight_tools(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_weight_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['WEIGHT_TOOLS']
    bl_options = {'DEFAULT_CLOSED'}
    panel_title = 'Weight Tools'
    panel_icon = 'WPAINT_HLT'

    def draw(self, context):
        props = context.scene.witch_tools
        ui = ui_state_owner(context)
        layout = self.layout

        if getattr(ui, 'ui_minimal_mode', False):
            return

        transfer = layout.box()
        if draw_section_toggle(transfer, ui, 'show_weight_transfer', 'Weight Transfer', section_icon='WPAINT_HLT'):
            if draw_centered_disclosure(transfer, ui, 'show_weight_transfer_howto'):
                draw_wrapped_text(transfer, context, [
                    'Single Transfer: pick one source mesh and one target mesh, then transfer.',
                    'Batch Transfer: choose a source set and a target set, then transfer by matching base names.',
                ])

            single_wrap = transfer.box()
            if draw_section_toggle(single_wrap, ui, 'show_weight_transfer_single', 'Single Transfer', section_icon='USER'):
                draw_help_title(single_wrap, 'Single Transfer', 'weight_transfer_single', icon='USER')
                draw_inline_label_prop(single_wrap, 'Source', props, 'source_object', icon='TRACKER', label_units=3.6, field_units=5.4)
                row = single_wrap.row(align=True)
                row.operator('witch_tools.set_active_as_source', text='Use Active As Source')
                draw_inline_label_prop(single_wrap, 'Target', props, 'target_object', icon='CON_OBJECTSOLVER', label_units=3.6, field_units=5.4)
                row = single_wrap.row(align=True)
                row.operator('witch_tools.set_active_as_target', text='Use Active As Target')
                single_wrap.operator('witch_tools.transfer_single_weights', text='Transfer Weights')

            batch_wrap = transfer.box()
            if draw_section_toggle(batch_wrap, ui, 'show_weight_transfer_batch', 'Batch Transfer', section_icon='COMMUNITY'):
                draw_help_title(batch_wrap, 'Batch Transfer', 'weight_transfer_batch', icon='COMMUNITY')
                draw_inline_label_prop(batch_wrap, 'Source', props, 'batch_source_mode', icon='TRACKER', label_units=3.6, field_units=5.4)
                if props.batch_source_mode == 'SELECTION':
                    row = batch_wrap.row(align=True)
                    row.operator('witch_tools.capture_batch_source_selection', text='Use Selected Objects')
                    note = batch_wrap.row()
                    note.alignment = 'CENTER'
                    note.label(text=f'Stored: {len(props.batch_source_objects)}')
                elif props.batch_source_mode == 'COLLECTION':
                    draw_inline_label_prop(batch_wrap, 'Collection', props, 'batch_source_collection', label_units=3.8, field_units=5.2)
                else:
                    draw_inline_label_prop(batch_wrap, 'Armature', props, 'batch_source_armature', label_units=3.8, field_units=5.2)
                batch_wrap.separator()
                draw_inline_label_prop(batch_wrap, 'Target', props, 'batch_target_mode', icon='CON_OBJECTSOLVER', label_units=3.6, field_units=5.4)
                if props.batch_target_mode == 'SELECTION':
                    row = batch_wrap.row(align=True)
                    row.operator('witch_tools.capture_batch_target_selection', text='Use Selected Objects')
                    note = batch_wrap.row()
                    note.alignment = 'CENTER'
                    note.label(text=f'Stored: {len(props.batch_target_objects)}')
                elif props.batch_target_mode == 'COLLECTION':
                    draw_inline_label_prop(batch_wrap, 'Collection', props, 'batch_target_collection', label_units=3.8, field_units=5.2)
                else:
                    draw_inline_label_prop(batch_wrap, 'Armature', props, 'batch_target_armature', label_units=3.8, field_units=5.2)
                batch_wrap.operator('witch_tools.transfer_batch_auto', text='Batch Transfer')

        mirror = layout.box()
        if draw_section_toggle(mirror, ui, 'show_weight_mirror', 'Weight Mirror', section_icon='MOD_MIRROR'):
            if draw_centered_disclosure(mirror, ui, 'show_weight_mirror_howto'):
                draw_wrapped_text(mirror, context, [
                    'Click Scan Groups.',
                    'Choose the groups you want to mirror.',
                    'Use the -X or +X toggle if needed.',
                    'Click Mirror Selected Weights.',
                ])
            if props.wtm_detected_left_suffix or props.wtm_detected_right_suffix:
                mirror.label(text=f'Detected: {props.wtm_detected_left_suffix} / {props.wtm_detected_right_suffix}')
            mirror.prop(props, 'wtm_include_single')

            cluster = mirror.box()
            dir_row = cluster.row(align=True)
            dir_row.label(text='', icon='MOD_MIRROR')
            buttons = dir_row.row(align=True)
            buttons.ui_units_x = 5.6
            buttons.prop_enum(props, 'wtm_single_source_half', 'NEGATIVE_X', text='-X')
            buttons.prop_enum(props, 'wtm_single_source_half', 'POSITIVE_X', text='+X')

            tol_row = cluster.row(align=True)
            tol_row.label(text='', icon='GROUP_VERTEX')
            tol_row.label(text='Tolerance')
            tol_field = tol_row.row(align=True)
            tol_field.ui_units_x = 3.6
            tol_field.prop(props, 'wtm_mirror_tolerance', text='')

            eps_row = cluster.row(align=True)
            eps_row.label(text='', icon='PROP_OFF')
            eps_row.label(text='Center Epsilon')
            eps_field = eps_row.row(align=True)
            eps_field.ui_units_x = 3.6
            eps_field.prop(props, 'wtm_center_epsilon', text='')

            mirror.prop(props, 'wtm_backup_groups')
            mirror.prop(props, 'wtm_normalize_after')
            mirror.prop(props, 'wtm_hide_other_armatures')
            mirror.operator('wtm.scan_groups', text='Scan Groups', icon='TRACKER')
            row = mirror.row(align=True)
            row.operator('wtm.select_defaults', text='All').mode = 'ALL'
            row.operator('wtm.select_defaults', text='None').mode = 'NONE'
            row.operator('wtm.select_defaults', text='Pairs').mode = 'PAIRED'
            row.operator('wtm.select_defaults', text='Singles').mode = 'SINGLE'
            mirror.template_list('WTM_UL_group_list', '', props, 'wtm_groups', props, 'wtm_active_index', rows=_group_list_rows(len(props.wtm_groups)))
            mirror.operator('wtm.mirror_selected', text='Mirror Selected Weights', icon='MOD_MIRROR')
            mirror.operator('wtm.restore_backups', text='Restore Backups', icon='LOOP_BACK')


PANELS = (VIEW3D_PT_wt_weight_tools,)
