from bpy.types import Panel

from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .utils_context import ui_state_owner


class VIEW3D_PT_wt_armour_tools(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_armour_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['ARMOUR_TOOLS']
    panel_title = 'Armour Tools'
    panel_icon = 'MOD_CLOTH'
    bl_options = {'DEFAULT_CLOSED'}
    bl_description = 'Armour editing, refit, modifier, and export-prep workflow tools.'

    def draw(self, context):
        if getattr(ui_state_owner(context), 'ui_minimal_mode', False):
            return
        box = self.layout.box()
        box.label(text='Armour workflow section.')
        box.label(text='This section is ready for incoming workflow tools.')


PANELS = (VIEW3D_PT_wt_armour_tools,)
