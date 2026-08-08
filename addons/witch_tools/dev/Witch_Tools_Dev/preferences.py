import rna_keymap_ui
from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences

from .operators_edit_tool_order import DEFAULT_EDIT_TOOL_ORDER
from .state import ADDON_PACKAGE, BUILD_TARGET_LABEL, MODE_CYCLE_ITEMS, VERSION_LABEL, addon_keymaps


class WitchToolsPreferences(AddonPreferences):
    bl_idname = ADDON_PACKAGE

    active_section: EnumProperty(
        name='Active Section',
        items=[
            ('GENERAL', 'General', ''),
            ('MODE_SWITCHER', 'Mode Switcher', ''),
            ('EDIT_TOOLS', 'Edit Tools', ''),
            ('WEIGHT_TOOLS', 'Weight Tools', ''),
            ('MODIFIER_TOOL', 'Quick Modifiers', ''),
            ('HEAD_TOOLS', 'Head Tools', ''),
            ('BODY_TOOLS', 'Body Tools', ''),
            ('ARMOUR_TOOLS', 'Armour Tools', ''),
            ('HAIR_TOOLS', 'Hair Tools', ''),
            ('ARMATURE_TOOLS', 'Armature Tools', ''),
            ('SHAPE_KEY_TOOLS', 'Shape Key Tools', ''),
            ('EXPORT_TOOLS', 'Export Tools', ''),
            ('TROUBLESHOOTING_TOOLS', 'Troubleshooting Tools', ''),
            ('KEYMAPS', 'Addon Keymaps', ''),
        ],
        default='GENERAL',
    )
    cycle_use_edit: BoolProperty(name='Cycle Edit', default=True)
    cycle_use_object: BoolProperty(name='Cycle Object', default=True)
    cycle_use_weight_paint: BoolProperty(name='Cycle Weight Paint', default=True)
    cycle_use_pose: BoolProperty(name='Cycle Pose', default=True)
    cycle_use_sculpt: BoolProperty(name='Cycle Sculpt', default=True)
    cycle_use_texture_paint: BoolProperty(name='Cycle Texture Paint', default=True)
    cycle_use_vertex_paint: BoolProperty(name='Cycle Vertex Paint', default=True)
    cycle_use_uv_data: BoolProperty(name='Cycle UV Editing', default=True)
    mirror_tolerance: FloatProperty(name='Mirror tolerance', default=0.0005, min=0.0, precision=6)

    ui_minimal_mode: BoolProperty(name='Minimal View', default=False)
    ui_state_snapshot: StringProperty(default='')
    edit_tool_reorder_mode: BoolProperty(
        name='Reorder Tools',
        description='Show compact draggable rows for changing the persistent Edit Tools section order',
        default=False,
    )
    edit_tool_order: StringProperty(
        name='Edit Tool Order',
        description='Persistent Witch Tools Edit Tools order',
        default=','.join(DEFAULT_EDIT_TOOL_ORDER),
        options={'HIDDEN'},
    )

    show_modifier_shrinkwrap: BoolProperty(name='Shrinkwrap', default=True)
    show_modifier_batch_tools: BoolProperty(name='Batch Object Tools', default=False)
    show_edit_vertex_snap: BoolProperty(name='Vertex Snap', default=True)
    show_edit_object_snap: BoolProperty(name='Object Snap', default=True)
    show_edit_vertex_inject: BoolProperty(name='Edge / Vertex Inject', default=True)
    show_edit_curvature_sync: BoolProperty(name='Curvature Sync', default=True)
    show_edit_guided_align: BoolProperty(name='Align Vertices / Edges / Faces', default=True)
    show_edit_edge_doctor: BoolProperty(name='Edge Doctor', default=True)
    show_edge_doctor_inject: BoolProperty(name='Missing Vertex / Edge Injector', default=True)
    show_edge_doctor_alignment: BoolProperty(name='Alignment Fixer', default=True)
    show_edge_doctor_curvature: BoolProperty(name='Curvature Sync', default=True)
    show_edit_selection_slots: BoolProperty(name='Selection Slots', default=True)
    show_edit_vertex_locks: BoolProperty(name='Vertex Locks', default=False)
    show_vertex_locks_core: BoolProperty(name='Vertex Locks Core', default=True)
    show_vertex_locks_zone: BoolProperty(name='Protected Edit Zone', default=True)
    show_vertex_locks_groups: BoolProperty(name='Groups', default=False)
    show_vertex_locks_sculpt: BoolProperty(name='Sculpt Protection', default=False)
    show_vertex_locks_shape: BoolProperty(name='Shape Mirror', default=False)
    vertex_locks_group_filter: StringProperty(name='Group Filter', default='')
    show_weight_transfer: BoolProperty(name='Weight Transfer', default=True)
    show_weight_transfer_howto: BoolProperty(name='How to Use', default=False)
    show_weight_transfer_single: BoolProperty(name='Single Transfer', default=True)
    show_weight_transfer_batch: BoolProperty(name='Batch Transfer', default=True)
    show_weight_mirror: BoolProperty(name='Weight Mirror', default=True)
    show_weight_mirror_howto: BoolProperty(name='How to Use', default=False)
    show_armature_cleanup: BoolProperty(name='Cleanup / Armature', default=True)
    show_head_prep: BoolProperty(name='Prep', default=True)
    show_head_editing: BoolProperty(name='Editing', default=True)
    show_head_finishing: BoolProperty(name='Finishing', default=True)
    show_footer_cycle_settings: BoolProperty(name='Cycle Settings', default=True)
    show_footer_hotkeys: BoolProperty(name='Hotkeys', default=False)

    def _section_box(self, layout, title, icon, section_key):
        box = layout.box()
        header = box.row(align=True)
        header.label(text=title, icon=icon)
        if self.active_section == section_key:
            marker = header.row(align=True)
            marker.alignment = 'RIGHT'
            marker.label(text='Active')
        return box

    def _draw_general_section(self, layout):
        box = self._section_box(layout, 'General', 'PREFERENCES', 'GENERAL')
        box.label(text=f'Build: {VERSION_LABEL}')
        box.label(text=f'Target build context: {BUILD_TARGET_LABEL}')

    def _draw_mode_switcher_section(self, layout):
        box = self._section_box(layout, 'Mode Switcher', 'FILE_REFRESH', 'MODE_SWITCHER')
        box.label(text='Select/deselect modes for Cycle:')
        row = box.row(align=True)
        for _mode, prop_name, _label, icon in MODE_CYCLE_ITEMS:
            row.prop(self, prop_name, text='', icon=icon, toggle=True)

    def _draw_edit_tools_section(self, layout):
        box = self._section_box(layout, 'Edit Tools', 'EDITMODE_HLT', 'EDIT_TOOLS')
        box.prop(self, 'edit_tool_reorder_mode', toggle=True)
        box.label(text='Tool order is edited directly from the Edit Tools N-panel.')

    def _draw_weight_tools_section(self, layout):
        box = self._section_box(layout, 'Weight Tools', 'WPAINT_HLT', 'WEIGHT_TOOLS')
        box.prop(self, 'mirror_tolerance')

    def _draw_keymaps_section(self, context, layout):
        box = self._section_box(layout, 'Addon Keymaps', 'KEYINGSET', 'KEYMAPS')
        if not addon_keymaps:
            box.label(text='No addon keymaps registered')
            return
        for km, kmi in addon_keymaps:
            inner = box.box()
            rna_keymap_ui.draw_kmi([], context.window_manager.keyconfigs.user, km, kmi, inner, 0)

    def draw(self, context):
        layout = self.layout
        self._draw_general_section(layout)
        self._draw_mode_switcher_section(layout)
        self._draw_edit_tools_section(layout)
        self._draw_weight_tools_section(layout)
        self._section_box(layout, 'Quick Modifiers', 'MODIFIER', 'MODIFIER_TOOL')
        self._section_box(layout, 'Head Tools', 'USER', 'HEAD_TOOLS')
        self._section_box(layout, 'Body Tools', 'RNA', 'BODY_TOOLS')
        self._section_box(layout, 'Armour Tools', 'MOD_CLOTH', 'ARMOUR_TOOLS')
        self._section_box(layout, 'Hair Tools', 'OUTLINER_OB_CURVES', 'HAIR_TOOLS')
        self._section_box(layout, 'Armature Tools', 'ARMATURE_DATA', 'ARMATURE_TOOLS')
        self._section_box(layout, 'Shape Key Tools', 'SHAPEKEY_DATA', 'SHAPE_KEY_TOOLS')
        self._section_box(layout, 'Export Tools', 'ORPHAN_DATA', 'EXPORT_TOOLS')
        self._section_box(layout, 'Troubleshooting Tools', 'ERROR', 'TROUBLESHOOTING_TOOLS')
        self._draw_keymaps_section(context, layout)
