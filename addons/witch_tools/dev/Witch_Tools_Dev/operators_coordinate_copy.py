from bpy.types import Operator
from mathutils import Euler, Matrix, Vector

from .precision_edit_common import (
    _EPSILON,
    PrecisionEditError,
    _apply_plan,
    _axis_mask,
    _co_from_space,
    _co_to_space,
    _edit_mesh_objects,
    _planned_move_blocked,
    _props,
    _require_axis,
    _selection_kind,
    _shape_key_preflight,
    _single_source,
    clear_current_edit_selection,
)
from .precision_edit_frames import _group_frame, _source_frame, _target_groups_for_object


class WT_OT_coordinate_copy_capture(Operator):
    bl_idname = 'mesh.wt_coordinate_copy_capture'
    bl_label = 'Capture Coordinate Source'
    bl_description = (
        'Capture the selected source element in the chosen Global or Local space. '
        'Vertex rotation uses its normal; edge/face rotation uses a deterministic geometry frame.'
    )
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        try:
            kind, (obj, _bm, element) = _single_source(context)
            center, basis, scale = _source_frame(obj, kind, element, props.coordinate_copy_space)
        except PrecisionEditError as error:
            props.coordinate_copy_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}

        euler = basis.to_euler('XYZ')
        props.coordinate_copy_source_location = center
        props.coordinate_copy_source_rotation = euler
        props.coordinate_copy_source_scale = scale
        props.coordinate_copy_source_type = kind
        props.coordinate_copy_source_object_name = obj.name
        props.coordinate_copy_captured_space = props.coordinate_copy_space
        props.coordinate_copy_has_source = True
        props.coordinate_copy_source_label = f'{obj.name} / {kind.title()}'
        props.coordinate_copy_last_report = f'Captured {kind.title()} source from {obj.name}. Select target geometry, then Apply.'
        clear_current_edit_selection(context)
        self.report({'INFO'}, props.coordinate_copy_last_report)
        return {'FINISHED'}


class WT_OT_coordinate_copy_clear(Operator):
    bl_idname = 'mesh.wt_coordinate_copy_clear'
    bl_label = 'Clear Coordinate Source'
    bl_description = 'Clear the currently captured Coordinate Copy source.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = _props(context)
        props.coordinate_copy_has_source = False
        props.coordinate_copy_source_label = 'No source captured'
        props.coordinate_copy_last_report = 'Select one source element and capture it.'
        return {'FINISHED'}


class WT_OT_coordinate_copy_apply(Operator):
    bl_idname = 'mesh.wt_coordinate_copy_apply'
    bl_label = 'Apply Copied Coordinates'
    bl_description = (
        'Apply the captured source transform to every selected target group. '
        'Targets are independent: vertices apply one-by-one; connected selected edges/faces apply per island, never as one global median.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        try:
            if not props.coordinate_copy_has_source:
                raise PrecisionEditError('Capture a Coordinate Copy source first.')
            if props.coordinate_copy_captured_space != props.coordinate_copy_space:
                raise PrecisionEditError('Coordinate space changed after capture. Recapture the source.')

            axes = _axis_mask(props, 'coordinate_copy_axis')
            _require_axis(axes)
            use_location = bool(props.coordinate_copy_use_location)
            use_rotation = bool(props.coordinate_copy_use_rotation)
            use_scale = bool(props.coordinate_copy_use_scale)
            if not (use_location or use_rotation or use_scale):
                raise PrecisionEditError('Enable Location, Rotation, Scale, or a combination of them.')

            objects = _edit_mesh_objects(context)
            if not objects:
                raise PrecisionEditError('Enter Mesh Edit Mode on at least one mesh object.')
            _shape_key_preflight(objects)

            kind = _selection_kind(context)
            plans = []
            group_count = 0

            source_center = Vector(props.coordinate_copy_source_location)
            source_euler = Euler(tuple(props.coordinate_copy_source_rotation), 'XYZ')
            source_scale = Vector(props.coordinate_copy_source_scale)
            space = props.coordinate_copy_space

            for obj in objects:
                bm, groups = _target_groups_for_object(obj, kind)
                if not groups:
                    continue
                entries = []
                planned_by_vert = {}
                for elements, verts in groups:
                    center, basis, target_scale = _group_frame(obj, kind, elements, verts, space)
                    target_euler = basis.to_euler('XYZ')
                    compatible_source = source_euler.copy()
                    compatible_source.make_compatible(target_euler)

                    desired_angles = [
                        compatible_source[index] if use_rotation and axes[index] else target_euler[index]
                        for index in range(3)
                    ]
                    desired_basis = Euler(tuple(desired_angles), 'XYZ').to_matrix()
                    rotation_delta = desired_basis @ basis.transposed() if use_rotation else Matrix.Identity(3)

                    ratios = [1.0, 1.0, 1.0]
                    if use_scale:
                        for index in range(3):
                            if not axes[index]:
                                continue
                            denominator = target_scale[index]
                            numerator = source_scale[index]
                            if abs(denominator) <= _EPSILON:
                                raise PrecisionEditError(f'{obj.name}: target scale is zero on axis {"XYZ"[index]}.')
                            ratios[index] = numerator / denominator
                    scale_delta = (
                        desired_basis @ Matrix.Diagonal(Vector(ratios)) @ desired_basis.transposed()
                        if use_scale
                        else Matrix.Identity(3)
                    )
                    linear = scale_delta @ rotation_delta

                    desired_center = center.copy()
                    if use_location:
                        for index in range(3):
                            if axes[index]:
                                desired_center[index] = source_center[index]
                    translation = desired_center - center

                    for vert in verts:
                        current = _co_to_space(obj, vert.co, space)
                        transformed = center + linear @ (current - center) + translation
                        new_local = _co_from_space(obj, transformed, space)
                        existing = planned_by_vert.get(vert)
                        if existing is not None and (existing - new_local).length_squared > 1.0e-16:
                            raise PrecisionEditError(
                                f'{obj.name}: overlapping target groups would move one vertex in two different ways.'
                            )
                        planned_by_vert[vert] = new_local
                    group_count += 1

                for vert, new_local in planned_by_vert.items():
                    blocked = _planned_move_blocked(obj, bm, vert, new_local)
                    if blocked:
                        raise PrecisionEditError(f'{obj.name}: target vertex {vert.index} is protected by {blocked}.')
                    entries.append((vert, new_local))
                if entries:
                    plans.append((obj, bm, entries))

            if not plans:
                raise PrecisionEditError('Select at least one target in the active vertex, edge, or face selection mode.')

            _apply_plan(plans)
            moved = sum(len(entries) for _obj, _bm, entries in plans)
            props.coordinate_copy_last_report = f'Applied to {group_count} target group(s), {moved} vertex coordinate(s).'
            self.report({'INFO'}, props.coordinate_copy_last_report)
            return {'FINISHED'}
        except PrecisionEditError as error:
            props.coordinate_copy_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            props.coordinate_copy_last_report = f'Blocked: Coordinate Copy failed: {error}'
            self.report({'ERROR'}, f'Coordinate Copy failed: {error}')
            return {'CANCELLED'}


CLASSES = (
    WT_OT_coordinate_copy_capture,
    WT_OT_coordinate_copy_clear,
    WT_OT_coordinate_copy_apply,
)
