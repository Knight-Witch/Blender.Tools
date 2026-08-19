import bpy
import bmesh
from mathutils import Vector
from bpy.types import Panel
from .state import PANEL_CATEGORY, PANEL_ORDERS


def _selected_edit_verts(context):
    obj = context.active_object
    if not obj or obj.type != 'MESH' or context.mode != 'EDIT_MESH': return None, []
    bm = bmesh.from_edit_mesh(obj.data)
    return bm, [v for v in bm.verts if v.select and not v.hide]


def _selection_median(verts):
    if not verts: return None
    co = verts[0].co.copy()
    for v in verts[1:]: co += v.co
    return co / len(verts)


def _get_edit_location(self):
    context = bpy.context; bm, verts = _selected_edit_verts(context); median = _selection_median(verts)
    if median is not None: return tuple(median)
    obj = context.active_object
    return tuple(obj.location) if obj else (0.0,0.0,0.0)


def _set_edit_location(self, value):
    context = bpy.context; bm, verts = _selected_edit_verts(context); median = _selection_median(verts)
    if bm is not None and median is not None:
        delta = Vector(value) - median
        for v in verts: v.co += delta
        bmesh.update_edit_mesh(context.active_object.data, loop_triangles=False, destructive=False)
        return
    obj = context.active_object
    if obj: obj.location = value


class WTTransformSelectionState(bpy.types.PropertyGroup):
    edit_location: bpy.props.FloatVectorProperty(name='Location', size=3, subtype='TRANSLATION', unit='LENGTH', get=_get_edit_location, set=_set_edit_location)


class VIEW3D_PT_wt_transform(Panel):
    bl_label = 'Transform'; bl_idname = 'VIEW3D_PT_wt_transform'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['TRANSFORM']; bl_description = 'Editable location, rotation, and scale without leaving the Witch Tools tab.'
    @classmethod
    def poll(cls, context): return context.active_object is not None
    def draw(self, context):
        obj = context.active_object
        if context.mode == 'EDIT_MESH' and obj.type == 'MESH':
            bm, verts = _selected_edit_verts(context)
            if verts: self.layout.label(text=f'Selection: {len(verts)} vert' + ('' if len(verts) == 1 else 's'), icon='VERTEXSEL')
            else: self.layout.label(text='No mesh vertices selected', icon='INFO')
        else: self.layout.label(text=obj.name, icon='OBJECT_DATA')


class VIEW3D_PT_wt_transform_location(Panel):
    bl_label = 'Location'; bl_idname = 'VIEW3D_PT_wt_transform_location'; bl_parent_id = 'VIEW3D_PT_wt_transform'
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY
    def draw(self, context):
        obj = context.active_object
        if context.mode == 'EDIT_MESH' and obj and obj.type == 'MESH':
            self.layout.prop(context.scene.wt_transform_state, 'edit_location', text='')
            self.layout.label(text='Selected mesh coordinates (local)', icon='VERTEXSEL')
        elif obj: self.layout.prop(obj, 'location', text='')


class VIEW3D_PT_wt_transform_rotation(Panel):
    bl_label = 'Rotation'; bl_idname = 'VIEW3D_PT_wt_transform_rotation'; bl_parent_id = 'VIEW3D_PT_wt_transform'
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY
    def draw(self, context):
        obj = context.active_object
        if not obj: return
        self.layout.prop(obj, 'rotation_mode', text='Mode')
        if obj.rotation_mode == 'QUATERNION': self.layout.prop(obj, 'rotation_quaternion', text='')
        elif obj.rotation_mode == 'AXIS_ANGLE': self.layout.prop(obj, 'rotation_axis_angle', text='')
        else: self.layout.prop(obj, 'rotation_euler', text='')
        if context.mode == 'EDIT_MESH': self.layout.label(text='Object rotation', icon='OBJECT_ORIGIN')


class VIEW3D_PT_wt_transform_scale(Panel):
    bl_label = 'Scale'; bl_idname = 'VIEW3D_PT_wt_transform_scale'; bl_parent_id = 'VIEW3D_PT_wt_transform'
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY
    def draw(self, context):
        obj = context.active_object
        if obj:
            self.layout.prop(obj, 'scale', text='')
            if context.mode == 'EDIT_MESH': self.layout.label(text='Object scale', icon='OBJECT_ORIGIN')


PANELS = (VIEW3D_PT_wt_transform, VIEW3D_PT_wt_transform_location, VIEW3D_PT_wt_transform_rotation, VIEW3D_PT_wt_transform_scale)
CLASSES = (WTTransformSelectionState,)

def register_props(): bpy.types.Scene.wt_transform_state = bpy.props.PointerProperty(type=WTTransformSelectionState)
def unregister_props():
    if hasattr(bpy.types.Scene, 'wt_transform_state'): del bpy.types.Scene.wt_transform_state
