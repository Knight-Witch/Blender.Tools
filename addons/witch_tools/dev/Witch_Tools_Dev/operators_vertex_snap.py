from bpy.types import Operator

from .utils_weights import selected_mesh_info, sync_edit_meshes


class MESH_OT_vertex_snap_global(Operator):
    bl_idname = 'mesh.vertex_snap_global'
    bl_label = 'Snap Vertices'
    bl_description = 'Snap one vertex to another in one click. Use selection order for single or multi-snap workflows.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def _snap_same_mesh(self, obj, ordered):
        if len(ordered) < 2:
            return False, 'Select at least 2 vertices'
        if len(ordered) % 2 != 0:
            return False, 'Select an even number of vertices on one mesh'
        half = len(ordered) // 2
        sources = ordered[:half]
        targets = ordered[half:]
        for source, target in zip(sources, targets):
            world = obj.matrix_world @ source.co
            target.co = obj.matrix_world.inverted() @ world
        return True, f'Snapped {half} vertex pair(s)'

    def _snap_two_meshes(self, active_obj, other_obj, active_data, other_data):
        sources = other_data['ordered']
        targets = active_data['ordered']
        if len(sources) != len(targets):
            return False, 'Source and target must have the same number of selected vertices'
        for source, target in zip(sources, targets):
            world = other_obj.matrix_world @ source.co
            target.co = active_obj.matrix_world.inverted() @ world
        return True, f'Snapped {len(sources)} vertex pair(s)'

    def execute(self, context):
        info = selected_mesh_info(context)
        meshes = list(info.keys())
        if not meshes:
            self.report({'ERROR'}, 'Select vertices first')
            return {'CANCELLED'}
        if len(meshes) == 1:
            ok, msg = self._snap_same_mesh(meshes[0], info[meshes[0]]['ordered'])
        elif len(meshes) == 2:
            active = context.active_object
            if active not in info:
                self.report({'ERROR'}, 'The active mesh must be one of the selected edit meshes')
                return {'CANCELLED'}
            other = meshes[0] if meshes[1] == active else meshes[1]
            ok, msg = self._snap_two_meshes(active, other, info[active], info[other])
        else:
            ok, msg = False, 'Vertex Snap supports one mesh or two meshes at a time'
        if not ok:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}
        sync_edit_meshes(context)
        self.report({'INFO'}, msg)
        return {'FINISHED'}
