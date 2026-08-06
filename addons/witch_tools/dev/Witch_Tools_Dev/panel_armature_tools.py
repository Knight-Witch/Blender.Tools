from bpy.types import Panel

from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .ui_helpers import draw_section_toggle, draw_wrapped_text
from .utils_context import ui_state_owner


class VIEW3D_PT_wt_armature_tools(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_armature_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['ARMATURE_TOOLS']
    panel_title = 'Armature Tools'
    panel_icon = 'ARMATURE_DATA'
    bl_options = {'DEFAULT_CLOSED'}
    bl_description = 'Armature checks, cleanup actions, and rig-support workflow tools.'

    def draw(self, context):
        props = context.scene.witch_tools
        ui = ui_state_owner(context)
        layout = self.layout

        if getattr(ui, 'ui_minimal_mode', False):
            return

        cleanup = layout.box()
        if draw_section_toggle(cleanup, ui, 'show_armature_cleanup', 'Cleanup / Armature', section_icon='ARMATURE_DATA'):
            cleanup.operator('witch_tools.cleanup_unused_vertex_groups', text='Remove Unused Vertex Groups')
            cleanup.operator('witch_tools.check_armature', text='Check Armature')
            if props.armature_check_summary:
                result = cleanup.box()
                result.label(text='Last Check')
                draw_wrapped_text(result, context, props.armature_check_summary)
                if props.armature_check_details:
                    draw_wrapped_text(result, context, props.armature_check_details.splitlines()[:6])

        upcoming = layout.box()
        upcoming.label(text='Rigging workflow section.')
        upcoming.label(text='Additional armature tools will land here.')


PANELS = (VIEW3D_PT_wt_armature_tools,)
