import json
import math
from dataclasses import dataclass

import bpy
import bmesh
from bpy.props import EnumProperty
from bpy.types import Operator
from mathutils import Vector

from . import operators_vertex_locks


_ANCHOR_KEYS = {
    'A': 'wt_curvature_sync_anchor_a',
    'M': 'wt_curvature_sync_anchor_m',
    'Z': 'wt_curvature_sync_anchor_z',
}
_EPSILON = 1.0e-9


class CurvatureSyncError(RuntimeError):
    pass


@dataclass
class ChainData:
    obj: object
    bm: object
    verts: list
    edges: list
    middle_index: int
    left_segments: int
    right_segments: int
    target_points_world: list = None
    slot_verts: dict = None


def _edit_mesh_objects(context):
    objects = [obj for obj in getattr(context, 'objects_in_mode_unique_data', ()) if obj and obj.type == 'MESH']
    if not objects:
        obj = getattr(context, 'active_object', None)
        if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            objects = [obj]
    return objects


def _prepare_bmesh(obj, source_bm=None):
    bm = source_bm if source_bm is not None else bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    return bm


def _read_anchor_indices(obj, anchor_type):
    raw = obj.get(_ANCHOR_KEYS[anchor_type], '')
    if not raw:
        return set()
    try:
        values = json.loads(raw)
    except Exception:
        return set()
    result = set()
    for value in values if isinstance(values, list) else ():
        try:
            result.add(int(value))
        except Exception:
            pass
    return result


def _write_anchor_indices(obj, anchor_type, indices):
    obj[_ANCHOR_KEYS[anchor_type]] = json.dumps(sorted({int(index) for index in indices}), separators=(',', ':'))


def _selected_vertex_indices(bm):
    return {vert.index for vert in bm.verts if vert.select}


def _selected_edge_components(bm):
    selected_edges = {edge for edge in bm.edges if edge.select}
    if not selected_edges:
        return []

    components = []
    remaining = set(selected_edges)
    while remaining:
        seed = remaining.pop()
        edges = {seed}
        verts = set(seed.verts)
        stack = list(seed.verts)
        while stack:
            vert = stack.pop()
            for edge in vert.link_edges:
                if edge not in selected_edges or edge in edges:
                    continue
                edges.add(edge)
                remaining.discard(edge)
                for linked in edge.verts:
                    if linked not in verts:
                        verts.add(linked)
                        stack.append(linked)
        components.append((verts, edges))
    return components


def _order_chain(component_verts, component_edges, a_vert, z_vert):
    adjacency = {vert: [] for vert in component_verts}
    for edge in component_edges:
        v0, v1 = edge.verts
        adjacency[v0].append((v1, edge))
        adjacency[v1].append((v0, edge))

    endpoints = [vert for vert, links in adjacency.items() if len(links) == 1]
    branches = [vert for vert, links in adjacency.items() if len(links) > 2]
    isolated = [vert for vert, links in adjacency.items() if len(links) == 0]
    if branches or isolated or len(endpoints) != 2:
        raise CurvatureSyncError('Each selected curve must be one open, non-branching edge chain')
    if a_vert not in endpoints or z_vert not in endpoints or a_vert is z_vert:
        raise CurvatureSyncError('A and Z must be the two endpoints of each selected curve chain')

    ordered_verts = [a_vert]
    ordered_edges = []
    previous = None
    current = a_vert
    visited = {a_vert}
    while current is not z_vert:
        candidates = [(vert, edge) for vert, edge in adjacency[current] if vert is not previous]
        if len(candidates) != 1:
            raise CurvatureSyncError('Selected curve traversal became ambiguous')
        next_vert, edge = candidates[0]
        if next_vert in visited and next_vert is not z_vert:
            raise CurvatureSyncError('Selected curve contains a cycle')
        ordered_edges.append(edge)
        ordered_verts.append(next_vert)
        visited.add(next_vert)
        previous, current = current, next_vert
        if len(ordered_edges) > len(component_edges):
            raise CurvatureSyncError('Selected curve traversal exceeded its edge count')

    if len(ordered_edges) != len(component_edges):
        raise CurvatureSyncError('Selected edges contain disconnected or unused topology')
    return ordered_verts, ordered_edges


def _build_chains_for_object(obj, bm):
    anchors = {key: _read_anchor_indices(obj, key) for key in ('A', 'M', 'Z')}
    for key, indices in anchors.items():
        if not indices:
            raise CurvatureSyncError(f'Object "{obj.name}" has no captured {key} anchors')

    chains = []
    used_anchors = {key: set() for key in anchors}
    for component_verts, component_edges in _selected_edge_components(bm):
        matches = {}
        for key, indices in anchors.items():
            found = [vert for vert in component_verts if vert.index in indices]
            if len(found) != 1:
                raise CurvatureSyncError(
                    f'Each selected chain on "{obj.name}" must contain exactly one captured {key} anchor'
                )
            matches[key] = found[0]
            used_anchors[key].add(found[0].index)

        ordered_verts, ordered_edges = _order_chain(
            component_verts,
            component_edges,
            matches['A'],
            matches['Z'],
        )
        try:
            middle_index = ordered_verts.index(matches['M'])
        except ValueError:
            raise CurvatureSyncError('The captured middle anchor is not on its selected chain')
        if middle_index <= 0 or middle_index >= len(ordered_verts) - 1:
            raise CurvatureSyncError('The middle anchor must lie strictly between A and Z')

        chains.append(
            ChainData(
                obj=obj,
                bm=bm,
                verts=ordered_verts,
                edges=ordered_edges,
                middle_index=middle_index,
                left_segments=middle_index,
                right_segments=len(ordered_verts) - 1 - middle_index,
            )
        )

    if not chains:
        raise CurvatureSyncError(f'Object "{obj.name}" has no selected curve edges')

    for key, indices in anchors.items():
        unused = indices - used_anchors[key]
        if unused:
            raise CurvatureSyncError(
                f'Object "{obj.name}" has captured {key} anchors outside the selected curve chains'
            )
    return chains


def _plane_indices(plane):
    if plane == 'XY':
        return 0, 1, 2
    if plane == 'XZ':
        return 0, 2, 1
    return 1, 2, 0


def _circumcircle(a, m, z):
    ax, ay = a
    mx, my = m
    zx, zy = z
    denominator = 2.0 * (ax * (my - zy) + mx * (zy - ay) + zx * (ay - my))
    if abs(denominator) <= _EPSILON:
        raise CurvatureSyncError('A, Middle, and Z are collinear; a circular curve cannot be determined')

    aa = ax * ax + ay * ay
    mm = mx * mx + my * my
    zz = zx * zx + zy * zy
    cx = (aa * (my - zy) + mm * (zy - ay) + zz * (ay - my)) / denominator
    cy = (aa * (zx - mx) + mm * (ax - zx) + zz * (mx - ax)) / denominator
    radius = math.hypot(ax - cx, ay - cy)
    if radius <= _EPSILON:
        raise CurvatureSyncError('The fitted curve radius is zero')
    return Vector((cx, cy)), radius


def _ccw_delta(start, end):
    return (end - start) % (2.0 * math.pi)


def _curve_targets(chain, target_segments, plane, snap_middle_axis=True):
    axis_u, axis_v, axis_w = _plane_indices(plane)
    matrix = chain.obj.matrix_world
    world = [matrix @ vert.co for vert in (chain.verts[0], chain.verts[chain.middle_index], chain.verts[-1])]
    a_world, m_world, z_world = world
    center, radius = _circumcircle(
        (a_world[axis_u], a_world[axis_v]),
        (m_world[axis_u], m_world[axis_v]),
        (z_world[axis_u], z_world[axis_v]),
    )

    angle_a = math.atan2(a_world[axis_v] - center.y, a_world[axis_u] - center.x)
    angle_m = math.atan2(m_world[axis_v] - center.y, m_world[axis_u] - center.x)
    angle_z = math.atan2(z_world[axis_v] - center.y, z_world[axis_u] - center.x)

    ccw_az = _ccw_delta(angle_a, angle_z)
    ccw_am = _ccw_delta(angle_a, angle_m)
    direction = 1.0 if ccw_am <= ccw_az + 1.0e-7 else -1.0

    def directed_delta(start, end):
        return _ccw_delta(start, end) if direction > 0.0 else _ccw_delta(end, start)

    if snap_middle_axis:
        # The captured Middle vertex establishes which side of the fitted circle is the
        # curved apex. Normalize it to the exact V-axis cardinal point of that circle.
        # For XY this produces the mathematically exact Y-axis middle column requested
        # by the collar workflow while A and Z remain fixed transition anchors.
        candidates = (math.pi * 0.5, -math.pi * 0.5)
        angle_m = min(
            candidates,
            key=lambda candidate: abs(
                math.atan2(math.sin(candidate - angle_m), math.cos(candidate - angle_m))
            ),
        )
        m_world = m_world.copy()
        m_world[axis_u] = center.x + math.cos(angle_m) * radius
        m_world[axis_v] = center.y + math.sin(angle_m) * radius

    delta_am = directed_delta(angle_a, angle_m)
    delta_mz = directed_delta(angle_m, angle_z)
    if delta_am <= _EPSILON or delta_mz <= _EPSILON:
        raise CurvatureSyncError('A, Middle, and Z do not define two non-zero arc spans')

    points = []
    total = target_segments * 2
    for slot in range(total + 1):
        if slot <= target_segments:
            t = slot / target_segments
            angle = angle_a + direction * delta_am * t
            axial = a_world[axis_w] + (m_world[axis_w] - a_world[axis_w]) * t
        else:
            t = (slot - target_segments) / target_segments
            angle = angle_m + direction * delta_mz * t
            axial = m_world[axis_w] + (z_world[axis_w] - m_world[axis_w]) * t

        point = Vector((0.0, 0.0, 0.0))
        point[axis_u] = center.x + math.cos(angle) * radius
        point[axis_v] = center.y + math.sin(angle) * radius
        point[axis_w] = axial
        points.append(point)

    # Exact anchor preservation avoids tiny floating-point drift.
    points[0] = a_world.copy()
    points[target_segments] = m_world.copy()
    points[-1] = z_world.copy()
    return points


def _distributed_slots(segment_count, target_segments):
    if segment_count > target_segments:
        raise CurvatureSyncError(
            f'A selected curve side has {segment_count} segments, exceeding the target {target_segments}'
        )
    slots = [0]
    previous = 0
    for index in range(1, segment_count):
        remaining = segment_count - index
        ideal = int(math.floor(index * target_segments / segment_count + 0.5))
        slot = max(previous + 1, ideal)
        slot = min(slot, target_segments - remaining)
        slots.append(slot)
        previous = slot
    slots.append(target_segments)
    return slots


def _assign_existing_slots(chain, target_segments):
    left_slots = _distributed_slots(chain.left_segments, target_segments)
    right_offsets = _distributed_slots(chain.right_segments, target_segments)
    mapping = {}
    for vert, slot in zip(chain.verts[: chain.middle_index + 1], left_slots):
        mapping[slot] = vert
    for vert, offset in zip(chain.verts[chain.middle_index :], right_offsets):
        mapping[target_segments + offset] = vert
    return mapping


def _snapshot_lock_references(obj, bm):
    groups = []
    anchors = {}
    bm.verts.ensure_lookup_table()
    for anchor_type in ('A', 'M', 'Z'):
        anchors[anchor_type] = [
            bm.verts[index]
            for index in _read_anchor_indices(obj, anchor_type)
            if 0 <= index < len(bm.verts)
        ]
    if not hasattr(obj, 'wvl_lock_groups'):
        return {'groups': groups, 'interior': [], 'anchors': anchors}
    for group in obj.wvl_lock_groups:
        refs = []
        for key, coordinate in operators_vertex_locks._parse_group(group).items():
            try:
                index = int(key)
            except Exception:
                continue
            if 0 <= index < len(bm.verts):
                refs.append((bm.verts[index], coordinate))
        groups.append((group, refs))

    interior = []
    raw = getattr(obj, 'wvl_last_edit_zone_indices', '')
    if raw:
        try:
            data = json.loads(raw)
            for index in data.get('interior', []):
                index = int(index)
                if 0 <= index < len(bm.verts):
                    interior.append(bm.verts[index])
        except Exception:
            interior = []
    return {'groups': groups, 'interior': interior, 'anchors': anchors}


def _restore_lock_references(obj, bm, snapshot):
    bm.verts.index_update()
    for group, refs in snapshot.get('groups', []):
        data = {}
        for vert, coordinate in refs:
            if vert.is_valid:
                data[str(vert.index)] = coordinate
        operators_vertex_locks._write_group(group, data)

    interior = [vert.index for vert in snapshot.get('interior', []) if vert.is_valid]
    if hasattr(obj, 'wvl_last_edit_zone_indices'):
        obj.wvl_last_edit_zone_indices = json.dumps({'interior': sorted(interior)}, separators=(',', ':'))

    for anchor_type, refs in snapshot.get('anchors', {}).items():
        _write_anchor_indices(obj, anchor_type, [vert.index for vert in refs if vert.is_valid])


def _locked_refs_for_chain(chain):
    if not hasattr(chain.obj, 'wvl_lock_groups'):
        return set()
    locked_indices = operators_vertex_locks._locked_indices(chain.obj, only_enabled=True)
    return {vert for vert in chain.verts if vert.index in locked_indices}


def _inject_missing_slots(chain, target_segments):
    slot_verts = _assign_existing_slots(chain, target_segments)
    assigned = sorted(slot_verts.items())
    for (left_slot, left_vert), (right_slot, right_vert) in zip(assigned, assigned[1:]):
        if right_slot - left_slot <= 1:
            continue
        current_vert = left_vert
        current_slot = left_slot
        for slot in range(left_slot + 1, right_slot):
            edge = chain.bm.edges.get((current_vert, right_vert))
            if edge is None:
                raise CurvatureSyncError('A required selected chain edge could not be found during injection')
            factor = (slot - current_slot) / (right_slot - current_slot)
            _new_edge, new_vert = bmesh.utils.edge_split(edge, current_vert, factor)
            new_vert.select = True
            slot_verts[slot] = new_vert
            current_vert = new_vert
            current_slot = slot
    chain.slot_verts = slot_verts
    return len(slot_verts) - len(chain.verts)


def _move_chain_to_targets(chain, target_segments, respect_locks, snap_middle_axis):
    locked = _locked_refs_for_chain(chain) if respect_locks else set()
    anchors = {chain.verts[0], chain.verts[-1]}
    middle_vert = chain.verts[chain.middle_index]
    middle_target_local = chain.obj.matrix_world.inverted_safe() @ chain.target_points_world[target_segments]
    if not snap_middle_axis or (middle_vert.co - middle_target_local).length_squared <= 1.0e-12:
        anchors.add(middle_vert)
    interior_locked = locked - anchors
    if interior_locked:
        raise CurvatureSyncError(
            f'Chain on "{chain.obj.name}" contains {len(interior_locked)} locked interior vertices; unlock them or exclude them from the repair span'
        )

    inverse = chain.obj.matrix_world.inverted_safe()
    moved = 0
    for slot, vert in chain.slot_verts.items():
        if vert in anchors or vert in locked:
            continue
        target_local = inverse @ chain.target_points_world[slot]
        if (vert.co - target_local).length_squared > 1.0e-16:
            vert.co = target_local
            moved += 1
    return moved


def _chain_face_set(chain):
    faces = set()
    for vert in chain.verts:
        faces.update(vert.link_faces)
    return faces


def _candidate_chain_pairs(chains):
    pairs = []
    face_sets = [_chain_face_set(chain) for chain in chains]
    for index, chain_a in enumerate(chains):
        for other_index in range(index + 1, len(chains)):
            chain_b = chains[other_index]
            if chain_a.obj is not chain_b.obj:
                continue
            shared_faces = face_sets[index] & face_sets[other_index]
            if shared_faces:
                pairs.append((chain_a, chain_b))
    return pairs




def _edge_has_nondefault_custom_data(bm, edge):
    """Return True when dissolving this edge would discard meaningful edge data."""
    layer_groups = (
        ('bool', False),
        ('int', 0),
        ('float', 0.0),
        ('string', b''),
        ('float_vector', None),
        ('color', None),
        ('float_color', None),
    )
    for group_name, zero in layer_groups:
        layers = getattr(bm.edges.layers, group_name, None)
        if layers is None:
            continue
        for layer_name in layers.keys():
            layer = layers.get(layer_name)
            try:
                value = edge[layer]
            except Exception:
                continue
            if zero is not None:
                if isinstance(value, (bytes, bytearray)):
                    if value:
                        return True
                elif isinstance(value, str):
                    if value:
                        return True
                elif isinstance(value, bool):
                    if value:
                        return True
                else:
                    try:
                        if abs(float(value)) > 1.0e-12:
                            return True
                    except Exception:
                        if value != zero:
                            return True
            else:
                try:
                    if any(abs(float(component)) > 1.0e-12 for component in value):
                        return True
                except Exception:
                    if value:
                        return True
    return False


def _collect_misaligned_column_edges(chains, pairs, target_segments):
    """Find safe interior cross-edges whose endpoints map to different lattice slots."""
    slot_by_chain = {}
    for chain in chains:
        slot_by_chain[id(chain)] = {
            vert: slot for slot, vert in _assign_existing_slots(chain, target_segments).items()
        }

    total_slot = target_segments * 2
    mismatched = set()
    for chain_a, chain_b in pairs:
        slots_a = slot_by_chain[id(chain_a)]
        slots_b = slot_by_chain[id(chain_b)]
        for vert_a, slot_a in slots_a.items():
            for edge in vert_a.link_edges:
                vert_b = edge.other_vert(vert_a)
                if vert_b not in slots_b:
                    continue
                slot_b = slots_b[vert_b]
                if slot_a == slot_b:
                    continue
                if slot_a in (0, total_slot) or slot_b in (0, total_slot):
                    raise CurvatureSyncError(
                        'A misaligned column edge touches an A/Z boundary. Repair that boundary manually before Curvature Sync'
                    )
                if len(edge.link_faces) != 2:
                    raise CurvatureSyncError(
                        'A misaligned column edge is not a two-face interior edge and cannot be replaced safely'
                    )
                if edge.seam or not edge.smooth or _edge_has_nondefault_custom_data(chain_a.bm, edge):
                    raise CurvatureSyncError(
                        'A misaligned column edge carries Seam, Sharp, Crease, bevel, or custom edge data. Clear or preserve it manually before replacement'
                    )
                face_materials = {face.material_index for face in edge.link_faces}
                face_smoothing = {face.smooth for face in edge.link_faces}
                if len(face_materials) != 1 or len(face_smoothing) != 1:
                    raise CurvatureSyncError(
                        'A misaligned column edge separates faces with different material or smoothing data and cannot be dissolved safely'
                    )
                mismatched.add(edge)
    return mismatched


def _repair_misaligned_column_edges(bm, edges):
    valid = [edge for edge in edges if edge.is_valid]
    if not valid:
        return 0
    count = len(valid)
    bmesh.ops.dissolve_edges(
        bm,
        edges=valid,
        use_verts=False,
        use_face_split=False,
    )
    return count


def _connect_chain_columns(pairs, target_segments):
    created = 0
    unresolved = 0
    for chain_a, chain_b in pairs:
        bm = chain_a.bm
        for slot in range(target_segments * 2 + 1):
            vert_a = chain_a.slot_verts[slot]
            vert_b = chain_b.slot_verts[slot]
            if bm.edges.get((vert_a, vert_b)) is not None:
                continue
            common_faces = set(vert_a.link_faces) & set(vert_b.link_faces)
            if not common_faces:
                unresolved += 1
                continue
            result = bmesh.ops.connect_verts(
                bm,
                verts=[vert_a, vert_b],
                faces_exclude=[],
                check_degenerate=True,
            )
            new_edges = result.get('edges', [])
            if not new_edges:
                unresolved += 1
                continue
            for edge in new_edges:
                try:
                    edge.seam = False
                    edge.smooth = True
                    edge.select = True
                except Exception:
                    pass
            created += len(new_edges)
    return created, unresolved


def _validate_shape_keys(objects, topology_changes):
    if not topology_changes:
        return
    for obj in objects:
        if getattr(obj.data, 'shape_keys', None):
            raise CurvatureSyncError(
                f'Object "{obj.name}" has shape keys. Missing-vertex injection is disabled for shape-key meshes'
            )


def _build_all_chains(objects, bm_overrides=None):
    chains = []
    by_object = {}
    for obj in objects:
        override = bm_overrides.get(obj.name) if bm_overrides else None
        bm = _prepare_bmesh(obj, override)
        object_chains = _build_chains_for_object(obj, bm)
        chains.extend(object_chains)
        by_object[obj.name] = object_chains
    return chains, by_object


def _target_segment_count(chains, props):
    existing_max = max(max(chain.left_segments, chain.right_segments) for chain in chains)
    if props.curvature_sync_segment_mode == 'CUSTOM':
        target = int(props.curvature_sync_segments_per_side)
        if target < existing_max:
            raise CurvatureSyncError(
                f'Custom segments per side ({target}) is lower than the selected existing maximum ({existing_max}); dissolving extra topology is not enabled'
            )
        return target
    return existing_max


def _run_sync(objects, props, dry_run=False, bm_overrides=None):
    chains, by_object = _build_all_chains(objects, bm_overrides=bm_overrides)
    target_segments = _target_segment_count(chains, props)

    need_injection = any(
        chain.left_segments < target_segments or chain.right_segments < target_segments for chain in chains
    )
    if need_injection and not props.curvature_sync_inject_missing:
        raise CurvatureSyncError('Selected chains have different segment counts. Enable Inject Missing Vertices')
    _validate_shape_keys(objects, need_injection)

    for chain in chains:
        chain.target_points_world = _curve_targets(
            chain,
            target_segments,
            props.curvature_sync_plane,
            props.curvature_sync_snap_middle_axis,
        )
        # Validate locks before mutation.
        if props.curvature_sync_respect_locks:
            locked = _locked_refs_for_chain(chain)
            anchors = {chain.verts[0], chain.verts[-1]}
            middle_vert = chain.verts[chain.middle_index]
            middle_target_local = chain.obj.matrix_world.inverted_safe() @ chain.target_points_world[target_segments]
            if (
                not props.curvature_sync_snap_middle_axis
                or (middle_vert.co - middle_target_local).length_squared <= 1.0e-12
            ):
                anchors.add(middle_vert)
            if locked - anchors:
                raise CurvatureSyncError(
                    f'Chain on "{chain.obj.name}" includes locked interior vertices. Only A/M/Z anchors may be locked inside a repair span'
                )

    pairs_by_object = {
        name: _candidate_chain_pairs(object_chains) for name, object_chains in by_object.items()
    }
    repair_edges_by_object = {name: set() for name in by_object}
    if props.curvature_sync_connect_columns and props.curvature_sync_repair_misaligned_columns:
        for name, object_chains in by_object.items():
            repair_edges_by_object[name] = _collect_misaligned_column_edges(
                object_chains,
                pairs_by_object[name],
                target_segments,
            )

    injected = 0
    moved = 0
    repaired = 0
    connected = 0
    unresolved = 0
    snapshots = {}
    for obj in objects:
        object_chains = by_object[obj.name]
        bm = object_chains[0].bm
        if not dry_run:
            snapshots[obj.name] = _snapshot_lock_references(obj, bm)
        for chain in object_chains:
            injected += _inject_missing_slots(chain, target_segments)
            moved += _move_chain_to_targets(
                chain,
                target_segments,
                props.curvature_sync_respect_locks,
                props.curvature_sync_snap_middle_axis,
            )
        if props.curvature_sync_connect_columns:
            if props.curvature_sync_repair_misaligned_columns:
                repaired += _repair_misaligned_column_edges(
                    bm,
                    repair_edges_by_object[obj.name],
                )
            made, missing = _connect_chain_columns(pairs_by_object[obj.name], target_segments)
            connected += made
            unresolved += missing
        bm.normal_update()
        bm.verts.index_update()
        bm.edges.index_update()
        bm.faces.index_update()
        if not dry_run:
            _restore_lock_references(obj, bm, snapshots[obj.name])
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=bool(injected or repaired or connected))

    return {
        'objects': len(objects),
        'chains': len(chains),
        'segments_per_side': target_segments,
        'injected': injected,
        'moved': moved,
        'repaired': repaired,
        'connected': connected,
        'unresolved': unresolved,
    }


class WT_OT_curvature_capture_anchor(Operator):
    bl_idname = 'mesh.wt_curvature_capture_anchor'
    bl_label = 'Capture Curvature Anchor'
    bl_options = {'REGISTER', 'UNDO'}

    anchor_type: EnumProperty(
        items=(
            ('A', 'A', 'Capture the A/start endpoints'),
            ('M', 'Middle', 'Capture the middle/symmetry anchors'),
            ('Z', 'Z', 'Capture the Z/end endpoints'),
        ),
        default='A',
    )

    def execute(self, context):
        if context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, 'Enter Edit Mode and select the anchor vertices')
            return {'CANCELLED'}
        total = 0
        objects = 0
        for obj in _edit_mesh_objects(context):
            bm = _prepare_bmesh(obj)
            selected_verts = [vert for vert in bm.verts if vert.select]
            if not selected_verts:
                continue
            selected = {vert.index for vert in selected_verts}
            _write_anchor_indices(obj, self.anchor_type, selected)
            for vert in selected_verts:
                vert.select_set(False)
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
            total += len(selected)
            objects += 1
        if not total:
            self.report({'ERROR'}, 'Select at least one anchor vertex')
            return {'CANCELLED'}
        label = 'Middle' if self.anchor_type == 'M' else self.anchor_type
        self.report({'INFO'}, f'Captured {total} {label} anchor(s) across {objects} object(s); selection cleared')
        return {'FINISHED'}


class WT_OT_curvature_clear_anchors(Operator):
    bl_idname = 'mesh.wt_curvature_clear_anchors'
    bl_label = 'Clear Curvature Anchors'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects = _edit_mesh_objects(context)
        if not objects:
            self.report({'ERROR'}, 'Enter Edit Mode on one or more mesh objects')
            return {'CANCELLED'}
        for obj in objects:
            for key in _ANCHOR_KEYS.values():
                if key in obj:
                    del obj[key]
        self.report({'INFO'}, f'Cleared Curvature Sync anchors on {len(objects)} object(s)')
        return {'FINISHED'}


class WT_OT_curvature_analyze(Operator):
    bl_idname = 'mesh.wt_curvature_analyze'
    bl_label = 'Analyze Curvature Sync Selection'
    bl_options = {'REGISTER'}

    def execute(self, context):
        if context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, 'Enter multi-object Edit Mode and select the curve edges')
            return {'CANCELLED'}
        props = context.scene.witch_tools
        try:
            chains, by_object = _build_all_chains(_edit_mesh_objects(context))
            target = _target_segment_count(chains, props)
            missing = sum(
                (target - chain.left_segments) + (target - chain.right_segments) for chain in chains
            )
            misaligned = 0
            if props.curvature_sync_connect_columns and props.curvature_sync_repair_misaligned_columns:
                for object_chains in by_object.values():
                    pairs = _candidate_chain_pairs(object_chains)
                    misaligned += len(_collect_misaligned_column_edges(object_chains, pairs, target))
            for chain in chains:
                _curve_targets(
                    chain,
                    target,
                    props.curvature_sync_plane,
                    props.curvature_sync_snap_middle_axis,
                )
            self.report(
                {'INFO'},
                f'{len(chains)} chain(s); {target} segments/side; {missing} missing vertex slot(s); {misaligned} misaligned column edge(s)',
            )
            return {'FINISHED'}
        except CurvatureSyncError as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}


class WT_OT_curvature_sync(Operator):
    bl_idname = 'mesh.wt_curvature_sync'
    bl_label = 'Apply Curvature Sync'
    bl_description = 'Synchronize selected A-to-Z curve chains around captured middle anchors, inject missing vertex slots, and connect corresponding columns where faces permit'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, 'Enter multi-object Edit Mode and select only the curve-chain edges')
            return {'CANCELLED'}
        objects = _edit_mesh_objects(context)
        if not objects:
            self.report({'ERROR'}, 'No editable mesh objects found')
            return {'CANCELLED'}

        props = context.scene.witch_tools
        copies = {}
        old_guard_suspended = operators_vertex_locks._GUARD_SUSPENDED
        operators_vertex_locks._GUARD_SUSPENDED = True
        try:
            # Full dry-run on copied BMeshes catches traversal, injection, and face-connect failures before mutation.
            for obj in objects:
                source = _prepare_bmesh(obj)
                copies[obj.name] = source.copy()
            _run_sync(objects, props, dry_run=True, bm_overrides=copies)
            for bm in copies.values():
                bm.free()
            copies.clear()

            result = _run_sync(objects, props, dry_run=False)
            message = (
                f"Curvature Sync: {result['chains']} chains, {result['segments_per_side']} segments/side, "
                f"{result['injected']} vertices injected, {result['moved']} moved, "
                f"{result['repaired']} misaligned column edges replaced, "
                f"{result['connected']} column edges created"
            )
            if result['unresolved']:
                message += f", {result['unresolved']} column positions unresolved"
                self.report({'WARNING'}, message)
            else:
                self.report({'INFO'}, message)
            return {'FINISHED'}
        except CurvatureSyncError as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            self.report({'ERROR'}, f'Curvature Sync failed: {error}')
            return {'CANCELLED'}
        finally:
            for bm in copies.values():
                try:
                    bm.free()
                except Exception:
                    pass
            operators_vertex_locks._GUARD_SUSPENDED = old_guard_suspended


CLASSES = (
    WT_OT_curvature_capture_anchor,
    WT_OT_curvature_clear_anchors,
    WT_OT_curvature_analyze,
    WT_OT_curvature_sync,
)
