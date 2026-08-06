import bpy
import re
from bpy.types import Operator

from .utils_head import (
    ensure_collection,
    find_base_head_mesh,
    find_head_aux_meshes,
    get_recursive_collection_objects,
)


class WT_OT_head_batch_rename(Operator):
    bl_idname = 'witch_tools.head_batch_rename'
    bl_label = 'Batch Rename & Unify Names'
    bl_description = 'Batch rename selected objects and unify object, mesh data, and UV map names.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_objects:
            self.report({'WARNING'}, 'No mesh objects selected')
            return {'CANCELLED'}

        selected_race = props.head_race if props.head_race != 'NONE' else None
        head_name = props.head_name.strip() or None
        races = ['DGB', 'DWR', 'ELF', 'HEL', 'HUM', 'GTY', 'GNO', 'HFL', 'HRC', 'TIF']
        body_types = ['F', 'M', 'FS', 'MS']
        race_pattern = '|'.join(races)
        body_pattern = '|'.join(body_types)
        mesh_suffixes = [
            'Mouth_Interior_Fangs_Mesh',
            'Mouth_Interior_Mesh',
            'Eyeshadow_Mesh',
            'Eyelashes_Mesh',
            'Tearline_Mesh',
            'Scalp_Mesh',
            'Eyes_Mesh',
            'Ears_Mesh',
            '_Mesh',
        ]

        for obj in selected_objects:
            new_name = obj.name
            nkd_match = re.match(f'^({race_pattern})_({body_pattern})_NKD_Head_([A-Z])_', obj.name)
            if nkd_match:
                original_race, body_type, letter = nkd_match.groups()
                rest = obj.name[nkd_match.end():]
                if selected_race and head_name:
                    new_name = f'{selected_race}_{body_type}_{head_name}_{rest}'
                elif head_name:
                    new_name = f'{original_race}_{body_type}_{head_name}_{rest}'
                elif selected_race:
                    new_name = f'{selected_race}_{body_type}_NKD_Head_{letter}_{rest}'
            else:
                custom_match = re.match(f'^({race_pattern})_({body_pattern})_([^_]+)_', obj.name)
                if custom_match:
                    original_race, body_type, original_head_name = custom_match.groups()
                    rest = obj.name[custom_match.end():]
                    if selected_race and head_name:
                        new_name = f'{selected_race}_{body_type}_{head_name}_{rest}'
                    elif head_name:
                        new_name = f'{original_race}_{body_type}_{head_name}_{rest}'
                    elif selected_race:
                        new_name = f'{selected_race}_{body_type}_{original_head_name}_{rest}'

            for suffix in mesh_suffixes:
                if suffix in new_name:
                    idx = new_name.find(suffix)
                    new_name = new_name[:idx + len(suffix)]
                    break

            obj.name = new_name
            if obj.data:
                obj.data.name = new_name
                if obj.data.uv_layers:
                    uv_name = f'{new_name}-uvs0'
                    for uv_layer in obj.data.uv_layers:
                        uv_layer.name = uv_name

        self.report({'INFO'}, f'Renamed {len(selected_objects)} mesh object(s)')
        return {'FINISHED'}


class WT_OT_create_head_collections(Operator):
    bl_idname = 'witch_tools.create_head_collections'
    bl_label = 'Create Collections'
    bl_description = "Create 'base', 'vanilla', and 'edited' collections."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        created = []
        for name in ('base', 'vanilla', 'edited'):
            existing = bpy.data.collections.get(name)
            if existing is None:
                ensure_collection(name, context.scene.collection)
                created.append(name)
        self.report({'INFO'}, f"Created: {', '.join(created)}" if created else 'All collections already exist')
        return {'FINISHED'}


class WT_OT_join_head_collection_meshes(Operator):
    bl_idname = 'witch_tools.join_head_collection_meshes'
    bl_label = 'Join Head / Eyes / Mouth'
    bl_description = 'Join base head mesh with eyes and mouth interior inside vanilla and edited collections.'
    bl_options = {'REGISTER', 'UNDO'}

    def _join_collection(self, context, collection_name, output_name):
        collection = bpy.data.collections.get(collection_name)
        if collection is None:
            return False, f"Collection '{collection_name}' not found"

        objects = [obj for obj in get_recursive_collection_objects(collection) if obj.type == 'MESH']
        base = find_base_head_mesh(objects)
        eyes, mouth = find_head_aux_meshes(objects)
        join_list = [obj for obj in (base, eyes, mouth) if obj is not None]
        if not join_list:
            return False, f"No matching meshes found in '{collection_name}'"

        bpy.ops.object.select_all(action='DESELECT')
        for obj in join_list:
            obj.select_set(True)
        context.view_layer.objects.active = join_list[0]
        bpy.ops.object.join()
        context.active_object.name = output_name
        context.active_object.data.name = output_name
        return True, f"Joined {len(join_list)} mesh(es) into '{output_name}'"

    def execute(self, context):
        results = []
        for collection_name, output_name in (('vanilla', 'joined-vanilla'), ('edited', 'joined-edited')):
            _ok, message = self._join_collection(context, collection_name, output_name)
            results.append(message)
        self.report({'INFO'}, ' | '.join(results))
        return {'FINISHED'}


class WT_OT_delete_other_head_meshes(Operator):
    bl_idname = 'witch_tools.delete_other_head_meshes'
    bl_label = 'Delete All Other Meshes'
    bl_description = 'Delete non-armature objects inside the base / vanilla / edited collections except joined outputs and ears.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        names = {'base', 'vanilla', 'edited'}
        targets = []
        for name in names:
            collection = bpy.data.collections.get(name)
            if collection is None:
                continue
            for obj in get_recursive_collection_objects(collection):
                if obj.type == 'ARMATURE':
                    continue
                lower = obj.name.lower()
                if obj.name in {'joined-vanilla', 'joined-edited'}:
                    continue
                if 'ears' in lower:
                    continue
                targets.append(obj)
        seen = set()
        deleted = 0
        for obj in targets:
            if obj.name in seen:
                continue
            seen.add(obj.name)
            bpy.data.objects.remove(obj, do_unlink=True)
            deleted += 1
        self.report({'INFO'}, f'Deleted {deleted} object(s) from managed head collections')
        return {'FINISHED'}


class WT_OT_beautify_armature(Operator):
    bl_idname = 'witch_tools.beautify_armature'
    bl_label = 'Beautify Armature'
    bl_description = 'Delete Icosphere helpers and set the active armature to stick display.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        armature = context.active_object
        for obj in list(bpy.data.objects):
            if obj.name.startswith('Icosphere'):
                bpy.data.objects.remove(obj, do_unlink=True)
        armature.data.display_type = 'STICK'
        armature.show_in_front = False
        self.report({'INFO'}, 'Armature display cleaned up')
        return {'FINISHED'}


CLASSES = (
    WT_OT_head_batch_rename,
    WT_OT_create_head_collections,
    WT_OT_join_head_collection_meshes,
    WT_OT_delete_other_head_meshes,
    WT_OT_beautify_armature,
)
