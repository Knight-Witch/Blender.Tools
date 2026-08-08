import bpy
import bmesh
from bpy.types import Operator

from . import operators_planar_edit, operators_vertex_inject, operators_vertex_locks
from . import precision_edit_common as precision_edit
from .operators_curvature_sync import _restore_lock_references, _snapshot_lock_references


_EPSILON = 1.0e-9


class EdgeDoctorError(RuntimeError):
    pass


def _selected_l_edges(bm):
    edges = [edge for edge in bm.edges if edge.select]
    if len(edges) != 2:
        return None
    shared = set(edges[0].verts) & set(edges[1].verts)
    if len(shared) != 1:
        raise EdgeDoctorError('Two-edge mode requires exactly two selected edges sharing one corner vertex (an L).')
    corner = next(iter(shared))
    a = edges[0].other_vert(corner)
    c = edges[1].other_vert(corner)
    if a is c:
        raise EdgeDoctorError('The selected L edges do not define two different legs.')
    return a, corner, c


def _find_existing_d(bm, desired, excluded, tolerance):
    best = None
    for vert in bm.verts:
        if not vert.is_valid or vert in excluded:
            continue
        distance = (vert.co - desired).length
        if distance <= tolerance and (best is None or distance < best[0]):
            best = (distance, vert)
    return best[1] if best is not None else None


def _perform_l_corner(bm, a_index, b_index, c_index, merge_ratio):
    bm.verts.ensure_lookup_table()
    for index in (a_index, b_index, c_index):
        if index < 0 or index >= len(bm.verts):
            raise EdgeDoctorError('The L-corner selection became invalid during preflight.')
    a = bm.verts[a_index]
    b = bm.verts[b_index]
    c = bm.verts[c_index]
    if bm.edges.get((a, b)) is None or bm.edges.get((b, c)) is None:
        raise EdgeDoctorError('The two selected L legs no longer share the expected corner.')

    ab = (a.co - b.co).length
    bc = (c.co - b.co).length
    if ab <= _EPSILON or bc <= _EPSILON:
        raise EdgeDoctorError('The selected L contains a zero-length edge.')

    desired = a.co + c.co - b.co
    tolerance = max(((ab + bc) * 0.5) * merge_ratio, 1.0e-8)
    d = _find_existing_d(bm, desired, {a, b, c}, tolerance)
    injected = False
    if d is None:
        d = bm.verts.new(desired)
        injected = True

    created_edges = []
    for start in (a, c):
        if start is d:
            raise EdgeDoctorError('The inferred missing corner collapses onto an existing L endpoint.')
        edge = bm.edges.get((start, d))
        if edge is None:
            try:
                edge = bm.edges.new((start, d))
            except ValueError:
                edge = bm.edges.get((start, d))
            if edge is None:
                raise EdgeDoctorError('Blender could not create one of the missing corner edges.')
            created_edges.append(edge)
        if (edge.verts[1].co - edge.verts[0].co).length <= 1.0e-12:
            raise EdgeDoctorError('The repair would create a zero-length edge.')

    for vert in bm.verts:
        vert.select_set(False)
    for edge in bm.edges:
        edge.select_set(False)
    a.select_set(True)
    c.select_set(True)
    d.select_set(True)
    for edge in created_edges:
        edge.select_set(True)
    bm.select_history.clear()
    bm.select_history.add(d)
    bm.normal_update()
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    return {'d_index': d.index, 'injected': injected, 'edge_count': len(created_edges)}


class WT_OT_edge_doctor_missing_inject(Operator):
    bl_idname = 'mesh.wt_edge_doctor_missing_inject'
    bl_label = 'Repair Missing Vertex / Edge'
    bl_description = (
        'Repair a missing regular-grid corner in either of two ways. '
        'A/B/C mode: select A then B then C; copies the A-B relation from C onto the inferred parallel target chain. '
        'L mode: select exactly two edges that share one corner; creates/reuses the inferred fourth parallelogram corner and connects both missing legs.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        obj = context.active_object
        if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks) > 1:
            self.report({'ERROR'}, 'Edge Doctor injection is disabled on meshes with multiple shape keys.')
            return {'CANCELLED'}

        props = context.scene.witch_tools
        bm = operators_vertex_inject._prepare_bmesh(obj)
        old_vertex_guard = operators_vertex_locks._GUARD_SUSPENDED
        old_planar_guard = operators_planar_edit._GUARD_SUSPENDED
        operators_vertex_locks._GUARD_SUSPENDED = True
        operators_planar_edit._GUARD_SUSPENDED = True
        copy_bm = None
        try:
            l_data = _selected_l_edges(bm)
            if l_data is not None:
                a, b, c = l_data
                indices = (a.index, b.index, c.index)
                copy_bm = bm.copy()
                copy_bm.verts.ensure_lookup_table()
                _perform_l_corner(copy_bm, *indices, props.vertex_inject_merge_ratio)
                copy_bm.free()
                copy_bm = None

                lock_snapshot = _snapshot_lock_references(obj, bm)
                result = _perform_l_corner(bm, *indices, props.vertex_inject_merge_ratio)
                if result['injected']:
                    bm.verts.ensure_lookup_table()
                    if 0 <= result['d_index'] < len(bm.verts):
                        precision_edit.clear_planar_lock_on_vertices(bm, [bm.verts[result['d_index']]])
                _restore_lock_references(obj, bm, lock_snapshot)
                bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)
                action = 'Injected missing D corner' if result['injected'] else 'Reused existing D corner'
                self.report({'INFO'}, f"{action}; created {result['edge_count']} missing edge(s).")
                return {'FINISHED'}

            a, b, c = operators_vertex_inject._ordered_selected_vertices(bm)
            indices = (a.index, b.index, c.index)
            copy_bm = bm.copy()
            operators_vertex_inject._prepare_bmesh(obj, copy_bm)
            operators_vertex_inject._perform_inject(
                copy_bm,
                *indices,
                props.vertex_inject_connect_split,
                props.vertex_inject_tolerance_ratio,
                props.vertex_inject_merge_ratio,
            )
            copy_bm.free()
            copy_bm = None

            lock_snapshot = _snapshot_lock_references(obj, bm)
            result = operators_vertex_inject._perform_inject(
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
            self.report({'INFO'}, f"{action}; target projection offset {result['projection_distance']:.6g}")
            return {'FINISHED'}
        except (EdgeDoctorError, operators_vertex_inject.VertexInjectError) as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            self.report({'ERROR'}, f'Edge Doctor failed: {error}')
            return {'CANCELLED'}
        finally:
            if copy_bm is not None:
                try:
                    copy_bm.free()
                except Exception:
                    pass
            operators_vertex_locks._GUARD_SUSPENDED = old_vertex_guard
            operators_planar_edit._GUARD_SUSPENDED = old_planar_guard


CLASSES = (WT_OT_edge_doctor_missing_inject,)
