import bpy

from .config import PANEL_CATEGORY
from .overlay import runtime
from .utils import addon_preferences


class VIEW3D_PT_witch_quickbar_controls(bpy.types.Panel):
    bl_label = 'Witch Quickbar'
    bl_idname = 'VIEW3D_PT_witch_quickbar_controls'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        prefs = addon_preferences(context)
        row = layout.row(align=True)
        if runtime.running:
            row.operator('witch_quickbar.hide', text='Hide Quickbar')
        else:
            row.operator('witch_quickbar.show', text='Show Quickbar')
        row.operator('witch_quickbar.reset_position', text='', icon='LOOP_BACK')
        if prefs:
            layout.prop(prefs, 'locked')
            layout.prop(prefs, 'auto_start')
            layout.prop(prefs, 'more_tools_open')
            row = layout.row(align=True)
            row.prop(prefs, 'rotate_open', text='Rotate')
            row.prop(prefs, 'tools_open', text='Origins & Cursor')
            row.prop(prefs, 'mirror_open', text='Mirror')
            layout.prop(prefs, 'dock_scale')

            box = layout.box()
            box.label(text='Hotkey Targets')
            row = box.row(align=True)
            row.operator('witch_quickbar.cycle_modes', text='Cycle Modes', icon='FILE_REFRESH')
            row.operator('witch_quickbar.last_mode', text='Last Mode', icon='LOOP_BACK')


CLASSES = (VIEW3D_PT_witch_quickbar_controls,)
