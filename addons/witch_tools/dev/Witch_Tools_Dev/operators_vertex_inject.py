import math

import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector

from . import operators_vertex_locks
from .operators_curvature_sync import _restore_lock_references, _snapshot_lock_references


_EPSILON = 1.0e-9


class VertexInjectError(RuntimeError):
    pass


def _prepare_bmesh(obj, source_bm=None):
    bm = source_bm if source_bm is not None else bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    return bm


def _ordered_selected_vertices(bm):
    selected = [vert for vert in bm.verts if vert.select]
    if len(selected) != 3:
        raise VertexInjectError('Select exactly three vertices in order: A, then B, then C')

    history = []
    for element in bm.select_history:
        if isinstance(element, bmesh.types.BMVert) and element.select and element.is_valid:
            if element in history:
                history.remove(element)
            history.append(element)

    if len(history) < 3:
        raise VertexInjectError(
            'Selection order is unavailable. Deselect everything, then click A, B, and C individually; C must be active last'
        )
    ordered = history[-3:]
    if set(ordered) != set(selected):
        raise VertexInjectError(
            'Selection history does not match the three selected vertices. Deselect and click A, B, C individually'
        )
    return tuple(ordered)


def _other_vert(edge, vert):
    return edge.verts[1] if edge.verts[0] is vert else edge.verts[0]


def _normalized(vector, label):
    if vector.length <= _EPSILON:
        raise VertexInjectError(f'{label} has zero length')
    return vector.normalized()


def _choose_continuation(current, incoming_edge, incoming_direction, blocked_edges):
    candidates = []
    for edge in current.link_edges:
        if edge is incoming_edge or edge in blocked_edges:
            continue
        other = _other_vert(edge, current)
        direction = other.co - current.co
        if direction.length <= _EPSILON:
            continue
        score = incoming_direction.dot(direction.normalized())
        if score > 0.15:
            candidates.append((score, edge, other, direction.normalized()))

    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    best = candidates[0]
    if best[0] < 0.45:
        raise VertexInjectError('Target chain bends too sharply or cannot be followed reliably')
    if len(candidates) > 1 and candidates[1][0] >= best[0] - 0.035:
        raise VertexInjectError('Target chain continuation is ambiguous at a topology fork')
    return best[1], best[2], best[3]


def _trace_target_chain(a_vert, source_edge, row_direction, max_steps=2048):
    blocked = {source_edge}
    start = _choose_continuation(a_vert, None, row_direction, blocked)
    if start is None:
        raise VertexInjectError('No target chain leaves A in the B-to-C row direction')

    edge, next_vert, direction = start
    segments = [(a_vert, next_vert, edge)]
    visited_edges = {edge, source_edge}
    current = next_vert
    incoming = edge

    for _step in range(max_steps - 1):
        next_data = _choose_continuation(current, incoming, direction, visited_edges)
        if next_data is None:
            break
        next_edge, next_vert, next_direction = next_data
        if next_edge in visited_edges:
            break
        segments.append((current, next_vert, next_edge))
        visited_edges.add(next_edge)
        current = next_vert
        incoming = next_edge
        direction = next_direction
    else:
        raise VertexInjectError('Target chain traversal exceeded the safety limit')

    return segments


def _closest_point_on_segment(point, start, end):
    delta = end - start
    length_squared = delta.length_squared
    if length_squared <= _EPSILON:
        return start.copy(), 0.0, (point - start).length
    factor = (point - start).dot(delta) / length_squared
    clamped = max(0.0, min(1.0, factor))
    closest = start + delta * clamped
    return closest, clamped, (point - closest).length


def _resolve_target_location(segments, ideal, tolerance, merge_tolerance):
    best = None
    for start_vert, end_vert, edge in segments:
        closest, factor, distance = _closest_point_on_segment(ideal, start_vert.co, end_vert.co)
        candidate = (distance, start_vert, end_vert, edge, closest, factor)
        if best is None or distance < best[0]:
            best = candidate

    if best is None or best[0] > tolerance:
        distance = best[0] if best else float('inf')
        raise VertexInjectError(
            f'Ideal vertex is {distance:.6g} units from the inferred target chain, beyond tolerance {tolerance:.6g}'
        )

    distance, start_vert, end_vert, edge, closest, factor = best
    if (closest - start_vert.co).length <= merge_tolerance:
        return start_vert, None, None, 0.0, distance
    if (closest - end_vert.co).length <= merge_tolerance:
        return end_vert, None, None, 1.0, distance
    if factor <= _EPSILON or factor >= 1.0 - _EPSILON:
        return start_vert if factor <= 0.5 else end_vert, None, None, factor, distance
    return None, edge, start_vert, factor, distance


def _validate_face_connection(c_vert, d_vert):
    if c_vert is d_vert:
        raise VertexInjectError('Calculated D resolves to C; no new column can be created')
    existing = c_vert.link_edges and next(
        (edge for edge in c_vert.link_edges if d_vert in edge.verts),
        None,
    )
    if existing is not None:
        return existing, False
    common_faces = set(c_vert.link_faces) & set(d_vert.link_faces)
    if not common_faces:
        raise VertexInjectError('C and the calculated D do not share a face; Connect & Split cannot be completed safely')
    if len(common_faces) > 1:
        raise VertexInjectError('C and D share multiple faces; the requested face split is ambiguous')
    return None, True


def _perform_inject(bm, a_index, b_index, c_index, connect_split, tolerance_ratio, merge_ratio):
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    for index in (a_index, b_index, c_index):
        if index < 0 or index >= len(bm.verts):
            raise VertexInjectError('Selection indices became invalid during preflight')

    a_vert = bm.verts[a_index]
    b_vert = bm.verts[b_index]
    c_vert = bm.verts[c_index]
    source_edge = bm.edges.get((a_vert, b_vert))
    row_edge = bm.edges.get((b_vert, c_vert))
    if source_edge is None:
        raise VertexInjectError('A and B must share the source edge')
    if row_edge is None:
        raise VertexInjectError('B and C must share the corresponding row edge')

    source_vector = a_vert.co - b_vert.co
    source_length = source_vector.length
    if source_length <= _EPSILON:
        raise VertexInjectError('The A-B source edge has zero length')
    row_direction = _normalized(c_vert.co - b_vert.co, 'The B-C row edge')
    ideal = c_vert.co + source_vector

    segments = _trace_target_chain(a_vert, source_edge, row_direction)
    tolerance = max(source_length * tolerance_ratio, 1.0e-7)
    merge_tolerance = max(source_length * merge_ratio, 1.0e-8)
    existing_vert, target_edge, split_start, factor, projection_distance = _resolve_target_location(
        segments,
        ideal,
        tolerance,
        merge_tolerance,
    )

    injected = False
    if existing_vert is not None:
        d_vert = existing_vert
    else:
        # edge_split factor is measured from the path-oriented start vertex returned by preflight.
        if factor <= 0.0 or factor >= 1.0:
            raise VertexInjectError('Calculated split factor lies outside the target edge')
        _new_edge, d_vert = bmesh.utils.edge_split(target_edge, split_start, factor)
        # edge_split positions D on the actual target edge. The ideal point is used only to choose/project the split.
        injected = True

    connected = False
    if connect_split:
        existing_edge, needs_connection = _validate_face_connection(c_vert, d_vert)
        if needs_connection:
            result = bmesh.ops.connect_verts(bm, verts=[c_vert, d_vert], check_degenerate=True)
            new_edges = [edge for edge in result.get('edges', ()) if edge.is_valid]
            if not new_edges and bm.edges.get((c_vert, d_vert)) is None:
                raise VertexInjectError('Blender could not split the shared face between C and D')
            connected = True

    bm.normal_update()
    for face in bm.faces:
        if face.is_valid and face.calc_area() <= 1.0e-16:
            raise VertexInjectError('The operation would create a zero-area face')

    for vert in bm.verts:
        vert.select_set(False)
    c_vert.select_set(True)
    d_vert.select_set(True)
    bm.select_history.clear()
    bm.select_history.add(c_vert)
    bm.select_history.add(d_vert)
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()

    return {
        'd_index': d_vert.index,
        'injected': injected,
        'connected': connected,
        'projection_distance': projection_distance,
    }


class WT_OT_vertex_inject_auto_aligned(Operator):
    bl_idname = 'mesh.wt_vertex_inject_auto_aligned'
    bl_label = 'Inject Auto-Aligned Vertex'
    bl_description = (
        'Select A, then B, then C. Copies the A-B relation from C onto the inferred parallel target chain, '
        'splits the target edge, and optionally connects C to the new vertex through the shared face'
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
            self.report({'ERROR'}, 'Enter Edit Mode on one mesh object')
            return {'CANCELLED'}
        if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks) > 1:
            self.report({'ERROR'}, 'Vertex injection is disabled on meshes with shape keys')
            return {'CANCELLED'}

        props = context.scene.witch_tools
        bm = _prepare_bmesh(obj)
        try:
            a_vert, b_vert, c_vert = _ordered_selected_vertices(bm)
            indices = (a_vert.index, b_vert.index, c_vert.index)
        except VertexInjectError as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}

        copy_bm = bm.copy()
        old_guard_suspended = operators_vertex_locks._GUARD_SUSPENDED
        operators_vertex_locks._GUARD_SUSPENDED = True
        try:
            _prepare_bmesh(obj, copy_bm)
            _perform_inject(
                copy_bm,
                *indices,
                props.vertex_inject_connect_split,
                props.vertex_inject_tolerance_ratio,
                props.vertex_inject_merge_ratio,
            )
            copy_bm.free()
            copy_bm = None

            lock_snapshot = _snapshot_lock_references(obj, bm)
            result = _perform_inject(
                bm,
                *indices,
                props.vertex_inject_connect_split,
                props.vertex_inject_tolerance_ratio,
                props.vertex_inject_merge_ratio,
            )
            _restore_lock_references(obj, bm, lock_snapshot)
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=result['injected'] or result['connected'])

            action = 'Injected new D vertex' if result['injected'] else 'Used existing D vertex'
            if result['connected']:
                action += ' and split the C-D face column'
            self.report(
                {'INFO'},
                f"{action}; target projection offset {result['projection_distance']:.6g}",
            )
            return {'FINISHED'}
        except VertexInjectError as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            self.report({'ERROR'}, f'Vertex Inject failed: {error}')
            return {'CANCELLED'}
        finally:
            if copy_bm is not None:
                try:
                    copy_bm.free()
                except Exception:
                    pass
            operators_vertex_locks._GUARD_SUSPENDED = old_guard_suspended


CLASSES = (WT_OT_vertex_inject_auto_aligned,)
