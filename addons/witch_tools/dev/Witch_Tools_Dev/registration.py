import bpy
from bpy.props import PointerProperty, StringProperty

from . import operators_coordinate_copy, operators_curvature_sync, operators_guided_align, operators_inject_new, operators_planar_edit, operators_vertex_inject, operators_selection_slots, operators_head_editing, operators_head_finishing, operators_head_prep, operators_vertex_locks, precision_edit_props
from .custom_icons import register_custom_icons, unregister_custom_icons
from .handlers import register_handlers, unregister_handlers
from .keymaps import register_default_keymaps, unregister_keymaps
from .operators_armature import WT_OT_check_armature, WT_OT_cleanup_unused_vertex_groups
from .operators_auto_mirror import WT_OT_toggle_auto_weight, WT_OT_toggle_edit_x, WT_OT_toggle_group_mirror, WT_OT_toggle_topology, WT_OT_toggle_weight_x
from .operators_batch import WT_OT_apply_all_transforms, WT_OT_apply_batch_rotation, WT_OT_batch_apply_tools
from .operators_object_snap import CLASSES as OBJECT_SNAP_CLASSES
from .operators_mode_switcher import (
    WTM_OT_cycle_mode_switcher,
    WTM_OT_return_temp_mode,
    WTM_OT_switch_edit_mode,
    WTM_OT_switch_object_mode,
    WTM_OT_switch_sculpt_mode,
    WTM_OT_switch_texture_paint_mode,
    WTM_OT_switch_uv_data_mode,
    WTM_OT_switch_vertex_paint_mode,
    WTM_OT_toggle_pose_mode,
    WTM_OT_toggle_weight_paint,
)
from .operators_ui import WITCHTOOLS_OT_help_tooltip, WITCHTOOLS_OT_open_link, WITCHTOOLS_OT_open_preferences, WITCHTOOLS_OT_toggle_minimal_view
from .operators_vertex_snap import MESH_OT_vertex_snap_global
from .operators_weight_mirror import WTM_OT_mirror_selected, WTM_OT_restore_backups, WTM_OT_scan_groups, WTM_OT_select_defaults, WTM_UL_group_list
from .operators_weight_transfer import WT_OT_add_shrinkwrap, WT_OT_apply_shrinkwrap, WT_OT_capture_batch_source_selection, WT_OT_capture_batch_target_selection, WT_OT_set_active_as_source, WT_OT_set_active_as_target, WT_OT_transfer_batch_auto, WT_OT_transfer_single_weights
from .panels import PANELS
from .preferences import WitchToolsPreferences
from .props import WTObjectRefItem, WTWeightMirrorItem, WitchToolsProperties
from .utils_context import prefs_mirror_tolerance


CORE_CLASSES = (
    WitchToolsPreferences,
    WTObjectRefItem,
    WTWeightMirrorItem,
    operators_selection_slots.WTSelectionSlotObjectRef,
    operators_selection_slots.WTSelectionSlotItem,
    WitchToolsProperties,
    *precision_edit_props.CLASSES,
    WITCHTOOLS_OT_help_tooltip,
    WITCHTOOLS_OT_open_preferences,
    WITCHTOOLS_OT_open_link,
    WITCHTOOLS_OT_toggle_minimal_view,
    MESH_OT_vertex_snap_global,
    *OBJECT_SNAP_CLASSES,
    WT_OT_set_active_as_source,
    WT_OT_set_active_as_target,
    WT_OT_capture_batch_source_selection,
    WT_OT_capture_batch_target_selection,
    WT_OT_transfer_single_weights,
    WT_OT_transfer_batch_auto,
    WT_OT_add_shrinkwrap,
    WT_OT_apply_shrinkwrap,
    WT_OT_apply_batch_rotation,
    WT_OT_apply_all_transforms,
    WT_OT_batch_apply_tools,
    WT_OT_toggle_auto_weight,
    WT_OT_toggle_edit_x,
    WT_OT_toggle_topology,
    WT_OT_toggle_weight_x,
    WT_OT_toggle_group_mirror,
    WT_OT_check_armature,
    WT_OT_cleanup_unused_vertex_groups,
    WTM_OT_switch_edit_mode,
    WTM_OT_switch_object_mode,
    WTM_OT_toggle_weight_paint,
    WTM_OT_toggle_pose_mode,
    WTM_OT_switch_sculpt_mode,
    WTM_OT_switch_texture_paint_mode,
    WTM_OT_switch_vertex_paint_mode,
    WTM_OT_switch_uv_data_mode,
    WTM_OT_cycle_mode_switcher,
    WTM_OT_return_temp_mode,
    WTM_OT_scan_groups,
    WTM_OT_select_defaults,
    WTM_OT_restore_backups,
    WTM_OT_mirror_selected,
    WTM_UL_group_list,
    *operators_head_prep.CLASSES,
    *operators_head_editing.CLASSES,
    *operators_head_finishing.CLASSES,
    *operators_vertex_locks.CLASSES,
    *operators_vertex_inject.CLASSES,
    *operators_selection_slots.CLASSES[2:],
    *operators_curvature_sync.CLASSES,
    *operators_guided_align.CLASSES,
    *operators_coordinate_copy.CLASSES,
    *operators_planar_edit.CLASSES,
    *operators_inject_new.CLASSES,
    *PANELS,
)


def register():
    register_custom_icons()
    for cls in CORE_CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.witch_tools = PointerProperty(type=WitchToolsProperties)
    bpy.types.Scene.wt_precision_edit = PointerProperty(type=precision_edit_props.WTPrecisionEditProperties)
    bpy.types.WindowManager.wt_return_object_name = StringProperty(default='')
    bpy.types.WindowManager.wt_return_mode = StringProperty(default='OBJECT')
    bpy.types.WindowManager.wt_return_workspace_name = StringProperty(default='')
    bpy.types.WindowManager.wt_temp_object_name = StringProperty(default='')
    bpy.types.WindowManager.wt_temp_mode = StringProperty(default='OBJECT')
    bpy.types.WindowManager.wt_temp_workspace_name = StringProperty(default='')
    bpy.types.WindowManager.wt_last_mesh_name = StringProperty(default='')
    bpy.types.WindowManager.wt_last_switcher_mode = StringProperty(default='OBJECT')

    operators_vertex_locks.register_rna()
    operators_planar_edit.register_planar_guard()

    if bpy.context and getattr(bpy.context, 'scene', None) and hasattr(bpy.context.scene, 'witch_tools'):
        bpy.context.scene.witch_tools.wtm_mirror_tolerance = prefs_mirror_tolerance()
        operators_selection_slots.ensure_selection_slots(bpy.context.scene)

    register_default_keymaps()
    register_handlers()


def _safe_delete(owner, name):
    if hasattr(owner, name):
        delattr(owner, name)


def unregister():
    unregister_handlers()
    unregister_keymaps()
    operators_planar_edit.unregister_planar_guard()
    operators_vertex_locks.unregister_rna()

    _safe_delete(bpy.types.WindowManager, 'wt_last_switcher_mode')
    _safe_delete(bpy.types.WindowManager, 'wt_last_mesh_name')
    _safe_delete(bpy.types.WindowManager, 'wt_temp_workspace_name')
    _safe_delete(bpy.types.WindowManager, 'wt_temp_mode')
    _safe_delete(bpy.types.WindowManager, 'wt_temp_object_name')
    _safe_delete(bpy.types.WindowManager, 'wt_return_workspace_name')
    _safe_delete(bpy.types.WindowManager, 'wt_return_mode')
    _safe_delete(bpy.types.WindowManager, 'wt_return_object_name')
    _safe_delete(bpy.types.Scene, 'wt_precision_edit')
    _safe_delete(bpy.types.Scene, 'witch_tools')

    for cls in reversed(CORE_CLASSES):
        bpy.utils.unregister_class(cls)

    unregister_custom_icons()
