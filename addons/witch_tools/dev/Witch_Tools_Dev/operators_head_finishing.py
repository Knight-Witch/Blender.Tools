import bpy
from bpy.types import Operator

from .utils_head import duplicate_object, purge_orphans, recalc_normals_edit_object, remove_object_if_exists


class WT_OT_fix_armature_ears(Operator):
    bl_idname = 'witch_tools.fix_armature_ears'
    bl_label = 'Fix Armature & Ears'
    bl_description = 'Fix ear Head_M weights and make sure ear meshes are properly bound to the selected armature.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        selected_objects = list(context.selected_objects)
        armature_obj = props.head_target_armature
        if armature_obj is None:
            armature_obj = next((obj for obj in selected_objects if obj.type == 'ARMATURE'), None)

        if armature_obj is None:
            self.report({'ERROR'}, 'Select or assign an armature first')
            return {'CANCELLED'}

        fixed = 0
        for obj in selected_objects:
            if obj.type != 'MESH':
                continue
            if 'ears' not in obj.name.lower():
                continue

            armature_modifiers = [mod for mod in obj.modifiers if mod.type == 'ARMATURE']
            for mod in list(armature_modifiers):
                if mod.object is None:
                    obj.modifiers.remove(mod)

            if 'Head_M' not in obj.vertex_groups:
                group = obj.vertex_groups.new(name='Head_M')
                group.add([vert.index for vert in obj.data.vertices], 1.0, 'REPLACE')

            arm_mod = next((mod for mod in obj.modifiers if mod.type == 'ARMATURE'), None)
            if arm_mod is None:
                arm_mod = obj.modifiers.new(name='Armature', type='ARMATURE')
            arm_mod.object = armature_obj
            if obj.parent != armature_obj:
                obj.parent = armature_obj
            fixed += 1

        self.report({'INFO'}, f'Fixed {fixed} ear mesh object(s)')
        return {'FINISHED'}


class WT_OT_fix_head_seam_normals(Operator):
    bl_idname = 'witch_tools.fix_head_seam_normals'
    bl_label = 'Fix Head Seam Normals'
    bl_description = 'Transfer seam normals to the active edited head using the assigned vanilla reference head plus matching ears.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        edited_head = context.active_object
        reference_head = props.head_reference_mesh
        if edited_head is None or edited_head.type != 'MESH':
            self.report({'ERROR'}, 'Set the edited head mesh active first')
            return {'CANCELLED'}
        if reference_head is None or reference_head.type != 'MESH':
            self.report({'ERROR'}, 'Assign a vanilla reference head in Head Tools > Finishing')
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        seam_group = edited_head.vertex_groups.get('SEAMS') or edited_head.vertex_groups.new(name='SEAMS')
        bpy.ops.object.vertex_group_assign()
        bpy.ops.object.mode_set(mode='OBJECT')

        ears_candidates = [obj for obj in bpy.data.objects if obj.type == 'MESH' and 'ears' in obj.name.lower()]
        ears_object = next((obj for obj in ears_candidates if obj != reference_head and obj != edited_head and obj.name.split('_')[0:3] == edited_head.name.split('_')[0:3]), None)
        if ears_object is None:
            ears_object = next((obj for obj in context.selected_objects if obj.type == 'MESH' and 'ears' in obj.name.lower()), None)
        if ears_object is None:
            self.report({'ERROR'}, 'Could not find a matching ears mesh')
            return {'CANCELLED'}

        remove_object_if_exists('WT_JOINED_REFERENCE')
        purge_orphans()

        dup_ears = duplicate_object(context, ears_object)
        dup_ref = duplicate_object(context, reference_head)
        bpy.ops.object.select_all(action='DESELECT')
        dup_ears.select_set(True)
        dup_ref.select_set(True)
        context.view_layer.objects.active = dup_ref
        bpy.ops.object.join()
        joined = context.active_object
        joined.name = 'WT_JOINED_REFERENCE'

        bpy.ops.object.select_all(action='DESELECT')
        edited_head.select_set(True)
        context.view_layer.objects.active = edited_head
        mod = edited_head.modifiers.new(name='WT_DataTransfer', type='DATA_TRANSFER')
        mod.object = joined
        mod.use_loop_data = True
        mod.data_types_loops = {'CUSTOM_NORMAL'}
        mod.loop_mapping = 'NEAREST_POLYNOR'
        mod.vertex_group = seam_group.name
        mod.use_object_transform = True
        bpy.ops.object.modifier_apply(modifier=mod.name)
        recalc_normals_edit_object(context, edited_head)
        self.report({'INFO'}, 'Transferred seam normals from the reference head')
        return {'FINISHED'}


class WT_OT_delete_lods(Operator):
    bl_idname = 'witch_tools.delete_lods'
    bl_label = 'Delete LODs in Selection'
    bl_description = 'Delete selected objects whose names contain _LOD followed by a number.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        import re
        pattern = re.compile(r'_LOD\d+')
        targets = [obj for obj in context.selected_objects if pattern.search(obj.name)]
        for obj in targets:
            bpy.data.objects.remove(obj, do_unlink=True)
        self.report({'INFO'}, f'Deleted {len(targets)} LOD object(s)')
        return {'FINISHED'}


class WT_OT_reset_lod_distance(Operator):
    bl_idname = 'witch_tools.reset_lod_distance'
    bl_label = 'Change All LOD Distance to 0'
    bl_description = 'Set LOD distance to 0 on selected mesh objects that expose ls_properties.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        changed = 0
        for obj in context.selected_objects:
            if obj.type != 'MESH' or not hasattr(obj.data, 'ls_properties'):
                continue
            obj.data.ls_properties.lod_distance = 0.0
            changed += 1
        self.report({'INFO'}, f'Reset LOD distance on {changed} object(s)')
        return {'FINISHED'}


class WT_OT_cleanup_export_orders(Operator):
    bl_idname = 'witch_tools.cleanup_export_orders'
    bl_label = 'Clean Up Export Orders'
    bl_description = 'Set export orders using BG3 head-mesh naming keywords.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mapping = [
            ('Eyeshadow', 7),
            ('Eyelashes', 6),
            ('Tearline', 5),
            ('Mouth', 2),
            ('Eyes', 3),
            ('Ears', 4),
            ('Scalp', 8),
        ]
        changed = 0
        for obj in context.selected_objects:
            if obj.type != 'MESH' or not hasattr(obj.data, 'ls_properties'):
                continue
            target_order = 1
            for keyword, order in mapping:
                if keyword in obj.name:
                    target_order = order
                    break
            if obj.data.ls_properties.export_order != target_order:
                obj.data.ls_properties.export_order = target_order
                changed += 1
        self.report({'INFO'}, f'Updated export orders on {changed} object(s)')
        return {'FINISHED'}


CLASSES = (
    WT_OT_fix_armature_ears,
    WT_OT_fix_head_seam_normals,
    WT_OT_delete_lods,
    WT_OT_reset_lod_distance,
    WT_OT_cleanup_export_orders,
)
