from bpy.types import Panel

from .state import PANEL_CATEGORY, PANEL_ORDERS
from .ui_helpers import draw_mode_switcher_row
from .utils_context import ui_state_owner


def _draw_mode_switcher_panel(layout, context):
    props = context.scene.witch_tools
    draw_mode_switcher_row(layout, context)
    row = layout.row(align=True)
    row.scale_y = 0.95
    row.prop(props, 'enable_pose_in_weight_paint', toggle=True, text='Pose in Weight Paint')


def _draw_mode_switcher_header(layout):
    prefs = ui_state_owner()
    is_minimal = bool(getattr(prefs, 'ui_minimal_mode', False)) if prefs else False
    op = layout.operator(
        'witch_tools.toggle_minimal_view',
        text='',
        icon='FULLSCREEN_ENTER' if is_minimal else 'FULLSCREEN_EXIT',
        emboss=False,
    )
    return op


class VIEW3D_PT_wt_mode_switcher(Panel):
    bl_label = 'Mode Switcher'
    bl_idname = 'VIEW3D_PT_wt_mode_switcher'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['MODE_SWITCHER']
    bl_description = 'Switch quickly between the core modeling and painting modes, plus Cycle and Last Used.'

    def draw_header_preset(self, _context):
        _draw_mode_switcher_header(self.layout)

    def draw(self, context):
        _draw_mode_switcher_panel(self.layout, context)


class IMAGE_PT_wt_mode_switcher(Panel):
    bl_label = 'Mode Switcher'
    bl_idname = 'IMAGE_PT_wt_mode_switcher'
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['MODE_SWITCHER']
    bl_description = 'Switch quickly between the core modeling and painting modes, plus Cycle and Last Used.'

    def draw_header_preset(self, _context):
        _draw_mode_switcher_header(self.layout)

    def draw(self, context):
        _draw_mode_switcher_panel(self.layout, context)


PANELS = (
    VIEW3D_PT_wt_mode_switcher,
    IMAGE_PT_wt_mode_switcher,
)
