import bpy
import bmesh
from bpy.props import EnumProperty
from bpy.types import Operator
from mathutils import Matrix, Vector


_EPSILON = 1.0e-10
_ELEMENT_TYPES = {
    'VERT': bmesh.types.BMVert,
    'EDGE': bmesh.types.BMEdge,
    'FACE': bmesh.types.BMFace,
}
_ELEMENT_LABELS = {
    'VERT': 'vertex',
    'EDGE': 'edge',
    'FACE': 'face',
}


class ObjectSnapError(RuntimeError):
    pass


def _edit_mesh_objects(context):
    return [obj for obj in context.objects_in_mode_unique_data if obj.type == 'MESH']


def _prepare_bmesh(obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    return bm


def _element_collection(bm, element_type):
    if element_type == 'VERT':
        return bm.verts
    if element_type == 'EDGE':
        return bm.edges
    return bm.faces


def _selected_elements(bm, element_type):
    return [elem for elem in _element_collection(bm, element_type) if elem.select]


def _active_element(bm, element_type, selected):
    expected_type = _ELEMENT_TYPES[element_type]
    active = bm.select_history.active
    if isinstance(active, expected_type) and active in selected:
        return active

    if element_type == 'FACE':
        active_face = bm.faces.active
        if active_face in selected:
            return active_face

    for elem in reversed(tuple(bm.select_history)):
        if isinstance(elem, expected_type) and elem in selected:
            return elem
    return None


def _resolve_anchors(context, element_type):
    selections = []
    for obj in _edit_mesh_objects(context):
        bm = _prepare_bmesh(obj)
        selected = _selected_elements(bm, element_type)
        if selected:
            selections.append({'object': obj, 'bm': bm, 'selected': selected})

    label = _ELEMENT_LABELS[element_type]
    total = sum(len(item['selected']) for item in selections)
    if total != 2:
        raise ObjectSnapError(f'Select exactly two {label}s: source first, target second')

    if len(selections) == 1:
        item = selections[0]
        if len(item['selected']) != 2:
            raise ObjectSnapError(f'Select exactly two {label}s on one mesh')
        target = _active_element(item['bm'], element_type, item['selected'])
        if target is None:
            raise ObjectSnapError('The target anchor must be the active, most recently selected element')
        source = item['selected'][0] if item['selected'][1] is target else item['selected'][1]
        return (
            {'object': item['object'], 'bm': item['bm'], 'element': source},
            {'object': item['object'], 'bm': item['bm'], 'element': target},
            'ISLAND',
        )

    if len(selections) != 2 or any(len(item['selected']) != 1 for item in selections):
        raise ObjectSnapError(f'Use one selected {label} on each of two edit-mode mesh objects')

    active_obj = context.active_object
    target_item = next((item for item in selections if item['object'] is active_obj), None)
    if target_item is None:
        raise ObjectSnapError('The target mesh must be the active edit-mode object')
    source_item = selections[0] if selections[1] is target_item else selections[1]
    return (
        {'object': source_item['object'], 'bm': source_item['bm'], 'element': source_item['selected'][0]},
        {'object': target_item['object'], 'bm': target_item['bm'], 'element': target_item['selected'][0]},
        'OBJECT',
    )


def _element_vertices(element):
    if isinstance(element, bmesh.types.BMVert):
        return (element,)
    return tuple(element.verts)


def _connected_vertices(seed_vertices):
    connected = set(seed_vertices)
    pending = list(seed_vertices)
    while pending:
        vert = pending.pop()
        for edge in vert.link_edges:
            other = edge.other_vert(vert)
            if other not in connected:
                connected.add(other)
                pending.append(other)
    return connected


def _target_island(source, target):
    target_vertices = _connected_vertices(_element_vertices(target['element']))
    if any(vert in target_vertices for vert in _element_vertices(source['element'])):
        raise ObjectSnapError('Source and target anchors are on the same connected mesh island')
    return target_vertices


def _world_point(obj, element):
    matrix = obj.matrix_world
    if isinstance(element, bmesh.types.BMVert):
        return matrix @ element.co
    if isinstance(element, bmesh.types.BMEdge):
        return (matrix @ element.verts[0].co + matrix @ element.verts[1].co) * 0.5
    return matrix @ element.calc_center_median()


def _world_normal(obj, local_normal):
    try:
        normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
    except (ValueError, ZeroDivisionError):
        raise ObjectSnapError(f'Object "{obj.name}" has a non-invertible transform')
    normal = normal_matrix @ local_normal
    if normal.length_squared <= _EPSILON:
        return None
    return normal.normalized()


def _edge_direction(obj, edge):
    start = obj.matrix_world @ edge.verts[0].co
    end = obj.matrix_world @ edge.verts[1].co
    direction = end - start
    if direction.length_squared <= _EPSILON:
        raise ObjectSnapError('A selected edge has zero world-space length')
    return direction.normalized()


def _edge_normal(obj, edge, direction):
    normals = []
    for face in edge.link_faces:
        normal = _world_normal(obj, face.normal)
        if normal is not None:
            normals.append(normal)
    if not normals:
        return None

    combined = Vector((0.0, 0.0, 0.0))
    for normal in normals:
        combined += normal
    if combined.length_squared <= _EPSILON:
        combined = normals[0].copy()

    combined -= direction * combined.dot(direction)
    if combined.length_squared <= _EPSILON:
        return None
    return combined.normalized()


def _anchor_data(anchor, element_type, include_orientation):
    obj = anchor['object']
    element = anchor['element']
    data = {'point': _world_point(obj, element)}
    if not include_orientation or element_type == 'VERT':
        return data

    if element_type == 'EDGE':
        direction = _edge_direction(obj, element)
        data['direction'] = direction
        data['normal'] = _edge_normal(obj, element, direction)
    elif element_type == 'FACE':
        normal = _world_normal(obj, element.normal)
        if normal is None:
            raise ObjectSnapError('A selected face has no usable world-space normal')
        data['normal'] = normal
    return data


def _frame(direction, normal):
    x_axis = direction.normalized()
    z_axis = normal - x_axis * normal.dot(x_axis)
    if z_axis.length_squared <= _EPSILON:
        return None
    z_axis.normalize()
    y_axis = z_axis.cross(x_axis)
    if y_axis.length_squared <= _EPSILON:
        return None
    y_axis.normalize()
    return Matrix((x_axis, y_axis, z_axis)).transposed()


def _matrix_angle(rotation):
    return abs(rotation.to_quaternion().angle)


def _edge_rotation(source_data, target_data, normal_mode):
    source_direction = source_data['direction']
    target_direction = target_data['direction']
    source_normal = source_data.get('normal')
    target_normal = target_data.get('normal')

    if source_normal is not None and target_normal is not None:
        desired_normal = source_normal if normal_mode == 'SAME' else -source_normal
        target_frame = _frame(target_direction, target_normal)
        if target_frame is not None:
            candidates = []
            for direction in (source_direction, -source_direction):
                source_frame = _frame(direction, desired_normal)
                if source_frame is not None:
                    candidates.append(source_frame @ target_frame.transposed())
            if candidates:
                return min(candidates, key=_matrix_angle), False

    candidates = []
    for direction in (source_direction, -source_direction):
        rotation = target_direction.rotation_difference(direction).to_matrix()
        candidates.append(rotation)
    return min(candidates, key=_matrix_angle), True


def _face_rotation(source_data, target_data, normal_mode):
    desired_normal = source_data['normal'] if normal_mode == 'SAME' else -source_data['normal']
    return target_data['normal'].rotation_difference(desired_normal).to_matrix()


def _rotation_matrix(source_data, target_data, element_type, match_orientation, normal_mode):
    if not match_orientation or element_type == 'VERT':
        return Matrix.Identity(3), False
    if element_type == 'FACE':
        return _face_rotation(source_data, target_data, normal_mode), False
    return _edge_rotation(source_data, target_data, normal_mode)


def _move_object(obj, rotation, target_point, source_point):
    transform = (
        Matrix.Translation(source_point)
        @ rotation.to_4x4()
        @ Matrix.Translation(-target_point)
    )
    obj.matrix_world = transform @ obj.matrix_world
    obj.update_tag()


def _move_island(obj, bm, vertices, rotation, target_point, source_point):
    try:
        inverse_world = obj.matrix_world.inverted()
    except (ValueError, ZeroDivisionError):
        raise ObjectSnapError(f'Object "{obj.name}" has a non-invertible transform')

    for vert in vertices:
        world = obj.matrix_world @ vert.co
        moved = source_point + rotation @ (world - target_point)
        vert.co = inverse_world @ moved
    bm.normal_update()
    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    obj.update_tag()


class MESH_OT_object_island_snap(Operator):
    bl_idname = 'mesh.object_island_snap'
    bl_label = 'Object / Island Snap'
    bl_description = 'Move an entire target object or disconnected mesh island using selected source and target anchors'
    bl_options = {'REGISTER'}

    element_type: EnumProperty(
        name='Anchor Type',
        items=[
            ('VERT', 'Vertex', 'Snap using one source vertex and one target vertex'),
            ('EDGE', 'Edge', 'Snap using source and target edge midpoints'),
            ('FACE', 'Face', 'Snap using source and target face centers'),
        ],
        default='VERT',
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.active_object is not None

    @classmethod
    def description(cls, _context, properties):
        element_type = getattr(properties, 'element_type', 'VERT')
        if element_type == 'VERT':
            return 'Move the entire target object or disconnected island so the active target vertex meets the source vertex'
        if element_type == 'EDGE':
            return 'Move the entire target object or disconnected island from target edge midpoint to source edge midpoint; optionally match orientation'
        return 'Move the entire target object or disconnected island from target face center to source face center; optionally match orientation'

    def execute(self, context):
        try:
            source, target, scope = _resolve_anchors(context, self.element_type)
            target_vertices = _target_island(source, target) if scope == 'ISLAND' else None

            props = context.scene.witch_tools
            match_orientation = bool(props.object_snap_match_orientation)
            normal_mode = props.object_snap_normal_mode

            source_data = _anchor_data(source, self.element_type, match_orientation)
            target_data = _anchor_data(target, self.element_type, match_orientation)
            rotation, normal_fallback = _rotation_matrix(
                source_data,
                target_data,
                self.element_type,
                match_orientation,
                normal_mode,
            )

            if scope == 'OBJECT':
                _move_object(
                    target['object'],
                    rotation,
                    target_data['point'],
                    source_data['point'],
                )
            else:
                _move_island(
                    target['object'],
                    target['bm'],
                    target_vertices,
                    rotation,
                    target_data['point'],
                    source_data['point'],
                )

            context.view_layer.update()
            if context.area:
                context.area.tag_redraw()
            try:
                bpy.ops.ed.undo_push(message='Object Snap')
            except Exception as undo_error:
                self.report({'WARNING'}, f'Object Snap completed, but Blender could not create an undo step: {undo_error}')

            label = _ELEMENT_LABELS[self.element_type].title()
            target_kind = 'object' if scope == 'OBJECT' else 'mesh island'
            if normal_fallback:
                self.report({'INFO'}, f'{label} snapped; aligned edge direction without a usable face normal')
            else:
                self.report({'INFO'}, f'{label} snapped target {target_kind}')
            return {'FINISHED'}
        except ObjectSnapError as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        except Exception as exc:
            self.report({'ERROR'}, f'Object Snap failed: {exc}')
            return {'CANCELLED'}


CLASSES = (
    MESH_OT_object_island_snap,
)
