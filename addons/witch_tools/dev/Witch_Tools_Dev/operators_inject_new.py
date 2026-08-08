import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector

from . import operators_planar_edit, operators_vertex_locks
from . import precision_edit_common as precision_edit
from . import precision_edit_drag as drag
from . import precision_edit_topology as topology
from .operators_curvature_sync import _restore_lock_references, _snapshot_lock_references


_EPSILON = 1.0e-9


class InjectNewError(RuntimeError):
    pass


def _active_edit_mesh(context):
    obj = getattr(context, 'active_object', None)
    if not obj or obj.type != 'MESH' or obj.mode != 'EDIT':
        raise InjectNewError('Enter Mesh Edit Mode on one active mesh object.')
    return obj


def _axis_mask(props):
    return drag.axis_mask(props.inject_new_axis_x, props.inject_new_axis_y, props.inject_new_axis_z)


class WT_OT_inject_new_capture_rail_end(Operator):
    bl_idname = 'mesh.wt_inject_new_capture_rail_end'
    bl_label = 'Capture Rail End'
    bl_description = (
        'Capture one vertex, edge midpoint, or face center as a straight Rail endpoint. '
        'Rail placement remains constrained to that exact source-to-end line.'
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
        props.inject_new_rail_target_label = 'No rail endpoint captured'
        props.inject_new_last_report = 'Rail endpoint cleared.'
        return {'FINISHED'}


class WT_OT_inject_new(Operator):
    bl_idname = 'mesh.wt_inject_new'
    bl_label = 'Inject New'
    bl_description = (
        'Create new topology and place it with the mouse. Solo leaves the copy disconnected; '
        'Branch connects source-to-copy vertices; Slide inserts one or more vertices into selected edges. '
        'Magnetic Snap can lock placement to hovered vertices, edges, or faces.'
    )
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    _obj = None
    _bm = None
    _created_verts = None
    _created_edges = None
    _created_faces = None
    _created_geom = None
    _source_verts = None
    _source_element = None
    _branch_edges = None
    _initial_local = None
    _initial_world = None
    _anchor_world = None
    _rail_start_world = None
    _rail_end_world = None
    _slide_records = None
    _slide_driver_index = 0
    _lock_snapshot = None
    _old_vertex_guard_suspended = False
    _old_planar_guard_suspended = False
    _mode = None
    _element_type = None
    _region = None
    _rv3d = None
    _highlighter = None
    _snap_target = None
    _snap_contacts = None
    _orbiting = False
    _finished = False

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

    def _stop_visuals(self, context):
        if self._highlighter is not None:
            self._highlighter.stop()
            self._highlighter = None
        if context.area:
            try:
                context.area.header_text_set(None)
                context.area.tag_redraw()
            except Exception:
                pass

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
        props = context.scene.wt_precision_edit
        if props.inject_new_mode != 'SLIDE' and not props.inject_new_use_rail and not any(_axis_mask(props)):
            raise InjectNewError('Enable at least one X/Y/Z movement axis.')
        return obj

    def _clear_new_plane_locks(self, verts):
        precision_edit.clear_planar_lock_on_vertices(self._bm, verts)

    def _setup_slide(self, context):
        props = context.scene.wt_precision_edit
        if props.inject_new_element_type != 'VERT':
            raise InjectNewError('Slide injects vertices, so the new element is Vertex.')
        edges = [edge for edge in self._bm.edges if edge.select and edge.is_valid and not edge.hide]
        if not edges:
            raise InjectNewError('Slide mode requires one or more selected source edges.')

        reference_start = self._obj.matrix_world @ edges[0].verts[0].co
        reference_end = self._obj.matrix_world @ edges[0].verts[1].co
        reference_direction = reference_end - reference_start
        if reference_direction.length <= _EPSILON:
            raise InjectNewError('A selected slide edge has zero length.')
        reference_direction.normalize()

        records = []
        created = []
        for edge in edges:
            first, second = edge.verts
            first_world = self._obj.matrix_world @ first.co
            second_world = self._obj.matrix_world @ second.co
            direction = second_world - first_world
            if direction.length <= _EPSILON:
                raise InjectNewError('A selected slide edge has zero length.')
            if direction.normalized().dot(reference_direction) < 0.0:
                first, second = second, first
                first_world, second_world = second_world, first_world

            _new_edge, new_vert = bmesh.utils.edge_split(edge, first, 0.5)
            self._clear_new_plane_locks([new_vert])
            records.append({
                'new_vert': new_vert,
                'start_vert': first,
                'end_vert': second,
                'start_world': first_world,
                'end_world': second_world,
            })
            created.append(new_vert)

        self._slide_records = records
        self._created_verts = created
        self._created_edges = []
        self._created_faces = []
        self._created_geom = list(created)
        self._source_verts = [record['start_vert'] for record in records] + [record['end_vert'] for record in records]
        self._initial_local = {vert: vert.co.copy() for vert in created}
        self._initial_world = {vert: self._obj.matrix_world @ vert.co for vert in created}
        self._anchor_world = sum((self._obj.matrix_world @ vert.co for vert in created), Vector()) / len(created)
        self._mode = 'SLIDE'
        self._element_type = 'VERT'

    def _setup_duplicate(self, context):
        props = context.scene.wt_precision_edit
        element_type = props.inject_new_element_type
        element = topology.source_element_from_selection(self._bm, element_type)
        anchor_world = topology.world_point(self._obj, element_type, element)

        if props.inject_new_use_rail:
            if not props.inject_new_rail_end_set:
                raise InjectNewError('Capture a Rail endpoint before enabling Rail.')
            rail_end = Vector(props.inject_new_rail_end)
            if (rail_end - anchor_world).length <= _EPSILON:
                raise InjectNewError('The captured Rail endpoint is the same as the source point.')
            self._rail_start_world = anchor_world.copy()
            self._rail_end_world = rail_end

        result = topology.duplicate_source(
            self._bm,
            element_type,
            element,
            make_branch=props.inject_new_mode == 'BRANCH',
        )
        self._clear_new_plane_locks(result['created_verts'])
        self._source_element = element
        self._source_verts = result['source_verts']
        self._created_verts = result['created_verts']
        self._created_edges = result['created_edges']
        self._created_faces = result['created_faces']
        self._created_geom = result['created_geom']
        self._branch_edges = result['branch_edges']
        self._initial_local = {vert: vert.co.copy() for vert in self._created_verts}
        self._initial_world = {vert: self._obj.matrix_world @ vert.co for vert in self._created_verts}
        self._anchor_world = anchor_world
        self._mode = props.inject_new_mode
        self._element_type = element_type

    def _reset_created(self):
        if self._mode == 'SLIDE':
            return
        for vert, local in self._initial_local.items():
            if vert.is_valid:
                vert.co = local.copy()

    def _set_duplicate_world_delta(self, delta_world):
        inverse = self._obj.matrix_world.inverted_safe()
        for vert in self._created_verts:
            if not vert.is_valid:
                continue
            initial_world = self._initial_world[vert]
            vert.co = inverse @ (initial_world + delta_world)

    def _current_center_world(self):
        points = [self._obj.matrix_world @ vert.co for vert in (self._created_verts or ()) if vert.is_valid]
        if not points:
            return self._anchor_world
        return sum(points, Vector()) / len(points)

    def _pick_target(self, mouse):
        exclude_verts = set(self._created_verts or ()) | set(self._source_verts or ())
        exclude_edges = set(self._created_edges or ()) | set(self._branch_edges or ())
        exclude_faces = set(self._created_faces or ())
        return drag.pick_mesh_element(
            self._obj,
            self._bm,
            self._region,
            self._rv3d,
            mouse,
            allowed=('VERT', 'EDGE', 'FACE'),
            exclude_verts=exclude_verts,
            exclude_edges=exclude_edges,
            exclude_faces=exclude_faces,
        )

    def _target_protection_reason(self, target):
        if target is None or target.element is None:
            return None
        verts = [target.element] if target.kind == 'VERT' else list(target.element.verts)
        locked = set(operators_vertex_locks._locked_indices(self._obj, only_enabled=True))
        if any(vert.index in locked for vert in verts if vert.is_valid):
            return 'Vertex Locks protect the magnetic merge target.'
        mask_layer, _x, _y, _z = precision_edit._planar_layers(self._bm, create=False)
        if mask_layer is not None and any(int(vert[mask_layer]) for vert in verts if vert.is_valid):
            return 'Plane Lock protects the magnetic merge target.'
        return None

    def _update_slide(self, mouse):
        best = None
        factor = 0.5
        for index, record in enumerate(self._slide_records):
            p0 = drag._screen_point(self._region, self._rv3d, record['start_world'])
            p1 = drag._screen_point(self._region, self._rv3d, record['end_world'])
            if p0 is None or p1 is None:
                continue
            _closest, candidate_factor, distance = drag._point_segment_2d(Vector(mouse), p0, p1)
            if best is None or distance < best[0]:
                best = (distance, index, candidate_factor)
        if best is not None:
            _distance, self._slide_driver_index, factor = best
        else:
            record = self._slide_records[self._slide_driver_index]
            factor = drag.project_rail_factor(
                self._region,
                self._rv3d,
                record['start_world'],
                record['end_world'],
                mouse,
            )

        factor = max(0.001, min(0.999, factor))
        inverse = self._obj.matrix_world.inverted_safe()
        for record in self._slide_records:
            target_world = record['start_world'].lerp(record['end_world'], factor)
            record['new_vert'].co = inverse @ target_world

        driver = self._slide_records[self._slide_driver_index]
        self._highlighter.set_target(None)
        self._highlighter.set_virtual_lines([(driver['start_world'], driver['end_world'])])
        self._snap_target = None
        self._snap_contacts = None

    def _update_duplicate(self, context, mouse):
        props = context.scene.wt_precision_edit
        self._reset_created()
        self._highlighter.set_virtual_lines(())

        if props.inject_new_use_rail:
            factor = drag.project_rail_factor(
                self._region,
                self._rv3d,
                self._rail_start_world,
                self._rail_end_world,
                mouse,
            )
            factor = max(0.0, min(1.0, factor))
            target_anchor = self._rail_start_world.lerp(self._rail_end_world, factor)
            base_delta = target_anchor - self._anchor_world
        else:
            target_anchor = drag.project_mouse_anchor(
                self._region,
                self._rv3d,
                self._anchor_world,
                mouse,
                _axis_mask(props),
            )
            base_delta = target_anchor - self._anchor_world

        self._set_duplicate_world_delta(base_delta)
        target = self._pick_target(mouse) if props.inject_new_magnetic_snap else None
        self._snap_target = target
        self._highlighter.set_target(target)
        self._snap_contacts = None

        if target is None or props.inject_new_use_rail:
            return

        mask = _axis_mask(props)
        if target.kind in {'VERT', 'EDGE'}:
            snap_delta, contacts = drag.rigid_snap_delta(self._obj, self._created_verts, target, mask)
            if snap_delta is not None:
                self._set_duplicate_world_delta(base_delta + snap_delta)
                self._snap_contacts = contacts
            return

        direction = drag.masked_vector(target.point_world - self._anchor_world, mask)
        if direction.length <= _EPSILON:
            direction = base_delta
        hits = drag.face_travel_hits(self._obj, target.element, self._initial_world, direction)
        if not hits:
            return
        inverse = self._obj.matrix_world.inverted_safe()
        contacts = []
        for vert, point in hits.items():
            if vert.is_valid:
                vert.co = inverse @ point
                kind, element, contact_point = drag.boundary_contact(
                    self._obj,
                    target.element,
                    point,
                    tolerance=1.0e-5,
                )
                contacts.append((vert, kind, element, contact_point))
        self._snap_contacts = contacts

    def _update_from_mouse(self, context, event):
        mouse = drag.mouse_xy(event, self._region)
        if self._mode == 'SLIDE':
            self._update_slide(mouse)
        else:
            self._update_duplicate(context, mouse)
        self._bm.normal_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=False)
        if context.area:
            context.area.tag_redraw()

    def _select_survivors(self):
        for vert in self._bm.verts:
            vert.select_set(False)
        for edge in self._bm.edges:
            edge.select_set(False)
        for face in self._bm.faces:
            face.select_set(False)

        selected_any = False
        for item in self._created_geom or ():
            if getattr(item, 'is_valid', False):
                try:
                    item.select_set(True)
                    selected_any = True
                except Exception:
                    pass
        if not selected_any and self._snap_contacts:
            for _created, kind, element, _point in self._snap_contacts:
                if kind == 'VERT' and getattr(element, 'is_valid', False):
                    element.select_set(True)
                elif kind == 'EDGE' and getattr(element, 'is_valid', False):
                    for vert in element.verts:
                        vert.select_set(True)

    def _apply_auto_merge(self, context):
        props = context.scene.wt_precision_edit
        if self._mode != 'BRANCH' or not props.inject_new_auto_merge or not self._snap_contacts:
            return
        reason = self._target_protection_reason(self._snap_target)
        if reason:
            raise InjectNewError(reason)
        face_target = self._snap_target.element if self._snap_target and self._snap_target.kind == 'FACE' else None
        drag.weld_contacts(
            self._bm,
            self._obj,
            self._snap_contacts,
            face_target=face_target,
            tolerance=1.0e-6,
        )

    def _finish(self, context):
        self._apply_auto_merge(context)
        self._bm.normal_update()
        topology.validate_no_zero_geometry(self._bm)
        _restore_lock_references(self._obj, self._bm, self._lock_snapshot)
        self._select_survivors()
        self._bm.verts.index_update()
        self._bm.edges.index_update()
        self._bm.faces.index_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)
        self._restore_guards()
        self._stop_visuals(context)
        self._finished = True

        props = context.scene.wt_precision_edit
        if self._mode == 'SLIDE':
            count = len(self._slide_records or ())
            props.inject_new_last_report = f'Injected {count} slide vertex{"es" if count != 1 else ""} at a shared rail position.'
        else:
            snap_label = ''
            if self._snap_target is not None:
                snap_label = f' • snapped to {self._snap_target.kind.title()}'
            if self._mode == 'BRANCH' and props.inject_new_auto_merge and self._snap_contacts:
                snap_label += ' • auto-merged'
            props.inject_new_last_report = f'Injected {self._element_type.title()} in {self._mode.title()} mode{snap_label}.'
        self.report({'INFO'}, props.inject_new_last_report)
        return {'FINISHED'}

    def _cancel(self, context, message=None):
        try:
            if self._mode == 'SLIDE':
                for record in reversed(self._slide_records or ()):
                    vert = record['new_vert']
                    if vert and vert.is_valid:
                        bmesh.ops.dissolve_verts(
                            self._bm,
                            verts=[vert],
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
        self._stop_visuals(context)
        props = context.scene.wt_precision_edit
        if message:
            props.inject_new_last_report = f'Blocked: {message}'
            self.report({'ERROR'}, message)
        else:
            props.inject_new_last_report = 'Inject New cancelled.'
        return {'CANCELLED'}

    def invoke(self, context, event):
        props = context.scene.wt_precision_edit
        self._created_verts = []
        self._created_edges = []
        self._created_faces = []
        self._created_geom = []
        self._source_verts = []
        self._branch_edges = []
        self._slide_records = []
        self._snap_contacts = None
        self._snap_target = None
        self._finished = False
        self._orbiting = False
        try:
            self._obj = self._validate_common(context)
            self._bm = topology.prepare_bmesh(self._obj)
            self._lock_snapshot = _snapshot_lock_references(self._obj, self._bm)
            self._suspend_guards()
            if props.inject_new_mode == 'SLIDE':
                self._setup_slide(context)
            else:
                self._setup_duplicate(context)

            self._highlighter = drag.HoverHighlighter()
            self._highlighter.start()
            self._bm.normal_update()
            bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)
            self._update_from_mouse(context, event)
        except (InjectNewError, precision_edit.PrecisionEditError, topology.PrecisionTopologyError, drag.DragSnapError) as error:
            if self._bm is not None and self._created_verts:
                return self._cancel(context, str(error))
            self._restore_guards()
            self._stop_visuals(context)
            props.inject_new_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            if self._bm is not None and self._created_verts:
                return self._cancel(context, f'Inject New failed: {error}')
            self._restore_guards()
            self._stop_visuals(context)
            props.inject_new_last_report = f'Blocked: Inject New failed: {error}'
            self.report({'ERROR'}, f'Inject New failed: {error}')
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        if context.area:
            context.area.header_text_set(
                'Inject New: move to place • Magnetic target highlights • MMB orbit around injection • '
                'Left Click/Enter confirm • Esc/Right Click cancel'
            )
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'MIDDLEMOUSE':
            if event.value == 'PRESS':
                self._orbiting = True
                drag.set_orbit_pivot(self._rv3d, self._current_center_world())
                return {'PASS_THROUGH'}
            if event.value == 'RELEASE':
                self._orbiting = False
                return {'PASS_THROUGH'}
        if self._orbiting:
            return {'PASS_THROUGH'}

        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            return self._cancel(context)

        if event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
            try:
                return self._finish(context)
            except (InjectNewError, topology.PrecisionTopologyError, drag.DragSnapError) as error:
                return self._cancel(context, str(error))
            except Exception as error:
                return self._cancel(context, f'Inject New failed: {error}')

        if event.type == 'MOUSEMOVE':
            try:
                self._update_from_mouse(context, event)
            except (InjectNewError, topology.PrecisionTopologyError, drag.DragSnapError) as error:
                return self._cancel(context, str(error))
            except Exception as error:
                return self._cancel(context, f'Inject New failed: {error}')
            return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if not self._finished:
            self._cancel(context)


CLASSES = (
    WT_OT_inject_new_capture_rail_end,
    WT_OT_inject_new_clear_rail,
    WT_OT_inject_new,
)
