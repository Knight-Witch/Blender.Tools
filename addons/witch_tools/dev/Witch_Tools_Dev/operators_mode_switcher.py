from bpy.types import Operator

from .runtime import next_switcher_mode, restore_temp_state, switch_mode


class WTM_OT_switch_edit_mode(Operator):
    bl_idname = 'wtm.switch_edit_mode'
    bl_label = 'Edit Mode'
    bl_description = 'Switch to Edit Mode. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'EDIT')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_switch_object_mode(Operator):
    bl_idname = 'wtm.switch_object_mode'
    bl_label = 'Object Mode'
    bl_description = 'Switch to Object Mode. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'OBJECT')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_toggle_weight_paint(Operator):
    bl_idname = 'wtm.toggle_weight_paint'
    bl_label = 'Weight Paint'
    bl_description = 'Switch to Weight Paint. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'WEIGHT_PAINT')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_toggle_pose_mode(Operator):
    bl_idname = 'wtm.toggle_pose_mode'
    bl_label = 'Pose Mode'
    bl_description = "Automatically selects the active object's armature and enters Pose Mode. Click again or use its hotkey to switch back to the last mode and active object."
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'POSE')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_switch_sculpt_mode(Operator):
    bl_idname = 'wtm.switch_sculpt_mode'
    bl_label = 'Sculpt Mode'
    bl_description = 'Switch to Sculpt Mode. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'SCULPT')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_switch_texture_paint_mode(Operator):
    bl_idname = 'wtm.switch_texture_paint_mode'
    bl_label = 'Texture Paint'
    bl_description = 'Switch to Texture Paint Mode. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'TEXTURE_PAINT')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_switch_vertex_paint_mode(Operator):
    bl_idname = 'wtm.switch_vertex_paint_mode'
    bl_label = 'Vertex Paint'
    bl_description = 'Switch to Vertex Paint Mode. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'VERTEX_PAINT')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_switch_uv_data_mode(Operator):
    bl_idname = 'wtm.switch_uv_data_mode'
    bl_label = 'UV Editing'
    bl_description = 'Switch to the UV Editing workspace for UV work. Click again or use its hotkey to switch back to the last mode and active object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, 'UV_DATA')
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_cycle_mode_switcher(Operator):
    bl_idname = 'wtm.cycle_mode_switcher'
    bl_label = 'Cycle'
    bl_description = 'Cycle through the Mode Switcher modes in the current tool order.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = switch_mode(context, next_switcher_mode(context))
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}


class WTM_OT_return_temp_mode(Operator):
    bl_idname = 'wtm.return_temp_mode'
    bl_label = 'Last Used'
    bl_description = 'Return to the last used non-switcher mode and object.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        ok, msg = restore_temp_state(context)
        if ok:
            return {'FINISHED'}
        self.report({'ERROR'}, msg)
        return {'CANCELLED'}
