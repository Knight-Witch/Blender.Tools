from .ui_helpers import draw_section_toggle, draw_shortcut_hint


def _report_row(layout, text):
    row = layout.row()
    row.scale_y = 0.62
    row.alert = str(text).startswith('Blocked:')
    row.label(text=text, icon='ERROR' if row.alert else 'INFO')


def draw_coordinate_copy(layout, context, state):
    box = layout.box()
    if not draw_section_toggle(
        box,
        state,
        'show_coordinate_copy',
        'Coordinate Copy',
        section_icon='COPYDOWN',
        help_topic='coordinate_copy_title',
    ):
        return

    if context.mode != 'EDIT_MESH':
        box.label(text='Enter Mesh Edit Mode on the mesh object(s).', icon='INFO')

    step1 = box.box()
    step1.label(text='1. Choose What to Copy', icon='ORIENTATION_GLOBAL')

    space = step1.row(align=True)
    space.label(text='Space')
    space.prop_enum(state, 'coordinate_copy_space', 'GLOBAL', text='Global')
    space.prop_enum(state, 'coordinate_copy_space', 'LOCAL', text='Local')

    axes = step1.row(align=True)
    axes.label(text='Axes')
    axes.prop(state, 'coordinate_copy_axis_x', text='X', toggle=True)
    axes.prop(state, 'coordinate_copy_axis_y', text='Y', toggle=True)
    axes.prop(state, 'coordinate_copy_axis_z', text='Z', toggle=True)

    components = step1.row(align=True)
    components.label(text='Copy')
    components.prop(state, 'coordinate_copy_use_location', text='Location', toggle=True)
    components.prop(state, 'coordinate_copy_use_rotation', text='Rotation', toggle=True)
    components.prop(state, 'coordinate_copy_use_scale', text='Scale', toggle=True)

    step2 = box.box()
    step2.label(text='2. Select One Source', icon='PIVOT_ACTIVE')
    capture = step2.row(align=True)
    capture.operator('mesh.wt_coordinate_copy_capture', text='Capture Source', icon='RESTRICT_SELECT_OFF')
    clear = capture.row(align=True)
    clear.ui_units_x = 1.2
    clear.enabled = state.coordinate_copy_has_source
    clear.operator('mesh.wt_coordinate_copy_clear', text='', icon='X')
    status = step2.row()
    status.scale_y = 0.62
    status.label(text=state.coordinate_copy_source_label)

    step3 = box.box()
    step3.label(text='3. Select Target(s) and Apply', icon='CHECKMARK')
    step3.operator('mesh.wt_coordinate_copy_apply', text='Apply Copied Coordinates', icon='CHECKMARK')
    draw_shortcut_hint(step3, 'mesh.wt_coordinate_copy_apply')
    _report_row(box, state.coordinate_copy_last_report)


def draw_planar_edit(layout, context, state):
    box = layout.box()
    if not draw_section_toggle(
        box,
        state,
        'show_planar_edit',
        'Planar Edit',
        section_icon='MESH_PLANE',
        help_topic='planar_edit_title',
    ):
        return

    if context.mode != 'EDIT_MESH':
        box.label(text='Enter Mesh Edit Mode on the mesh object(s).', icon='INFO')

    lock = box.box()
    lock.label(text='Plane Lock', icon='LOCKED')
    lock.label(text='Freeze selected geometry on object-local axis coordinates.')
    axes = lock.row(align=True)
    axes.label(text='Lock Axes')
    axes.prop(state, 'planar_lock_axis_x', text='X', toggle=True)
    axes.prop(state, 'planar_lock_axis_y', text='Y', toggle=True)
    axes.prop(state, 'planar_lock_axis_z', text='Z', toggle=True)
    actions = lock.row(align=True)
    actions.operator('mesh.wt_planar_lock_selected', text='Lock Selected', icon='LOCKED')
    actions.operator('mesh.wt_planar_unlock_selected', text='Unlock Selected', icon='UNLOCKED')
    clear = lock.row()
    clear.scale_y = 0.82
    clear.operator('mesh.wt_planar_clear_all', text='Clear All Plane Locks', icon='X')

    level = box.box()
    level.label(text='Level', icon='MESH_PLANE')
    level.label(text='Copy exact source world coordinates to every selected target vertex.')
    capture = level.row(align=True)
    capture.operator('mesh.wt_planar_level_capture', text='1. Capture Source', icon='PIVOT_ACTIVE')
    source = capture.row()
    source.alignment = 'RIGHT'
    source.label(text=state.planar_level_source_label)
    axes = level.row(align=True)
    axes.label(text='Axes')
    axes.prop(state, 'planar_level_axis_x', text='X', toggle=True)
    axes.prop(state, 'planar_level_axis_y', text='Y', toggle=True)
    axes.prop(state, 'planar_level_axis_z', text='Z', toggle=True)
    level.operator('mesh.wt_planar_level_targets', text='2. Level Targets', icon='CHECKMARK')

    _report_row(box, state.planar_edit_last_report)


def draw_inject_new(layout, context, state, legacy_props):
    box = layout.box()
    if not draw_section_toggle(
        box,
        state,
        'show_inject_new',
        'Inject New',
        section_icon='MOD_EDGESPLIT',
        help_topic='inject_new_title',
    ):
        return

    if context.mode != 'EDIT_MESH':
        box.label(text='Enter Edit Mode on one mesh object.', icon='INFO')

    step1 = box.box()
    step1.label(text='1. Initial Setup', icon='MOD_EDGESPLIT')
    modes = step1.row(align=True)
    modes.prop_enum(state, 'inject_new_mode', 'SOLO', text='Solo')
    modes.prop_enum(state, 'inject_new_mode', 'BRANCH', text='Branch')
    modes.prop_enum(state, 'inject_new_mode', 'SLIDE', text='Slide')

    step2 = box.box()
    step2.label(text='2. Movement', icon='EMPTY_ARROWS')
    if state.inject_new_mode == 'SLIDE':
        step2.label(text='Slide uses the selected source edge as its rail.', icon='EDGESEL')
    else:
        movement = step2.row(align=True)
        movement.prop_enum(state, 'inject_new_move', 'X', text='X')
        movement.prop_enum(state, 'inject_new_move', 'Y', text='Y')
        movement.prop_enum(state, 'inject_new_move', 'Z', text='Z')
        movement.prop_enum(state, 'inject_new_move', 'RAIL', text='Rail')
        if state.inject_new_move == 'RAIL':
            rail = step2.row(align=True)
            rail.operator('mesh.wt_inject_new_capture_rail_end', text='Capture Rail End', icon='PIVOT_ACTIVE')
            clear = rail.row(align=True)
            clear.ui_units_x = 1.2
            clear.enabled = state.inject_new_rail_end_set
            clear.operator('mesh.wt_inject_new_clear_rail', text='', icon='X')
            status = step2.row()
            status.scale_y = 0.62
            status.label(text=state.inject_new_rail_target_label)

    step3 = box.box()
    step3.label(text='3. New Element', icon='VERTEXSEL')
    if state.inject_new_mode == 'SLIDE':
        selected = step3.row()
        selected.alignment = 'CENTER'
        selected.label(text='Vertex', icon='VERTEXSEL')
    else:
        elements = step3.row(align=True)
        elements.prop_enum(state, 'inject_new_element_type', 'VERT', text='Vertex', icon='VERTEXSEL')
        elements.prop_enum(state, 'inject_new_element_type', 'EDGE', text='Edge', icon='EDGESEL')
        elements.prop_enum(state, 'inject_new_element_type', 'FACE', text='Face', icon='FACESEL')

    step4 = box.box()
    step4.label(text='4. Select Source and Inject', icon='RESTRICT_SELECT_OFF')
    if state.inject_new_mode == 'SLIDE':
        step4.label(text='Select exactly one edge. A new vertex will divide it.')
    else:
        step4.label(text='Select exactly one source vertex, edge, or face matching Step 3.')
    step4.operator('mesh.wt_inject_new', text='Inject New', icon='MOD_EDGESPLIT')
    _report_row(box, state.inject_new_last_report)

    legacy = box.box()
    if draw_section_toggle(
        legacy,
        state,
        'show_auto_aligned_inject',
        'Auto-Aligned Repair',
        section_icon='MOD_EDGESPLIT',
        help_topic='vertex_inject_title',
    ):
        legacy.label(text='Existing A-B-C → D repair workflow.')
        legacy.label(text='Click A, then B, then C; C must be active last.')
        legacy.prop(legacy_props, 'vertex_inject_connect_split', toggle=True)
        tolerance = legacy.row(align=True)
        tolerance.label(text='Projection Tolerance')
        tolerance.prop(legacy_props, 'vertex_inject_tolerance_ratio', text='')
        merge = legacy.row(align=True)
        merge.label(text='Existing Vertex Tolerance')
        merge.prop(legacy_props, 'vertex_inject_merge_ratio', text='')
        legacy.operator(
            'mesh.wt_vertex_inject_auto_aligned',
            text='Inject Auto-Aligned Vertex',
            icon='MOD_EDGESPLIT',
        )
