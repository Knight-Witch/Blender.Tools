from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences

from .config import (
    DEFAULT_CYCLE_MODE_FILTER,
    DEFAULT_MODE_ORDER,
    DEFAULT_TOOL_ORDER,
    MODE_BUTTON_MAP,
    MODE_SEQUENCE,
    cycle_enabled_modes,
    mode_order,
)
from .state import ADDON_PACKAGE


class WQBAR_Preferences(AddonPreferences):
    bl_idname = ADDON_PACKAGE

    auto_start: BoolProperty(
        name='Show Quickbar Automatically',
        default=True,
    )

    dock_x: IntProperty(
        name='Quickbar X',
        default=48,
        min=0,
    )

    dock_y: IntProperty(
        name='Quickbar Y',
        default=36,
        min=0,
    )

    dock_scale: FloatProperty(
        name='Quickbar Scale',
        default=1.0,
        min=0.80,
        max=1.60,
    )


    dock_width: IntProperty(
        name='Quickbar Width',
        default=0,
        min=0,
    )

    dock_height_extra: IntProperty(
        name='Quickbar Extra Height',
        default=0,
        min=0,
    )

    display_state: EnumProperty(
        name='Display State',
        items=(
            ('FULL', 'Full', ''),
            ('MINIMIZED', 'Minimized', ''),
            ('CLOSED', 'Closed Launcher', ''),
        ),
        default='FULL',
    )

    last_open_state: EnumProperty(
        name='Last Open State',
        items=(
            ('FULL', 'Full', ''),
            ('MINIMIZED', 'Minimized', ''),
        ),
        default='FULL',
    )

    launcher_x: IntProperty(
        name='Launcher X',
        default=18,
        min=0,
    )

    launcher_y: IntProperty(
        name='Launcher Y',
        default=18,
        min=0,
    )

    more_tools_open: BoolProperty(
        name='Show More Tools',
        default=True,
    )

    rotate_open: BoolProperty(
        name='Show Rotate',
        default=True,
    )

    mirror_open: BoolProperty(
        name='Show Mirror Objects',
        default=True,
    )

    tools_open: BoolProperty(
        name='Show Origins & Cursor',
        default=True,
    )

    mirror_pivot_mode: StringProperty(
        name='Mirror Pivot Mode',
        default='CURSOR',
    )

    tool_order: StringProperty(
        name='More Tools Order',
        default=DEFAULT_TOOL_ORDER,
    )

    mode_order: StringProperty(
        name='Mode Button Order',
        default=DEFAULT_MODE_ORDER,
    )

    cycle_mode_filter: StringProperty(
        name='Cycle Mode Filter',
        default=DEFAULT_CYCLE_MODE_FILTER,
    )

    open_close_shortcut_type: StringProperty(
        name='Open/Close Shortcut Type',
        default='',
    )

    open_close_shortcut_value: StringProperty(
        name='Open/Close Shortcut Value',
        default='PRESS',
    )

    open_close_shortcut_ctrl: BoolProperty(
        name='Open/Close Ctrl',
        default=False,
    )

    open_close_shortcut_shift: BoolProperty(
        name='Open/Close Shift',
        default=False,
    )

    open_close_shortcut_alt: BoolProperty(
        name='Open/Close Alt',
        default=False,
    )

    open_close_shortcut_oskey: BoolProperty(
        name='Open/Close OS Key',
        default=False,
    )

    maximize_shortcut_type: StringProperty(
        name='Maximize Shortcut Type',
        default='',
    )

    maximize_shortcut_value: StringProperty(
        name='Maximize Shortcut Value',
        default='PRESS',
    )

    maximize_shortcut_ctrl: BoolProperty(
        name='Maximize Ctrl',
        default=True,
    )

    maximize_shortcut_shift: BoolProperty(
        name='Maximize Shift',
        default=False,
    )

    maximize_shortcut_alt: BoolProperty(
        name='Maximize Alt',
        default=False,
    )

    maximize_shortcut_oskey: BoolProperty(
        name='Maximize OS Key',
        default=False,
    )

    cycle_shortcut_type: StringProperty(
        name='Cycle Modes Shortcut Type',
        default='',
    )

    cycle_shortcut_value: StringProperty(
        name='Cycle Modes Shortcut Value',
        default='PRESS',
    )

    cycle_shortcut_ctrl: BoolProperty(
        name='Cycle Modes Ctrl',
        default=False,
    )

    cycle_shortcut_shift: BoolProperty(
        name='Cycle Modes Shift',
        default=False,
    )

    cycle_shortcut_alt: BoolProperty(
        name='Cycle Modes Alt',
        default=False,
    )

    cycle_shortcut_oskey: BoolProperty(
        name='Cycle Modes OS Key',
        default=False,
    )

    last_shortcut_type: StringProperty(
        name='Last Mode Shortcut Type',
        default='',
    )

    last_shortcut_value: StringProperty(
        name='Last Mode Shortcut Value',
        default='PRESS',
    )

    last_shortcut_ctrl: BoolProperty(
        name='Last Mode Ctrl',
        default=False,
    )

    last_shortcut_shift: BoolProperty(
        name='Last Mode Shift',
        default=False,
    )

    last_shortcut_alt: BoolProperty(
        name='Last Mode Alt',
        default=False,
    )

    last_shortcut_oskey: BoolProperty(
        name='Last Mode OS Key',
        default=False,
    )

    locked: BoolProperty(
        name='Lock Quickbar Position',
        default=False,
    )

    footer_settings_open: BoolProperty(
        name='Show Footer Hotkeys',
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'auto_start')
        layout.prop(self, 'locked')
        row = layout.row(align=True)
        row.prop(self, 'dock_x')
        row.prop(self, 'dock_y')
        layout.prop(self, 'dock_scale')
        row = layout.row(align=True)
        row.prop(self, 'display_state')
        row.prop(self, 'last_open_state')
        layout.separator()
        layout.prop(self, 'more_tools_open')
        row = layout.row(align=True)
        row.prop(self, 'rotate_open')
        row.prop(self, 'mirror_open')
        row.prop(self, 'tools_open')
        layout.separator()
        self._draw_shortcuts(layout, context)

    def _draw_shortcuts(self, layout, context):
        from .icons import preview_icon
        from .keymaps import shortcut_label

        box = layout.box()
        box.label(text='Quick Access Shortcuts')

        cycle_box = box.box()
        cycle_box.label(text='Cycle Modes: Included Modes')
        row = cycle_box.row(align=True)
        enabled_modes = set(cycle_enabled_modes(self))
        for key in mode_order(self):
            if key not in MODE_SEQUENCE:
                continue
            data = MODE_BUTTON_MAP.get(key)
            if not data:
                continue
            _, icon_name, tooltip, _target = data
            icon_value = preview_icon(icon_name)
            op = row.operator(
                'witch_quickbar.toggle_cycle_mode',
                text='',
                icon_value=icon_value,
                depress=key in enabled_modes,
            )
            op.mode_key = key

        cycle_box.label(text='Cycling follows the current Mode button order and skips inactive icons.')

        for target, label in (('open_close', 'Open/Close'), ('maximize', 'Maximize Open/Close'), ('cycle', 'Cycle Modes'), ('last', 'Last Mode Used')):
            row = box.row(align=True)
            row.label(text=label)
            row.label(text=shortcut_label(context, target))
            op = row.operator('witch_quickbar.assign_shortcut', text='Assign')
            op.target = target
            op = row.operator('witch_quickbar.clear_shortcut', text='', icon='X')
            op.target = target

        footer = box.row(align=True)
        footer.operator('witch_quickbar.open_preferences', text='Open Preferences', icon='PREFERENCES')
        footer.operator('witch_quickbar.check_updates', text='Check for Updates', icon='IMPORT')
