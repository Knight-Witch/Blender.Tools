import bpy
from bpy.types import Operator

from .utils_weights import (
    find_best_source_for_target,
    mesh_pool_from_armature,
    mesh_pool_from_collection,
    transfer_weights,
)


def _clear_refs(refs):
    while refs:
        refs.remove(len(refs) - 1)


def _fill_refs(refs, objects):
    _clear_refs(refs)
    for obj in objects:
        item = refs.add()
        item.object_name = obj.name


def _objects_from_refs(refs):
    result = []
    seen = set()
    for item in refs:
        obj = bpy.data.objects.get(item.object_name)
        if obj is None or obj.type != 'MESH' or obj.name in seen:
            continue
        result.append(obj)
        seen.add(obj.name)
    return result


def _pool_from_mode(props, which):
    mode = getattr(props, f'batch_{which}_mode')
    if mode == 'SELECTION':
        return _objects_from_refs(getattr(props, f'batch_{which}_objects'))
    if mode == 'COLLECTION':
        return mesh_pool_from_collection(getattr(props, f'batch_{which}_collection'))
    if mode == 'ARMATURE':
        return mesh_pool_from_armature(getattr(props, f'batch_{which}_armature'))
    return []


class WT_OT_set_active_as_source(Operator):
    bl_idname = 'witch_tools.set_active_as_source'
    bl_label = 'Use Active As Source'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context):
        context.scene.witch_tools.source_object = context.active_object
        return {'FINISHED'}


class WT_OT_set_active_as_target(Operator):
    bl_idname = 'witch_tools.set_active_as_target'
    bl_label = 'Use Active As Target'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context):
        context.scene.witch_tools.target_object = context.active_object
        return {'FINISHED'}


class WT_OT_transfer_single_weights(Operator):
    bl_idname = 'witch_tools.transfer_single_weights'
    bl_label = 'Transfer Weights'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        source = props.source_object
        target = props.target_object
        if source is None or target is None:
            self.report({'ERROR'}, 'Pick both source and target mesh objects')
            return {'CANCELLED'}
        ok, msg = transfer_weights(source, target)
        self.report({'INFO' if ok else 'WARNING'}, msg)
        return {'FINISHED' if ok else 'CANCELLED'}


class WT_OT_capture_batch_source_selection(Operator):
    bl_idname = 'witch_tools.capture_batch_source_selection'
    bl_label = 'Use Selected Objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        items = [obj for obj in context.selected_objects if obj.type == 'MESH']
        props = context.scene.witch_tools
        props.batch_source_objects.clear()
        for obj in items:
            item = props.batch_source_objects.add()
            item.object_name = obj.name
        self.report({'INFO'}, f'Stored {len(items)} source object(s)')
        return {'FINISHED'}


class WT_OT_capture_batch_target_selection(Operator):
    bl_idname = 'witch_tools.capture_batch_target_selection'
    bl_label = 'Use Selected Objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        items = [obj for obj in context.selected_objects if obj.type == 'MESH']
        props = context.scene.witch_tools
        props.batch_target_objects.clear()
        for obj in items:
            item = props.batch_target_objects.add()
            item.object_name = obj.name
        self.report({'INFO'}, f'Stored {len(items)} target object(s)')
        return {'FINISHED'}


class WT_OT_transfer_batch_auto(Operator):
    bl_idname = 'witch_tools.transfer_batch_auto'
    bl_label = 'Batch Transfer'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        source_pool = _pool_from_mode(props, 'source')
        target_pool = _pool_from_mode(props, 'target')
        if not source_pool or not target_pool:
            self.report({'ERROR'}, 'Source and target pools both need at least one mesh')
            return {'CANCELLED'}

        applied, skipped, failed = [], [], []
        for target in target_pool:
            source = find_best_source_for_target(target, source_pool)
            if source is None:
                skipped.append(target.name)
                continue
            ok, msg = transfer_weights(source, target)
            (applied if ok else failed).append(msg)

        summary = []
        if applied:
            summary.append(f'Applied: {len(applied)}')
        if skipped:
            summary.append(f'Skipped: {len(skipped)}')
        if failed:
            summary.append(f'Failed: {len(failed)}')
        if applied:
            self.report({'INFO'}, ' | '.join(summary))
            return {'FINISHED'}
        self.report({'WARNING'}, ' | '.join(summary) if summary else 'No matching source meshes found')
        return {'CANCELLED'}


class WT_OT_add_shrinkwrap(Operator):
    bl_idname = 'witch_tools.add_shrinkwrap_modifier'
    bl_label = 'Add / Update Shrinkwrap'
    bl_description = 'Add or update a shrinkwrap modifier on the active mesh or all selected meshes using the current settings.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode == 'OBJECT' and obj is not None and obj.type == 'MESH'

    def _targets(self, context, props):
        meshes = [context.active_object]
        if props.shrinkwrap_apply_to_selected:
            meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        return meshes

    def _configure_modifier(self, obj, target, props):
        mod = None
        for existing in obj.modifiers:
            if existing.type == 'SHRINKWRAP' and existing.name == 'WT_Shrinkwrap':
                mod = existing
                break
        if mod is None:
            mod = obj.modifiers.new(name='WT_Shrinkwrap', type='SHRINKWRAP')
        mod.target = target
        mod.wrap_method = props.shrinkwrap_wrap_method
        if hasattr(mod, 'wrap_mode'):
            mod.wrap_mode = props.shrinkwrap_wrap_mode
        if hasattr(mod, 'offset'):
            mod.offset = props.shrinkwrap_offset
        mod.vertex_group = props.shrinkwrap_vertex_group or ''
        return mod

    def execute(self, context):
        props = context.scene.witch_tools
        target = props.shrinkwrap_target
        if target is None or target.type != 'MESH':
            self.report({'ERROR'}, 'Pick a valid mesh shrinkwrap target')
            return {'CANCELLED'}

        targets = []
        skipped = []
        for obj in self._targets(context, props):
            if obj == target:
                skipped.append(obj.name)
                continue
            self._configure_modifier(obj, target, props)
            targets.append(obj.name)

        if not targets:
            self.report({'ERROR'}, 'No valid mesh objects were available for shrinkwrap')
            return {'CANCELLED'}

        msg = f'Updated shrinkwrap on {len(targets)} object(s)'
        if skipped:
            msg += f' | Skipped target: {", ".join(skipped[:3])}'
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class WT_OT_apply_shrinkwrap(Operator):
    bl_idname = 'witch_tools.apply_shrinkwrap_modifier'
    bl_label = 'Apply Shrinkwrap'
    bl_description = 'Apply matching shrinkwrap modifiers on the active mesh or all selected meshes.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return context.mode == 'OBJECT' and obj is not None and obj.type == 'MESH'

    def _targets(self, context, props):
        meshes = [context.active_object]
        if props.shrinkwrap_apply_to_selected:
            meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        return meshes

    def execute(self, context):
        props = context.scene.witch_tools
        target_mesh = props.shrinkwrap_target
        view_layer = context.view_layer
        prev_active = view_layer.objects.active
        prev_selected = list(context.selected_objects)
        applied = 0
        skipped = 0

        for obj in self._targets(context, props):
            if obj.type != 'MESH' or obj == target_mesh:
                skipped += 1
                continue

            modifier_name = None
            for mod in obj.modifiers:
                if mod.type != 'SHRINKWRAP':
                    continue
                if target_mesh and mod.target != target_mesh:
                    continue
                modifier_name = mod.name
                break

            if not modifier_name:
                skipped += 1
                continue

            for item in list(context.selected_objects):
                item.select_set(False)
            obj.select_set(True)
            view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=modifier_name)
            applied += 1

        for item in list(context.selected_objects):
            item.select_set(False)
        for obj in prev_selected:
            if obj.name in bpy.data.objects:
                obj.select_set(True)
        if prev_active and prev_active.name in bpy.data.objects:
            view_layer.objects.active = prev_active

        if applied == 0:
            self.report({'WARNING'}, 'No matching shrinkwrap modifiers were available to apply')
            return {'CANCELLED'}

        self.report({'INFO'}, f'Applied shrinkwrap on {applied} object(s) | Skipped: {skipped}')
        return {'FINISHED'}
