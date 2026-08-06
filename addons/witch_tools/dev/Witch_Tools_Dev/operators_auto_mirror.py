from bpy.types import Operator

from .utils_context import active_mesh_for_panel


class _AutoMirrorBase:
    @classmethod
    def poll(cls, context):
        return active_mesh_for_panel(context) is not None

    def mesh(self, context):
        obj = active_mesh_for_panel(context)
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, 'Active mesh required')
            return None
        return obj


class WT_OT_toggle_auto_weight(Operator):
    bl_idname = 'witch_tools.toggle_auto_weight_mirror'
    bl_label = 'Auto Weight'
    bl_description = 'Automatically enable weight-paint X mirror when you enter Weight Paint mode.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        props.auto_enable_weight_paint_mirror = not props.auto_enable_weight_paint_mirror
        return {'FINISHED'}


class WT_OT_toggle_edit_x(_AutoMirrorBase, Operator):
    bl_idname = 'witch_tools.toggle_edit_x_mirror'
    bl_label = 'Edit X'
    bl_description = 'Toggle edit-mode X mirror on the active mesh.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = self.mesh(context)
        if obj is None:
            return {'CANCELLED'}
        obj.data.use_mirror_x = not bool(getattr(obj.data, 'use_mirror_x', False))
        return {'FINISHED'}


class WT_OT_toggle_topology(_AutoMirrorBase, Operator):
    bl_idname = 'witch_tools.toggle_topology_mirror'
    bl_label = 'Topology'
    bl_description = 'Toggle topology mirror on the active mesh.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = self.mesh(context)
        if obj is None:
            return {'CANCELLED'}
        obj.data.use_mirror_topology = not bool(getattr(obj.data, 'use_mirror_topology', False))
        return {'FINISHED'}


class WT_OT_toggle_weight_x(_AutoMirrorBase, Operator):
    bl_idname = 'witch_tools.toggle_weight_x_mirror'
    bl_label = 'Weight X'
    bl_description = 'Toggle weight-paint X mirror on the active mesh.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = self.mesh(context)
        if obj is None:
            return {'CANCELLED'}
        obj.use_mesh_mirror_x = not bool(getattr(obj, 'use_mesh_mirror_x', False))
        return {'FINISHED'}


class WT_OT_toggle_group_mirror(_AutoMirrorBase, Operator):
    bl_idname = 'witch_tools.toggle_mirror_vertex_groups'
    bl_label = 'Groups'
    bl_description = 'Toggle mirrored vertex-group behavior on the active mesh.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = self.mesh(context)
        if obj is None:
            return {'CANCELLED'}
        obj.data.use_mirror_vertex_groups = not bool(getattr(obj.data, 'use_mirror_vertex_groups', False))
        return {'FINISHED'}
