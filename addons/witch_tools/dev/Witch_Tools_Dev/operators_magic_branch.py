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
_DRAG_THRESHOLD = 4.0


class MagicBranchError(RuntimeError):
    pass


def _active_edit_mesh(context):
    obj = getattr(context, 'active_object', None)
    if not obj or obj.type != 'MESH' or obj.mode != 'EDIT':
        raise MagicBranchError('Enter Mesh Edit Mode on one active mesh object.')
    if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks) > 1:
        raise MagicBranchError('Magic Branch is disabled on meshes with multiple shape keys.')
    return obj


def _inside_region(event, region):
    return region.x <= event.mouse_x < region.x + region.width and region.y <= event.mouse_y < region.y + region.height


def _select_only(bm, element):
    for vert in bm.verts:
        vert.select_set(False)
    for edge in bm.edges:
        edge.select_set(False)
    for face in bm.faces:
        face.select_set(False)
    if element is not None and getattr(element, 'is_valid', False):
        element.select_set(True)
        if isinstance(element, bmesh.types.BMEdge):
            for vert in element.verts:
                vert.select_set(True)
        elif isinstance(element, bmesh.types.BMFace):
            for vert in element.verts:
                vert.select_set(True)
            for edge in element.edges:
                edge.select_set(True)
        bm.select_history.clear()
        try:
            bm.select_history.add(element)
        except Exception:
            pass


def _world_center(obj, verts):
    valid = [vert for vert in verts or () if getattr(vert, 'is_valid', False)]
    if not valid:
        return None
    matrix = obj.matrix_world
    return sum((matrix @ vert.co for vert in valid), Vector()) / len(valid)


def _best_face_edge(obj, face, region, rv3d, mouse):
    center_world = obj.matrix_world @ face.calc_center_median()
    center_screen = drag._screen_point(region, rv3d, center_world)
    if center_screen is None:
        return face.edges[0]
    mouse_vec = Vector(mouse) - center_screen
    if mouse_vec.length <= _EPSILON:
        return face.edges[0]
    mouse_dir = mouse_vec.normalized()
    best = None
    for edge in face.edges:
        midpoint = (edge.verts[0].co + edge.verts[1].co) * 0.5
        edge_screen = drag._screen_point(region, rv3d, obj.matrix_world @ midpoint)
        if edge_screen is None:
            continue
        radial = edge_screen - center_screen
        if radial.length <= _EPSILON:
            continue
        score = radial.normalized().dot(mouse_dir)
        if best is None or score > best[0]:
            best = (score, edge)
    return best[1] if best is not None else face.edges[0]


def _target_protection_reason(obj, bm, target):
    if target is None or target.element is None or not getattr(target.element, 'is_valid', False):
        return None
    verts = [target.element] if target.kind == 'VERT' else list(target.element.verts)
    locked = set(operators_vertex_locks._locked_indices(obj, only_enabled=True))
    if any(vert.index in locked for vert in verts):
        return 'Magnetic Auto-Merge target is protected by Vertex Locks.'
    mask_layer, _x, _y, _z = precision_edit._planar_layers(bm, create=False)
    if mask_layer is not None and any(int(vert[mask_layer]) for vert in verts):
        return 'Magnetic Auto-Merge target is protected by Plane Lock.'
    return None


class WT_OT_magic_branch_toggle_persistent(Operator):
    bl_idname = 'mesh.wt_magic_branch_toggle_persistent'
    bl_label = 'Toggle Persistent Magic Branch'
    bl_description = 'Toggle whether Magic Branch stays armed after each completed branch. This operator can be assigned to any Blender hotkey.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.wt_precision_edit
        props.magic_branch_persistent = not props.magic_branch_persistent
        state = 'Persistent' if props.magic_branch_persistent else 'Single Branch'
        props.magic_branch_last_report = f'Magic Branch mode: {state}.'
        self.report({'INFO'}, props.magic_branch_last_report)
        return {'FINISHED'}


class WT_OT_magic_branch(Operator):
    bl_idname = 'mesh.wt_magic_branch'
    bl_label = 'Start Magic Branch'
    bl_description = (
        'Arm drag-and-drop mesh branching. Click-drag a source vertex, edge, or face in the viewport. '
        'Persistent mode stays armed after a completed branch; Single Branch exits after one commit.'
    )
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    _obj = None
    _bm = None
    _region = None
    _rv3d = None
    _highlighter = None
    _state = 'WAITING'
    _pressed_source = None
    _press_mouse = None
    _source_kind = None
    _source_element = None
    _source_edge = None
    _branch_data = None
    _initial_local = None
    _anchor_world = None
    _contacts = None
    _hover_target = None
    _paver_count = 0
    _orbiting = False
    _lock_snapshot = None
    _old_vertex_guard_suspended = False
    _old_planar_guard_suspended = False

    @classmethod
    def poll(cls, context):
        return bool(
            context.mode == 'EDIT_MESH'
            and context.active_object
            and context.active_object.type == 'MESH'
            and context.area
            and context.area.type == 'VIEW_3D'
        )

    def _props(self, context):
        return context.scene.wt_precision_edit

    def _axes(self, context):
        props = self._props(context)
        mask = drag.axis_mask(props.magic_branch_axis_x, props.magic_branch_axis_y, props.magic_branch_axis_z)
        if not any(mask):
            raise MagicBranchError('Enable at least one Magic Branch movement axis.')
        return mask

    def _suspend_guards(self):
        self._old_vertex_guard_suspended = operators_vertex_locks._GUARD_SUSPENDED
        self._old_planar_guard_suspended = operators_planar_edit._GUARD_SUSPENDED
        operators_vertex_locks._GUARD_SUSPENDED = True
        operators_planar_edit._GUARD_SUSPENDED = True

    def _restore_guards(self):
        operators_vertex_locks._GUARD_SUSPENDED = self._old_vertex_guard_suspended
        operators_planar_edit._GUARD_SUSPENDED = self._old_planar_guard_suspended

    def _set_header(self, context, text=None):
        if context.area:
            context.area.header_text_set(text)

    def _clear_live(self):
        self._state = 'WAITING'
        self._pressed_source = None
        self._press_mouse = None
        self._source_kind = None
        self._source_element = None
        self._source_edge = None
        self._branch_data = None
        self._initial_local = None
        self._anchor_world = None
        self._contacts = None
        self._hover_target = None
        self._paver_count = 0
        if self._highlighter:
            self._highlighter.set_target(None)
            self._highlighter.set_virtual_lines(())

    def _delete_live_geometry(self):
        if self._bm is None or not self._branch_data:
            return
        valid = [vert for vert in self._branch_data.get('created_verts', ()) if getattr(vert, 'is_valid', False)]
        if valid:
            bmesh.ops.delete(self._bm, geom=valid, context='VERTS')
        self._bm.normal_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)

    def _pick_source(self, context, event):
        if not _inside_region(event, self._region):
            return None
        kind = self._props(context).magic_branch_element_type
        return drag.pick_mesh_element(
            self._obj,
            self._bm,
            self._region,
            self._rv3d,
            drag.mouse_xy(event, self._region),
            allowed=(kind,),
        )

    def _begin_drag(self, context, event):
        props = self._props(context)
        if self._pressed_source is None or self._pressed_source.element is None:
            raise MagicBranchError('Click-drag a visible source element in the viewport.')
        self._source_kind = props.magic_branch_element_type
        self._source_element = self._pressed_source.element
        if not getattr(self._source_element, 'is_valid', False):
            raise MagicBranchError('The chosen source geometry is no longer valid.')

        if self._source_kind in {'VERT', 'EDGE'}:
            self._branch_data = topology.duplicate_source(self._bm, self._source_kind, self._source_element, make_branch=True)
            precision_edit.clear_planar_lock_on_vertices(self._bm, self._branch_data['created_verts'])
            self._initial_local = {vert: vert.co.copy() for vert in self._branch_data['created_verts']}
            self._anchor_world = topology.world_point(self._obj, self._source_kind, self._source_element)
        else:
            mouse = drag.mouse_xy(event, self._region)
            self._source_edge = _best_face_edge(self._obj, self._source_element, self._region, self._rv3d, mouse)
            self._rebuild_face_branch(context, event, force=True)

        self._state = 'DRAGGING'
        self._update_drag(context, event)

    def _face_step_local(self, context, source_face, source_edge):
        raw_local = topology.face_edge_outward_vector(source_face, source_edge)
        world_step = self._obj.matrix_world.to_3x3() @ raw_local
        masked_world = drag.masked_vector(world_step, self._axes(context))
        if masked_world.length <= _EPSILON:
            raise MagicBranchError('The selected movement axes collapse this face branch direction to zero.')
        return self._obj.matrix_world.to_3x3().inverted_safe() @ masked_world

    def _rebuild_face_branch(self, context, event, force=False):
        props = self._props(context)
        mouse = drag.mouse_xy(event, self._region)
        edge = _best_face_edge(self._obj, self._source_element, self._region, self._rv3d, mouse)
        if props.magic_branch_face_mode == 'ORGANIC':
            if force or edge is not self._source_edge or not self._branch_data:
                if self._branch_data:
                    self._delete_live_geometry()
                self._source_edge = edge
                self._branch_data = topology.create_organic_face(self._bm, self._source_element, edge)
                precision_edit.clear_planar_lock_on_vertices(self._bm, self._branch_data['created_verts'])
                self._initial_local = {vert: vert.co.copy() for vert in self._branch_data['created_verts']}
                self._anchor_world = self._obj.matrix_world @ ((edge.verts[0].co + edge.verts[1].co) * 0.5)
            return

        step_local = self._face_step_local(context, self._source_element, edge)
        step_world = self._obj.matrix_world.to_3x3() @ step_local
        anchor_world = self._obj.matrix_world @ ((edge.verts[0].co + edge.verts[1].co) * 0.5)
        hover = self._pick_hover(context, event, extra_excludes=False)
        if hover is not None and props.magic_branch_magnetic_snap:
            target_world = hover.point_world
        else:
            target_world = drag.project_mouse_anchor(self._region, self._rv3d, anchor_world, mouse, self._axes(context))
        distance = max(0.0, (Vector(target_world) - anchor_world).dot(step_world.normalized()))
        count = max(1, int(distance / max(step_world.length, _EPSILON) + 0.5))
        if force or edge is not self._source_edge or count != self._paver_count or not self._branch_data:
            old = self._branch_data
            self._source_edge = edge
            self._branch_data = topology.rebuild_paver(
                self._bm,
                self._source_element,
                edge,
                count,
                existing_created=old,
                step_local=step_local,
            )
            precision_edit.clear_planar_lock_on_vertices(self._bm, self._branch_data['created_verts'])
            self._initial_local = {vert: vert.co.copy() for vert in self._branch_data['created_verts']}
            self._anchor_world = anchor_world
            self._paver_count = count

    def _reset_created(self):
        for vert, co in (self._initial_local or {}).items():
            if getattr(vert, 'is_valid', False):
                vert.co = co

    def _set_created_delta(self, delta_world, verts=None):
        inverse = self._obj.matrix_world.inverted_safe()
        matrix = self._obj.matrix_world
        for vert in (verts if verts is not None else self._branch_data.get('created_verts', ())):
            if not getattr(vert, 'is_valid', False):
                continue
            base = self._initial_local.get(vert, vert.co)
            vert.co = inverse @ (matrix @ base + Vector(delta_world))

    def _pick_hover(self, context, event, extra_excludes=True):
        if not _inside_region(event, self._region):
            return None
        exclude_verts = set()
        exclude_edges = set()
        exclude_faces = set()
        if extra_excludes and self._branch_data:
            exclude_verts.update(self._branch_data.get('created_verts', ()))
            exclude_edges.update(self._branch_data.get('created_edges', ()))
            exclude_edges.update(self._branch_data.get('branch_edges', ()))
            exclude_faces.update(self._branch_data.get('created_faces', ()))
        if self._source_kind == 'VERT' and self._source_element is not None:
            exclude_verts.add(self._source_element)
        return drag.pick_mesh_element(
            self._obj,
            self._bm,
            self._region,
            self._rv3d,
            drag.mouse_xy(event, self._region),
            allowed=('VERT', 'EDGE', 'FACE'),
            exclude_verts=exclude_verts,
            exclude_edges=exclude_edges,
            exclude_faces=exclude_faces,
        )

    def _update_duplicate_branch(self, context, event):
        props = self._props(context)
        mask = self._axes(context)
        self._reset_created()
        mouse = drag.mouse_xy(event, self._region)
        target_anchor = drag.project_mouse_anchor(self._region, self._rv3d, self._anchor_world, mouse, mask)
        base_delta = target_anchor - self._anchor_world
        self._set_created_delta(base_delta)
        self._contacts = []

        hover = self._pick_hover(context, event)
        self._hover_target = hover if props.magic_branch_magnetic_snap else None
        if props.magic_branch_magnetic_snap and hover is not None:
            if hover.kind in {'VERT', 'EDGE'}:
                snap_delta, contacts = drag.rigid_snap_delta(self._obj, self._branch_data['created_verts'], hover, mask)
                if snap_delta is not None:
                    self._set_created_delta(base_delta + snap_delta)
                    self._contacts = list(contacts or ())
            elif hover.kind == 'FACE':
                direction = drag.masked_vector(hover.point_world - self._anchor_world, mask)
                if direction.length <= _EPSILON:
                    direction = base_delta
                initial_world = {vert: self._obj.matrix_world @ co for vert, co in self._initial_local.items()}
                hits = drag.face_travel_hits(self._obj, hover.element, initial_world, direction)
                inverse = self._obj.matrix_world.inverted_safe()
                contacts = []
                for vert, point in hits.items():
                    vert.co = inverse @ point
                    kind, element, resolved = drag.boundary_contact(self._obj, hover.element, point)
                    contacts.append((vert, kind, element, resolved))
                if contacts:
                    self._contacts = contacts
        self._highlighter.set_target(self._hover_target)

    def _update_face_branch(self, context, event):
        props = self._props(context)
        self._rebuild_face_branch(context, event)
        hover = self._pick_hover(context, event)
        self._hover_target = hover if props.magic_branch_magnetic_snap else None
        self._contacts = []

        if props.magic_branch_face_mode == 'ORGANIC':
            self._reset_created()
            mask = self._axes(context)
            mouse = drag.mouse_xy(event, self._region)
            target_anchor = drag.project_mouse_anchor(self._region, self._rv3d, self._anchor_world, mouse, mask)
            base_delta = target_anchor - self._anchor_world
            outer = self._branch_data.get('outer_verts', ())
            self._set_created_delta(base_delta, verts=outer)
            if self._hover_target is not None:
                if hover.kind in {'VERT', 'EDGE'}:
                    snap_delta, contacts = drag.rigid_snap_delta(self._obj, outer, hover, mask)
                    if snap_delta is not None:
                        self._set_created_delta(base_delta + snap_delta, verts=outer)
                        self._contacts = list(contacts or ())
                elif hover.kind == 'FACE':
                    direction = drag.masked_vector(hover.point_world - self._anchor_world, mask)
                    if direction.length <= _EPSILON:
                        direction = base_delta
                    initial_world = {vert: self._obj.matrix_world @ self._initial_local[vert] for vert in outer}
                    hits = drag.face_travel_hits(self._obj, hover.element, initial_world, direction)
                    inverse = self._obj.matrix_world.inverted_safe()
                    for vert, point in hits.items():
                        vert.co = inverse @ point
                        kind, element, resolved = drag.boundary_contact(self._obj, hover.element, point)
                        self._contacts.append((vert, kind, element, resolved))
        else:
            outer = self._branch_data.get('outer_verts', ())
            matrix = self._obj.matrix_world
            tol = 1.0e-5
            if self._hover_target is not None and hover.kind == 'VERT':
                for vert in outer:
                    world = matrix @ vert.co
                    if (world - hover.point_world).length <= tol:
                        self._contacts = [(vert, 'VERT', hover.element, hover.point_world)]
                        break
            elif self._hover_target is not None and hover.kind == 'EDGE':
                start = matrix @ hover.element.verts[0].co
                end = matrix @ hover.element.verts[1].co
                for vert in outer:
                    world = matrix @ vert.co
                    closest, _factor, distance = drag.closest_point_segment_3d(world, start, end)
                    if distance <= tol:
                        self._contacts.append((vert, 'EDGE', hover.element, closest))

        self._highlighter.set_target(self._hover_target)
        outer = self._branch_data.get('outer_verts', ()) if self._branch_data else ()
        if len(outer) == 2:
            matrix = self._obj.matrix_world
            self._highlighter.set_virtual_lines(((matrix @ outer[0].co, matrix @ outer[1].co),))

    def _update_drag(self, context, event):
        if self._source_kind in {'VERT', 'EDGE'}:
            self._update_duplicate_branch(context, event)
        else:
            self._update_face_branch(context, event)
        self._bm.normal_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=False)
        if context.area:
            context.area.tag_redraw()

    def _commit_live(self, context):
        props = self._props(context)
        if props.magic_branch_auto_merge and props.magic_branch_magnetic_snap and self._contacts:
            reason = _target_protection_reason(self._obj, self._bm, self._hover_target)
            if reason:
                raise MagicBranchError(reason)
            face_target = self._hover_target.element if self._hover_target and self._hover_target.kind == 'FACE' else None
            drag.weld_contacts(self._bm, self._obj, self._contacts, face_target=face_target)

        topology.validate_no_zero_geometry(self._bm)
        _restore_lock_references(self._obj, self._bm, self._lock_snapshot)
        self._bm.normal_update()
        self._bm.verts.index_update()
        self._bm.edges.index_update()
        self._bm.faces.index_update()
        bmesh.update_edit_mesh(self._obj.data, loop_triangles=True, destructive=True)

        label = self._source_kind.title()
        if self._source_kind == 'FACE':
            label += f' / {props.magic_branch_face_mode.title()}'
        props.magic_branch_last_report = f'Created Magic Branch: {label}.'
        self.report({'INFO'}, props.magic_branch_last_report)

        if props.magic_branch_persistent:
            self._bm = topology.prepare_bmesh(self._obj)
            self._lock_snapshot = _snapshot_lock_references(self._obj, self._bm)
            try:
                bpy.ops.ed.undo_push(message='Magic Branch')
            except Exception:
                pass
            self._clear_live()
            self._set_header(context, 'Magic Branch Persistent: click-drag source • MMB orbit • Esc exits')
            return {'RUNNING_MODAL'}
        return self._finish_session(context)

    def _cancel_live(self):
        try:
            self._delete_live_geometry()
            _restore_lock_references(self._obj, self._bm, self._lock_snapshot)
        except Exception:
            pass
        self._clear_live()

    def _finish_session(self, context, cancelled=False):
        if self._highlighter:
            self._highlighter.stop()
        self._restore_guards()
        self._set_header(context, None)
        if cancelled:
            self._props(context).magic_branch_last_report = 'Magic Branch exited.'
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        props = self._props(context)
        try:
            self._obj = _active_edit_mesh(context)
            self._axes(context)
            self._bm = topology.prepare_bmesh(self._obj)
            self._region = next((region for region in context.area.regions if region.type == 'WINDOW'), None)
            self._rv3d = getattr(context.space_data, 'region_3d', None)
            if self._region is None or self._rv3d is None:
                raise MagicBranchError('The active 3D View has no usable window region.')
            self._lock_snapshot = _snapshot_lock_references(self._obj, self._bm)
            self._suspend_guards()
            self._highlighter = drag.HoverHighlighter()
            self._highlighter.start()
            self._clear_live()
            self._orbiting = False
        except Exception as error:
            self._restore_guards()
            props.magic_branch_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        mode = 'Persistent' if props.magic_branch_persistent else 'Single Branch'
        self._set_header(context, f'Magic Branch {mode}: click-drag source • MMB orbit • Esc exits')
        props.magic_branch_last_report = f'Magic Branch armed: {mode}.'
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        props = self._props(context)

        if event.type == 'MIDDLEMOUSE':
            if event.value == 'PRESS':
                self._orbiting = True
                pivot = _world_center(self._obj, self._branch_data.get('created_verts', ())) if self._branch_data else None
                if pivot is None and self._pressed_source is not None:
                    pivot = self._pressed_source.point_world
                drag.set_orbit_pivot(self._rv3d, pivot)
                return {'PASS_THROUGH'}
            if event.value == 'RELEASE':
                self._orbiting = False
                return {'PASS_THROUGH'}
        if self._orbiting:
            return {'PASS_THROUGH'}

        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            if self._state == 'DRAGGING':
                self._cancel_live()
            return self._finish_session(context, cancelled=True)

        if self._state == 'WAITING':
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and _inside_region(event, self._region):
                target = self._pick_source(context, event)
                if target is None:
                    return {'PASS_THROUGH'}
                self._pressed_source = target
                self._press_mouse = Vector((event.mouse_x, event.mouse_y))
                _select_only(self._bm, target.element)
                bmesh.update_edit_mesh(self._obj.data, loop_triangles=False, destructive=False)
                self._highlighter.set_target(target)
                return {'RUNNING_MODAL'}

            if event.type == 'MOUSEMOVE' and self._pressed_source is not None:
                current = Vector((event.mouse_x, event.mouse_y))
                if (current - self._press_mouse).length >= _DRAG_THRESHOLD:
                    try:
                        self._begin_drag(context, event)
                    except Exception as error:
                        self._cancel_live()
                        props.magic_branch_last_report = f'Blocked: {error}'
                        self.report({'ERROR'}, str(error))
                    return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and self._pressed_source is not None:
                self._pressed_source = None
                self._press_mouse = None
                self._highlighter.set_target(None)
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}

        if self._state == 'DRAGGING':
            if event.type == 'MOUSEMOVE':
                try:
                    self._update_drag(context, event)
                except Exception as error:
                    self._cancel_live()
                    props.magic_branch_last_report = f'Blocked: {error}'
                    self.report({'ERROR'}, str(error))
                return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                try:
                    return self._commit_live(context)
                except Exception as error:
                    self._cancel_live()
                    props.magic_branch_last_report = f'Blocked: {error}'
                    self.report({'ERROR'}, str(error))
                    if props.magic_branch_persistent:
                        return {'RUNNING_MODAL'}
                    return self._finish_session(context, cancelled=True)

        return {'RUNNING_MODAL'}


CLASSES = (
    WT_OT_magic_branch_toggle_persistent,
    WT_OT_magic_branch,
)
