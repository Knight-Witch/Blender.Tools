import uuid

import bmesh
import bpy
from bpy.props import BoolProperty, CollectionProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import Operator, PropertyGroup


_MAX_SLOTS = 20
_LAYER_PREFIX = 'wt_sel_slot_'


def _new_uid():
    return uuid.uuid4().hex[:12]


def _layer_name(uid, domain):
    return f'{_LAYER_PREFIX}{uid}_{domain}'


def _ensure_slot_identity(slot, fallback_index=0):
    if not slot.uid:
        slot.uid = _new_uid()
    if not slot.name:
        slot.name = f'Slot {fallback_index + 1}'


def ensure_selection_slots(scene):
    props = getattr(scene, 'witch_tools', None) if scene else None
    if props is None:
        return None
    if len(props.selection_slots) == 0:
        slot = props.selection_slots.add()
        slot.uid = _new_uid()
        slot.name = 'Slot 1'
        props.selection_slot_index = 0
    for index, slot in enumerate(props.selection_slots):
        _ensure_slot_identity(slot, index)
    props.selection_slot_index = max(0, min(props.selection_slot_index, len(props.selection_slots) - 1))
    return props.selection_slots


def _mesh_objects_in_edit_mode(context):
    objects = []
    seen_data = set()
    for obj in getattr(context, 'objects_in_mode_unique_data', ()) or ():
        if obj and obj.type == 'MESH' and obj.data not in seen_data:
            seen_data.add(obj.data)
            objects.append(obj)
    active = getattr(context, 'active_object', None)
    if not objects and active and active.type == 'MESH' and active.mode == 'EDIT':
        objects.append(active)
    return objects


def _domain_info(bm, domain):
    if domain == 'v':
        return bm.verts, bm.verts.layers.int
    if domain == 'e':
        return bm.edges, bm.edges.layers.int
    if domain == 'f':
        return bm.faces, bm.faces.layers.int
    raise ValueError(domain)


def _remove_layer_from_mesh(mesh, layer_name, domain):
    if mesh is None:
        return
    if getattr(mesh, 'is_editmode', False):
        bm = bmesh.from_edit_mesh(mesh)
        _elements, layers = _domain_info(bm, domain)
        layer = layers.get(layer_name)
        if layer is not None:
            layers.remove(layer)
            bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
        return
    attribute = mesh.attributes.get(layer_name)
    if attribute is not None:
        mesh.attributes.remove(attribute)


def _clear_slot_layers(slot):
    if not slot.uid:
        return
    object_refs = [ref.object for ref in slot.objects if ref.object and ref.object.type == 'MESH']
    seen_meshes = set()
    for obj in object_refs:
        mesh = obj.data
        if mesh in seen_meshes:
            continue
        seen_meshes.add(mesh)
        for domain in ('v', 'e', 'f'):
            _remove_layer_from_mesh(mesh, _layer_name(slot.uid, domain), domain)


def _reset_slot_metadata(slot):
    slot.has_data = False
    slot.use_vert = False
    slot.use_edge = False
    slot.use_face = False
    slot.vertex_count = 0
    slot.edge_count = 0
    slot.face_count = 0
    slot.objects.clear()


def _slot_at(context, index):
    scene = getattr(context, 'scene', None)
    slots = ensure_selection_slots(scene)
    if slots is None or index < 0 or index >= len(slots):
        return None
    return slots[index]


def _selection_mode(context):
    mode = tuple(bool(value) for value in context.tool_settings.mesh_select_mode)
    if not any(mode):
        return (True, False, False)
    return mode


def _selection_counts(objects, mode):
    totals = [0, 0, 0]
    per_object = []
    for obj in objects:
        bm = bmesh.from_edit_mesh(obj.data)
        counts = (
            sum(1 for vert in bm.verts if vert.select) if mode[0] else 0,
            sum(1 for edge in bm.edges if edge.select) if mode[1] else 0,
            sum(1 for face in bm.faces if face.select) if mode[2] else 0,
        )
        per_object.append((obj, counts))
        totals[0] += counts[0]
        totals[1] += counts[1]
        totals[2] += counts[2]
    return tuple(totals), per_object


def _write_slot_object(slot, obj, mode):
    bm = bmesh.from_edit_mesh(obj.data)
    selected_any = False
    domain_settings = (
        ('v', mode[0], bm.verts),
        ('e', mode[1], bm.edges),
        ('f', mode[2], bm.faces),
    )
    for domain, enabled, elements in domain_settings:
        if not enabled:
            continue
        _unused, layers = _domain_info(bm, domain)
        layer = layers.get(_layer_name(slot.uid, domain)) or layers.new(_layer_name(slot.uid, domain))
        for element in elements:
            value = 1 if element.select else 0
            element[layer] = value
            selected_any = selected_any or bool(value)
    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return selected_any


def _saved_objects(slot, context):
    objects = []
    seen_data = set()
    view_objects = context.view_layer.objects
    for ref in slot.objects:
        obj = ref.object
        if not obj or obj.type != 'MESH' or obj.data in seen_data:
            continue
        if view_objects.get(obj.name) is None:
            continue
        if obj.hide_get() or obj.hide_viewport:
            continue
        seen_data.add(obj.data)
        objects.append(obj)
    return objects


def _ensure_edit_mode_objects(context, objects):
    target_data = {obj.data for obj in objects}
    current_objects = _mesh_objects_in_edit_mode(context)
    current_data = {obj.data for obj in current_objects}
    if context.mode == 'EDIT_MESH' and current_data == target_data:
        return True

    if context.mode != 'OBJECT':
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            return False

    for obj in list(context.selected_objects):
        obj.select_set(False)
    for obj in objects:
        obj.select_set(True)
    context.view_layer.objects.active = objects[0]
    try:
        bpy.ops.object.mode_set(mode='EDIT')
    except Exception:
        return False
    return True


def _read_slot_selection(slot, objects, mode):
    totals = [0, 0, 0]
    for obj in objects:
        bm = bmesh.from_edit_mesh(obj.data)
        for vert in bm.verts:
            vert.select_set(False)
        for edge in bm.edges:
            edge.select_set(False)
        for face in bm.faces:
            face.select_set(False)
        bm.select_history.clear()

        domain_settings = (
            ('v', mode[0], bm.verts, 0),
            ('e', mode[1], bm.edges, 1),
            ('f', mode[2], bm.faces, 2),
        )
        for domain, enabled, elements, total_index in domain_settings:
            if not enabled:
                continue
            _unused, layers = _domain_info(bm, domain)
            layer = layers.get(_layer_name(slot.uid, domain))
            if layer is None:
                continue
            for element in elements:
                if element[layer]:
                    element.select_set(True)
                    totals[total_index] += 1
        bm.select_flush_mode()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return tuple(totals)


class WTSelectionSlotObjectRef(PropertyGroup):
    object: PointerProperty(type=bpy.types.Object)


class WTSelectionSlotItem(PropertyGroup):
    name: StringProperty(
        name='Selection Slot Name',
        description='Editable name for this saved mesh-element selection',
        default='',
    )
    uid: StringProperty(default='')
    has_data: BoolProperty(default=False)
    use_vert: BoolProperty(default=False)
    use_edge: BoolProperty(default=False)
    use_face: BoolProperty(default=False)
    vertex_count: IntProperty(default=0, min=0)
    edge_count: IntProperty(default=0, min=0)
    face_count: IntProperty(default=0, min=0)
    objects: CollectionProperty(type=WTSelectionSlotObjectRef)


class MESH_OT_wt_selection_slot_add(Operator):
    bl_idname = 'mesh.wt_selection_slot_add'
    bl_label = 'Add Selection Slot'
    bl_description = 'Add another saved-selection slot'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.witch_tools
        was_empty = len(props.selection_slots) == 0
        ensure_selection_slots(context.scene)
        # The panel fallback uses Add to initialize legacy/new scenes safely outside
        # Panel.draw(). In that case Slot 1 was just created, so do not also add Slot 2.
        if was_empty:
            props.selection_slot_index = 0
            return {'FINISHED'}
        if len(props.selection_slots) >= _MAX_SLOTS:
            self.report({'WARNING'}, f'Maximum of {_MAX_SLOTS} selection slots reached')
            return {'CANCELLED'}
        slot = props.selection_slots.add()
        slot.uid = _new_uid()
        slot.name = f'Slot {len(props.selection_slots)}'
        props.selection_slot_index = len(props.selection_slots) - 1
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_remove(Operator):
    bl_idname = 'mesh.wt_selection_slot_remove'
    bl_label = 'Remove Selection Slot'
    bl_description = 'Delete this slot and its stored selection data'
    bl_options = {'REGISTER', 'UNDO'}

    slot_index: IntProperty(default=0, min=0)

    def execute(self, context):
        props = context.scene.witch_tools
        slot = _slot_at(context, self.slot_index)
        if slot is None:
            return {'CANCELLED'}
        _clear_slot_layers(slot)
        props.selection_slots.remove(self.slot_index)
        ensure_selection_slots(context.scene)
        props.selection_slot_index = min(self.slot_index, len(props.selection_slots) - 1)
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_save(Operator):
    bl_idname = 'mesh.wt_selection_slot_save'
    bl_label = 'Save Selection Slot'
    bl_description = 'Overwrite this slot with the current mesh vertex, edge, or face selection'
    bl_options = {'REGISTER', 'UNDO'}

    slot_index: IntProperty(default=0, min=0)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and bool(_mesh_objects_in_edit_mode(context))

    def execute(self, context):
        slot = _slot_at(context, self.slot_index)
        if slot is None:
            return {'CANCELLED'}
        _ensure_slot_identity(slot, self.slot_index)
        objects = _mesh_objects_in_edit_mode(context)
        mode = _selection_mode(context)
        totals, per_object = _selection_counts(objects, mode)
        if sum(totals) == 0:
            self.report({'WARNING'}, 'No vertices, edges, or faces are selected in the active selection mode')
            return {'CANCELLED'}

        _clear_slot_layers(slot)
        _reset_slot_metadata(slot)

        slot.use_vert, slot.use_edge, slot.use_face = mode
        for obj, counts in per_object:
            if sum(counts) == 0:
                continue
            if _write_slot_object(slot, obj, mode):
                ref = slot.objects.add()
                ref.object = obj

        slot.vertex_count, slot.edge_count, slot.face_count = totals
        slot.has_data = bool(len(slot.objects))
        context.scene.witch_tools.selection_slot_index = self.slot_index
        self.report(
            {'INFO'},
            f'Saved {totals[0]} vertices, {totals[1]} edges, and {totals[2]} faces to {slot.name}',
        )
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_clear(Operator):
    bl_idname = 'mesh.wt_selection_slot_clear'
    bl_label = 'Clear Selection Slot'
    bl_description = 'Erase the saved selection while keeping the slot and its name'
    bl_options = {'REGISTER', 'UNDO'}

    slot_index: IntProperty(default=0, min=0)

    def execute(self, context):
        slot = _slot_at(context, self.slot_index)
        if slot is None:
            return {'CANCELLED'}
        _clear_slot_layers(slot)
        _reset_slot_metadata(slot)
        context.scene.witch_tools.selection_slot_index = self.slot_index
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_clear_all(Operator):
    bl_idname = 'mesh.wt_selection_slot_clear_all'
    bl_label = 'Clear All Selection Slots'
    bl_description = 'Erase saved selection data from every slot while preserving the slot rows and names'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        slots = ensure_selection_slots(context.scene)
        for slot in slots:
            _clear_slot_layers(slot)
            _reset_slot_metadata(slot)
        self.report({'INFO'}, 'Cleared all saved selections')
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_reselect(Operator):
    bl_idname = 'mesh.wt_selection_slot_reselect'
    bl_label = 'Reselect Saved Selection'
    bl_description = 'Replace the current mesh selection with the vertices, edges, or faces stored in this slot'
    bl_options = {'REGISTER'}

    slot_index: IntProperty(default=0, min=0)

    def execute(self, context):
        slot = _slot_at(context, self.slot_index)
        if slot is None or not slot.has_data:
            self.report({'WARNING'}, 'This selection slot is empty')
            return {'CANCELLED'}
        objects = _saved_objects(slot, context)
        if not objects:
            self.report({'WARNING'}, 'None of the meshes saved in this slot are available and visible in the current view layer')
            return {'CANCELLED'}
        if not _ensure_edit_mode_objects(context, objects):
            self.report({'WARNING'}, 'Could not enter multi-object Edit Mode for the saved meshes')
            return {'CANCELLED'}

        mode = (slot.use_vert, slot.use_edge, slot.use_face)
        if not any(mode):
            mode = (True, False, False)
        context.tool_settings.mesh_select_mode = mode
        totals = _read_slot_selection(slot, objects, mode)
        context.scene.witch_tools.selection_slot_index = self.slot_index
        if sum(totals) == 0:
            self.report({'WARNING'}, 'The slot data exists, but no matching mesh elements remain')
            return {'CANCELLED'}
        self.report(
            {'INFO'},
            f'Reselected {totals[0]} vertices, {totals[1]} edges, and {totals[2]} faces from {slot.name}',
        )
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_rename(Operator):
    bl_idname = 'mesh.wt_selection_slot_rename'
    bl_label = 'Rename Selection Slot'
    bl_description = 'Rename a saved-selection slot'
    bl_options = {'REGISTER'}

    slot_index: IntProperty(default=0, min=0)
    name: StringProperty(name='Slot Name', default='')

    def execute(self, context):
        slot = _slot_at(context, self.slot_index)
        if slot is None:
            return {'CANCELLED'}
        slot.name = (self.name or '').strip() or f'Slot {self.slot_index + 1}'
        context.scene.witch_tools.selection_slot_index = self.slot_index
        return {'FINISHED'}


class MESH_OT_wt_selection_slot_move(Operator):
    bl_idname = 'mesh.wt_selection_slot_move'
    bl_label = 'Move Selection Slot'
    bl_description = 'Move this selection slot up or down in the list'
    bl_options = {'REGISTER'}

    slot_index: IntProperty(default=0, min=0)
    direction: StringProperty(default='UP')

    def execute(self, context):
        props = context.scene.witch_tools
        ensure_selection_slots(context.scene)
        source = self.slot_index
        target = source - 1 if self.direction == 'UP' else source + 1
        if source < 0 or source >= len(props.selection_slots) or target < 0 or target >= len(props.selection_slots):
            return {'CANCELLED'}
        props.selection_slots.move(source, target)
        props.selection_slot_index = target
        return {'FINISHED'}


CLASSES = (
    WTSelectionSlotObjectRef,
    WTSelectionSlotItem,
    MESH_OT_wt_selection_slot_add,
    MESH_OT_wt_selection_slot_remove,
    MESH_OT_wt_selection_slot_save,
    MESH_OT_wt_selection_slot_clear,
    MESH_OT_wt_selection_slot_clear_all,
    MESH_OT_wt_selection_slot_reselect,
    MESH_OT_wt_selection_slot_rename,
    MESH_OT_wt_selection_slot_move,
)
