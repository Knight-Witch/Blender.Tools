import bmesh
from mathutils import Matrix, Vector

from .precision_edit_common import (
    _EPSILON,
    PrecisionEditError,
    _co_to_space,
    _normal_to_space,
    _point_local,
    _prepare_bmesh,
)


def _least_parallel_axis(direction):
    axes = (
        Vector((1.0, 0.0, 0.0)),
        Vector((0.0, 1.0, 0.0)),
        Vector((0.0, 0.0, 1.0)),
    )
    return min(axes, key=lambda axis: abs(axis.dot(direction)))


def _basis_from_normal(normal):
    z_axis = normal.normalized() if normal.length > _EPSILON else Vector((0.0, 0.0, 1.0))
    reference = _least_parallel_axis(z_axis)
    x_axis = reference.cross(z_axis)
    if x_axis.length <= _EPSILON:
        x_axis = Vector((1.0, 0.0, 0.0))
    else:
        x_axis.normalize()
    y_axis = z_axis.cross(x_axis)
    if y_axis.length <= _EPSILON:
        y_axis = Vector((0.0, 1.0, 0.0))
    else:
        y_axis.normalize()
    x_axis = y_axis.cross(z_axis).normalized()
    return Matrix((x_axis, y_axis, z_axis)).transposed()


def _edge_normal(obj, edge, space):
    normal = Vector((0.0, 0.0, 0.0))
    for face in edge.link_faces:
        normal += _normal_to_space(obj, face.normal, space)
    if normal.length > _EPSILON:
        return normal.normalized()
    return None


def _basis_from_edge(obj, edge, space):
    start = _co_to_space(obj, edge.verts[0].co, space)
    end = _co_to_space(obj, edge.verts[1].co, space)
    direction = end - start
    if direction.length <= _EPSILON:
        raise PrecisionEditError('The source or target edge has zero length.')
    x_axis = direction.normalized()
    normal = _edge_normal(obj, edge, space)
    if normal is None or abs(normal.dot(x_axis)) > 0.9999:
        reference = _least_parallel_axis(x_axis)
        z_axis = x_axis.cross(reference)
        if z_axis.length <= _EPSILON:
            z_axis = Vector((0.0, 0.0, 1.0))
        else:
            z_axis.normalize()
    else:
        z_axis = normal - x_axis * normal.dot(x_axis)
        if z_axis.length <= _EPSILON:
            z_axis = x_axis.cross(_least_parallel_axis(x_axis))
        z_axis.normalize()
    y_axis = z_axis.cross(x_axis)
    if y_axis.length <= _EPSILON:
        y_axis = _least_parallel_axis(x_axis).cross(x_axis)
    y_axis.normalize()
    z_axis = x_axis.cross(y_axis).normalized()
    return Matrix((x_axis, y_axis, z_axis)).transposed()


def _basis_from_face(obj, face, space):
    z_axis = _normal_to_space(obj, face.normal, space)
    best = None
    for edge in face.edges:
        a = _co_to_space(obj, edge.verts[0].co, space)
        b = _co_to_space(obj, edge.verts[1].co, space)
        vector = b - a
        projected = vector - z_axis * vector.dot(z_axis)
        if projected.length <= _EPSILON:
            continue
        if best is None or projected.length > best.length:
            best = projected
    if best is None:
        return _basis_from_normal(z_axis)
    x_axis = best.normalized()
    y_axis = z_axis.cross(x_axis)
    if y_axis.length <= _EPSILON:
        return _basis_from_normal(z_axis)
    y_axis.normalize()
    x_axis = y_axis.cross(z_axis).normalized()
    return Matrix((x_axis, y_axis, z_axis)).transposed()


def _source_frame(obj, kind, element, space):
    center = _co_to_space(obj, _point_local(kind, element), space)
    if kind == 'VERT':
        basis = _basis_from_normal(_normal_to_space(obj, element.normal, space))
        points = [center]
    elif kind == 'EDGE':
        basis = _basis_from_edge(obj, element, space)
        points = [_co_to_space(obj, vert.co, space) for vert in element.verts]
    else:
        basis = _basis_from_face(obj, element, space)
        points = [_co_to_space(obj, vert.co, space) for vert in element.verts]
    scale = _scale_from_points(points, center, basis, kind)
    return center, basis, scale


def _scale_from_points(points, center, basis, kind):
    if kind == 'VERT' or len(points) <= 1:
        return Vector((1.0, 1.0, 1.0))
    inv_basis = basis.transposed()
    components = [inv_basis @ (point - center) for point in points]
    extents = []
    for axis in range(3):
        values = [co[axis] for co in components]
        extent = max(values) - min(values)
        extents.append(extent if extent > _EPSILON else 1.0)
    if kind == 'EDGE' and len(points) == 2:
        extents[1] = 1.0
        extents[2] = 1.0
    if kind == 'FACE':
        extents[2] = 1.0
    return Vector(extents)


def _group_frame(obj, kind, elements, verts, space):
    points = [_co_to_space(obj, vert.co, space) for vert in verts]
    center = sum(points, Vector((0.0, 0.0, 0.0))) / max(1, len(points))

    if kind == 'VERT':
        vert = verts[0]
        basis = _basis_from_normal(_normal_to_space(obj, vert.normal, space))
    elif kind == 'EDGE':
        edge = max(
            elements,
            key=lambda item: (_co_to_space(obj, item.verts[1].co, space) - _co_to_space(obj, item.verts[0].co, space)).length_squared,
        )
        basis = _basis_from_edge(obj, edge, space)
    else:
        normal = Vector((0.0, 0.0, 0.0))
        for face in elements:
            normal += _normal_to_space(obj, face.normal, space) * max(face.calc_area(), _EPSILON)
        if normal.length <= _EPSILON:
            normal = _normal_to_space(obj, elements[0].normal, space)
        normal.normalize()

        best_vector = None
        best_length = -1.0
        seen_edges = set()
        for face in elements:
            for edge in face.edges:
                if edge in seen_edges:
                    continue
                seen_edges.add(edge)
                a = _co_to_space(obj, edge.verts[0].co, space)
                b = _co_to_space(obj, edge.verts[1].co, space)
                vector = b - a
                projected = vector - normal * vector.dot(normal)
                if projected.length_squared > best_length and projected.length > _EPSILON:
                    best_vector = projected
                    best_length = projected.length_squared
        if best_vector is None:
            basis = _basis_from_normal(normal)
        else:
            x_axis = best_vector.normalized()
            y_axis = normal.cross(x_axis)
            if y_axis.length <= _EPSILON:
                basis = _basis_from_normal(normal)
            else:
                y_axis.normalize()
                x_axis = y_axis.cross(normal).normalized()
                basis = Matrix((x_axis, y_axis, normal)).transposed()

    scale = _scale_from_points(points, center, basis, kind)
    return center, basis, scale


def _target_groups_for_object(obj, kind):
    bm = _prepare_bmesh(obj)
    if kind == 'VERT':
        return bm, [([vert], [vert]) for vert in bm.verts if vert.select]

    if kind == 'EDGE':
        selected = {edge for edge in bm.edges if edge.select}
        groups = []
        while selected:
            seed = selected.pop()
            stack = [seed]
            edges = [seed]
            verts = set(seed.verts)
            while stack:
                edge = stack.pop()
                for vert in edge.verts:
                    for linked in vert.link_edges:
                        if linked in selected:
                            selected.remove(linked)
                            stack.append(linked)
                            edges.append(linked)
                            verts.update(linked.verts)
            groups.append((edges, list(verts)))
        return bm, groups

    selected = {face for face in bm.faces if face.select}
    groups = []
    while selected:
        seed = selected.pop()
        stack = [seed]
        faces = [seed]
        verts = set(seed.verts)
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for linked in edge.link_faces:
                    if linked in selected:
                        selected.remove(linked)
                        stack.append(linked)
                        faces.append(linked)
                        verts.update(linked.verts)
        groups.append((faces, list(verts)))
    return bm, groups
