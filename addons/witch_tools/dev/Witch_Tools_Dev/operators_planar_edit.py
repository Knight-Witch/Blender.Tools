import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector

from .precision_edit_common import (
    _AXIS_BITS,
    PrecisionEditError,
    _apply_plan,
    _axis_mask,
    _edit_mesh_objects,
    _planar_layers,
    _planned_move_blocked,
    _point_world,
    _prepare_bmesh,
    _props,
    _require_axis,
    _shape_key_preflight,
    _single_source,
    clear_current_edit_selection,
)


_GUARD_ENABLED = False
_TIMER_RUNNING = False
_GUARD_SUSPENDED = False


class WT_OT_planar_lock_selected(Operator):
    bl_idname = 'mesh.wt_planar_lock_selected'
    bl_label = 'Lock Selected Planes'
    bl_description = (
        'Freeze the enabled object-local X/Y/Z coordinate of every selected vertex. '
        'Selecting edges or faces locks their vertices. Unlocked coordinates remain editable.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        axes = _axis_mask(props, 'planar_lock_axis')
        try:
            _require_axis(axes)
            count = 0
            for obj in _edit_mesh_objects(context):
                bm = _prepare_bmesh(obj)
                selected = [vert for vert in bm.verts if vert.select]
                if not selected:
                    continue
                mask_layer, x_layer, y_layer, z_layer = _planar_layers(bm, create=True)
                layers = (x_layer, y_layer, z_layer)
                for vert in selected:
                    mask = int(vert[mask_layer])
                    for axis, bit in enumerate(_AXIS_BITS):
                        if axes[axis]:
                            vert[layers[axis]] = float(vert.co[axis])
                            mask |= bit
                    vert[mask_layer] = mask
                    count += 1
                bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
            if not count:
                raise PrecisionEditError('Select at least one vertex, edge, or face to lock.')
            props.planar_edit_last_report = f'Plane Lock updated on {count} selected vertices.'
            self.report({'INFO'}, props.planar_edit_last_report)
            return {'FINISHED'}
        except PrecisionEditError as error:
            props.planar_edit_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}


class WT_OT_planar_unlock_selected(Operator):
    bl_idname = 'mesh.wt_planar_unlock_selected'
    bl_label = 'Unlock Selected Planes'
    bl_description = 'Remove the enabled X/Y/Z Plane Lock axes from the selected vertices.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        axes = _axis_mask(props, 'planar_lock_axis')
        try:
            _require_axis(axes)
            count = 0
            remove_bits = 0
            for axis, bit in enumerate(_AXIS_BITS):
                if axes[axis]:
                    remove_bits |= bit
            for obj in _edit_mesh_objects(context):
                bm = _prepare_bmesh(obj)
                mask_layer, _x, _y, _z = _planar_layers(bm, create=False)
                if mask_layer is None:
                    continue
                for vert in bm.verts:
                    if not vert.select:
                        continue
                    old = int(vert[mask_layer])
                    new = old & ~remove_bits
                    if new != old:
                        vert[mask_layer] = new
                        count += 1
                bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
            if not count:
                raise PrecisionEditError('No selected vertices had the enabled Plane Lock axes.')
            props.planar_edit_last_report = f'Unlocked enabled axes on {count} selected vertices.'
            self.report({'INFO'}, props.planar_edit_last_report)
            return {'FINISHED'}
        except PrecisionEditError as error:
            props.planar_edit_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}


class WT_OT_planar_clear_all(Operator):
    bl_idname = 'mesh.wt_planar_clear_all'
    bl_label = 'Clear All Plane Locks'
    bl_description = 'Remove every Plane Lock axis from every edit-mode mesh object.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        count = 0
        for obj in _edit_mesh_objects(context):
            bm = _prepare_bmesh(obj)
            mask_layer, _x, _y, _z = _planar_layers(bm, create=False)
            if mask_layer is None:
                continue
            for vert in bm.verts:
                if int(vert[mask_layer]):
                    vert[mask_layer] = 0
                    count += 1
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        props.planar_edit_last_report = f'Cleared Plane Locks from {count} vertices.'
        self.report({'INFO'}, props.planar_edit_last_report)
        return {'FINISHED'}


class WT_OT_planar_level_capture(Operator):
    bl_idname = 'mesh.wt_planar_level_capture'
    bl_label = 'Capture Level Source'
    bl_description = 'Capture one source vertex coordinate, edge midpoint, or face center in world space.'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        try:
            kind, (obj, _bm, element) = _single_source(context)
            point = _point_world(obj, kind, element)
        except PrecisionEditError as error:
            props.planar_edit_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}

        props.planar_level_source_location = point
        props.planar_level_source_label = f'{obj.name} / {kind.title()}'
        props.planar_level_has_source = True
        props.planar_edit_last_report = f'Captured Level source from {obj.name}. Select targets, then Level Targets.'
        clear_current_edit_selection(context)
        self.report({'INFO'}, props.planar_edit_last_report)
        return {'FINISHED'}


class WT_OT_planar_level_targets(Operator):
    bl_idname = 'mesh.wt_planar_level_targets'
    bl_label = 'Level Targets'
    bl_description = (
        'Set every selected target vertex to the captured source world coordinate on the enabled axes. '
        'This is absolute per-vertex leveling, not a median transform.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.mode == 'EDIT_MESH' and context.active_object and context.active_object.type == 'MESH')

    def execute(self, context):
        props = _props(context)
        try:
            if not props.planar_level_has_source:
                raise PrecisionEditError('Capture a Level source first.')
            axes = _axis_mask(props, 'planar_level_axis')
            _require_axis(axes)
            objects = _edit_mesh_objects(context)
            _shape_key_preflight(objects)
            source = Vector(props.planar_level_source_location)
            plans = []
            for obj in objects:
                bm = _prepare_bmesh(obj)
                entries = []
                for vert in bm.verts:
                    if not vert.select:
                        continue
                    world = obj.matrix_world @ vert.co
                    target = world.copy()
                    for axis in range(3):
                        if axes[axis]:
                            target[axis] = source[axis]
                    new_local = obj.matrix_world.inverted_safe() @ target
                    blocked = _planned_move_blocked(obj, bm, vert, new_local)
                    if blocked:
                        raise PrecisionEditError(f'{obj.name}: target vertex {vert.index} is protected by {blocked}.')
                    entries.append((vert, new_local))
                if entries:
                    plans.append((obj, bm, entries))
            if not plans:
                raise PrecisionEditError('Select at least one target vertex, edge, or face.')
            _apply_plan(plans)
            count = sum(len(entries) for _obj, _bm, entries in plans)
            props.planar_edit_last_report = f'Leveled {count} target vertices.'
            self.report({'INFO'}, props.planar_edit_last_report)
            return {'FINISHED'}
        except PrecisionEditError as error:
            props.planar_edit_last_report = f'Blocked: {error}'
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        except Exception as error:
            props.planar_edit_last_report = f'Blocked: Level failed: {error}'
            self.report({'ERROR'}, f'Level failed: {error}')
            return {'CANCELLED'}


def _enforce_object_planar_locks(obj):
    if not obj or obj.type != 'MESH' or obj.mode != 'EDIT':
        return False
    bm = _prepare_bmesh(obj)
    mask_layer, x_layer, y_layer, z_layer = _planar_layers(bm, create=False)
    if mask_layer is None:
        return False
    changed = False
    layers = (x_layer, y_layer, z_layer)
    for vert in bm.verts:
        mask = int(vert[mask_layer])
        if not mask:
            continue
        for axis, bit in enumerate(_AXIS_BITS):
            layer = layers[axis]
            if mask & bit and layer is not None:
                locked = float(vert[layer])
                if abs(vert.co[axis] - locked) > 1.0e-9:
                    vert.co[axis] = locked
                    changed = True
    if changed:
        bm.normal_update()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return changed


def _planar_guard_timer():
    global _TIMER_RUNNING
    if not _GUARD_ENABLED:
        _TIMER_RUNNING = False
        return None
    if _GUARD_SUSPENDED:
        return 0.05
    try:
        context = bpy.context
        for obj in _edit_mesh_objects(context):
            _enforce_object_planar_locks(obj)
    except Exception:
        pass
    return 0.05


def _start_planar_guard():
    global _TIMER_RUNNING
    if _TIMER_RUNNING:
        return
    _TIMER_RUNNING = True
    bpy.app.timers.register(_planar_guard_timer, first_interval=0.03)


def register_planar_guard():
    global _GUARD_ENABLED
    _GUARD_ENABLED = True
    _start_planar_guard()


def unregister_planar_guard():
    global _GUARD_ENABLED
    _GUARD_ENABLED = False


CLASSES = (
    WT_OT_planar_lock_selected,
    WT_OT_planar_unlock_selected,
    WT_OT_planar_clear_all,
    WT_OT_planar_level_capture,
    WT_OT_planar_level_targets,
)
