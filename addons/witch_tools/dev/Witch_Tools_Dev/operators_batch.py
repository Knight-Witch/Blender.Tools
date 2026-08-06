import bpy
import math
from bpy.types import Operator


class WT_OT_apply_batch_rotation(Operator):
    bl_idname = 'witch_tools.apply_batch_rotation'
    bl_label = 'Apply Rotation'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def execute(self, context):
        props = context.scene.witch_tools
        axes = []
        radians = {}

        if props.batch_rotate_use_x:
            axes.append('X')
            radians[0] = math.radians(props.batch_rotate_x_degrees)
        if props.batch_rotate_use_y:
            axes.append('Y')
            radians[1] = math.radians(props.batch_rotate_y_degrees)
        if props.batch_rotate_use_z:
            axes.append('Z')
            radians[2] = math.radians(props.batch_rotate_z_degrees)

        if not radians:
            self.report({'WARNING'}, 'No rotation axes are enabled')
            return {'CANCELLED'}

        for obj in context.selected_objects:
            for index, amount in radians.items():
                obj.rotation_euler[index] += amount

        axis_text = ', '.join(axes)
        self.report({'INFO'}, f'Rotated {len(context.selected_objects)} object(s) on {axis_text}')
        return {'FINISHED'}


class WT_OT_apply_all_transforms(Operator):
    bl_idname = 'witch_tools.apply_all_transforms'
    bl_label = 'Apply All Transforms'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def execute(self, context):
        view_layer = context.view_layer
        prev_active = view_layer.objects.active
        prev_selected = list(context.selected_objects)
        for obj in prev_selected:
            for item in list(context.selected_objects):
                item.select_set(False)
            obj.select_set(True)
            view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        for item in list(context.selected_objects):
            item.select_set(False)
        for obj in prev_selected:
            if obj.name in bpy.data.objects:
                obj.select_set(True)
        if prev_active and prev_active.name in bpy.data.objects:
            view_layer.objects.active = prev_active
        self.report({'INFO'}, f'Applied transforms to {len(prev_selected)} object(s)')
        return {'FINISHED'}


class WT_OT_batch_apply_tools(Operator):
    bl_idname = 'witch_tools.batch_apply_tools'
    bl_label = 'Apply To Selected'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and bool(context.selected_objects)

    def execute(self, context):
        props = context.scene.witch_tools
        view_layer = context.view_layer
        prev_active = view_layer.objects.active
        prev_selected = list(context.selected_objects)

        rotation_amounts = {}
        if props.batch_rotate_use_x:
            rotation_amounts[0] = math.radians(props.batch_rotate_x_degrees)
        if props.batch_rotate_use_y:
            rotation_amounts[1] = math.radians(props.batch_rotate_y_degrees)
        if props.batch_rotate_use_z:
            rotation_amounts[2] = math.radians(props.batch_rotate_z_degrees)

        for obj in prev_selected:
            obj.scale = (props.scale_value, props.scale_value, props.scale_value)
            if props.batch_auto_apply_rotation:
                for index, amount in rotation_amounts.items():
                    obj.rotation_euler[index] += amount
            if props.remove_modifiers:
                obj.modifiers.clear()
            if props.apply_transforms:
                for item in list(context.selected_objects):
                    item.select_set(False)
                obj.select_set(True)
                view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        for item in list(context.selected_objects):
            item.select_set(False)
        for obj in prev_selected:
            if obj.name in bpy.data.objects:
                obj.select_set(True)
        if prev_active and prev_active.name in bpy.data.objects:
            view_layer.objects.active = prev_active
        return {'FINISHED'}
