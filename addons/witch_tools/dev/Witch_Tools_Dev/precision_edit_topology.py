import bmesh
from mathutils import Vector


_EPSILON = 1.0e-9


class PrecisionTopologyError(RuntimeError):
    pass


def prepare_bmesh(obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    bm.normal_update()
    return bm


def source_element_from_selection(bm, element_type, allow_multiple=False):
    if element_type == 'VERT':
        elements = [vert for vert in bm.verts if vert.select]
        label = 'vertex'
    elif element_type == 'EDGE':
        elements = [edge for edge in bm.edges if edge.select]
        label = 'edge'
    elif element_type == 'FACE':
        elements = [face for face in bm.faces if face.select]
        label = 'face'
    else:
        raise PrecisionTopologyError(f'Unsupported source element type: {element_type}')

    if allow_multiple:
        if not elements:
            raise PrecisionTopologyError(f'Select at least one source {label}.')
        return elements

    if len(elements) != 1:
        raise PrecisionTopologyError(f'Select exactly one source {label}.')
    return elements[0]


def source_closure(element_type, element):
    if element_type == 'VERT':
        return [element], [element]
    if element_type == 'EDGE':
        return [*element.verts, element], list(element.verts)
    if element_type == 'FACE':
        return [*element.verts, *element.edges, element], list(element.verts)
    raise PrecisionTopologyError(f'Unsupported source element type: {element_type}')


def world_point(obj, element_type, element):
    if element_type == 'VERT':
        local = element.co
    elif element_type == 'EDGE':
        local = (element.verts[0].co + element.verts[1].co) * 0.5
    else:
        local = element.calc_center_median()
    return obj.matrix_world @ local


def match_duplicate_verts(source_verts, duplicate_verts):
    mapping = {}
    unused = set(duplicate_verts)
    for source in source_verts:
        best = None
        best_distance = None
        for duplicate in unused:
            distance = (duplicate.co - source.co).length_squared
            if best is None or distance < best_distance:
                best = duplicate
                best_distance = distance
        if best is None:
            raise PrecisionTopologyError('Could not map duplicated vertices back to the source geometry.')
        mapping[source] = best
        unused.remove(best)
    return mapping


def duplicate_source(bm, element_type, element, make_branch=False):
    source_geom, source_verts = source_closure(element_type, element)
    result = bmesh.ops.duplicate(bm, geom=source_geom)
    duplicate_geom = [item for item in result.get('geom', ()) if getattr(item, 'is_valid', False)]
    duplicate_verts = [item for item in duplicate_geom if isinstance(item, bmesh.types.BMVert)]
    duplicate_edges = [item for item in duplicate_geom if isinstance(item, bmesh.types.BMEdge)]
    duplicate_faces = [item for item in duplicate_geom if isinstance(item, bmesh.types.BMFace)]
    if len(duplicate_verts) != len(source_verts):
        raise PrecisionTopologyError('Blender did not create the expected number of duplicated vertices.')

    vert_map = result.get('vert_map') or result.get('isovert_map') or {}
    mapped = {source: vert_map.get(source) for source in source_verts if vert_map.get(source) in duplicate_verts}
    if len(mapped) != len(source_verts):
        mapped = match_duplicate_verts(source_verts, duplicate_verts)

    branch_edges = []
    if make_branch:
        for source in source_verts:
            duplicate = mapped[source]
            edge = bm.edges.get((source, duplicate))
            if edge is None:
                try:
                    edge = bm.edges.new((source, duplicate))
                except ValueError:
                    edge = bm.edges.get((source, duplicate))
            if edge is not None:
                branch_edges.append(edge)

    return {
        'source_verts': source_verts,
        'source_to_duplicate': mapped,
        'created_geom': duplicate_geom,
        'created_verts': duplicate_verts,
        'created_edges': duplicate_edges,
        'created_faces': duplicate_faces,
        'branch_edges': branch_edges,
    }


def oriented_edge_vertices(face, edge):
    loops = list(face.loops)
    for loop in loops:
        if loop.edge is edge:
            return loop.vert, loop.link_loop_next.vert
    return edge.verts[0], edge.verts[1]


def face_edge_outward_vector(face, edge):
    if len(face.verts) < 3:
        raise PrecisionTopologyError('Face branching requires a valid face.')
    start, end = oriented_edge_vertices(face, edge)
    midpoint = (start.co + end.co) * 0.5

    if len(face.verts) == 4:
        opposite = next(
            (
                candidate
                for candidate in face.edges
                if candidate is not edge and all(vert not in edge.verts for vert in candidate.verts)
            ),
            None,
        )
        if opposite is not None:
            opposite_mid = (opposite.verts[0].co + opposite.verts[1].co) * 0.5
            vector = midpoint - opposite_mid
            if vector.length > _EPSILON:
                return vector

    center = face.calc_center_median()
    direction = midpoint - center
    direction -= face.normal * direction.dot(face.normal)
    if direction.length <= _EPSILON:
        raise PrecisionTopologyError('Could not determine an outward direction from the chosen face edge.')
    depth = max((midpoint - center).length * 2.0, _EPSILON)
    return direction.normalized() * depth


def create_organic_face(bm, source_face, source_edge):
    start, end = oriented_edge_vertices(source_face, source_edge)
    new_start = bm.verts.new(start.co.copy())
    new_end = bm.verts.new(end.co.copy())
    try:
        face = bm.faces.new((start, end, new_end, new_start))
    except ValueError as error:
        bmesh.ops.delete(bm, geom=[new_start, new_end], context='VERTS')
        raise PrecisionTopologyError(f'Could not create Organic branch face: {error}')
    return {
        'created_verts': [new_start, new_end],
        'created_edges': [edge for edge in face.edges if edge is not source_edge],
        'created_faces': [face],
        'outer_verts': [new_start, new_end],
        'source_edge_verts': [start, end],
    }


def rebuild_paver(bm, source_face, source_edge, count, existing_created=None, step_local=None):
    if existing_created:
        valid = [vert for vert in existing_created.get('created_verts', ()) if getattr(vert, 'is_valid', False)]
        if valid:
            bmesh.ops.delete(bm, geom=valid, context='VERTS')

    count = max(1, int(count))
    start, end = oriented_edge_vertices(source_face, source_edge)
    step = Vector(step_local) if step_local is not None else face_edge_outward_vector(source_face, source_edge)
    if step.length <= _EPSILON:
        raise PrecisionTopologyError('The enabled movement axes collapse the Paver direction to zero.')

    created_verts = []
    created_faces = []
    created_edges = []
    previous_start = start
    previous_end = end
    outer_verts = None

    for index in range(1, count + 1):
        next_start = bm.verts.new(start.co + step * index)
        next_end = bm.verts.new(end.co + step * index)
        created_verts.extend((next_start, next_end))
        try:
            face = bm.faces.new((previous_start, previous_end, next_end, next_start))
        except ValueError as error:
            bmesh.ops.delete(bm, geom=created_verts, context='VERTS')
            raise PrecisionTopologyError(f'Could not create Paver tile {index}: {error}')
        created_faces.append(face)
        for edge in face.edges:
            if edge is source_edge:
                continue
            if edge not in created_edges:
                created_edges.append(edge)
        previous_start = next_start
        previous_end = next_end
        outer_verts = [next_start, next_end]

    return {
        'created_verts': created_verts,
        'created_edges': created_edges,
        'created_faces': created_faces,
        'outer_verts': outer_verts or [],
        'source_edge_verts': [start, end],
        'step_local': step,
        'count': count,
    }


def validate_no_zero_geometry(bm):
    for edge in bm.edges:
        if edge.is_valid and (edge.verts[1].co - edge.verts[0].co).length <= 1.0e-12:
            raise PrecisionTopologyError('The operation would leave a zero-length edge.')
    for face in bm.faces:
        if face.is_valid and face.calc_area() <= 1.0e-16:
            raise PrecisionTopologyError('The operation would leave a zero-area face.')
