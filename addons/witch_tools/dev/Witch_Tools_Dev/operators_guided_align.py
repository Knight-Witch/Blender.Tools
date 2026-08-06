"""Guided vertex/edge/face alignment for Witch Tools.

The operator works in world space, plans every coordinate before mutation, and
uses persistent BMesh marker layers for anchors and slide rails. Edges and faces
participate through their vertices, so no topology is created or removed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import bmesh
import bpy
from bpy.types import Operator
from mathutils import Vector

from .guided_align_math import (
    build_frame,
    component_delta,
    from_frame,
    line_extent,
    match_components,
    median_point,
    solve_slide_parameter,
    to_frame,
)
from .operators_vertex_locks import _locked_indices


_ANCHOR_LAYER = 'wt_align_selection_source'
_RAIL_LAYER = 'wt_align_selection_rail'
_EPS = 1.0e-8


class GuidedAlignError(RuntimeError):
    pass


@dataclass
class _MeshState:
    obj: bpy.types.Object
    bm: bmesh.types.BMesh
    world_points: dict[int, Vector]
    selected: set[int]
    anchors: set[int]
    active_anchors: set[int]
    rail_edges: set[int]


@dataclass
class _RailComponent:
    obj: bpy.types.Object
    vertex_indices: set[int]
    edge_indices: set[int]
    anchor_indices: set[int]
    world_points: dict[int, Vector]


@dataclass
class _MoveGroup:
    state: _MeshState
    target_indices: set[int]
    rail_component: _RailComponent | None = None


def _edit_mesh_objects(context) -> list[bpy.types.Object]:
    objects: list[bpy.types.Object] = []
    seen = set()
    for obj in getattr(context, 'objects_in_mode_unique_data', ()) or ():
        if obj and obj.type == 'MESH' and obj.data not in seen:
            seen.add(obj.data)
            objects.append(obj)
    active = getattr(context, 'active_object', None)
    if not objects and active and active.type == 'MESH' and active.mode == 'EDIT':
        objects.append(active)
    return objects


def _all_meshes_with_attribute(name: str) -> list[bpy.types.Mesh]:
    return [mesh for mesh in bpy.data.meshes if getattr(mesh, 'attributes', None) and mesh.attributes.get(name)]


def _remove_marker_everywhere(name: str, domain: str) -> None:
    touched = set()
    for obj in bpy.data.objects:
        if obj.type != 'MESH' or obj.data in touched:
            continue
        mesh = obj.data
        touched.add(mesh)
        if getattr(mesh, 'is_editmode', False):
            bm = bmesh.from_edit_mesh(mesh)
            layers = bm.verts.layers.int if domain == 'POINT' else bm.edges.layers.int
            layer = layers.get(name)
            if layer is not None:
                layers.remove(layer)
                bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
        else:
            attribute = mesh.attributes.get(name) if hasattr(mesh, 'attributes') else None
            if attribute is not None:
                mesh.attributes.remove(attribute)


def _selected_vertices(bm: bmesh.types.BMesh) -> set[int]:
    bm.verts.ensure_lookup_table()
    return {vert.index for vert in bm.verts if vert.select}


def _selected_edges(bm: bmesh.types.BMesh) -> set[int]:
    bm.edges.ensure_lookup_table()
    return {edge.index for edge in bm.edges if edge.select}


def _active_selected_vertex_indices(bm: bmesh.types.BMesh) -> set[int]:
    active = bm.select_history.active
    if active is None:
        return set()
    if isinstance(active, bmesh.types.BMVert):
        return {active.index} if active.select else set()
    if isinstance(active, bmesh.types.BMEdge):
        return {vert.index for vert in active.verts} if active.select else set()
    if isinstance(active, bmesh.types.BMFace):
        return {vert.index for vert in active.verts} if active.select else set()
    return set()


def _write_vertex_capture(context, layer_name: str, *, active_value: bool = False) -> tuple[int, int]:
    objects = _edit_mesh_objects(context)
    if context.mode != 'EDIT_MESH' or not objects:
        raise GuidedAlignError('Enter Mesh Edit Mode before capturing geometry.')

    selections: list[tuple[bpy.types.Object, set[int], set[int]]] = []
    total = 0
    active_total = 0
    for obj in objects:
        bm = bmesh.from_edit_mesh(obj.data)
        selected = _selected_vertices(bm)
        active = _active_selected_vertex_indices(bm) if active_value else set()
        if selected:
            selections.append((obj, selected, active & selected))
            total += len(selected)
            active_total += len(active & selected)
    if not total:
        raise GuidedAlignError('Select at least one vertex, edge, or face to capture.')

    _remove_marker_everywhere(layer_name, 'POINT')
    for obj, selected, active in selections:
        bm = bmesh.from_edit_mesh(obj.data)
        layer = bm.verts.layers.int.get(layer_name) or bm.verts.layers.int.new(layer_name)
        for vert in bm.verts:
            vert[layer] = 2 if vert.index in active else (1 if vert.index in selected else 0)
        for face in bm.faces:
            face.select_set(False)
        for edge in bm.edges:
            edge.select_set(False)
        for vert in bm.verts:
            vert.select_set(False)
        bm.select_history.clear()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return total, active_total


def _write_edge_capture(context, layer_name: str) -> int:
    objects = _edit_mesh_objects(context)
    if context.mode != 'EDIT_MESH' or not objects:
        raise GuidedAlignError('Enter Mesh Edit Mode before capturing slide rails.')

    selections: list[tuple[bpy.types.Object, set[int]]] = []
    total = 0
    for obj in objects:
        bm = bmesh.from_edit_mesh(obj.data)
        selected = _selected_edges(bm)
        if selected:
            selections.append((obj, selected))
            total += len(selected)
    if not total:
        raise GuidedAlignError('Select one or more rail edges before Capture Rails.')

    _remove_marker_everywhere(layer_name, 'EDGE')
    for obj, selected in selections:
        bm = bmesh.from_edit_mesh(obj.data)
        layer = bm.edges.layers.int.get(layer_name) or bm.edges.layers.int.new(layer_name)
        for edge in bm.edges:
            edge[layer] = 1 if edge.index in selected else 0
        for face in bm.faces:
            face.select_set(False)
        for edge in bm.edges:
            edge.select_set(False)
        for vert in bm.verts:
            vert.select_set(False)
        bm.select_history.clear()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return total


def _world_point(obj: bpy.types.Object, local_co) -> Vector:
    return obj.matrix_world @ Vector(local_co)


def _matrix_is_invertible(obj: bpy.types.Object) -> bool:
    try:
        return abs(obj.matrix_world.to_3x3().determinant()) > _EPS
    except Exception:
        return False


def _collect_states(context) -> list[_MeshState]:
    states: list[_MeshState] = []
    for obj in _edit_mesh_objects(context):
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        anchor_layer = bm.verts.layers.int.get(_ANCHOR_LAYER)
        rail_layer = bm.edges.layers.int.get(_RAIL_LAYER)
        anchors = set()
        active_anchors = set()
        if anchor_layer is not None:
            anchors = {vert.index for vert in bm.verts if int(vert[anchor_layer]) > 0}
            active_anchors = {vert.index for vert in bm.verts if int(vert[anchor_layer]) == 2}
        rail_edges = set()
        if rail_layer is not None:
            rail_edges = {edge.index for edge in bm.edges if int(edge[rail_layer]) > 0}
        states.append(
            _MeshState(
                obj=obj,
                bm=bm,
                world_points={vert.index: _world_point(obj, vert.co) for vert in bm.verts},
                selected=_selected_vertices(bm),
                anchors=anchors,
                active_anchors=active_anchors,
                rail_edges=rail_edges,
            )
        )
    return states


def _anchor_reference(states: Iterable[_MeshState], reference_mode: str) -> Vector:
    anchors: list[Vector] = []
    active: list[Vector] = []
    for state in states:
        anchors.extend(state.world_points[index] for index in state.anchors)
        active.extend(state.world_points[index] for index in state.active_anchors)
    if not anchors:
        raise GuidedAlignError('No captured anchor was found. Select it and press Capture Anchor.')
    values = active if reference_mode == 'ACTIVE' and active else anchors
    point = median_point(tuple(tuple(value) for value in values))
    return Vector(point)


def _selected_components(state: _MeshState, indices: set[int]) -> list[set[int]]:
    remaining = set(indices)
    groups: list[set[int]] = []
    while remaining:
        start = remaining.pop()
        group = {start}
        stack = [start]
        while stack:
            index = stack.pop()
            vert = state.bm.verts[index]
            for edge in vert.link_edges:
                other = edge.other_vert(vert).index
                if other in remaining:
                    remaining.remove(other)
                    group.add(other)
                    stack.append(other)
        groups.append(group)
    return groups


def _rail_components(state: _MeshState) -> list[_RailComponent]:
    remaining = set(state.rail_edges)
    components: list[_RailComponent] = []
    while remaining:
        first = remaining.pop()
        edge_indices = {first}
        vertices = {vert.index for vert in state.bm.edges[first].verts}
        stack = list(vertices)
        while stack:
            vertex_index = stack.pop()
            vert = state.bm.verts[vertex_index]
            for edge in vert.link_edges:
                if edge.index not in remaining:
                    continue
                remaining.remove(edge.index)
                edge_indices.add(edge.index)
                for other in edge.verts:
                    if other.index not in vertices:
                        vertices.add(other.index)
                        stack.append(other.index)
        components.append(
            _RailComponent(
                obj=state.obj,
                vertex_indices=vertices,
                edge_indices=edge_indices,
                anchor_indices=vertices & state.anchors,
                world_points=state.world_points,
            )
        )
    return components


def _group_targets(states: list[_MeshState], props) -> list[_MoveGroup]:
    groups: list[_MoveGroup] = []
    anchor_keys = {(state.obj.data.as_pointer(), index) for state in states for index in state.anchors}
    for state in states:
        targets = {
            index for index in state.selected
            if (state.obj.data.as_pointer(), index) not in anchor_keys
        }
        if not targets:
            continue
        if props.align_grouping == 'PER_ISLAND' or props.align_relationship == 'PAIRED_RAIL':
            groups.extend(_MoveGroup(state=state, target_indices=group) for group in _selected_components(state, targets))
        else:
            groups.append(_MoveGroup(state=state, target_indices=targets))
    if not groups:
        raise GuidedAlignError('Select one or more subordinate vertices, edges, or faces before Analyze or Align.')
    return groups


def _attach_rails(states: list[_MeshState], groups: list[_MoveGroup], paired: bool) -> None:
    by_object = {state.obj: _rail_components(state) for state in states}
    if not any(by_object.values()):
        raise GuidedAlignError('No captured rails were found. Select the slide edges and press Capture Rails.')

    for group in groups:
        candidates = [
            component for component in by_object.get(group.state.obj, [])
            if component.vertex_indices & group.target_indices
        ]
        if len(candidates) != 1:
            raise GuidedAlignError(
                f'{group.state.obj.name}: each subordinate island must touch exactly one captured rail; found {len(candidates)}.'
            )
        component = candidates[0]
        if paired and len(component.anchor_indices) != 1:
            raise GuidedAlignError(
                f'{group.state.obj.name}: paired rails require exactly one captured anchor vertex per rail; found {len(component.anchor_indices)}.'
            )
        group.rail_component = component


def _frame_and_mask(props, anchor_reference: Vector):
    mask = (bool(props.align_match_x), bool(props.align_match_y), bool(props.align_match_z))
    if props.align_frame == 'WORLD':
        if not any(mask):
            raise GuidedAlignError('Enable at least one Match axis.')
        frame = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        reference = tuple(anchor_reference)
        return frame, reference, mask

    if not props.align_guide_start_set or not props.align_guide_end_set:
        raise GuidedAlignError('Capture or enter both Custom Guide points first.')
    try:
        frame = build_frame(tuple(props.align_guide_start), tuple(props.align_guide_end))
    except ValueError as exc:
        raise GuidedAlignError(str(exc)) from exc
    if props.align_custom_target == 'GUIDE_LINE':
        reference = (0.0, 0.0, 0.0)
        mask = (False, True, True)
    else:
        if not any(mask):
            raise GuidedAlignError('Enable at least one Custom Frame Match axis.')
        reference = to_frame(tuple(anchor_reference), frame)
    return frame, reference, mask


def _group_anchor(group: _MoveGroup, global_anchor: Vector, paired: bool) -> Vector:
    if not paired:
        return global_anchor
    component = group.rail_component
    if component is None or len(component.anchor_indices) != 1:
        raise GuidedAlignError('Paired rail mapping is incomplete.')
    index = next(iter(component.anchor_indices))
    return component.world_points[index].copy()


def _target_reference(group: _MoveGroup, preserve_shape: bool) -> Vector:
    state = group.state
    if preserve_shape and group.rail_component is not None:
        handles = group.target_indices & group.rail_component.vertex_indices
        if handles:
            return Vector(median_point(tuple(tuple(state.world_points[index]) for index in handles)))
    return Vector(median_point(tuple(tuple(state.world_points[index]) for index in group.target_indices)))


def _rail_direction_and_extent(group: _MoveGroup, target_reference: Vector, tolerance: float):
    component = group.rail_component
    if component is None:
        raise GuidedAlignError('Missing rail component.')
    rail_points = [component.world_points[index] for index in component.vertex_indices]
    anchors = [component.world_points[index] for index in component.anchor_indices]
    if anchors:
        direction = anchors[0] - target_reference
    else:
        # Use the most distant rail point to establish a stable line direction.
        farthest = max(rail_points, key=lambda point: (point - target_reference).length_squared)
        direction = farthest - target_reference
    if direction.length <= _EPS:
        raise GuidedAlignError('Captured rail has zero usable length.')
    direction.normalize()
    minimum, maximum, deviation = line_extent(
        tuple(tuple(point) for point in rail_points),
        tuple(target_reference),
        tuple(direction),
    )
    if deviation > tolerance:
        raise GuidedAlignError(
            f'Captured rail is not straight enough for safe sliding (deviation {deviation:.6g}).'
        )
    return direction, minimum, maximum


def _planned_world_positions(context, props):
    states = _collect_states(context)
    if not states:
        raise GuidedAlignError('Enter Mesh Edit Mode on at least one mesh object.')

    captured_count = sum(len(state.anchors) for state in states)
    if props.align_anchor_count and captured_count != props.align_anchor_count:
        raise GuidedAlignError(
            f'Captured anchor markers changed after topology edits ({captured_count} found; {props.align_anchor_count} expected). Recapture Anchor.'
        )
    rail_count = sum(len(state.rail_edges) for state in states)
    if props.align_move_mode == 'SLIDE_RAIL' and props.align_rail_edge_count and rail_count != props.align_rail_edge_count:
        raise GuidedAlignError(
            f'Captured rail markers changed after topology edits ({rail_count} found; {props.align_rail_edge_count} expected). Recapture Rails.'
        )

    global_anchor = _anchor_reference(states, props.align_reference_mode)
    groups = _group_targets(states, props)
    paired = props.align_relationship == 'PAIRED_RAIL'
    if props.align_move_mode == 'SLIDE_RAIL' or paired:
        _attach_rails(states, groups, paired)

    for group in groups:
        if not _matrix_is_invertible(group.state.obj):
            raise GuidedAlignError(f'{group.state.obj.name} has a non-invertible object transform.')
        keys = getattr(group.state.obj.data, 'shape_keys', None)
        if keys is not None and len(keys.key_blocks) > 1:
            raise GuidedAlignError(f'{group.state.obj.name} has multiple shape keys; alignment is blocked to avoid corrupting them.')
        if props.align_respect_locks:
            locked = _locked_indices(group.state.obj, only_enabled=True)
            conflict = locked & group.target_indices
            if conflict:
                raise GuidedAlignError(
                    f'{group.state.obj.name}: {len(conflict)} subordinate vertices are protected by enabled Vertex Locks.'
                )

    plan: dict[tuple[bpy.types.Object, int], Vector] = {}
    moved_groups = 0
    for group in groups:
        anchor = _group_anchor(group, global_anchor, paired)
        frame, reference_frame, mask = _frame_and_mask(props, anchor)
        inverse = group.state.obj.matrix_world.inverted()

        if props.align_preserve_shape:
            target_reference = _target_reference(group, True)
            target_frame = to_frame(tuple(target_reference), frame)
            if props.align_move_mode == 'SLIDE_RAIL':
                direction, minimum, maximum = _rail_direction_and_extent(
                    group, target_reference, props.align_rail_straight_tolerance
                )
                direction_frame = to_frame(tuple(target_reference + direction), frame)
                direction_frame = Vector(direction_frame) - Vector(target_frame)
                try:
                    parameter = solve_slide_parameter(
                        target_frame,
                        direction_frame,
                        reference_frame,
                        mask,
                        tolerance=props.align_solve_tolerance,
                    )
                except ValueError as exc:
                    raise GuidedAlignError(str(exc)) from exc
                world_delta = direction * parameter
                if props.align_clamp_to_rail:
                    projected = parameter
                    if projected < minimum - props.align_solve_tolerance or projected > maximum + props.align_solve_tolerance:
                        raise GuidedAlignError('Required alignment point lies outside the captured rail extent.')
            else:
                delta_frame = component_delta(target_frame, reference_frame, mask)
                world_target = Vector(from_frame(tuple(Vector(target_frame) + Vector(delta_frame)), frame))
                world_delta = world_target - target_reference

            for index in group.target_indices:
                world = group.state.world_points[index] + world_delta
                plan[(group.state.obj, index)] = inverse @ world
            moved_groups += 1
            continue

        for index in group.target_indices:
            world = group.state.world_points[index]
            point_frame = to_frame(tuple(world), frame)
            if props.align_move_mode == 'SLIDE_RAIL':
                direction, minimum, maximum = _rail_direction_and_extent(
                    group, world, props.align_rail_straight_tolerance
                )
                direction_frame = Vector(to_frame(tuple(world + direction), frame)) - Vector(point_frame)
                try:
                    parameter = solve_slide_parameter(
                        point_frame,
                        tuple(direction_frame),
                        reference_frame,
                        mask,
                        tolerance=props.align_solve_tolerance,
                    )
                except ValueError as exc:
                    raise GuidedAlignError(str(exc)) from exc
                if props.align_clamp_to_rail and (
                    parameter < minimum - props.align_solve_tolerance
                    or parameter > maximum + props.align_solve_tolerance
                ):
                    raise GuidedAlignError('Required alignment point lies outside the captured rail extent.')
                new_world = world + direction * parameter
            else:
                new_frame = match_components(point_frame, reference_frame, mask)
                new_world = Vector(from_frame(new_frame, frame))
            plan[(group.state.obj, index)] = inverse @ new_world
        moved_groups += 1

    return states, plan, moved_groups


def _capture_reference_point(context, props) -> Vector:
    objects = _edit_mesh_objects(context)
    if context.mode != 'EDIT_MESH' or not objects:
        raise GuidedAlignError('Enter Mesh Edit Mode before capturing a guide point.')
    selected: list[Vector] = []
    active: list[Vector] = []
    for obj in objects:
        bm = bmesh.from_edit_mesh(obj.data)
        indices = _selected_vertices(bm)
        selected.extend(_world_point(obj, bm.verts[index].co) for index in indices)
        active_indices = _active_selected_vertex_indices(bm)
        active.extend(_world_point(obj, bm.verts[index].co) for index in active_indices)
    if not selected:
        raise GuidedAlignError('Select a vertex, edge, or face first.')
    values = active if props.align_reference_mode == 'ACTIVE' and active else selected
    return Vector(median_point(tuple(tuple(value) for value in values)))


class MESH_OT_wt_guided_align_capture_anchor(Operator):
    bl_idname = 'mesh.wt_guided_align_capture_anchor'
    bl_label = 'Capture Align Anchor'
    bl_description = 'Store the selected vertex, edge, or face vertices as the parent anchor; the active element is retained for Active Element reference mode'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        try:
            total, active_total = _write_vertex_capture(context, _ANCHOR_LAYER, active_value=True)
        except GuidedAlignError as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        props = context.scene.witch_tools
        props.align_anchor_count = total
        props.align_anchor_active_count = active_total
        props.align_last_report = f'Captured {total} anchor vertices.'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


class MESH_OT_wt_guided_align_capture_rails(Operator):
    bl_idname = 'mesh.wt_guided_align_capture_rails'
    bl_label = 'Capture Slide Rails'
    bl_description = 'Store the selected edges as movement rails; targets can then slide along those edges while matching the requested coordinates'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        try:
            total = _write_edge_capture(context, _RAIL_LAYER)
        except GuidedAlignError as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        props = context.scene.witch_tools
        props.align_rail_edge_count = total
        props.align_last_report = f'Captured {total} slide-rail edges.'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


class MESH_OT_wt_guided_align_capture_guide_point(Operator):
    bl_idname = 'mesh.wt_guided_align_capture_guide_point'
    bl_label = 'Capture Custom Guide Point'
    bl_description = 'Copy the active or median selected geometry position into the Custom Guide start or end point'
    bl_options = {'REGISTER'}

    point: bpy.props.EnumProperty(
        items=[('START', 'Start', ''), ('END', 'End', '')],
        default='START',
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        props = context.scene.witch_tools
        try:
            point = _capture_reference_point(context, props)
        except GuidedAlignError as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        if self.point == 'START':
            props.align_guide_start = point
            props.align_guide_start_set = True
        else:
            props.align_guide_end = point
            props.align_guide_end_set = True
        props.align_last_report = f'Custom Guide {self.point.title()} captured.'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


class MESH_OT_wt_guided_align_copy_anchor_to_guide_start(Operator):
    bl_idname = 'mesh.wt_guided_align_copy_anchor_to_guide_start'
    bl_label = 'Copy Anchor to Guide Start'
    bl_description = 'Set Custom Guide Start to the captured anchor reference point'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.witch_tools
        try:
            anchor = _anchor_reference(_collect_states(context), props.align_reference_mode)
        except GuidedAlignError as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        props.align_guide_start = anchor
        props.align_guide_start_set = True
        props.align_last_report = 'Copied Anchor to Custom Guide Start.'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


class MESH_OT_wt_guided_align_clear(Operator):
    bl_idname = 'mesh.wt_guided_align_clear'
    bl_label = 'Clear Guided Align Captures'
    bl_description = 'Clear captured anchors, rails, guide points, and diagnostic counts without moving geometry'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _remove_marker_everywhere(_ANCHOR_LAYER, 'POINT')
        _remove_marker_everywhere(_RAIL_LAYER, 'EDGE')
        props = context.scene.witch_tools
        props.align_anchor_count = 0
        props.align_anchor_active_count = 0
        props.align_rail_edge_count = 0
        props.align_guide_start_set = False
        props.align_guide_end_set = False
        props.align_last_report = 'Guided Align captures cleared.'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


class MESH_OT_wt_guided_align_analyze(Operator):
    bl_idname = 'mesh.wt_guided_align_analyze'
    bl_label = 'Analyze Guided Align'
    bl_description = 'Validate anchors, targets, axis constraints, rails, locks, shape keys, and object transforms without moving geometry'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        props = context.scene.witch_tools
        try:
            _states, plan, groups = _planned_world_positions(context, props)
        except GuidedAlignError as exc:
            props.align_last_report = f'Blocked: {exc}'
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        props.align_last_report = f'Ready: {len(plan)} vertices in {groups} group(s). No geometry moved.'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


class MESH_OT_wt_guided_align_apply(Operator):
    bl_idname = 'mesh.wt_guided_align_apply'
    bl_label = 'Align Selection'
    bl_description = 'Align the selected subordinate vertices, edges, or faces to the captured anchor using the configured frame and movement constraints'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        props = context.scene.witch_tools
        try:
            states, plan, groups = _planned_world_positions(context, props)
        except GuidedAlignError as exc:
            props.align_last_report = f'Blocked: {exc}'
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}

        by_object: dict[bpy.types.Object, list[tuple[int, Vector]]] = {}
        originals: dict[tuple[bpy.types.Object, int], Vector] = {}
        for (obj, index), local in plan.items():
            by_object.setdefault(obj, []).append((index, local))
        for state in states:
            for index, _local in by_object.get(state.obj, []):
                originals[(state.obj, index)] = state.bm.verts[index].co.copy()

        try:
            for state in states:
                changes = by_object.get(state.obj)
                if not changes:
                    continue
                for index, local in changes:
                    state.bm.verts[index].co = local
                state.bm.normal_update()
            for state in states:
                if by_object.get(state.obj):
                    bmesh.update_edit_mesh(state.obj.data, loop_triangles=False, destructive=False)
        except Exception as exc:
            for state in states:
                for index, _local in by_object.get(state.obj, []):
                    original = originals.get((state.obj, index))
                    if original is not None:
                        state.bm.verts[index].co = original
                if by_object.get(state.obj):
                    try:
                        state.bm.normal_update()
                        bmesh.update_edit_mesh(state.obj.data, loop_triangles=False, destructive=False)
                    except Exception:
                        pass
            props.align_last_report = f'Blocked: unexpected apply failure; geometry rollback attempted: {exc}'
            self.report({'ERROR'}, props.align_last_report)
            return {'CANCELLED'}

        props.align_last_report = f'Aligned {len(plan)} vertices in {groups} group(s).'
        self.report({'INFO'}, props.align_last_report)
        return {'FINISHED'}


CLASSES = (
    MESH_OT_wt_guided_align_capture_anchor,
    MESH_OT_wt_guided_align_capture_rails,
    MESH_OT_wt_guided_align_capture_guide_point,
    MESH_OT_wt_guided_align_copy_anchor_to_guide_start,
    MESH_OT_wt_guided_align_clear,
    MESH_OT_wt_guided_align_analyze,
    MESH_OT_wt_guided_align_apply,
)
