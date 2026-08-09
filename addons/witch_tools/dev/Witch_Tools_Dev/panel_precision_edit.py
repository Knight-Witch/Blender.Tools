from .ui_helpers import draw_section_toggle, draw_shortcut_hint


def _report_row(layout, text):
    row = layout.row()
    row.scale_y = 0.62
    row.alert = str(text).startswith('Blocked:')
    row.label(text=text, icon='ERROR' if row.alert else 'INFO')


def draw_coordinate_copy(layout, context, state):
    box = layout.box()
    if not draw_section_toggle(box, state, 'show_coordinate_copy', 'Coordinate Copy', section_icon='COPYDOWN', help_topic='coordinate_copy_title'):
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
    if not draw_section_toggle(box, state, 'show_planar_edit', 'Planar Edit', section_icon='MESH_PLANE', help_topic='planar_edit_title'):
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


def draw_inject_new(layout, context, state, _legacy_props):
    box = layout.box()
    if not draw_section_toggle(box, state, 'show_inject_new', 'Inject New', section_icon='MOD_EDGESPLIT', help_topic='inject_new_title'):
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
        step2.label(text='Selected edges are rails; all injected verts share one slide factor.', icon='EDGESEL')
    else:
        axes = step2.row(align=True)
        axes.label(text='Axes')
        axes.enabled = not state.inject_new_use_rail
        axes.prop(state, 'inject_new_axis_x', text='X', toggle=True)
        axes.prop(state, 'inject_new_axis_y', text='Y', toggle=True)
        axes.prop(state, 'inject_new_axis_z', text='Z', toggle=True)
        rail_toggle = step2.row(align=True)
        rail_toggle.prop(state, 'inject_new_use_rail', text='Use Captured Rail', icon='EDGESEL', toggle=True)
        if state.inject_new_use_rail:
            rail = step2.row(align=True)
            rail.operator('mesh.wt_inject_new_capture_rail_end', text='Capture Rail End', icon='PIVOT_ACTIVE')
            clear = rail.row(align=True)
            clear.ui_units_x = 1.2
            clear.enabled = state.inject_new_rail_end_set
            clear.operator('mesh.wt_inject_new_clear_rail', text='', icon='X')
            status = step2.row()
            status.scale_y = 0.62
            status.label(text=state.inject_new_rail_target_label)

    snap = step2.row(align=True)
    snap.enabled = state.inject_new_mode != 'SLIDE'
    snap.prop(state, 'inject_new_magnetic_snap', text='Magnetic Snap', icon='SNAP_ON', toggle=True)
    merge = snap.row(align=True)
    merge.enabled = state.inject_new_mode == 'BRANCH' and state.inject_new_magnetic_snap
    merge.prop(state, 'inject_new_auto_merge', text='Auto-Merge', icon='AUTOMERGE_ON', toggle=True)

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
        step4.label(text='Select one or more edges. One new vertex is injected into each.')
    else:
        if state.inject_new_element_type == 'EDGE':
            step4.label(text='Select one or more source edges, then drag the new geometry.')
        else:
            step4.label(text='Select exactly one source matching Step 3, then drag the new geometry.')
    step4.operator('mesh.wt_inject_new', text='Inject New', icon='MOD_EDGESPLIT')
    hint = step4.row()
    hint.scale_y = 0.65
    hint.label(text='Plain MMB orbits around the live injection; Shift/Ctrl+MMB keep normal viewport navigation.')
    _report_row(box, state.inject_new_last_report)


def draw_magic_branch(layout, context, state):
    box = layout.box()
    if not draw_section_toggle(box, state, 'show_magic_branch', 'Magic Branch', section_icon='NODETREE', help_topic='magic_branch_title'):
        return
    if context.mode != 'EDIT_MESH':
        box.label(text='Enter Edit Mode on one mesh object.', icon='INFO')

    mode = box.box()
    mode.label(text='1. Tool Mode', icon='RECOVER_LAST')
    active = mode.operator(
        'mesh.wt_magic_branch_toggle_active',
        text='Magic Branch ON' if state.magic_branch_active else 'Magic Branch OFF',
        icon='PAUSE' if state.magic_branch_active else 'PLAY',
        depress=state.magic_branch_active,
    )
    del active
    draw_shortcut_hint(mode, 'mesh.wt_magic_branch_toggle_active')
    row = mode.row(align=True)
    row.prop(state, 'magic_branch_persistent', text='Stay Armed (Persistent)', icon='PINNED', toggle=True)
    row.operator('mesh.wt_magic_branch_toggle_persistent', text='', icon='FILE_REFRESH')
    draw_shortcut_hint(mode, 'mesh.wt_magic_branch_toggle_persistent')
    sub = mode.row()
    sub.scale_y = 0.65
    sub.label(text='Persistent OFF = one branch then tool turns OFF. ON = keep click-drag branching.')

    setup = box.box()
    setup.label(text='2. Branch Type', icon='MESH_DATA')
    types = setup.row(align=True)
    for element_type, label, icon in (
        ('VERT', 'Vertex', 'VERTEXSEL'),
        ('EDGE', 'Edge', 'EDGESEL'),
        ('FACE', 'Face', 'FACESEL'),
    ):
        op = types.operator(
            'mesh.wt_magic_branch_set_element_type',
            text=label,
            icon=icon,
            depress=state.magic_branch_element_type == element_type,
        )
        op.element_type = element_type
    if state.magic_branch_element_type == 'FACE':
        face_mode = setup.row(align=True)
        face_mode.label(text='Face Build')
        face_mode.prop_enum(state, 'magic_branch_face_mode', 'PAVER', text='Paver')
        face_mode.prop_enum(state, 'magic_branch_face_mode', 'ORGANIC', text='Organic')

    movement = box.box()
    movement.label(text='3. Drag / Snap', icon='EMPTY_ARROWS')
    axes = movement.row(align=True)
    axes.label(text='Axes')
    axes.prop(state, 'magic_branch_axis_x', text='X', toggle=True)
    axes.prop(state, 'magic_branch_axis_y', text='Y', toggle=True)
    axes.prop(state, 'magic_branch_axis_z', text='Z', toggle=True)
    snap = movement.row(align=True)
    snap.prop(state, 'magic_branch_magnetic_snap', text='Magnetic Snap', icon='SNAP_ON', toggle=True)
    merge = snap.row(align=True)
    merge.enabled = state.magic_branch_magnetic_snap
    merge.prop(state, 'magic_branch_auto_merge', text='Auto-Merge', icon='AUTOMERGE_ON', toggle=True)

    start = box.box()
    start.label(text='4. Build in Viewport', icon='PLAY')
    status = start.row()
    status.alert = not state.magic_branch_active
    status.label(
        text='Tool is ON — click-drag source geometry.' if state.magic_branch_active else 'Turn Magic Branch ON in Step 1 to begin.',
        icon='CHECKMARK' if state.magic_branch_active else 'INFO',
    )
    hint = start.column(align=True)
    hint.scale_y = 0.65
    hint.label(text='Branch Type also switches Blender Vertex / Edge / Face selection mode.')
    hint.label(text='Plain MMB orbits around live geometry only while dragging; Shift+MMB pans normally.')
    hint.label(text='Esc or the ON/OFF toggle exits Magic Branch.')
    _report_row(box, state.magic_branch_last_report)
