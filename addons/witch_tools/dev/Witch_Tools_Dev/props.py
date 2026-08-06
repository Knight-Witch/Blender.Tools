import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, FloatProperty, FloatVectorProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import PropertyGroup

from .operators_selection_slots import WTSelectionSlotItem


_SYNC_FLAG = '_wt_syncing_mirror_direction'


def _poll_mesh(_self, obj):
    return bool(obj and obj.type == 'MESH')


def _poll_armature(_self, obj):
    return bool(obj and obj.type == 'ARMATURE')


def _sync_runtime(self, context):
    from .runtime import sync_weight_paint_session
    sync_weight_paint_session(context)


def _sync_half_from_side(self, _context):
    if self.get(_SYNC_FLAG, False):
        return
    self[_SYNC_FLAG] = True
    try:
        self.wtm_single_source_half = 'NEGATIVE_X' if self.wtm_source_suffix == 'LEFT' else 'POSITIVE_X'
    finally:
        self[_SYNC_FLAG] = False


def _sync_side_from_half(self, _context):
    if self.get(_SYNC_FLAG, False):
        return
    self[_SYNC_FLAG] = True
    try:
        self.wtm_source_suffix = 'LEFT' if self.wtm_single_source_half == 'NEGATIVE_X' else 'RIGHT'
    finally:
        self[_SYNC_FLAG] = False


def _active_mesh_vertex_groups(self, context):
    items = [('', '-- None --', 'Do not restrict shrinkwrap to a vertex group')]
    obj = getattr(context, 'active_object', None)
    if obj and obj.type == 'MESH':
        items.extend((group.name, group.name, '') for group in obj.vertex_groups)
    return items


class WTObjectRefItem(PropertyGroup):
    object_name: StringProperty(default='')


class WTWeightMirrorItem(PropertyGroup):
    source_name: StringProperty()
    target_name: StringProperty()
    enabled: BoolProperty(default=True)
    kind: EnumProperty(items=[('PAIRED', 'Paired', ''), ('SINGLE', 'Single', '')])
    status: StringProperty(default='')


class WitchToolsProperties(PropertyGroup):
    # Saved Mesh Selections
    selection_slots: CollectionProperty(type=WTSelectionSlotItem)
    selection_slot_index: IntProperty(name='Active Selection Slot', default=0, min=0)

    # Object / Island Snap
    object_snap_match_orientation: BoolProperty(
        name='Match Orientation',
        description='Rotate the target while snapping edge or face anchors',
        default=False,
    )
    object_snap_normal_mode: EnumProperty(
        name='Normal Direction',
        description='Choose how source and target surface normals meet when orientation matching is enabled',
        items=[
            ('OPPOSING', 'Opposing', 'Match with source and target normals pointing in opposite directions'),
            ('SAME', 'Same', 'Match with source and target normals pointing in the same direction'),
        ],
        default='OPPOSING',
    )

    # Edge / Vertex Inject
    vertex_inject_connect_split: BoolProperty(
        name='Connect & Split Face',
        description='After placing D, connect C to D and split their shared face when required',
        default=True,
    )
    vertex_inject_tolerance_ratio: FloatProperty(
        name='Projection Tolerance',
        description='Maximum distance from the ideal D position to the inferred target chain, measured as a fraction of A-B length',
        default=0.35,
        min=0.001,
        max=2.0,
        precision=3,
    )
    vertex_inject_merge_ratio: FloatProperty(
        name='Existing Vertex Tolerance',
        description='Reuse an existing target-chain vertex instead of creating a near-duplicate, measured as a fraction of A-B length',
        default=0.01,
        min=0.0,
        max=0.25,
        precision=4,
    )

    # Curvature Sync
    curvature_sync_plane: EnumProperty(
        name='Curve Plane',
        description='Plane used to fit the circular A-M-Z arcs; the remaining axis is preserved',
        items=[
            ('XY', 'XY', 'Fit curvature in the XY plane and preserve Z'),
            ('XZ', 'XZ', 'Fit curvature in the XZ plane and preserve Y'),
            ('YZ', 'YZ', 'Fit curvature in the YZ plane and preserve X'),
        ],
        default='XY',
    )
    curvature_sync_segment_mode: EnumProperty(
        name='Segment Count',
        description='Choose how many equal segments are created on each side of the captured middle anchor',
        items=[
            ('MAX_SELECTED', 'Match Selected Maximum', 'Use the largest existing A-to-M or M-to-Z segment count across all selected chains'),
            ('CUSTOM', 'Custom Per Side', 'Use an explicit equal segment count on each side of Middle'),
        ],
        default='MAX_SELECTED',
    )
    curvature_sync_segments_per_side: IntProperty(
        name='Segments per Side',
        description='Equal number of segments from A to Middle and Middle to Z',
        default=12,
        min=1,
        soft_max=128,
    )
    curvature_sync_snap_middle_axis: BoolProperty(
        name='Normalize Middle to Curve Axis',
        description='Use the captured Middle vertex to choose the apex side, then move it to the exact mathematical middle axis of the fitted circle',
        default=True,
    )
    curvature_sync_inject_missing: BoolProperty(
        name='Inject Missing Vertices',
        description='Split selected chain edges to add missing canonical column positions',
        default=True,
    )
    curvature_sync_connect_columns: BoolProperty(
        name='Build Missing Column Edges',
        description='Connect corresponding vertices across adjacent selected curve chains when they share a face',
        default=True,
    )
    curvature_sync_repair_misaligned_columns: BoolProperty(
        name='Replace Misaligned Column Edges',
        description='Dissolve safe interior cross-edges that connect different canonical slots, then rebuild correct same-slot columns',
        default=True,
    )
    curvature_sync_respect_locks: BoolProperty(
        name='Respect Vertex Locks',
        description='Keep enabled Vertex Lock vertices fixed and preserve lock-group indices through topology changes',
        default=True,
    )

    # Guided Align
    align_reference_mode: EnumProperty(
        name='Anchor Reference',
        description='Use the active captured element when available, or the median of every captured anchor vertex',
        items=[
            ('ACTIVE', 'Active Element', 'Use the captured active vertex, edge midpoint, or face center'),
            ('MEDIAN', 'Median', 'Use the median of all captured anchor vertices'),
        ],
        default='ACTIVE',
    )
    align_frame: EnumProperty(
        name='Alignment Frame',
        description='Match normal world coordinates or coordinates measured in an arbitrary custom guide frame',
        items=[
            ('WORLD', 'World XYZ', 'Use Blender world X, Y, and Z'),
            ('CUSTOM', 'Custom Guide', 'Use a frame whose X axis follows the captured guide line'),
        ],
        default='WORLD',
    )
    align_custom_target: EnumProperty(
        name='Custom Target',
        description='Choose whether the custom frame matches the anchor or projects targets onto the guide line itself',
        items=[
            ('ANCHOR_FRAME', 'Match Anchor in Guide Frame', 'Match selected custom-frame components to the captured anchor'),
            ('GUIDE_LINE', 'Project to Guide Line', 'Move targets onto the guide line by matching custom Y and Z while preserving distance along custom X'),
        ],
        default='ANCHOR_FRAME',
    )
    align_match_x: BoolProperty(
        name='X',
        description='Match world X, or custom-frame X when Custom Guide is active; disabled components remain unchanged',
        default=False,
    )
    align_match_y: BoolProperty(
        name='Y',
        description='Match world Y, or custom-frame Y when Custom Guide is active; disabled components remain unchanged',
        default=False,
    )
    align_match_z: BoolProperty(
        name='Z',
        description='Match world Z, or custom-frame Z when Custom Guide is active; disabled components remain unchanged',
        default=True,
    )
    align_move_mode: EnumProperty(
        name='Move Along',
        description='Move freely on the enabled coordinate components or restrict movement to captured straight rail edges',
        items=[
            ('FREE', 'Free Coordinates', 'Change only the enabled coordinate components'),
            ('SLIDE_RAIL', 'Captured Rails', 'Slide along captured straight edge rails until the requested coordinates match'),
        ],
        default='FREE',
    )
    align_relationship: EnumProperty(
        name='Anchor Mapping',
        description='Use one anchor for all targets or derive one parent/child relationship from each captured rail',
        items=[
            ('ONE_TO_ALL', 'One Anchor to All', 'Every subordinate group aligns to the same captured anchor reference'),
            ('PAIRED_RAIL', 'Paired by Rail', 'Each rail component must contain exactly one captured parent anchor and one subordinate island'),
        ],
        default='ONE_TO_ALL',
    )
    align_grouping: EnumProperty(
        name='Target Groups',
        description='When preserving shape, move all selected targets together or move each connected selected island independently',
        items=[
            ('WHOLE_SELECTION', 'Whole Selection', 'Treat all selected subordinate vertices on each object as one group'),
            ('PER_ISLAND', 'Per Selected Island', 'Treat disconnected selected regions as independent groups'),
        ],
        default='WHOLE_SELECTION',
    )
    align_preserve_shape: BoolProperty(
        name='Preserve Relative Spacing / Shape',
        description='Apply one rigid translation per target group so relative vertex spacing and the selected shape are preserved',
        default=False,
    )
    align_clamp_to_rail: BoolProperty(
        name='Stay Within Captured Rail',
        description='Cancel instead of extending past the minimum or maximum point of the captured rail',
        default=True,
    )
    align_respect_locks: BoolProperty(
        name='Respect Vertex Locks',
        description='Cancel the entire operation if an enabled Vertex Lock protects any subordinate vertex',
        default=True,
    )
    align_solve_tolerance: FloatProperty(
        name='Solve Tolerance',
        description='Numerical tolerance used when multiple requested components must meet the same rail point',
        default=0.00001,
        min=0.000000001,
        soft_max=0.01,
        precision=7,
    )
    align_rail_straight_tolerance: FloatProperty(
        name='Rail Straightness',
        description='Maximum world-space deviation allowed before a captured rail is considered curved or ambiguous',
        default=0.0001,
        min=0.000000001,
        soft_max=0.1,
        precision=7,
        unit='LENGTH',
    )
    align_guide_start: FloatVectorProperty(
        name='Guide Start',
        description='World-space start of the arbitrary custom guide line',
        size=3,
        subtype='XYZ',
        unit='LENGTH',
        precision=5,
    )
    align_guide_end: FloatVectorProperty(
        name='Guide End',
        description='World-space end of the arbitrary custom guide line',
        size=3,
        subtype='XYZ',
        unit='LENGTH',
        default=(1.0, 0.0, 0.0),
        precision=5,
    )
    align_guide_start_set: BoolProperty(default=False, options={'HIDDEN'})
    align_guide_end_set: BoolProperty(default=False, options={'HIDDEN'})
    align_anchor_count: IntProperty(default=0, min=0, options={'HIDDEN'})
    align_anchor_active_count: IntProperty(default=0, min=0, options={'HIDDEN'})
    align_rail_edge_count: IntProperty(default=0, min=0, options={'HIDDEN'})
    align_last_report: StringProperty(default='Capture an anchor, select subordinate geometry, then Analyze or Align.')

    # Weight Transfer
    source_object: PointerProperty(name='Source', type=bpy.types.Object, poll=_poll_mesh)
    target_object: PointerProperty(name='Target', type=bpy.types.Object, poll=_poll_mesh)

    batch_source_mode: EnumProperty(
        name='Source',
        items=[
            ('SELECTION', 'Selected Objects', ''),
            ('COLLECTION', 'Collection', ''),
            ('ARMATURE', 'Armature', ''),
        ],
        default='SELECTION',
    )
    batch_target_mode: EnumProperty(
        name='Target',
        items=[
            ('SELECTION', 'Selected Objects', ''),
            ('COLLECTION', 'Collection', ''),
            ('ARMATURE', 'Armature', ''),
        ],
        default='SELECTION',
    )
    batch_source_collection: PointerProperty(name='Source Collection', type=bpy.types.Collection)
    batch_target_collection: PointerProperty(name='Target Collection', type=bpy.types.Collection)
    batch_source_armature: PointerProperty(name='Source Armature', type=bpy.types.Object, poll=_poll_armature)
    batch_target_armature: PointerProperty(name='Target Armature', type=bpy.types.Object, poll=_poll_armature)
    batch_source_objects: CollectionProperty(type=WTObjectRefItem)
    batch_target_objects: CollectionProperty(type=WTObjectRefItem)

    # Modifier Tool
    shrinkwrap_target: PointerProperty(name='Target', type=bpy.types.Object, poll=_poll_mesh)
    shrinkwrap_wrap_method: EnumProperty(
        name='Wrap Method',
        items=[
            ('NEAREST_SURFACEPOINT', 'Nearest Surface', ''),
            ('PROJECT', 'Project', ''),
            ('NEAREST_VERTEX', 'Nearest Vertex', ''),
            ('TARGET_PROJECT', 'Target Project', ''),
        ],
        default='NEAREST_SURFACEPOINT',
    )
    shrinkwrap_wrap_mode: EnumProperty(
        name='Snap',
        items=[
            ('ON_SURFACE', 'On Surface', ''),
            ('OUTSIDE', 'Outside', ''),
            ('INSIDE', 'Inside', ''),
            ('ABOVE_SURFACE', 'Above Surface', ''),
        ],
        default='ON_SURFACE',
    )
    shrinkwrap_offset: FloatProperty(name='Offset', default=0.0, precision=6)
    shrinkwrap_vertex_group: EnumProperty(name='Vertex Group', items=_active_mesh_vertex_groups)
    shrinkwrap_apply_to_selected: BoolProperty(name='Selected Meshes', default=True)

    scale_value: FloatProperty(name='Uniform Scale', default=1.0, precision=6)
    batch_rotate_use_x: BoolProperty(name='Use X', default=True)
    batch_rotate_use_y: BoolProperty(name='Use Y', default=False)
    batch_rotate_use_z: BoolProperty(name='Use Z', default=False)
    batch_rotate_x_degrees: FloatProperty(name='Rotate X', default=90.0, precision=3)
    batch_rotate_y_degrees: FloatProperty(name='Rotate Y', default=0.0, precision=3)
    batch_rotate_z_degrees: FloatProperty(name='Rotate Z', default=180.0, precision=3)
    batch_auto_apply_rotation: BoolProperty(name='Auto-Apply Selected Rotation', default=False)
    apply_transforms: BoolProperty(name='Apply Transforms in Apply To Selected', default=False)
    remove_modifiers: BoolProperty(name='Remove Modifiers', default=False)

    # Mode Switcher / Auto Mirror
    auto_enable_weight_paint_mirror: BoolProperty(name='Auto Weight', default=True, update=_sync_runtime)
    enable_pose_in_weight_paint: BoolProperty(
        name='Pose in Weight Paint',
        description='When enabled, the armature stays selectable while using non-brush tools in Weight Paint so you can quickly pose without leaving the workflow.',
        default=False,
        update=_sync_runtime,
    )

    # Head Tools
    head_race: EnumProperty(
        name='Race',
        items=[
            ('NONE', '-- Select Race --', ''),
            ('DGB', 'DGB', ''),
            ('DWR', 'DWR', ''),
            ('ELF', 'ELF', ''),
            ('HEL', 'HEL', ''),
            ('HUM', 'HUM', ''),
            ('GTY', 'GTY', ''),
            ('GNO', 'GNO', ''),
            ('HFL', 'HFL', ''),
            ('HRC', 'HRC', ''),
            ('TIF', 'TIF', ''),
        ],
        default='NONE',
    )
    head_name: StringProperty(name='Head Name', default='')
    head_target_armature: PointerProperty(name='Armature', type=bpy.types.Object, poll=_poll_armature)
    head_target_mesh: PointerProperty(name='Reference Mesh', type=bpy.types.Object, poll=_poll_mesh)
    head_reference_mesh: PointerProperty(name='Vanilla Reference', type=bpy.types.Object, poll=_poll_mesh)
    head_offset_distance: FloatProperty(name='Surface Offset', default=0.00015, min=0.0, max=0.01, precision=5, unit='LENGTH')
    # Weight Mirror
    wtm_groups: CollectionProperty(type=WTWeightMirrorItem)
    wtm_active_index: IntProperty(default=0)
    wtm_left_suffix: StringProperty(default='.L')
    wtm_right_suffix: StringProperty(default='.R')
    wtm_source_suffix: EnumProperty(
        name='Mirror Direction',
        items=[('LEFT', 'Left', ''), ('RIGHT', 'Right', '')],
        default='LEFT',
        update=_sync_half_from_side,
    )
    wtm_include_single: BoolProperty(name='Include single-name groups', default=True)
    wtm_single_source_half: EnumProperty(
        name='Single-Name Source',
        items=[('NEGATIVE_X', '-X', ''), ('POSITIVE_X', '+X', '')],
        default='NEGATIVE_X',
        update=_sync_side_from_half,
    )
    wtm_mirror_tolerance: FloatProperty(name='Vertex match tolerance', default=0.0005, min=0.0, precision=6)
    wtm_center_epsilon: FloatProperty(name='Center epsilon', default=0.0001, min=0.0, precision=6)
    wtm_backup_groups: BoolProperty(name='Backup touched groups', default=True)
    wtm_detected_left_suffix: StringProperty(default='')
    wtm_detected_right_suffix: StringProperty(default='')
    wtm_normalize_after: BoolProperty(name='Normalize after mirror', default=False)
    wtm_hide_other_armatures: BoolProperty(name='Hide other armatures', default=False)

    # Cleanup / Armature results
    armature_check_summary: StringProperty(default='')
    armature_check_details: StringProperty(default='')
