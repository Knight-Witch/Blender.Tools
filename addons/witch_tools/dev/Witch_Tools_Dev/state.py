ADDON_PACKAGE = __package__
ADDON_VERSION = (2, 11, 0)
IS_DEV_BUILD = True
VERSION_LABEL = 'Dev_v2.11.0' if IS_DEV_BUILD else 'v2.11.0'
ADDON_NAME = f'Witch Tools {VERSION_LABEL}'
BUILD_TARGET_LABEL = 'Blender 4.5'
PANEL_CATEGORY = 'Witch Tools'
MODE_SWITCHER_SEQUENCE = (
    'EDIT', 'OBJECT', 'WEIGHT_PAINT', 'POSE', 'SCULPT', 'TEXTURE_PAINT', 'VERTEX_PAINT', 'UV_DATA',
)

MODE_CYCLE_ITEMS = (
    ('EDIT', 'cycle_use_edit', 'Edit', 'EDITMODE_HLT'),
    ('OBJECT', 'cycle_use_object', 'Object', 'OBJECT_DATAMODE'),
    ('WEIGHT_PAINT', 'cycle_use_weight_paint', 'Weight Paint', 'WPAINT_HLT'),
    ('POSE', 'cycle_use_pose', 'Pose', 'POSE_HLT'),
    ('SCULPT', 'cycle_use_sculpt', 'Sculpt', 'SCULPTMODE_HLT'),
    ('TEXTURE_PAINT', 'cycle_use_texture_paint', 'Texture Paint', 'TPAINT_HLT'),
    ('VERTEX_PAINT', 'cycle_use_vertex_paint', 'Vertex Paint', 'VPAINT_HLT'),
    ('UV_DATA', 'cycle_use_uv_data', 'UV Editing', 'UV_DATA'),
)

FOOTER_LINKS = (
    ('GitHub', 'CUSTOM', 'github', 'https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools'),
    ('Patreon', 'CUSTOM', 'patreon', 'https://www.patreon.com/cw/TheKnightWitch'),
    ('Ko-fi', 'CUSTOM', 'kofi', 'https://ko-fi.com/knightwitch'),
    ('PayPal', 'CUSTOM', 'paypal', 'https://paypal.me/KnightWitch'),
    ('Nexus', 'CUSTOM', 'nexus', 'https://www.nexusmods.com/profile/TheKnightWitch'),
    ('Website', 'CUSTOM', 'website', 'https://knightwitchapparel.com/'),
)

UI_STATE_PROPS = (
    'show_modifier_shrinkwrap', 'show_modifier_batch_tools',
    'show_edit_vertex_snap', 'show_edit_object_snap',
    'show_edit_vertex_inject', 'show_edit_curvature_sync', 'show_edit_guided_align',
    'show_edit_edge_doctor', 'show_edge_doctor_inject', 'show_edge_doctor_alignment', 'show_edge_doctor_curvature',
    'show_edit_selection_slots', 'show_edit_vertex_locks',
    'show_vertex_locks_core', 'show_vertex_locks_zone', 'show_vertex_locks_groups', 'show_vertex_locks_sculpt', 'show_vertex_locks_shape',
    'vertex_locks_group_filter',
    'show_weight_transfer', 'show_weight_transfer_howto', 'show_weight_transfer_single', 'show_weight_transfer_batch',
    'show_weight_mirror', 'show_weight_mirror_howto', 'show_armature_cleanup',
    'show_head_prep', 'show_head_editing', 'show_head_finishing',
    'show_footer_cycle_settings', 'show_footer_hotkeys',
)

PANEL_ORDERS = {
    'MODE_SWITCHER': 0,
    'TRANSFORM': 1,
    'AUTO_MIRROR': 2,
    'PRINT3D': 3,
    'EDIT_TOOLS': 4,
    'MODIFIER_TOOL': 5,
    'HEAD_TOOLS': 6,
    'BODY_TOOLS': 7,
    'ARMOUR_TOOLS': 8,
    'HAIR_TOOLS': 9,
    'WEIGHT_TOOLS': 10,
    'ARMATURE_TOOLS': 11,
    'SHAPE_KEY_TOOLS': 12,
    'EXPORT_TOOLS': 13,
    'TROUBLESHOOTING_TOOLS': 14,
    'FOOTER': 99,
}

addon_keymaps = []
armature_hide_select_state = {}
runtime_cache = {'weight_paint_key': None}
