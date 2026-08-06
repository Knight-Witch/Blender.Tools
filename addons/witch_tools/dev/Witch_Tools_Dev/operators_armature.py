from bpy.types import Operator

from .utils_weights import armature_check_from_object


class WT_OT_check_armature(Operator):
    bl_idname = 'witch_tools.check_armature'
    bl_label = 'Check Armature'
    bl_description = 'Check the selected mesh or linked armature for weighted vertex groups that do not exist as bones on the current armature.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.witch_tools
        issue, summary, details = armature_check_from_object(context.active_object)
        props.armature_check_summary = summary
        props.armature_check_details = details
        self.report({'WARNING' if issue else 'INFO'}, summary)
        return {'FINISHED'}


class WT_OT_cleanup_unused_vertex_groups(Operator):
    bl_idname = 'witch_tools.cleanup_unused_vertex_groups'
    bl_label = 'Remove Unused Vertex Groups'
    bl_description = 'Remove vertex groups that have no weighted vertices from the selected mesh objects.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        count_meshes = 0
        total_removed = 0

        for obj in context.selected_objects:
            if obj.type != 'MESH' or not obj.data or not obj.data.vertices:
                continue

            used_groups = set()
            for vert in obj.data.vertices:
                for group in vert.groups:
                    used_groups.add(group.group)

            all_group_indices = {i for i, _ in enumerate(obj.vertex_groups)}
            unused_groups = all_group_indices - used_groups
            if not unused_groups:
                continue

            for index in sorted(unused_groups, reverse=True):
                group = obj.vertex_groups[index]
                obj.vertex_groups.remove(group)
                total_removed += 1
            count_meshes += 1

        self.report({'INFO'}, f'Removed {total_removed} unused group(s) on {count_meshes} mesh object(s)')
        return {'FINISHED'}
