import bpy
import bmesh
import gpu
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Vector, geometry


_EPSILON = 1.0e-9


class DragSnapError(RuntimeError):
    pass


class HoverTarget:
    __slots__ = ('kind', 'element', 'point_world', 'factor', 'distance_px', 'virtual_points')

    def __init__(self, kind, element=None, point_world=None, factor=None, distance_px=0.0, virtual_points=None):
        self.kind = kind
        self.element = element
        self.point_world = Vector(point_world) if point_world is not None else None
        self.factor = factor
        self.distance_px = float(distance_px)
        self.virtual_points = tuple(Vector(p) for p in (virtual_points or ()))


def _screen_point(region, rv3d, world):
    point = view3d_utils.location_3d_to_region_2d(region, rv3d, world)
    return Vector(point) if point is not None else None


def _mouse_vector(event, region):
    return Vector((event.mouse_x - region.x, event.mouse_y - region.y))


def mouse_xy(event, region):
    point = _mouse_vector(event, region)
    return (point.x, point.y)


def _point_segment_2d(point, start, end):
    delta = end - start
    denom = delta.length_squared
    if denom <= _EPSILON:
        return start.copy(), 0.0, (point - start).length
    factor = (point - start).dot(delta) / denom
    factor = max(0.0, min(1.0, factor))
    closest = start + delta * factor
    return closest, factor, (point - closest).length


def closest_point_segment_3d(point, start, end):
    delta = end - start
    denom = delta.length_squared
    if denom <= _EPSILON:
        return start.copy(), 0.0, (point - start).length
    factor = (point - start).dot(delta) / denom
    factor = max(0.0, min(1.0, factor))
    closest = start + delta * factor
    return closest, factor, (point - closest).length


def _point_in_polygon_2d(point, polygon):
    if len(polygon) < 3:
        return False
    inside = False
    px, py = point.x, point.y
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i].x, polygon[i].y
        xj, yj = polygon[j].x, polygon[j].y
        crosses = (yi > py) != (yj > py)
        if crosses:
            denom = yj - yi
            if abs(denom) <= _EPSILON:
                denom = _EPSILON if denom >= 0.0 else -_EPSILON
            x_at_y = (xj - xi) * (py - yi) / denom + xi
            if px < x_at_y:
                inside = not inside
        j = i
    return inside


def _face_world_vertices(obj, face):
    matrix = obj.matrix_world
    return [matrix @ vert.co for vert in face.verts]


def _world_face_normal(obj, face):
    normal_matrix = obj.matrix_world.to_3x3().inverted_safe().transposed()
    normal = normal_matrix @ face.normal
    if normal.length <= _EPSILON:
        return Vector((0.0, 0.0, 1.0))
    return normal.normalized()


def _ray_plane_point(region, rv3d, mouse, plane_point, plane_normal):
    origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse)
    direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse)
    if origin is None or direction is None:
        return None
    return geometry.intersect_line_plane(
        Vector(origin),
        Vector(origin) + Vector(direction) * 1000000.0,
        Vector(plane_point),
        Vector(plane_normal),
        False,
    )


def pick_mesh_element(
    obj,
    bm,
    region,
    rv3d,
    mouse,
    allowed=('VERT', 'EDGE', 'FACE'),
    exclude_verts=None,
    exclude_edges=None,
    exclude_faces=None,
    vertex_radius=13.0,
    edge_radius=9.0,
):
    exclude_verts = set(exclude_verts or ())
    exclude_edges = set(exclude_edges or ())
    exclude_faces = set(exclude_faces or ())
    mouse = Vector(mouse)
    matrix = obj.matrix_world

    if 'VERT' in allowed:
        best = None
        for vert in bm.verts:
            if not vert.is_valid or vert.hide or vert in exclude_verts:
                continue
            screen = _screen_point(region, rv3d, matrix @ vert.co)
            if screen is None:
                continue
            distance = (mouse - screen).length
            if distance <= vertex_radius and (best is None or distance < best[0]):
                best = (distance, vert)
        if best is not None:
            distance, vert = best
            return HoverTarget('VERT', vert, matrix @ vert.co, distance_px=distance)

    if 'EDGE' in allowed:
        best = None
        for edge in bm.edges:
            if not edge.is_valid or edge.hide or edge in exclude_edges:
                continue
            if any(vert in exclude_verts for vert in edge.verts):
                continue
            world0 = matrix @ edge.verts[0].co
            world1 = matrix @ edge.verts[1].co
            screen0 = _screen_point(region, rv3d, world0)
            screen1 = _screen_point(region, rv3d, world1)
            if screen0 is None or screen1 is None:
                continue
            _closest, factor, distance = _point_segment_2d(mouse, screen0, screen1)
            if distance <= edge_radius and (best is None or distance < best[0]):
                best = (distance, edge, factor, world0.lerp(world1, factor))
        if best is not None:
            distance, edge, factor, point_world = best
            return HoverTarget('EDGE', edge, point_world, factor=factor, distance_px=distance)

    if 'FACE' in allowed:
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse)
        best = None
        for face in bm.faces:
            if not face.is_valid or face.hide or face in exclude_faces:
                continue
            if any(vert in exclude_verts for vert in face.verts):
                continue
            world = _face_world_vertices(obj, face)
            projected = [_screen_point(region, rv3d, point) for point in world]
            if any(point is None for point in projected):
                continue
            if not _point_in_polygon_2d(mouse, projected):
                continue
            center = sum(world, Vector()) / len(world)
            depth = (center - Vector(ray_origin)).length if ray_origin is not None else 0.0
            if best is None or depth < best[0]:
                normal = _world_face_normal(obj, face)
                hit = _ray_plane_point(region, rv3d, mouse, world[0], normal)
                best = (depth, face, hit if hit is not None else center)
        if best is not None:
            _depth, face, point_world = best
            return HoverTarget('FACE', face, point_world, distance_px=0.0)

    return None


def axis_mask(x, y, z):
    return (bool(x), bool(y), bool(z))


def axis_count(mask):
    return sum(1 for value in mask if value)


def masked_vector(vector, mask):
    return Vector(tuple(vector[index] if mask[index] else 0.0 for index in range(3)))


def project_mouse_anchor(region, rv3d, anchor_world, mouse, mask):
    mask = tuple(bool(value) for value in mask)
    count = axis_count(mask)
    if count == 0:
        raise DragSnapError('Enable at least one movement axis.')

    anchor_world = Vector(anchor_world)
    mouse = Vector(mouse)

    if count == 1:
        index = next(index for index, enabled in enumerate(mask) if enabled)
        axis = Vector((1.0 if index == 0 else 0.0, 1.0 if index == 1 else 0.0, 1.0 if index == 2 else 0.0))
        p0 = _screen_point(region, rv3d, anchor_world)
        p1 = _screen_point(region, rv3d, anchor_world + axis)
        if p0 is None or p1 is None:
            raise DragSnapError('The movement axis cannot be projected in the current view.')
        screen_axis = p1 - p0
        denom = screen_axis.length_squared
        if denom <= 1.0e-8:
            raise DragSnapError('The selected movement axis points almost directly at the camera. Orbit the view slightly.')
        distance = (mouse - p0).dot(screen_axis) / denom
        return anchor_world + axis * distance

    if count == 2:
        locked_index = next(index for index, enabled in enumerate(mask) if not enabled)
        normal = Vector((1.0 if locked_index == 0 else 0.0, 1.0 if locked_index == 1 else 0.0, 1.0 if locked_index == 2 else 0.0))
        hit = _ray_plane_point(region, rv3d, mouse, anchor_world, normal)
        if hit is None:
            raise DragSnapError('The movement plane is parallel to the current view ray. Orbit the view slightly.')
        result = Vector(hit)
        result[locked_index] = anchor_world[locked_index]
        return result

    point = view3d_utils.region_2d_to_location_3d(region, rv3d, mouse, anchor_world)
    if point is None:
        raise DragSnapError('The mouse position cannot be projected into the current 3D view.')
    return Vector(point)


def project_rail_factor(region, rv3d, start_world, end_world, mouse):
    p0 = _screen_point(region, rv3d, start_world)
    p1 = _screen_point(region, rv3d, end_world)
    if p0 is None or p1 is None:
        raise DragSnapError('The rail cannot be projected in the current view.')
    screen_rail = p1 - p0
    denom = screen_rail.length_squared
    if denom <= 1.0e-8:
        raise DragSnapError('The rail points almost directly at the camera. Orbit the view slightly.')
    return (Vector(mouse) - p0).dot(screen_rail) / denom


def _drop_axis(vector, axis):
    if axis == 0:
        return Vector((vector.y, vector.z))
    if axis == 1:
        return Vector((vector.x, vector.z))
    return Vector((vector.x, vector.y))


def point_in_face_world(obj, face, point_world):
    world = _face_world_vertices(obj, face)
    normal = _world_face_normal(obj, face)
    dominant = max(range(3), key=lambda index: abs(normal[index]))
    polygon = [_drop_axis(point, dominant) for point in world]
    return _point_in_polygon_2d(_drop_axis(Vector(point_world), dominant), polygon)


def closest_face_boundary(obj, face, point_world):
    point_world = Vector(point_world)
    best = None
    matrix = obj.matrix_world
    for edge in face.edges:
        start = matrix @ edge.verts[0].co
        end = matrix @ edge.verts[1].co
        closest, factor, distance = closest_point_segment_3d(point_world, start, end)
        if best is None or distance < best[0]:
            best = (distance, edge, factor, closest)
    return best


def face_travel_hits(obj, face, initial_world, travel_delta):
    travel_delta = Vector(travel_delta)
    if travel_delta.length <= _EPSILON:
        return {}
    direction = travel_delta.normalized()
    world = _face_world_vertices(obj, face)
    if not world:
        return {}
    normal = _world_face_normal(obj, face)
    plane_point = world[0]
    hits = {}
    for vert, start in initial_world.items():
        hit = geometry.intersect_line_plane(Vector(start), Vector(start) + direction, plane_point, normal, False)
        if hit is None:
            continue
        hit = Vector(hit)
        if (hit - Vector(start)).dot(direction) < -1.0e-7:
            continue
        if not point_in_face_world(obj, face, hit):
            boundary = closest_face_boundary(obj, face, hit)
            if boundary is not None:
                hit = boundary[3]
        hits[vert] = hit
    return hits


def boundary_contact(obj, face, point_world, tolerance=1.0e-5):
    matrix = obj.matrix_world
    point_world = Vector(point_world)
    for vert in face.verts:
        world = matrix @ vert.co
        if (world - point_world).length <= tolerance:
            return ('VERT', vert, world)
    best = closest_face_boundary(obj, face, point_world)
    if best is not None and best[0] <= tolerance:
        _distance, edge, _factor, closest = best
        return ('EDGE', edge, closest)
    return ('FACE', face, point_world)


def rigid_snap_delta(obj, created_verts, target, mask, tolerance=1.0e-5):
    mask = tuple(bool(value) for value in mask)
    matrix = obj.matrix_world
    if target is None or target.kind not in {'VERT', 'EDGE'}:
        return None, None

    if target.kind == 'VERT':
        target_point = target.point_world
        best = None
        for vert in created_verts:
            current = matrix @ vert.co
            delta = masked_vector(target_point - current, mask)
            residual = (current + delta - target_point).length
            score = (residual, delta.length)
            if best is None or score < best[0]:
                best = (score, vert, delta, target_point)
        if best is None:
            return None, None
        score, vert, delta, point = best
        if score[0] > tolerance:
            return None, None
        return delta, [(vert, 'VERT', target.element, point)]

    edge = target.element
    start = matrix @ edge.verts[0].co
    end = matrix @ edge.verts[1].co
    best = None
    for vert in created_verts:
        current = matrix @ vert.co
        closest, _factor, _distance = closest_point_segment_3d(current, start, end)
        delta = masked_vector(closest - current, mask)
        residual = (current + delta - closest).length
        score = (residual, delta.length)
        if best is None or score < best[0]:
            best = (score, vert, delta, closest)
    if best is None:
        return None, None
    score, vert, delta, point = best
    if score[0] > tolerance:
        return None, None
    return delta, [(vert, 'EDGE', edge, point)]


def _edge_world_closest(obj, edge, point_world):
    matrix = obj.matrix_world
    start = matrix @ edge.verts[0].co
    end = matrix @ edge.verts[1].co
    return closest_point_segment_3d(Vector(point_world), start, end)


def _merge_excluded_edges(bm, created_verts=(), created_edges=(), branch_edges=()):
    created_vert_set = {vert for vert in created_verts or () if getattr(vert, 'is_valid', False)}
    excluded = {edge for edge in (*tuple(created_edges or ()), *tuple(branch_edges or ())) if getattr(edge, 'is_valid', False)}
    for edge in bm.edges:
        if edge.is_valid and any(vert in created_vert_set for vert in edge.verts):
            excluded.add(edge)
    return created_vert_set, excluded


def collect_auto_merge_contacts(
    bm,
    obj,
    created_verts,
    created_edges=(),
    branch_edges=(),
    explicit_contacts=(),
    tolerance=1.0e-6,
):
    """Resolve every supported created-vertex overlap before mutating target topology.

    Explicit magnetic contacts win. Remaining created vertices are checked against
    pre-existing vertices first, then pre-existing edges. New/branch geometry is
    excluded so Auto-Merge cannot accidentally consume its own live topology.
    """
    created_vert_set, excluded_edges = _merge_excluded_edges(
        bm,
        created_verts=created_verts,
        created_edges=created_edges,
        branch_edges=branch_edges,
    )
    matrix = obj.matrix_world
    by_created = {}

    for created_vert, kind, element, point_world in explicit_contacts or ():
        if created_vert not in created_vert_set or not created_vert.is_valid:
            continue
        if kind not in {'VERT', 'EDGE'} or element is None or not getattr(element, 'is_valid', False):
            continue
        if kind == 'VERT' and element in created_vert_set:
            continue
        if kind == 'EDGE' and element in excluded_edges:
            continue
        by_created[created_vert] = (created_vert, kind, element, Vector(point_world))

    existing_verts = [
        vert for vert in bm.verts
        if vert.is_valid and not vert.hide and vert not in created_vert_set
    ]
    existing_edges = [
        edge for edge in bm.edges
        if edge.is_valid and not edge.hide and edge not in excluded_edges
    ]

    for created_vert in created_vert_set:
        if not created_vert.is_valid or created_vert in by_created:
            continue
        point_world = matrix @ created_vert.co

        best_vert = None
        for target_vert in existing_verts:
            distance = (matrix @ target_vert.co - point_world).length
            if distance <= tolerance and (best_vert is None or distance < best_vert[0]):
                best_vert = (distance, target_vert)
        if best_vert is not None:
            _distance, target_vert = best_vert
            by_created[created_vert] = (
                created_vert,
                'VERT',
                target_vert,
                matrix @ target_vert.co,
            )
            continue

        best_edge = None
        for target_edge in existing_edges:
            closest, factor, distance = _edge_world_closest(obj, target_edge, point_world)
            if distance <= tolerance and (best_edge is None or distance < best_edge[0]):
                best_edge = (distance, target_edge, factor, closest)
        if best_edge is not None:
            _distance, target_edge, _factor, closest = best_edge
            by_created[created_vert] = (
                created_vert,
                'EDGE',
                target_edge,
                closest,
            )

    return list(by_created.values())


def contact_target_vertices(contact):
    _created_vert, kind, element, _point_world = contact
    if element is None or not getattr(element, 'is_valid', False):
        return ()
    if kind == 'VERT':
        return (element,)
    if kind == 'EDGE':
        return tuple(element.verts)
    return ()


def materialize_edge_point(
    bm,
    obj,
    edge,
    point_world,
    tolerance=1.0e-6,
    excluded_edges=(),
    created_verts=(),
):
    excluded_edges = {candidate for candidate in excluded_edges or () if getattr(candidate, 'is_valid', False)}
    created_vert_set = {vert for vert in created_verts or () if getattr(vert, 'is_valid', False)}
    candidates = []
    if edge is not None and getattr(edge, 'is_valid', False) and edge not in excluded_edges:
        candidates.append(edge)
        for vert in edge.verts:
            for linked in vert.link_edges:
                if (
                    linked.is_valid
                    and linked not in candidates
                    and linked not in excluded_edges
                    and not any(candidate_vert in created_vert_set for candidate_vert in linked.verts)
                ):
                    candidates.append(linked)
    if not candidates:
        candidates = [
            candidate for candidate in bm.edges
            if (
                candidate.is_valid
                and not candidate.hide
                and candidate not in excluded_edges
                and not any(candidate_vert in created_vert_set for candidate_vert in candidate.verts)
            )
        ]

    best = None
    for candidate in candidates:
        closest, factor, distance = _edge_world_closest(obj, candidate, point_world)
        if best is None or distance < best[0]:
            best = (distance, candidate, factor, closest)
    if best is None:
        raise DragSnapError('Could not resolve the magnetic target edge.')
    distance, candidate, factor, closest = best
    if distance > max(tolerance, 1.0e-5):
        raise DragSnapError('The magnetic merge point no longer lies on the target edge.')

    matrix = obj.matrix_world
    start, end = candidate.verts
    if (closest - matrix @ start.co).length <= tolerance:
        return start
    if (closest - matrix @ end.co).length <= tolerance:
        return end
    factor = max(1.0e-6, min(1.0 - 1.0e-6, factor))
    _new_edge, new_vert = bmesh.utils.edge_split(candidate, start, factor)
    return new_vert


def weld_contacts(
    bm,
    obj,
    contacts,
    face_target=None,
    tolerance=1.0e-6,
    created_verts=(),
    created_edges=(),
    branch_edges=(),
):
    created_vert_set, excluded_edges = _merge_excluded_edges(
        bm,
        created_verts=created_verts,
        created_edges=created_edges,
        branch_edges=branch_edges,
    )
    target_map = {}
    face_boundary_targets = []
    face_boundary_sources = {
        created_vert
        for created_vert, kind, element, _point_world in contacts or ()
        if (
            face_target is not None
            and kind in {'VERT', 'EDGE'}
            and element is not None
            and getattr(element, 'is_valid', False)
            and (
                (kind == 'VERT' and element in face_target.verts)
                or (kind == 'EDGE' and element in face_target.edges)
            )
        )
    }

    for created_vert, kind, element, point_world in contacts or ():
        if not getattr(created_vert, 'is_valid', False):
            continue
        if kind == 'VERT':
            target_vert = element
        elif kind == 'EDGE':
            target_vert = materialize_edge_point(
                bm,
                obj,
                element,
                point_world,
                tolerance=tolerance,
                excluded_edges=excluded_edges,
                created_verts=created_vert_set,
            )
        else:
            continue
        if target_vert is created_vert or not getattr(target_vert, 'is_valid', False):
            continue
        target_map[created_vert] = target_vert
        if created_vert in face_boundary_sources:
            face_boundary_targets.append(target_vert)

    if target_map:
        bmesh.ops.weld_verts(bm, targetmap=target_map)

    face_boundary_targets = [
        vert for index, vert in enumerate(face_boundary_targets)
        if vert.is_valid and vert not in face_boundary_targets[:index]
    ]
    if face_target is not None and getattr(face_target, 'is_valid', False) and len(face_boundary_targets) == 2:
        first, second = face_boundary_targets
        if first is not second:
            existing = bm.edges.get((first, second))
            if existing is not None and existing.is_valid and len(existing.link_faces) == 0:
                bmesh.ops.delete(bm, geom=[existing], context='EDGES')
                existing = None
            if existing is None:
                try:
                    bmesh.ops.connect_verts(bm, verts=[first, second], check_degenerate=True)
                except Exception:
                    pass
    return tuple(face_boundary_targets)


class HoverHighlighter:
    def __init__(self):
        self.target = None
        self.virtual_lines = ()
        self._handle = None

    def start(self):
        if self._handle is None:
            self._handle = bpy.types.SpaceView3D.draw_handler_add(self._draw, (), 'WINDOW', 'POST_VIEW')

    def stop(self):
        if self._handle is not None:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            except Exception:
                pass
            self._handle = None

    def set_target(self, target):
        self.target = target

    def set_virtual_lines(self, lines):
        self.virtual_lines = tuple((Vector(start), Vector(end)) for start, end in (lines or ()))

    def _draw(self):
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        try:
            gpu.state.blend_set('ALPHA')
            if self.virtual_lines:
                coords = []
                for start, end in self.virtual_lines:
                    coords.extend((start, end))
                batch = batch_for_shader(shader, 'LINES', {'pos': coords})
                gpu.state.line_width_set(3.0)
                shader.bind()
                shader.uniform_float('color', (0.95, 0.65, 0.15, 0.95))
                batch.draw(shader)

            target = self.target
            if target is None:
                return
            if target.kind == 'VERT' and target.element is not None and target.element.is_valid:
                batch = batch_for_shader(shader, 'POINTS', {'pos': [target.point_world]})
                gpu.state.point_size_set(12.0)
                shader.bind()
                shader.uniform_float('color', (0.2, 0.85, 1.0, 1.0))
                batch.draw(shader)
                return
            if target.kind == 'EDGE' and target.element is not None and target.element.is_valid:
                obj = bpy.context.active_object
                if obj is None:
                    return
                edge = target.element
                coords = [obj.matrix_world @ edge.verts[0].co, obj.matrix_world @ edge.verts[1].co]
                batch = batch_for_shader(shader, 'LINES', {'pos': coords})
                gpu.state.line_width_set(5.0)
                shader.bind()
                shader.uniform_float('color', (0.2, 0.85, 1.0, 1.0))
                batch.draw(shader)
                return
            if target.kind == 'FACE' and target.element is not None and target.element.is_valid:
                obj = bpy.context.active_object
                face = target.element
                if obj is None or len(face.verts) < 3:
                    return
                world = [obj.matrix_world @ vert.co for vert in face.verts]
                triangles = []
                for index in range(1, len(world) - 1):
                    triangles.extend((world[0], world[index], world[index + 1]))
                if triangles:
                    batch = batch_for_shader(shader, 'TRIS', {'pos': triangles})
                    shader.bind()
                    shader.uniform_float('color', (0.2, 0.85, 1.0, 0.22))
                    batch.draw(shader)
                line_coords = []
                for index, point in enumerate(world):
                    line_coords.extend((point, world[(index + 1) % len(world)]))
                batch = batch_for_shader(shader, 'LINES', {'pos': line_coords})
                gpu.state.line_width_set(4.0)
                shader.bind()
                shader.uniform_float('color', (0.2, 0.85, 1.0, 0.95))
                batch.draw(shader)
        finally:
            try:
                gpu.state.line_width_set(1.0)
                gpu.state.point_size_set(1.0)
                gpu.state.blend_set('NONE')
            except Exception:
                pass


def set_orbit_pivot(rv3d, point_world):
    if rv3d is None or point_world is None:
        return
    try:
        rv3d.view_location = Vector(point_world)
    except Exception:
        pass
