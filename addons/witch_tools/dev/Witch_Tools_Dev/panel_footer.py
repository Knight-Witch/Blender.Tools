import rna_keymap_ui

from bpy.types import Panel

from .custom_icons import get_icon_id
from .state import BUILD_TARGET_LABEL, FOOTER_LINKS, MODE_CYCLE_ITEMS, PANEL_CATEGORY, PANEL_ORDERS, VERSION_LABEL, addon_keymaps
from .ui_helpers import draw_section_toggle, draw_wrapped_text
from .utils_context import addon_preferences


_KEYMAP_IDS = (
    'witch_tools.toggle_minimal_view',
    'mesh.vertex_snap_global',
    'wtm.cycle_mode_switcher',
    'wtm.return_temp_mode',
    'wtm.switch_edit_mode',
    'wtm.switch_object_mode',
    'wtm.toggle_weight_paint',
    'wtm.toggle_pose_mode',
)


class VIEW3D_PT_wt_footer(Panel):
    bl_label = VERSION_LABEL
    bl_idname = 'VIEW3D_PT_wt_footer'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['FOOTER']
    bl_description = 'Build information, keymaps, cycle settings, and links.'

    def _draw_cycle_settings(self, context, layout, prefs):
        if not draw_section_toggle(layout, prefs, 'show_footer_cycle_settings', 'Mode Cycle Settings', 'FILE_REFRESH'):
            return
        box = layout.box()
        draw_wrapped_text(box, context, 'Select/deselect modes for Cycle.')
        row = box.row(align=True)
        row.alignment = 'CENTER'
        buttons = row.row(align=True)
        for _mode, prop_name, _label, icon in MODE_CYCLE_ITEMS:
            buttons.prop(prefs, prop_name, text='', icon=icon, toggle=True)
        pref_row = box.row(align=True)
        pref_row.alignment = 'CENTER'
        op = pref_row.operator('witch_tools.open_preferences', text='Mode Switcher Preferences', icon='PREFERENCES')
        op.section = 'MODE_SWITCHER'

    def _draw_hotkeys(self, context, layout, prefs):
        if not draw_section_toggle(layout, prefs, 'show_footer_hotkeys', 'Hotkeys', 'KEYINGSET'):
            return
        box = layout.box()
        draw_wrapped_text(box, context, 'Important Witch Tools hotkeys. Edit them here or open full keymap preferences.')
        user_keyconfig = context.window_manager.keyconfigs.user
        drawn = 0
        for km, kmi in addon_keymaps:
            if kmi.idname not in _KEYMAP_IDS:
                continue
            inner = box.box()
            rna_keymap_ui.draw_kmi([], user_keyconfig, km, kmi, inner, 0)
            drawn += 1
        if drawn == 0:
            box.label(text='No tracked keymaps registered.')
        pref_row = box.row(align=True)
        pref_row.alignment = 'CENTER'
        op = pref_row.operator('witch_tools.open_preferences', text='All Addon Keymaps', icon='PREFERENCES')
        op.section = 'KEYMAPS'

    def _draw_links_row(self, layout):
        row = layout.row(align=True)
        row.alignment = 'CENTER'
        row.scale_x = 1.62
        row.scale_y = 1.62
        buttons = row.row(align=True)
        for label, icon_kind, icon_ref, url in FOOTER_LINKS:
            if icon_kind == 'CUSTOM':
                op = buttons.operator('witch_tools.open_link', text='', icon_value=get_icon_id(icon_ref), emboss=True)
            else:
                op = buttons.operator('witch_tools.open_link', text='', icon=icon_ref, emboss=True)
            op.url = url
            op.label = label

    def draw(self, context):
        layout = self.layout
        prefs = addon_preferences(context)
        if prefs is None:
            layout.label(text='Witch Tools preferences unavailable.', icon='ERROR')
            return

        summary = layout.row(align=True)
        summary.scale_y = 0.85
        summary.label(text=BUILD_TARGET_LABEL)
        pref_op = summary.operator('witch_tools.open_preferences', text='', icon='PREFERENCES', emboss=True)
        pref_op.section = 'GENERAL'

        self._draw_links_row(layout)
        self._draw_cycle_settings(context, layout, prefs)
        self._draw_hotkeys(context, layout, prefs)


PANELS = (VIEW3D_PT_wt_footer,)
