import bpy
import bmesh
from mathutils import Vector

from . import operators_vertex_locks


_EPSILON = 1.0e-9
_AXIS_BITS = (1, 2, 4)
_PLANE_MASK_LAYER = 'wt_plane_lock_mask'
_PLANE_X_LAYER = 'wt_plane_lock_x'
_PLANE_Y_LAYER = 'wt_plane_lock_y'
_PLANE_Z_LAYER = 'wt_plane_lock_z'


class PrecisionEditError(RuntimeError):
    pass


def _props(context):
    return context.scene.wt_precision_edit


def _edit_mesh_objects(context):
    objects = []
    seen_data = set()
    candidates = getattr(context, 'objects_in_mode_unique_data', None) or ()
    for obj in candidates:
        if obj and obj.type == 'MESH' and obj.mode == 'EDIT' and obj.data not in seen_data:
            objects.append(obj)
            seen_data.add(obj.data)
    if not objects:
        obj = getattr(context, 'active_object', None)
        if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            objects.append(obj)
    return objects


def _prepare_bmesh(obj):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    bm.normal_update()
    return bm


def _selection_kind(context):
    mode = getattr(context.tool_settings, 'mesh_select_mode', (True, False, False))
    if mode[2]:
        return 'FACE'
    if mode[1]:
        return 'EDGE'
    return 'VERT'


def _selected_elements(obj, kind):
    bm = _prepare_bmesh(obj)
    if kind == 'FACE':
        return bm, [face for face in bm.faces if face.select]
    if kind == 'EDGE':
        return bm, [edge for edge in bm.edges if edge.select]
    return bm, [vert for vert in bm.verts if vert.select]


def _collect_selected(context, kind=None):
    kind = kind or _selection_kind(context)
    found = []
    for obj in _edit_mesh_objects(context):
        bm, elements = _selected_elements(obj, kind)
        found.extend((obj, bm, element) for element in elements)
    return kind, found


def clear_current_edit_selection(context):
    """Clear mesh element selection on every object participating in multi-object Edit Mode."""
    for obj in _edit_mesh_objects(context):
        bm = _prepare_bmesh(obj)
        for vert in bm.verts:
            vert.select_set(False)
        for edge in bm.edges:
            edge.select_set(False)
        for face in bm.faces:
            face.select_set(False)
        bm.select_history.clear()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)


def _single_source(context):
    kind, found = _collect_selected(context)
    if len(found) != 1:
        label = {'VERT': 'vertex', 'EDGE': 'edge', 'FACE': 'face'}[kind]
        raise PrecisionEditError(f'Select exactly one source {label} in the active mesh selection mode.')
    return kind, found[0]


def _point_local(kind, element):
    if kind == 'VERT':
        return element.co.copy()
    if kind == 'EDGE':
        return (element.verts[0].co + element.verts[1].co) * 0.5
    return element.calc_center_median()


def _point_world(obj, kind, element):
    return obj.matrix_world @ _point_local(kind, element)


def capture_selected_point_world(context):
    kind, (obj, _bm, element) = _single_source(context)
    return kind, obj, element, _point_world(obj, kind, element)


def _co_to_space(obj, local_co, space):
    if space == 'GLOBAL':
        return obj.matrix_world @ local_co
    return local_co.copy()


def _co_from_space(obj, co, space):
    if space == 'GLOBAL':
        try:
            return obj.matrix_world.inverted_safe() @ co
        except Exception as exc:
            raise PrecisionEditError(f'{obj.name}: object transform cannot be inverted.') from exc
    return co.copy()


def _normal_to_space(obj, normal, space):
    normal = normal.copy()
    if space == 'GLOBAL':
        try:
            normal = obj.matrix_world.to_3x3().inverted_safe().transposed() @ normal
        except Exception:
            normal = obj.matrix_world.to_3x3() @ normal
    if normal.length <= _EPSILON:
        return Vector((0.0, 0.0, 1.0))
    return normal.normalized()


def _axis_mask(props, prefix):
    return (
        bool(getattr(props, f'{prefix}_x')),
        bool(getattr(props, f'{prefix}_y')),
        bool(getattr(props, f'{prefix}_z')),
    )


def _require_axis(mask):
    if not any(mask):
        raise PrecisionEditError('Enable at least one axis.')


def _planar_layers(bm, create=False):
    mask = bm.verts.layers.int.get(_PLANE_MASK_LAYER)
    x_layer = bm.verts.layers.float.get(_PLANE_X_LAYER)
    y_layer = bm.verts.layers.float.get(_PLANE_Y_LAYER)
    z_layer = bm.verts.layers.float.get(_PLANE_Z_LAYER)
    if create:
        mask = mask or bm.verts.layers.int.new(_PLANE_MASK_LAYER)
        x_layer = x_layer or bm.verts.layers.float.new(_PLANE_X_LAYER)
        y_layer = y_layer or bm.verts.layers.float.new(_PLANE_Y_LAYER)
        z_layer = z_layer or bm.verts.layers.float.new(_PLANE_Z_LAYER)
    return mask, x_layer, y_layer, z_layer


def clear_planar_lock_on_vertices(bm, verts):
    mask_layer, _x, _y, _z = _planar_layers(bm, create=False)
    if mask_layer is None:
        return
    for vert in verts:
        if vert.is_valid:
            vert[mask_layer] = 0


def _planned_move_blocked(obj, bm, vert, new_local):
    if vert.index in operators_vertex_locks._locked_indices(obj, only_enabled=True):
        if (new_local - vert.co).length_squared > 1.0e-18:
            return 'Vertex Locks'

    mask_layer, x_layer, y_layer, z_layer = _planar_layers(bm, create=False)
    if mask_layer is None:
        return None
    mask = int(vert[mask_layer])
    if not mask:
        return None
    saved = (
        float(vert[x_layer]) if x_layer is not None else vert.co.x,
        float(vert[y_layer]) if y_layer is not None else vert.co.y,
        float(vert[z_layer]) if z_layer is not None else vert.co.z,
    )
    for axis, bit in enumerate(_AXIS_BITS):
        if mask & bit and abs(new_local[axis] - saved[axis]) > 1.0e-8:
            return 'Plane Lock'
    return None


def _apply_plan(plans):
    for obj, bm, entries in plans:
        for vert, new_local in entries:
            vert.co = new_local
        bm.normal_update()
        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=False)


def _shape_key_preflight(objects):
    for obj in objects:
        keys = getattr(obj.data, 'shape_keys', None)
        if keys and len(keys.key_blocks) > 1:
            raise PrecisionEditError(f'{obj.name}: precision edit tools are disabled on meshes with multiple shape keys.')
