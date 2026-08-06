from bpy.types import Panel

from .operators_vertex_locks import _active_group, _active_mesh, _selection_toggle_label
from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .ui_helpers import (
    draw_fullwidth_operator,
    draw_inline_label_prop,
    draw_section_toggle,
    draw_shortcut_hint,
)
from .utils_context import ui_state_owner


class VIEW3D_PT_wt_edit_tools(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_edit_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['EDIT_TOOLS']
    panel_title = 'Edit Tools'
    panel_icon = 'EDITMODE_HLT'
    bl_options = {'DEFAULT_CLOSED'}
    bl_description = 'Vertex Snap, Object Snap, topology repair, saved selections, protected edit-zone, and vertex-lock tools.'

    def draw(self, context):
        props = context.scene.witch_tools
        ui = ui_state_owner(context)
        layout = self.layout

        if getattr(ui, 'ui_minimal_mode', False):
            return

        snap = layout.box()
        if draw_section_toggle(
            snap,
            ui,
            'show_edit_vertex_snap',
            'Vertex Snap',
            section_icon='SNAP_VERTEX',
            help_topic='vertex_snap_title',
        ):
            draw_fullwidth_operator(snap, 'mesh.vertex_snap_global', 'Snap Vertices')
            draw_shortcut_hint(snap, 'mesh.vertex_snap_global')

        object_snap = layout.box()
        if draw_section_toggle(
            object_snap,
            ui,
            'show_edit_object_snap',
            'Object Snap',
            section_icon='AREA_JOIN_DOWN',
            help_topic='object_snap_title',
        ):
            actions = object_snap.row(align=True)
            op = actions.operator('mesh.object_island_snap', text='Vertex', icon='VERTEXSEL')
            op.element_type = 'VERT'
            op = actions.operator('mesh.object_island_snap', text='Edge', icon='EDGESEL')
            op.element_type = 'EDGE'
            op = actions.operator('mesh.object_island_snap', text='Face', icon='FACESEL')
            op.element_type = 'FACE'

            select_mode = context.tool_settings.mesh_select_mode
            if select_mode[1] or select_mode[2]:
                options = object_snap.row(align=True)
                options.prop(
                    props,
                    'object_snap_match_orientation',
                    text='Match Orientation',
                    icon='SNAP_NORMAL',
                    toggle=True,
                )
                direction = options.row(align=True)
                direction.ui_units_x = 2.2
                direction.enabled = props.object_snap_match_orientation
                direction.prop_enum(
                    props,
                    'object_snap_normal_mode',
                    'OPPOSING',
                    text='',
                    icon='ARROW_LEFTRIGHT',
                )
                direction.prop_enum(
                    props,
                    'object_snap_normal_mode',
                    'SAME',
                    text='',
                    icon='FORWARD',
                )

        inject = layout.box()
        if draw_section_toggle(
            inject,
            ui,
            'show_edit_vertex_inject',
            'Edge / Vertex Inject',
            section_icon='MOD_EDGESPLIT',
            help_topic='vertex_inject_title',
        ):
            if context.mode != 'EDIT_MESH':
                inject.label(text='Enter Edit Mode on one mesh object.', icon='INFO')
            else:
                inject.label(text='Click A, then B, then C. C must be active last.')
                inject.label(text='A-B = source column; B-C = row direction.')

            inject.prop(props, 'vertex_inject_connect_split', toggle=True)
            tolerance = inject.row(align=True)
            tolerance.label(text='Projection Tolerance')
            tolerance.prop(props, 'vertex_inject_tolerance_ratio', text='')
            merge = inject.row(align=True)
            merge.label(text='Existing Vertex Tolerance')
            merge.prop(props, 'vertex_inject_merge_ratio', text='')
            inject.operator(
                'mesh.wt_vertex_inject_auto_aligned',
                text='Inject Auto-Aligned Vertex',
                icon='MOD_EDGESPLIT',
            )

        curvature = layout.box()
        if draw_section_toggle(
            curvature,
            ui,
            'show_edit_curvature_sync',
            'Curvature Sync',
            section_icon='CURVE_BEZCURVE',
            help_topic='curvature_sync_title',
        ):
            if context.mode != 'EDIT_MESH':
                curvature.label(text='Enter Edit Mode on the mesh object(s).', icon='INFO')
            else:
                curvature.label(text='Capture one A / Middle / Z vertex per selected curve chain.')

            anchors = curvature.row(align=True)
            op = anchors.operator('mesh.wt_curvature_capture_anchor', text='Capture A', icon='TRACKING_REFINE_BACKWARDS')
            op.anchor_type = 'A'
            op = anchors.operator('mesh.wt_curvature_capture_anchor', text='Middle', icon='PIVOT_MEDIAN')
            op.anchor_type = 'M'
            op = anchors.operator('mesh.wt_curvature_capture_anchor', text='Capture Z', icon='TRACKING_REFINE_FORWARDS')
            op.anchor_type = 'Z'

            curvature.operator('mesh.wt_curvature_clear_anchors', text='Clear Captured Anchors', icon='X')

            plane_row = curvature.row(align=True)
            plane_row.label(text='Curve Plane')
            plane_row.prop(props, 'curvature_sync_plane', text='')

            count_row = curvature.row(align=True)
            count_row.label(text='Segments')
            count_row.prop(props, 'curvature_sync_segment_mode', text='')
            if props.curvature_sync_segment_mode == 'CUSTOM':
                custom = curvature.row(align=True)
                custom.label(text='Per Side')
                custom.prop(props, 'curvature_sync_segments_per_side', text='')

            toggles = curvature.column(align=True)
            toggles.prop(props, 'curvature_sync_snap_middle_axis', toggle=True)
            toggles.prop(props, 'curvature_sync_inject_missing', toggle=True)
            toggles.prop(props, 'curvature_sync_connect_columns', toggle=True)
            repair_row = toggles.row(align=True)
            repair_row.enabled = props.curvature_sync_connect_columns
            repair_row.prop(props, 'curvature_sync_repair_misaligned_columns', toggle=True)
            toggles.prop(props, 'curvature_sync_respect_locks', toggle=True)

            actions = curvature.row(align=True)
            actions.operator('mesh.wt_curvature_analyze', text='Analyze', icon='VIEWZOOM')
            actions.operator('mesh.wt_curvature_sync', text='Apply Curvature Sync', icon='MOD_CURVE')

        align = layout.box()
        if draw_section_toggle(
            align,
            ui,
            'show_edit_guided_align',
            'Align Vertices / Edges / Faces',
            section_icon='PIVOT_ACTIVE',
            help_topic='guided_align_title',
        ):
            if context.mode != 'EDIT_MESH':
                align.label(text='Enter Mesh Edit Mode on the mesh object(s).', icon='INFO')

            step1 = align.box()
            step1.label(text='1. Capture Parent Anchor', icon='PIVOT_ACTIVE')
            reference = step1.row(align=True)
            reference.label(text='Anchor Point')
            reference.prop(props, 'align_reference_mode', text='')
            step1.operator(
                'mesh.wt_guided_align_capture_anchor',
                text='Capture Selected Anchor',
                icon='RESTRICT_SELECT_OFF',
            )
            captured = step1.row(align=True)
            captured.scale_y = 0.72
            captured.label(
                text=f'Captured: {props.align_anchor_count} verts'
                + (f' ({props.align_anchor_active_count} active)' if props.align_anchor_active_count else '')
            )

            step2 = align.box()
            step2.label(text='2. Choose Alignment Target', icon='ORIENTATION_GLOBAL')
            frame = step2.row(align=True)
            frame.label(text='Frame')
            frame.prop(props, 'align_frame', text='')

            if props.align_frame == 'CUSTOM':
                target = step2.row(align=True)
                target.label(text='Custom Target')
                target.prop(props, 'align_custom_target', text='')

                guide_start = step2.column(align=True)
                guide_start.prop(props, 'align_guide_start', text='Guide Start')
                start_actions = guide_start.row(align=True)
                op = start_actions.operator('mesh.wt_guided_align_capture_guide_point', text='Capture Start', icon='IMPORT')
                op.point = 'START'
                start_actions.operator('mesh.wt_guided_align_copy_anchor_to_guide_start', text='Copy Anchor', icon='PIVOT_ACTIVE')

                guide_end = step2.column(align=True)
                guide_end.prop(props, 'align_guide_end', text='Guide End')
                op = guide_end.operator('mesh.wt_guided_align_capture_guide_point', text='Capture End from Selection', icon='EXPORT')
                op.point = 'END'
                guide_status = step2.row(align=True)
                guide_status.scale_y = 0.72
                guide_status.label(
                    text='Guide: '
                    + ('Start set' if props.align_guide_start_set else 'Start missing')
                    + ' / '
                    + ('End set' if props.align_guide_end_set else 'End missing')
                )

            if not (props.align_frame == 'CUSTOM' and props.align_custom_target == 'GUIDE_LINE'):
                axes = step2.row(align=True)
                axes.label(text='Match Coordinates')
                axes.prop(props, 'align_match_x', text='X', toggle=True)
                axes.prop(props, 'align_match_y', text='Y', toggle=True)
                axes.prop(props, 'align_match_z', text='Z', toggle=True)
                unchanged = step2.row()
                unchanged.scale_y = 0.66
                unchanged.label(text='Axes left off stay unchanged.')
            else:
                line_hint = step2.row()
                line_hint.scale_y = 0.72
                line_hint.label(text='Projects to the guide line; distance along the line is preserved.')

            step3 = align.box()
            step3.label(text='3. Choose How Targets May Move', icon='EMPTY_ARROWS')
            movement = step3.row(align=True)
            movement.label(text='Move Along')
            movement.prop(props, 'align_move_mode', text='')
            mapping = step3.row(align=True)
            mapping.label(text='Parent Mapping')
            mapping.prop(props, 'align_relationship', text='')

            needs_rails = props.align_move_mode == 'SLIDE_RAIL' or props.align_relationship == 'PAIRED_RAIL'
            if needs_rails:
                rails = step3.operator(
                    'mesh.wt_guided_align_capture_rails',
                    text='Capture Selected Slide Rails',
                    icon='EDGESEL',
                )
                rail_status = step3.row()
                rail_status.scale_y = 0.72
                rail_status.label(text=f'Captured: {props.align_rail_edge_count} rail edges')
                if props.align_move_mode == 'SLIDE_RAIL':
                    step3.prop(props, 'align_clamp_to_rail', toggle=True)

            step3.prop(props, 'align_preserve_shape', toggle=True)
            if props.align_preserve_shape:
                grouping = step3.row(align=True)
                grouping.label(text='Move Groups')
                grouping.prop(props, 'align_grouping', text='')
            step3.prop(props, 'align_respect_locks', toggle=True)

            step4 = align.box()
            step4.label(text='4. Select Subordinates and Apply', icon='RESTRICT_SELECT_OFF')
            step4.label(text='Select the vertices, edges, or faces that should move.')
            actions = step4.row(align=True)
            actions.operator('mesh.wt_guided_align_analyze', text='Analyze', icon='VIEWZOOM')
            actions.operator('mesh.wt_guided_align_apply', text='Align', icon='CHECKMARK')

            report = align.row()
            report.alert = props.align_last_report.startswith('Blocked:')
            report.label(text=props.align_last_report, icon='ERROR' if report.alert else 'INFO')
            align.operator('mesh.wt_guided_align_clear', text='Clear All Captures', icon='X')

        selection_slots = layout.box()
        slots_open = bool(getattr(ui, 'show_edit_selection_slots', True))
        slot_header = selection_slots.split(factor=0.68, align=True)
        slot_left = slot_header.row(align=True)

        arrow = slot_left.row(align=True)
        arrow.ui_units_x = 0.85
        arrow.prop(
            ui,
            'show_edit_selection_slots',
            text='',
            emboss=False,
            icon='TRIA_DOWN' if slots_open else 'TRIA_RIGHT',
        )
        # Make the title itself clickable as well as the small disclosure arrow.
        slot_left.prop(
            ui,
            'show_edit_selection_slots',
            text='Selection Slots',
            emboss=False,
            icon='LONGDISPLAY',
        )

        slot_right = slot_header.row(align=True)
        slot_right.alignment = 'RIGHT'
        slot_right.operator('mesh.wt_selection_slot_clear_all', text='Clear All', icon='TRASH')

        if slots_open:
            # Never mutate Scene/mesh data from Panel.draw(). New or legacy scenes that
            # have no initialized rows receive a safe operator button instead.
            slots = props.selection_slots
            if len(slots) == 0:
                initialize = selection_slots.row(align=True)
                initialize.label(text='No selection slots initialized.', icon='INFO')
                initialize.operator('mesh.wt_selection_slot_add', text='Create Slot 1', icon='ADD')
            else:
                for index, slot in enumerate(slots):
                    try:
                        row = selection_slots.row(align=True)

                        move = row.row(align=True)
                        move.ui_units_x = 1.7
                        up = move.row(align=True)
                        up.enabled = index > 0
                        op = up.operator('mesh.wt_selection_slot_move', text='', icon='TRIA_UP')
                        op.slot_index = index
                        op.direction = 'UP'
                        down = move.row(align=True)
                        down.enabled = index < len(slots) - 1
                        op = down.operator('mesh.wt_selection_slot_move', text='', icon='TRIA_DOWN')
                        op.slot_index = index
                        op.direction = 'DOWN'

                        name_field = row.row(align=True)
                        name_field.prop(slot, 'name', text='')

                        select_button = row.row(align=True)
                        select_button.ui_units_x = 1.05
                        select_button.enabled = bool(slot.has_data)
                        op = select_button.operator('mesh.wt_selection_slot_reselect', text='', icon='RESTRICT_SELECT_OFF')
                        op.slot_index = index

                        save_button = row.row(align=True)
                        save_button.ui_units_x = 1.05
                        save_button.enabled = context.mode == 'EDIT_MESH'
                        op = save_button.operator('mesh.wt_selection_slot_save', text='', icon='FILE_TICK')
                        op.slot_index = index

                        clear_button = row.row(align=True)
                        clear_button.ui_units_x = 1.05
                        clear_button.enabled = bool(slot.has_data)
                        op = clear_button.operator('mesh.wt_selection_slot_clear', text='', icon='TRASH')
                        op.slot_index = index

                        remove_button = row.row(align=True)
                        remove_button.ui_units_x = 1.05
                        op = remove_button.operator('mesh.wt_selection_slot_remove', text='', icon='REMOVE')
                        op.slot_index = index

                        if index == len(slots) - 1:
                            add_button = row.row(align=True)
                            add_button.ui_units_x = 1.05
                            add_button.operator('mesh.wt_selection_slot_add', text='', icon='ADD')
                    except Exception as exc:
                        error = selection_slots.row()
                        error.alert = True
                        error.label(text=f'Slot {index + 1} UI error: {type(exc).__name__}', icon='ERROR')

                hint = selection_slots.row()
                hint.scale_y = 0.62
                hint.label(text='Name fields expand with the N-panel width. Hover clipped names for the full value.')

        locks = layout.box()
        if draw_section_toggle(
            locks,
            ui,
            'show_edit_vertex_locks',
            'Vertex Locks',
            section_icon='LOCKED',
            help_topic='vertex_locks_title',
        ):
            obj = _active_mesh(context)
            if not obj:
                locks.label(text='Select a mesh object.')
                return

            wm = context.window_manager
            if len(obj.wvl_lock_groups) > 0:
                active_index = max(0, min(getattr(obj, 'wvl_active_group', 0), len(obj.wvl_lock_groups) - 1))
                active_group = obj.wvl_lock_groups[active_index]
            else:
                active_group = None

            core = locks.box()
            if draw_section_toggle(core, ui, 'show_vertex_locks_core', 'Vertex Locks', section_icon='FAKE_USER_ON', help_topic='vertex_locks_core_title'):
                top = core.row(align=True)
                guard = top.row(align=True)
                guard.ui_units_x = 3.0
                guard.operator(
                    'witch_vertex_locks.toggle_guard',
                    text='Guard ON' if wm.wvl_guard_enabled else 'Guard OFF',
                    icon='FAKE_USER_ON' if wm.wvl_guard_enabled else 'FAKE_USER_OFF',
                    depress=wm.wvl_guard_enabled,
                )

                interval_hint = top.row(align=True)
                interval_hint.ui_units_x = 3.0
                hint = interval_hint.operator('witch_tools.help_tooltip', text='Guard Interval', icon='SORTTIME')
                hint.topic = 'vertex_locks_guard_interval'

                interval_value = top.row(align=True)
                interval_value.ui_units_x = 2.6
                interval_value.prop(wm, 'wvl_guard_interval', text='')

                draw_fullwidth_operator(core, 'witch_vertex_locks.refresh_mesh_normals', 'Refresh Locked', icon='FILE_REFRESH')

            zone = locks.box()
            if draw_section_toggle(zone, ui, 'show_vertex_locks_zone', 'Protected Edit Zone', section_icon='SELECT_SET', help_topic='vertex_locks_zone_title'):
                name_row = zone.row(align=True)
                name_row.label(text='Name', icon='INFO')
                name_field = name_row.row(align=True)
                name_field.ui_units_x = 8.4
                name_field.prop(wm, 'wvl_zone_name', text='')

                op = draw_fullwidth_operator(zone, 'witch_vertex_locks.create_edit_zone', 'Create Edit Zone', icon='MESH_GRID')
                op.zone_name = wm.wvl_zone_name
                op.clear_existing = wm.wvl_clear_existing_on_zone

                zone.prop(wm, 'wvl_clear_existing_on_zone', text='Clear Existing Locks First')
                draw_fullwidth_operator(zone, 'witch_vertex_locks.select_edit_zone_interior', 'Select Editable Interior', icon='SELECT_INTERSECT')
                if obj.wvl_last_edit_zone_name:
                    zone.label(text=f'Last Zone: {obj.wvl_last_edit_zone_name}')

            groups = locks.box()
            if draw_section_toggle(groups, ui, 'show_vertex_locks_groups', 'Groups', section_icon='GROUP_VERTEX', help_topic='vertex_locks_groups_title'):
                row = groups.row(align=True)
                op = row.operator('witch_vertex_locks.toggle_selected', text='Lock Selected', icon='LOCKED')
                op = row.operator('witch_vertex_locks.lock_selected', text='New Group', icon='ADD')
                op.new_group = True

                row = groups.row(align=True)
                op = row.operator('witch_vertex_locks.unlock_selected', text='Unlock Selected', icon='UNLOCKED')
                op.active_only = False
                op = row.operator('witch_vertex_locks.unlock_selected', text='Unlock Active Group', icon='GROUP_VERTEX')
                op.active_only = True

                search = groups.row(align=True)
                search.prop(ui, 'vertex_locks_group_filter', text='', icon='VIEWZOOM')

                rows = 1 if len(obj.wvl_lock_groups) == 0 else min(3, len(obj.wvl_lock_groups))
                groups.template_list('WVL_UL_lock_groups', '', obj, 'wvl_lock_groups', obj, 'wvl_active_group', rows=rows)

                group_state_icon = 'LOCKED' if active_group and active_group.kind != 'EDITABLE' and active_group.locked else 'UNLOCKED'
                row = groups.row(align=True)
                row.operator('witch_vertex_locks.group_toggle_lock', text='Toggle Active', icon=group_state_icon)
                row.operator('witch_vertex_locks.delete_group', text='Delete Active', icon='TRASH')

                row = groups.row(align=True)
                op = row.operator('witch_vertex_locks.select_group', text='Select Active', icon='RESTRICT_SELECT_OFF')
                op.all_groups = False
                op = row.operator('witch_vertex_locks.select_group', text='Select All Locked', icon='GROUP_VERTEX')
                op.all_groups = True

                row = groups.row(align=True)
                op = row.operator('witch_vertex_locks.unlock_all', text='Disable All', icon='HIDE_OFF')
                op.clear_groups = False
                op = row.operator('witch_vertex_locks.unlock_all', text='Clear All', icon='TRASH')
                op.clear_groups = True

            sculpt = locks.box()
            if draw_section_toggle(sculpt, ui, 'show_vertex_locks_sculpt', 'Sculpt Protection', section_icon='SCULPTMODE_HLT', help_topic='vertex_locks_sculpt_title'):
                row = sculpt.row(align=True)
                op = row.operator('witch_vertex_locks.apply_sculpt_mask_from_locks', text='Sculpt Mask', icon='CHECKMARK')
                op.selected_meshes_only = True
                op = row.operator('witch_vertex_locks.clear_sculpt_mask', text='Clear Sculpt Mask', icon='PANEL_CLOSE')
                op.selected_meshes_only = True

            mirror = locks.box()
            if draw_section_toggle(mirror, ui, 'show_vertex_locks_shape', 'Shape Mirror', section_icon='MOD_MIRROR', help_topic='vertex_locks_shape_mirror_title'):
                draw_inline_label_prop(mirror, 'Direction', wm, 'wvl_mirror_direction', label_units=3.0, field_units=5.6)

                toggle_row = mirror.row(align=True)
                selected_icon = 'RESTRICT_SELECT_ON' if wm.wvl_mirror_selected_target_only else 'RESTRICT_SELECT_OFF'
                preserve_icon = 'LOCKED' if wm.wvl_mirror_preserve_locked else 'UNLOCKED'
                toggle_row.prop(wm, 'wvl_mirror_selected_target_only', text='Target Only', icon=selected_icon, toggle=True)
                toggle_row.prop(wm, 'wvl_mirror_preserve_locked', text='Preserve Locked', icon=preserve_icon, toggle=True)

                dist_row = mirror.row(align=True)
                dist_row.label(text='Max Match Distance')
                dist_field = dist_row.row(align=True)
                dist_field.ui_units_x = 3.6
                dist_field.prop(wm, 'wvl_mirror_max_distance', text='')
                op = draw_fullwidth_operator(mirror, 'witch_vertex_locks.mirror_shape_area', 'Mirror Selected Shape', icon='MOD_MIRROR')
                op.direction = wm.wvl_mirror_direction
                op.selected_target_only = wm.wvl_mirror_selected_target_only
                op.preserve_locked = wm.wvl_mirror_preserve_locked
                op.max_distance = wm.wvl_mirror_max_distance


PANELS = (VIEW3D_PT_wt_edit_tools,)
