import bpy
import bmesh
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Vector

from . import operators_planar_edit, operators_vertex_locks
from . import precision_edit_common as precision_edit
from .operators_curvature_sync import _restore_lock_references, _snapshot_lock_references


_EPSILON = 1.0e-9


class InjectNewError(RuntimeError):
    pass


def _active_edit_mesh(context):
    obj = getattr(context, 'active_object', None)
    if not obj or obj.type != 'MESH' or obj.mode != 'EDIT':
        raise InjectNewError('Enter Mesh Edit Mode on one active mesh object.')
    return obj


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


def _selected_source_element(bm, element_type):
    if element_type == 'VERT':
        elements = [vert for vert in bm.verts if vert.select]
        label = 'vertex'
    elif element_type == 'EDGE':
        elements = [edge for edge in bm.edges if edge.select]
        label = 'edge'
    else:
        elements = [face for face in bm.faces if face.select]
        label = 'face'
    if len(elements) != 1:
        raise InjectNewError(f'Select exactly one source {label}.')
    return elements[0]


def _source_closure(element_type, element):
    if element_type == 'VERT':
        return [element], [element]
    if element_type == 'EDGE':
        return [*element.verts, element], list(element.verts)
    geom = [*element.verts, *element.edges, element]
    return geom, list(element.verts)


def _world_point(obj, element_type, element):
    if element_type == 'VERT':
        local = element.co
    elif element_type == 'EDGE':
        local = (element.verts[0].co + element.verts[1].co) * 0.5
    else:
        local = element.calc_center_median()
    return obj.matrix_world @ local


def _match_duplicate_verts(source_verts, duplicate_verts):
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
            raise InjectNewError('Could not map duplicated vertices back to the source geometry.')
        mapping[source] = best
        unused.remove(best)
    return mapping


def _project_axis_parameter(region, rv3d, anchor_world, axis_world, mouse_xy):
    p0 = view3d_utils.location_3d_to_region_2d(region, rv3d, anchor_world)
    p1 = view3d_utils.location_3d_to_region_2d(region, rv3d, anchor_world + axis_world)
    if p0 is None or p1 is None:
        raise InjectNewError('The source is not projectable in the current 3D view.')
    screen_axis = p1 - p0
    denom = screen_axis.length_squared
    if denom <= 1.0e-8:
        raise InjectNewError('The chosen axis points almost directly at the camera. Orbit the view slightly and try again.')
    mouse = Vector(mouse_xy)
    return (mouse - p0).dot(screen_axis) / denom


def _project_rail_factor(region, rv3d, start_world, end_world, mouse_xy):
    p0 = view3d_utils.location_3d_to_region_2d(region, rv3d, start_world)
    p1 = view3d_utils.location_3d_to_region_2d(region, rv3d, end_world)
    if p0 is None or p1 is None:
        raise InjectNewError('The rail is not projectable in the current 3D view.')
    screen_rail = p1 - p0
    denom = screen_rail.length_squared
    if denom <= 1.0e-8:
        raise InjectNewError('The rail points almost directly at the camera. Orbit the view slightly and try again.')
    mouse = Vector(mouse_xy)
    return (mouse - p0).dot(screen_rail) / denom


class WT_OT_inject_new_capture_rail_end(Operator):
    bl_idname = 'mesh.wt_inject_new_capture_rail_end'
    bl_label = 'Capture Rail End'
    bl_description = (
        'Capture one vertex, edge midpoint, or face center as the Rail endpoint. '
        'For Solo/Branch, the injected copy slides between the source and this point.'
    )
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = context.scene.wt_precision_edit
        try:
            kind, obj, _element, point = precision_edit.capture_selected_point_world(context)
        except Exception as error:
            props.inject_new_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        props.inject_new_rail_end = point
        props.inject_new_rail_end_set = True
        props.inject_new_rail_target_label = f'{obj.name} / {kind.title()}'
        props.inject_new_last_report = f'Captured rail end: {props.inject_new_rail_target_label}.'
        try:
            precision_edit.clear_current_edit_selection(context)
        except Exception:
            pass
        self.report({'INFO'}, props.inject_new_last_report)
        return {'FINISHED'}


class WT_OT_inject_new_clear_rail(Operator):
    bl_idname = 'mesh.wt_inject_new_clear_rail'
    bl_label = 'Clear Rail End'
    bl_description = 'Clear the captured Inject New Rail endpoint.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.wt_precision_edit
        props.inject_new_rail_end_set = False
        props.inject_new_rail_target_label = 'No rail end captured'
        props.inject_new_last_report = 'Rail end cleared.'
        return {'FINISHED'}


class WT_OT_inject_new(Operator):
    bl_idname = 'mesh.wt_inject_new'
    bl_label = 'Inject New'
    bl_description = (
        'Create a new editable copy and place it interactively. Solo leaves it disconnected; Branch adds source-to-copy edges; '
        'Slide inserts one new vertex into exactly one selected edge. Move the mouse and left-click/Enter to place; Esc/right-click cancels.'
    )
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    _obj = None
    _bm = None
    _created_verts = None
    _created_geom = None
    _source_verts = None
    _branch_edges = None
    _initial_local = None
    _anchor_world = None
    _rail_start_world = None
    _rail_end_world = None
    _slide_vert = None
    _slide_edge_verts = None
    _lock_snapshot = None
    _old_vertex_guard_suspended = False
    _old_planar_guard_suspended = False
    _mode = None
    _move = None
    _region = None
    _rv3d = None

    @classmethod
    def poll(cls, context):
        return bool(
            context.mode == 'EDIT_MESH'
            and context.active_object
            and context.active_object.type == 'MESH'
            and context.area
            and context.area.type == 'VIEW_3D'
        )

    def _suspend_guards(self):
        self._old_vertex_guard_suspended = operators_vertex_locks._GUARD_SUSPENDED
        self._old_planar_guard_suspended = operators_planar_edit._GUARD_SUSPENDED
        operators_vertex_locks._GUARD_SUSPENDED = True
        operators_planar_edit._GUARD_SUSPENDED = True

    def _restore_guards(self):
        operators_vertex_locks._GUARD_SUSPENDED = self._old_vertex_guard_suspended
        operators_planar_edit._GUARD_SUSPENDED = self._old_planar_guard_suspended

    def _validate_common(self, context):
        obj = _active_edit_mesh(context)
        if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks) > 1:
            raise InjectNewError('Inject New is disabled on meshes with multiple shape keys.')
        if context.area is None or context.area.type != 'VIEW_3D' or context.space_data is None:
            raise InjectNewError('Run Inject New from a 3D View.')
        self._region = next((region for region in context.area.regions if region.type == 'WINDOW'), None)
        self._rv3d = getattr(context.space_data, 'region_3d', None)
        if self._region is None or self._rv3d is None:
            raise InjectNewError('The active 3D View has no usable window region.')
        return obj

    def _setup_slide(self, context, obj, bm):
        props = context.scene.wt_precision_edit
        if props.inject_new_element_type != 'VERT':
            raise InjectNewError('Slide injects a new vertex, so choose the Vertex element icon.')
        edges = [edge for edge in bm.edges if edge.select]
        if len(edges) != 1:
            raise InjectNewError('Slide mode requires exactly one selected source edge.')
        edge = edges[0]
        start_vert, end_vert = edge.verts
        start_world = obj.matrix_world @ start_vert.co
        end_world = obj.matrix_world @ end_vert.co
        if (end_world - start_world).length <= _EPSILON:
            raise InjectNewError('The selected slide edge has zero length.')

        _new_edge, new_vert = bmesh.utils.edge_split(edge, start_vert, 0.5)
        precision_edit.clear_planar_lock_on_vertices(bm, [new_vert])

        self._created_verts = [new_vert]
        self._created_geom = [new_vert]
        self._slide_vert = new_vert
        self._slide_edge_verts = (start_vert, end_vert)
        self._rail_start_world = start_world
        self._rail_end_world = end_world
        self._anchor_world = (start_world + end_world) * 0.5
        self._initial_local = {new_vert: new_vert.co.copy()}
        self._move = 'RAIL'
        self._mode = 'SLIDE'

    def _setup_duplicate(self, context, obj, bm):
        props = context.scene.wt_precision_edit
        element_type = props.inject_new_element_type
        element = _selected_source_element(bm, element_type)
        source_geom, source_verts = _source_closure(element_type, element)
        anchor_world = _world_point(obj, element_type, element)

        rail_end = None
        if props.inject_new_move == 'RAIL':
            if not props.inject_new_rail_end_set:
                raise InjectNewError('Capture a Rail endpoint before using Rail movement.')
            rail_end = Vector(props.inject_new_rail_end)
            if (rail_end - anchor_world).length <= _EPSILON:
                raise InjectNewError('The captured Rail endpoint is the same as the source point.')

        result = bmesh.ops.duplicate(bm, geom=source_geom)
        duplicate_geom = [item for item in result.get('geom', ()) if getattr(item, 'is_valid', False)]
        duplicate_verts = [item for item in duplicate_geom if isinstance(item, bmesh.types.BMVert)]
        if len(duplicate_verts) != len(source_verts):
            raise InjectNewError('Blender did not create the expected number of duplicated vertices.')

        vert_map = result.get('vert_map') or result.get('isovert_map') or {}
        mapped = {source: vert_map.get(source) for source in source_verts if vert_map.get(source) in duplicate_verts}
        if len(mapped) != len(source_verts):
            mapped = _match_duplicate_verts(source_verts, duplicate_verts)

        precision_edit.clear_planar_lock_on_vertices(bm, duplicate_verts)

        branch_edges = []
        if props.inject_new_mode == 'BRANCH':
            for source in source_verts:
                duplicate = mapped[source]
                existing = bm.edges.get((source, duplicate))
                if existing is None:
                    try:
                        existing = bm.edges.new((source, duplicate))
                    except ValueError:
                        existing = bm.edges.get((source, duplicate))
                if existing is not None:
                    branch_edges.append(existing)

        self._created_verts = duplicate_verts
        self._created_geom = duplicate_geom
        self._source_verts = source_verts
        self._branch_edges = branch_edges
        self._initial_local = {vert: vert.co.copy() for vert in duplicate_verts}
        self._anchor_world = anchor_world
        self._mode = props.inject_new_mode
        self._move = props.inject_new_move

        if self._move == 'RAIL':
            self._rail_start_world = anchor_world.copy()
            self._rail_end_world = rail_end

    def _set_duplicate_world_delta(self, delta_world):
        inverse = self._obj.matrix_world.inverted_safe()
        for vert in self._created_verts:
            initial_world = self._obj.matrix_world @ self._initial_local[vert]
            vert.co = inverse @ (initial_world + delta_world)

    def _update_from_mouse(self, context, event):
        mouse_xy = (event.mouse_x - self._region.x, event.mouse_y - self._region.y)
        if self._mode == 'SLIDE' or self._move == 'RAIL':
            factor = _project_rail_factor(
                self._region,
                self._rv3d,
                self._rail_start_world,
                self._rail_end_world,
                mouse_xy,
            )
            if self._mode == 'SLIDE':
                factor = max(0.001, min(0.999, factor))
                target_world = self._rail_start_world.lerp(self._rail_end_world, factor)
                self._slide_vert.co = self._obj.matrix_world.inverted_safe() @ target_world
            else:
                factor = max(0.0, min(1.0, factor))
                target_anchor = self._rail_start_world.lerp(self._rail_end_world, factor)
                self._set_duplicate_world_delta(target_anchor - self._anchor_world)
        else:
            axis_index = {'X': 0, 'Y': 1, 'Z': 2}[self._move]
            axis = Vector((1.0 if axis_index == 0 else 0.0, 1.0 if axis_index == 1 else 0.0, 1.0 if axis_index == 2 else 0.0))
            distance = _project_axis_parameter(
                self._region,
                self._rv3d,
                self._anchor_world,
                axis,
                mouse_xy,
            )
            self._set_duplicate_world_delta(axis * distance)

        self._bm.normal_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=False)

    def _select_created(self):
        for vert in self._bm.verts:
            vert.select_set(False)
        for edge in self._bm.edges:
            edge.select_set(False)
        for face in self._bm.faces:
            face.select_set(False)
        for item in self._created_geom or ():
            if getattr(item, 'is_valid', False):
                try:
                    item.select_set(True)
                except Exception:
                    pass
        if self._slide_vert and self._slide_vert.is_valid:
            self._slide_vert.select_set(True)

    def _finish(self, context):
        self._bm.normal_update()
        for face in self._bm.faces:
            if face.is_valid and face.calc_area() <= 1.0e-16:
                raise InjectNewError('The operation would leave a zero-area face.')
        _restore_lock_references(self._obj, self._bm, self._lock_snapshot)
        self._select_created()
        self._bm.verts.index_update()
        self._bm.edges.index_update()
        self._bm.faces.index_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)
        self._restore_guards()
        context.scene.wt_precision_edit.inject_new_last_report = (
            'Injected vertex on the selected edge.'
            if self._mode == 'SLIDE'
            else f'Injected {context.scene.wt_precision_edit.inject_new_element_type.title()} in {self._mode.title()} mode.'
        )
        self.report({'INFO'}, context.scene.wt_precision_edit.inject_new_last_report)
        if context.area:
            context.area.header_text_set(None)
        return {'FINISHED'}

    def _cancel(self, context, message=None):
        try:
            if self._mode == 'SLIDE':
                if self._slide_vert and self._slide_vert.is_valid:
                    bmesh.ops.dissolve_verts(
                        self._bm,
                        verts=[self._slide_vert],
                        use_face_split=False,
                        use_boundary_tear=False,
                    )
            else:
                valid_new = [vert for vert in (self._created_verts or ()) if vert.is_valid]
                if valid_new:
                    bmesh.ops.delete(self._bm, geom=valid_new, context='VERTS')
            _restore_lock_references(self._obj, self._bm, self._lock_snapshot)
            self._bm.normal_update()
            bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)
        except Exception:
            pass
        self._restore_guards()
        if context.area:
            context.area.header_text_set(None)
        if message:
            context.scene.wt_precision_edit.inject_new_last_report = f'Blocked: {message}'
            self.report({'ERROR'}, message)
        else:
            context.scene.wt_precision_edit.inject_new_last_report = 'Inject New cancelled.'
        return {'CANCELLED'}

    def invoke(self, context, event):
        props = context.scene.wt_precision_edit
        try:
            self._obj = self._validate_common(context)
            self._bm = _prepare_bmesh(self._obj)
            self._lock_snapshot = _snapshot_lock_references(self._obj, self._bm)
            self._suspend_guards()

            if props.inject_new_mode == 'SLIDE':
                self._setup_slide(context, self._obj, self._bm)
            else:
                self._setup_duplicate(context, self._obj, self._bm)

            self._bm.normal_update()
            bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)
            self._update_from_mouse(context, event)
        except (InjectNewError, precision_edit.PrecisionEditError) as error:
            if self._bm is not None and self._created_verts:
                return self._cancel(context, str(error))
            self._restore_guards()
            props.inject_new_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            if self._bm is not None and self._created_verts:
                return self._cancel(context, f'Inject New failed: {error}')
            self._restore_guards()
            props.inject_new_last_report = f'Blocked: Inject New failed: {error}'
            self.report({'ERROR'}, f'Inject New failed: {error}')
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        if context.area:
            context.area.header_text_set('Inject New: move mouse to place • Left Click/Enter confirm • Esc/Right Click cancel')
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            return self._cancel(context)

        if event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
            try:
                return self._finish(context)
            except InjectNewError as error:
                return self._cancel(context, str(error))
            except Exception as error:
                return self._cancel(context, f'Inject New failed: {error}')

        if event.type == 'MOUSEMOVE':
            try:
                self._update_from_mouse(context, event)
            except InjectNewError as error:
                return self._cancel(context, str(error))
            except Exception as error:
                return self._cancel(context, f'Inject New failed: {error}')
            return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}


CLASSES = (
    WT_OT_inject_new_capture_rail_end,
    WT_OT_inject_new_clear_rail,
    WT_OT_inject_new,
)
