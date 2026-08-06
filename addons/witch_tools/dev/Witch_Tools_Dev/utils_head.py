import bpy
import bmesh
from mathutils import Vector


def get_recursive_collection_objects(collection):
    objects = list(collection.objects)
    for child in collection.children:
        objects.extend(get_recursive_collection_objects(child))
    return objects


HEAD_EXCLUDE_KEYWORDS = ('ear', 'eyes', 'eyeshadow', 'eyelashes', 'mouth_interior', 'scalp', 'tearline')


def find_base_head_mesh(objects):
    for obj in objects:
        if obj.type != 'MESH':
            continue
        name = obj.name.lower()
        if 'mesh' not in name:
            continue
        if any(keyword in name for keyword in HEAD_EXCLUDE_KEYWORDS):
            continue
        return obj
    return None


def find_head_aux_meshes(objects):
    eyes = None
    mouth = None
    for obj in objects:
        if obj.type != 'MESH':
            continue
        name = obj.name.lower()
        if 'eyes' in name and 'eyeshadow' not in name:
            eyes = obj
        elif 'mouth_interior' in name:
            mouth = obj
    return eyes, mouth


def ensure_collection(name, scene_collection):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        scene_collection.children.link(collection)
    return collection


def boundary_loops_from_bmesh(bm):
    boundary_edges = [edge for edge in bm.edges if edge.is_boundary]
    if not boundary_edges:
        return []

    remaining = set(boundary_edges)
    loops = []
    while remaining:
        start = remaining.pop()
        loop = [start]
        current = start
        while True:
            next_edge = None
            for vert in current.verts:
                for edge in vert.link_edges:
                    if edge.is_boundary and edge != current and edge in remaining:
                        next_edge = edge
                        break
                if next_edge:
                    break
            if next_edge is None:
                break
            loop.append(next_edge)
            remaining.remove(next_edge)
            current = next_edge
        loops.append(loop)
    return loops



def ordered_loop_verts(edge_loop, start_vert=None):
    if not edge_loop:
        return []
    if start_vert is None:
        start_vert = edge_loop[0].verts[0]

    ordered = [start_vert]
    current_vert = start_vert
    current_edge = next((edge for edge in edge_loop if start_vert in edge.verts), None)
    if current_edge is None:
        return ordered

    for _ in range(len(edge_loop)):
        next_vert = current_edge.other_vert(current_vert)
        if next_vert == start_vert:
            break
        ordered.append(next_vert)
        found = False
        for edge in edge_loop:
            if edge != current_edge and next_vert in edge.verts:
                current_edge = edge
                current_vert = next_vert
                found = True
                break
        if not found:
            break
    return ordered



def closest_vert_pair(ear_verts, head_verts, obj_ear, obj_head):
    min_dist = float('inf')
    closest_pair = (None, None)
    for i, evert in enumerate(ear_verts):
        ear_co = obj_ear.matrix_world @ evert.co
        for j, hvert in enumerate(head_verts):
            head_co = obj_head.matrix_world @ hvert.co
            dist = (ear_co - head_co).length
            if dist < min_dist:
                min_dist = dist
                closest_pair = (i, j)
    return closest_pair[0], closest_pair[1], min_dist



def duplicate_object(context, obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    return context.active_object



def remove_object_if_exists(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)



def purge_orphans():
    try:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    except Exception:
        pass



def recalc_normals_edit_object(context, obj):
    previous_mode = obj.mode
    if context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    try:
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    except Exception:
        pass
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    if previous_mode == 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')



def object_world_avg_x(obj, verts):
    return sum((obj.matrix_world @ vert.co).x for vert in verts) / len(verts)



def centroid(verts):
    return Vector((
        sum(v.co.x for v in verts) / len(verts),
        sum(v.co.y for v in verts) / len(verts),
        sum(v.co.z for v in verts) / len(verts),
    ))
