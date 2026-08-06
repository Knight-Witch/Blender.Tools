import bpy
import bmesh
import json
import uuid
from mathutils import Vector
from mathutils.kdtree import KDTree
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, FloatProperty, IntProperty, StringProperty

from .utils_context import addon_preferences


_TIMER_RUNNING = False
_GUARD_SUSPENDED = False


def _active_mesh(context):
    obj = context.object
    if not obj or obj.type != "MESH":
        return None
    return obj


def _parse_group(group):
    if not group.data:
        return {}
    try:
        data = json.loads(group.data)
    except Exception:
        return {}
    verts = data.get("verts", {})
    if not isinstance(verts, dict):
        return {}
    return verts


def _write_group(group, verts):
    clean = {}
    for key, value in verts.items():
        try:
            index = int(key)
            co = value
            if len(co) != 3:
                continue
            clean[str(index)] = [float(co[0]), float(co[1]), float(co[2])]
        except Exception:
            continue
    group.data = json.dumps({"verts": clean}, separators=(",", ":"))
    group.count = len(clean)





def _safe_mesh_update(mesh):
    try:
        if mesh:
            mesh.update()
    except Exception:
        pass

    try:
        if mesh and hasattr(mesh, "update_gpu_tag"):
            mesh.update_gpu_tag()
    except Exception:
        pass

    try:
        bpy.context.view_layer.update()
    except Exception:
        pass


def _safe_edit_mesh_update(obj, bm=None, loop_triangles=True, destructive=False):
    try:
        if bm is not None:
            bm.normal_update()
    except Exception:
        pass

    try:
        bmesh.update_edit_mesh(obj.data, loop_triangles=loop_triangles, destructive=destructive)
    except Exception:
        pass


def _selected_meshes(context):
    meshes = [obj for obj in context.selected_objects if obj and obj.type == "MESH"]
    if not meshes:
        obj = _active_mesh(context)
        if obj:
            meshes = [obj]
    return meshes


def _editable_meshes(context):
    meshes = []
    if hasattr(context, "objects_in_mode_unique_data"):
        meshes = [obj for obj in context.objects_in_mode_unique_data if obj and obj.type == "MESH"]
    if not meshes:
        meshes = _selected_meshes(context)
    return meshes


def _enforce_selected_meshes(context):
    changed = 0
    for obj in _selected_meshes(context):
        try:
            if _enforce_object(obj):
                changed += 1
        except Exception:
            pass
    return changed


def _set_sculpt_mask_for_object(obj, locked_indices=None, clear_unlocked=True):
    if not obj or obj.type != "MESH":
        return 0

    locked = locked_indices
    if locked is None:
        locked = _locked_indices(obj, only_enabled=True)

    if obj.mode == "EDIT":
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        mask_layer = bm.verts.layers.float.get(".sculpt_mask")
        if mask_layer is None:
            mask_layer = bm.verts.layers.float.new(".sculpt_mask")

        changed = 0
        for vert in bm.verts:
            target = 1.0 if vert.index in locked else 0.0
            if not clear_unlocked and vert.index not in locked:
                continue
            if abs(vert[mask_layer] - target) > 0.00001:
                vert[mask_layer] = target
                changed += 1

        _safe_edit_mesh_update(obj, bm, loop_triangles=True, destructive=False)
        return changed

    mesh = obj.data

    attr = None
    if hasattr(mesh, "attributes"):
        attr = mesh.attributes.get(".sculpt_mask")
        if attr is None:
            try:
                attr = mesh.attributes.new(".sculpt_mask", "FLOAT", "POINT")
            except Exception:
                attr = None

    changed = 0
    if attr is not None:
        for vert in mesh.vertices:
            target = 1.0 if vert.index in locked else 0.0
            if not clear_unlocked and vert.index not in locked:
                continue
            if abs(attr.data[vert.index].value - target) > 0.00001:
                attr.data[vert.index].value = target
                changed += 1
        _safe_mesh_update(mesh)
        return changed

    return 0


def _clear_sculpt_mask_for_object(obj):
    if not obj or obj.type != "MESH":
        return 0

    if obj.mode == "EDIT":
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        mask_layer = bm.verts.layers.float.get(".sculpt_mask")
        if mask_layer is None:
            return 0

        changed = 0
        for vert in bm.verts:
            if abs(vert[mask_layer]) > 0.00001:
                vert[mask_layer] = 0.0
                changed += 1

        _safe_edit_mesh_update(obj, bm, loop_triangles=True, destructive=False)
        return changed

    mesh = obj.data
    attr = mesh.attributes.get(".sculpt_mask") if hasattr(mesh, "attributes") else None
    if attr is None:
        return 0

    changed = 0
    for item in attr.data:
        if abs(item.value) > 0.00001:
            item.value = 0.0
            changed += 1

    _safe_mesh_update(mesh)
    return changed


def _selected_verts_with_coords(obj):
    selected = {}
    if obj.mode == "EDIT":
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        for vert in bm.verts:
            if vert.select:
                selected[vert.index] = [vert.co.x, vert.co.y, vert.co.z]
    else:
        for vert in obj.data.vertices:
            if vert.select:
                selected[vert.index] = [vert.co.x, vert.co.y, vert.co.z]
    return selected


def _coords_for_indices(obj, indices):
    coords = {}
    if obj.mode == "EDIT":
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        total = len(bm.verts)
        for index in indices:
            if 0 <= index < total:
                vert = bm.verts[index]
                coords[index] = [vert.co.x, vert.co.y, vert.co.z]
    else:
        total = len(obj.data.vertices)
        for index in indices:
            if 0 <= index < total:
                vert = obj.data.vertices[index]
                coords[index] = [vert.co.x, vert.co.y, vert.co.z]
    return coords


def _selected_indices(obj):
    if obj.mode == "EDIT":
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        return {vert.index for vert in bm.verts if vert.select}
    return {vert.index for vert in obj.data.vertices if vert.select}


def _locked_indices(obj, only_enabled=True):
    indices = set()
    for group in obj.wvl_lock_groups:
        if only_enabled and not group.locked:
            continue
        indices.update(int(index) for index in _parse_group(group).keys())
    return indices


def _new_group_name(obj, base="Lock Group"):
    existing = {group.name for group in obj.wvl_lock_groups}
    i = 1
    while True:
        name = f"{base} {i:03d}"
        if name not in existing:
            return name
        i += 1


def _add_group(obj, name, verts, locked=True, kind="LOCK"):
    group = obj.wvl_lock_groups.add()
    group.name = name
    group.uid = str(uuid.uuid4())
    group.locked = locked
    group.kind = kind
    _write_group(group, verts)
    obj.wvl_active_group = len(obj.wvl_lock_groups) - 1
    return group


def _ensure_active_group(obj):
    if len(obj.wvl_lock_groups) == 0:
        return _add_group(obj, _new_group_name(obj), {}, True, "LOCK")
    index = max(0, min(obj.wvl_active_group, len(obj.wvl_lock_groups) - 1))
    obj.wvl_active_group = index
    return obj.wvl_lock_groups[index]


def _active_group(obj):
    if len(obj.wvl_lock_groups) == 0:
        return None
    index = max(0, min(getattr(obj, "wvl_active_group", 0), len(obj.wvl_lock_groups) - 1))
    return obj.wvl_lock_groups[index]


def _enforce_object(obj):
    if not obj or obj.type != "MESH":
        return False
    groups = [group for group in obj.wvl_lock_groups if group.locked and group.data]
    if not groups:
        return False

    changed = False

    if obj.mode == "EDIT":
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        total = len(bm.verts)
        for group in groups:
            verts = _parse_group(group)
            for key, co in verts.items():
                index = int(key)
                if index < 0 or index >= total:
                    continue
                target = Vector((co[0], co[1], co[2]))
                vert = bm.verts[index]
                if (vert.co - target).length_squared > 0.0:
                    vert.co = target
                    changed = True
        if changed:
            _safe_edit_mesh_update(obj, bm, loop_triangles=True, destructive=False)
        return changed

    total = len(obj.data.vertices)
    for group in groups:
        verts = _parse_group(group)
        for key, co in verts.items():
            index = int(key)
            if index < 0 or index >= total:
                continue
            target = Vector((co[0], co[1], co[2]))
            vert = obj.data.vertices[index]
            if (vert.co - target).length_squared > 0.0:
                vert.co = target
                changed = True
    if changed:
        _safe_mesh_update(obj.data)
    return changed


def _timer():
    global _TIMER_RUNNING
    wm = bpy.context.window_manager
    if _GUARD_SUSPENDED:
        return 0.05
    if not getattr(wm, "wvl_guard_enabled", False):
        _TIMER_RUNNING = False
        return None

    try:
        _enforce_selected_meshes(bpy.context)
    except Exception:
        obj = bpy.context.object
        if obj and obj.type == "MESH":
            try:
                _enforce_object(obj)
            except Exception:
                pass

    return max(0.02, min(2.0, wm.wvl_guard_interval))


def _start_timer():
    global _TIMER_RUNNING
    if not _TIMER_RUNNING:
        _TIMER_RUNNING = True
        bpy.app.timers.register(_timer, first_interval=0.03)


def _selection_toggle_label(context):
    obj = _active_mesh(context)
    if not obj:
        return "Lock Selected Vertices"
    selected = _selected_indices(obj)
    if not selected:
        return "Lock Selected Vertices"
    locked = _locked_indices(obj, only_enabled=False)
    if selected and selected.issubset(locked):
        return "Unlock Selected Vertices"
    return "Lock Selected Vertices"


def _select_indices_edit_mode(obj, indices):
    if obj.mode != "EDIT":
        bpy.ops.object.mode_set(mode="EDIT")

    bpy.ops.mesh.select_mode(type="VERT")
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()

    for vert in bm.verts:
        vert.select_set(False)

    selected = 0
    total = len(bm.verts)
    for index in indices:
        if 0 <= index < total:
            bm.verts[index].select_set(True)
            selected += 1

    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return selected


def _detect_edit_zone(obj):
    if obj.mode != "EDIT":
        raise RuntimeError("Edit Zone must be created in Edit Mode from a vertex selection.")

    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()

    selected = {vert.index for vert in bm.verts if vert.select}
    if not selected:
        raise RuntimeError("Select the region you want to edit first.")

    all_indices = {vert.index for vert in bm.verts}
    outside = all_indices - selected
    boundary = set()

    for vert in bm.verts:
        if vert.index not in selected:
            continue
        for edge in vert.link_edges:
            other = edge.other_vert(vert)
            if other.index not in selected:
                boundary.add(vert.index)
                break

    interior = selected - boundary
    if not interior:
        raise RuntimeError("No editable interior was detected. Select a larger region with at least one inner row of vertices.")

    return selected, boundary, outside, interior


def _side_value(direction):
    if direction == "POS_TO_NEG":
        return 1.0, -1.0
    return -1.0, 1.0


def _mirror_x(co):
    return Vector((-co.x, co.y, co.z))


def _non_destructive_mirror_edit(obj, direction, selected_target_only, max_distance, preserve_locked):
    if obj.mode != "EDIT":
        raise RuntimeError("Non-destructive shape mirror must be run in Edit Mode.")

    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()

    source_side, target_side = _side_value(direction)
    locked = _locked_indices(obj, only_enabled=True) if preserve_locked else set()

    source_verts = []
    target_verts = []

    for vert in bm.verts:
        if preserve_locked and vert.index in locked:
            continue

        x = vert.co.x
        is_source = x * source_side > 0.000001
        is_target = x * target_side > 0.000001

        if is_source and vert.select:
            source_verts.append(vert)

        if is_target:
            if selected_target_only and not vert.select:
                continue
            target_verts.append(vert)

    if not source_verts:
        raise RuntimeError("No selected source-side vertices found. Select the side you want to copy from.")
    if not target_verts:
        raise RuntimeError("No target-side vertices found. Disable 'Selected Target Only' or select the matching target area too.")

    tree = KDTree(len(target_verts))
    target_lookup = {}
    for i, vert in enumerate(target_verts):
        tree.insert(vert.co, i)
        target_lookup[i] = vert
    tree.balance()

    moved = 0
    skipped = 0
    used_targets = set()

    for source in source_verts:
        mirrored = _mirror_x(source.co)
        found = tree.find(mirrored)

        if not found:
            skipped += 1
            continue

        _location, target_index, distance = found
        if max_distance > 0.0 and distance > max_distance:
            skipped += 1
            continue

        target = target_lookup[target_index]
        if preserve_locked and target.index in locked:
            skipped += 1
            continue
        if target.index in used_targets:
            skipped += 1
            continue

        target.co = mirrored
        used_targets.add(target.index)
        moved += 1

    if moved:
        _safe_edit_mesh_update(obj, bm, loop_triangles=True, destructive=False)
    return moved, skipped


class WVL_LockGroup(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Lock Group")
    uid: StringProperty(default="")
    locked: BoolProperty(name="Locked", default=True)
    count: IntProperty(name="Vertices", default=0)
    data: StringProperty(name="Data", default="")
    kind: StringProperty(name="Kind", default="LOCK")


class WVL_UL_lock_groups(bpy.types.UIList):
    def filter_items(self, context, data, propname):
        items = getattr(data, propname, [])
        query = getattr(context.scene.witch_tools, 'vertex_locks_group_filter', '').strip().lower()
        if not query:
            return [self.bitflag_filter_item] * len(items), []
        flags = []
        for item in items:
            visible = query in getattr(item, 'name', '').lower()
            flags.append(self.bitflag_filter_item if visible else 0)
        return flags, []

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        kind_icon = {
            'EDITABLE': 'SELECT_INTERSECT',
            'BOUNDARY': 'LOCKED',
            'OUTSIDE': 'HIDE_OFF',
            'LOCK': 'GROUP_VERTEX',
        }.get(getattr(item, 'kind', ''), 'GROUP_VERTEX')
        row.label(text='', icon=kind_icon)
        if item.kind == "EDITABLE":
            row.prop(item, "name", text="", emboss=False)
        else:
            row.prop(item, "locked", text="", emboss=True, icon_only=True)
            row.prop(item, "name", text="", emboss=False)
        count = row.row(align=True)
        count.alignment = 'RIGHT'
        count.label(text=str(item.count))


class WVL_OT_toggle_guard(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.toggle_guard"
    bl_label = "Toggle Vertex Lock Guard"
    bl_description = "Turn on to lock vertices outside designated area. Turn off to unlock protected vertices."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        wm.wvl_guard_enabled = not wm.wvl_guard_enabled
        if wm.wvl_guard_enabled:
            _start_timer()
            self.report({"INFO"}, "Vertex Lock Guard enabled.")
        else:
            self.report({"INFO"}, "Vertex Lock Guard disabled.")
        return {"FINISHED"}


class WVL_OT_lock_selected(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.lock_selected"
    bl_label = "Lock Selected Vertices"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def description(cls, _context, properties):
        if getattr(properties, 'new_group', False):
            return 'Create a new lock group from the selected vertices and turn Guard on.'
        return 'Add the selected vertices to the active lock group and turn Guard on.'

    new_group: BoolProperty(default=False)

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        selected = _selected_verts_with_coords(obj)
        if not selected:
            self.report({"ERROR"}, "Select at least one vertex.")
            return {"CANCELLED"}

        if self.new_group or len(obj.wvl_lock_groups) == 0:
            group = _add_group(obj, _new_group_name(obj), selected, True, "LOCK")
        else:
            group = _ensure_active_group(obj)
            verts = _parse_group(group)
            for index, co in selected.items():
                verts[str(index)] = co
            group.locked = True
            _write_group(group, verts)

        context.window_manager.wvl_guard_enabled = True
        _start_timer()
        self.report({"INFO"}, f"Locked {len(selected)} selected vertices in {group.name}.")
        return {"FINISHED"}


class WVL_OT_create_edit_zone(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.create_edit_zone"
    bl_label = "Create Edit Zone From Selection"
    bl_description = "Create a protected edit zone from the current selection and lock the surrounding vertices for guarded editing."
    bl_options = {"REGISTER", "UNDO"}

    zone_name: StringProperty(name="Zone Name", default="Edit Zone")
    clear_existing: BoolProperty(name="Clear Existing Locks", default=True)

    def execute(self, context):
        meshes = _editable_meshes(context)
        if not meshes:
            self.report({"ERROR"}, "Select at least one mesh object.")
            return {"CANCELLED"}

        if context.mode != "EDIT_MESH":
            self.report({"ERROR"}, "Create Edit Zone must be run in Edit Mode.")
            return {"CANCELLED"}

        base = self.zone_name.strip() or "Edit Zone"
        created = 0
        total_interior = 0
        total_boundary = 0
        total_outside = 0
        errors = []

        for obj in meshes:
            try:
                selected, boundary, outside, interior = _detect_edit_zone(obj)
            except RuntimeError as error:
                errors.append(f"{obj.name}: {error}")
                continue

            if self.clear_existing:
                obj.wvl_lock_groups.clear()
                obj.wvl_active_group = 0

            existing_names = {group.name for group in obj.wvl_lock_groups}
            suffix = 1
            zone_base = base
            while f"{zone_base} - Boundary Anchors" in existing_names or f"{zone_base} - Outside Lock" in existing_names:
                suffix += 1
                zone_base = f"{base} {suffix:03d}"

            _add_group(
                obj,
                f"{zone_base} - Editable Interior",
                _coords_for_indices(obj, interior),
                False,
                "EDITABLE",
            )
            _add_group(
                obj,
                f"{zone_base} - Boundary Anchors",
                _coords_for_indices(obj, boundary),
                True,
                "BOUNDARY",
            )
            _add_group(
                obj,
                f"{zone_base} - Outside Lock",
                _coords_for_indices(obj, outside),
                True,
                "OUTSIDE",
            )

            obj.wvl_last_edit_zone_name = zone_base
            obj.wvl_last_edit_zone_indices = json.dumps({"interior": sorted(interior)}, separators=(",", ":"))

            _set_sculpt_mask_for_object(obj)
            _enforce_object(obj)

            created += 1
            total_interior += len(interior)
            total_boundary += len(boundary)
            total_outside += len(outside)

        if created == 0:
            self.report({"ERROR"}, errors[0] if errors else "No valid edit zones were created.")
            return {"CANCELLED"}

        active = _active_mesh(context)
        if active and active.wvl_last_edit_zone_indices:
            try:
                data = json.loads(active.wvl_last_edit_zone_indices)
                _select_indices_edit_mode(active, {int(index) for index in data.get("interior", [])})
            except Exception:
                pass

        context.window_manager.wvl_guard_enabled = True
        _start_timer()
        try:
            prefs = addon_preferences(context)
            if prefs is not None:
                prefs.show_vertex_locks_groups = True
        except Exception:
            pass

        if errors:
            self.report(
                {"WARNING"},
                f"Created edit zones on {created} mesh object(s). Some selected meshes had no valid selected zone.",
            )
        else:
            self.report(
                {"INFO"},
                f"Created edit zones on {created} mesh object(s): {total_interior} editable, {total_boundary} anchors, {total_outside} outside locked.",
            )
        return {"FINISHED"}


class WVL_OT_select_edit_zone_interior(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.select_edit_zone_interior"
    bl_label = "Select Editable Interior"
    bl_description = "Reselect the stored editable interior vertices for the current protected edit zone."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        if not obj.wvl_last_edit_zone_indices:
            self.report({"ERROR"}, "No stored editable interior selection for this object.")
            return {"CANCELLED"}

        try:
            data = json.loads(obj.wvl_last_edit_zone_indices)
            indices = {int(index) for index in data.get("interior", [])}
        except Exception:
            self.report({"ERROR"}, "Stored editable interior data is invalid.")
            return {"CANCELLED"}

        selected = _select_indices_edit_mode(obj, indices)
        self.report({"INFO"}, f"Selected {selected} editable interior vertices.")
        return {"FINISHED"}


class WVL_OT_mirror_shape_area(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.mirror_shape_area"
    bl_label = "Mirror Shape Area Without Deleting"
    bl_description = "Mirror the selected shape across the mesh without deleting or symmetrizing topology."
    bl_options = {"REGISTER", "UNDO"}

    direction: EnumProperty(
        name="Direction",
        items=(
            ("POS_TO_NEG", "+X to -X", "Copy selected +X shape to the -X side"),
            ("NEG_TO_POS", "-X to +X", "Copy selected -X shape to the +X side"),
        ),
        default="POS_TO_NEG",
    )
    selected_target_only: BoolProperty(
        name="Selected Target Only",
        default=False,
        description="Only move already-selected vertices on the target side",
    )
    preserve_locked: BoolProperty(
        name="Preserve Locked Vertices",
        default=True,
        description="Do not use locked vertices as source or target vertices",
    )
    max_distance: FloatProperty(
        name="Max Match Distance",
        default=0.25,
        min=0.0,
        soft_min=0.0,
        soft_max=1.0,
        description="Maximum distance allowed when finding the matching mirrored vertex. Use 0 for unlimited.",
    )

    def execute(self, context):
        global _GUARD_SUSPENDED

        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        if obj.mode != "EDIT":
            self.report({"ERROR"}, "Mirror Selected Shape must be run in Edit Mode on the active mesh.")
            return {"CANCELLED"}

        was_suspended = _GUARD_SUSPENDED
        _GUARD_SUSPENDED = True

        try:
            moved, skipped = _non_destructive_mirror_edit(
                obj,
                self.direction,
                self.selected_target_only,
                self.max_distance,
                self.preserve_locked,
            )
        except RuntimeError as error:
            _GUARD_SUSPENDED = was_suspended
            self.report({"ERROR"}, str(error))
            return {"CANCELLED"}
        except Exception as error:
            _GUARD_SUSPENDED = was_suspended
            self.report({"ERROR"}, f"Mirror failed: {error}")
            return {"CANCELLED"}

        _GUARD_SUSPENDED = was_suspended

        self.report({"INFO"}, f"Mirrored {moved} vertices without topology changes. Skipped {skipped}.")
        return {"FINISHED"}






class WVL_OT_apply_sculpt_mask_from_locks(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.apply_sculpt_mask_from_locks"
    bl_label = "Apply Sculpt Mask From Locks"
    bl_description = "Apply a sculpt mask to locked vertices so protected areas stay masked while sculpting."
    bl_options = {"REGISTER", "UNDO"}

    selected_meshes_only: BoolProperty(
        name="Selected Meshes Only",
        default=True,
        description="Apply masks to selected mesh objects instead of only the active mesh",
    )

    def execute(self, context):
        meshes = _selected_meshes(context) if self.selected_meshes_only else [_active_mesh(context)]
        meshes = [obj for obj in meshes if obj and obj.type == "MESH"]

        if not meshes:
            self.report({"ERROR"}, "Select at least one mesh object.")
            return {"CANCELLED"}

        total = 0
        for obj in meshes:
            total += _set_sculpt_mask_for_object(obj)

        self.report({"INFO"}, f"Applied sculpt masks from locked groups on {len(meshes)} mesh object(s). Updated {total} vertices.")
        return {"FINISHED"}


class WVL_OT_clear_sculpt_mask(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.clear_sculpt_mask"
    bl_label = "Clear Sculpt Mask"
    bl_description = "Clear the sculpt mask created from locked vertices."
    bl_options = {"REGISTER", "UNDO"}

    selected_meshes_only: BoolProperty(
        name="Selected Meshes Only",
        default=True,
        description="Clear masks on selected mesh objects instead of only the active mesh",
    )

    def execute(self, context):
        meshes = _selected_meshes(context) if self.selected_meshes_only else [_active_mesh(context)]
        meshes = [obj for obj in meshes if obj and obj.type == "MESH"]

        if not meshes:
            self.report({"ERROR"}, "Select at least one mesh object.")
            return {"CANCELLED"}

        total = 0
        for obj in meshes:
            total += _clear_sculpt_mask_for_object(obj)

        self.report({"INFO"}, f"Cleared sculpt masks on {len(meshes)} mesh object(s). Updated {total} vertices.")
        return {"FINISHED"}


class WVL_OT_refresh_mesh_normals(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.refresh_mesh_normals"
    bl_label = "Refresh Locked Mesh / Normals"
    bl_description = "Refresh Locked Mesh / Normals: refresh the locked mesh, viewport data, and protected coordinates after edits."
    bl_options = {"REGISTER", "UNDO"}

    recalc_outside: BoolProperty(
        name="Recalculate Outside",
        default=False,
        description="Recalculate face normals outside. Leave off if you only need a viewport refresh.",
    )

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        current_mode = obj.mode

        if current_mode == "EDIT":
            bm = bmesh.from_edit_mesh(obj.data)
            bm.verts.ensure_lookup_table()
            bm.faces.ensure_lookup_table()

            if self.recalc_outside and bm.faces:
                bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))

            _safe_edit_mesh_update(obj, bm, loop_triangles=True, destructive=False)
        else:
            _safe_mesh_update(obj.data)

        if context.window_manager.wvl_guard_enabled:
            _enforce_object(obj)

        self.report({"INFO"}, "Mesh normals/viewport data refreshed.")
        return {"FINISHED"}


class WVL_OT_unlock_selected(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.unlock_selected"
    bl_label = "Unlock Selected Vertices"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def description(cls, _context, properties):
        if getattr(properties, 'active_only', False):
            return 'Remove the selected vertices only from the active lock group.'
        return 'Remove the selected vertices from all lock groups.'

    active_only: BoolProperty(default=False)

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        selected = _selected_indices(obj)
        if not selected:
            self.report({"ERROR"}, "Select at least one vertex.")
            return {"CANCELLED"}

        groups = []
        if self.active_only:
            group = _active_group(obj)
            if group:
                groups = [group]
        else:
            groups = list(obj.wvl_lock_groups)

        removed = 0
        for group in groups:
            verts = _parse_group(group)
            before = len(verts)
            for index in selected:
                verts.pop(str(index), None)
            _write_group(group, verts)
            removed += before - len(verts)

        self.report({"INFO"}, f"Unlocked {removed} vertex lock entries.")
        return {"FINISHED"}


class WVL_OT_toggle_selected(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.toggle_selected"
    bl_label = "Lock Selected Vertices"
    bl_description = "Toggle the selected vertices between locked and unlocked across the current lock sets."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        selected = _selected_indices(obj)
        if not selected:
            self.report({"ERROR"}, "Select at least one vertex.")
            return {"CANCELLED"}

        locked = _locked_indices(obj, only_enabled=False)
        if selected.issubset(locked):
            return bpy.ops.witch_vertex_locks.unlock_selected(active_only=False)
        return bpy.ops.witch_vertex_locks.lock_selected(new_group=False)


class WVL_OT_group_toggle_lock(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.group_toggle_lock"
    bl_label = "Lock/Unlock Active Group"
    bl_description = "Lock/Unlock Active Group: enable or disable the active lock group without deleting it."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = _active_mesh(context)
        group = _active_group(obj) if obj else None
        if not group:
            self.report({"ERROR"}, "No active lock group.")
            return {"CANCELLED"}
        if group.kind == "EDITABLE":
            self.report({"ERROR"}, "Editable Interior is a selection set, not a lock group.")
            return {"CANCELLED"}

        group.locked = not group.locked
        if group.locked:
            context.window_manager.wvl_guard_enabled = True
            _start_timer()
            _enforce_object(obj)
        self.report({"INFO"}, f"{group.name} is now {'locked' if group.locked else 'unlocked'}.")
        return {"FINISHED"}


class WVL_OT_select_group(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.select_group"
    bl_label = "Select Active Lock Group"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def description(cls, _context, properties):
        if getattr(properties, 'all_groups', False):
            return 'Select all currently stored locked vertices across every lock group.'
        return 'Select the vertices stored in the active lock group.'

    all_groups: BoolProperty(default=False)

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        if self.all_groups:
            indices = _locked_indices(obj, only_enabled=False)
        else:
            group = _active_group(obj)
            if not group:
                self.report({"ERROR"}, "No active lock group.")
                return {"CANCELLED"}
            indices = {int(index) for index in _parse_group(group).keys()}

        if not indices:
            self.report({"ERROR"}, "No vertices in the requested lock set.")
            return {"CANCELLED"}

        selected = _select_indices_edit_mode(obj, indices)
        self.report({"INFO"}, f"Selected {selected} group vertices.")
        return {"FINISHED"}


class WVL_OT_delete_group(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.delete_group"
    bl_label = "Delete Active Lock Group"
    bl_description = "Delete Active Group: remove the active lock group and its stored vertex coordinates."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj or len(obj.wvl_lock_groups) == 0:
            self.report({"ERROR"}, "No active lock group.")
            return {"CANCELLED"}

        index = max(0, min(obj.wvl_active_group, len(obj.wvl_lock_groups) - 1))
        name = obj.wvl_lock_groups[index].name
        obj.wvl_lock_groups.remove(index)
        obj.wvl_active_group = max(0, min(index, len(obj.wvl_lock_groups) - 1))
        self.report({"INFO"}, f"Deleted {name}.")
        return {"FINISHED"}


class WVL_OT_unlock_all(bpy.types.Operator):
    bl_idname = "witch_vertex_locks.unlock_all"
    bl_label = "Unlock All"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def description(cls, _context, properties):
        if getattr(properties, 'clear_groups', False):
            return 'Clear all stored lock groups and remove the last protected edit zone state.'
        return 'Disable all lock groups without deleting them.'

    clear_groups: BoolProperty(default=False)

    def execute(self, context):
        obj = _active_mesh(context)
        if not obj:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        if self.clear_groups:
            obj.wvl_lock_groups.clear()
            obj.wvl_active_group = 0
            obj.wvl_last_edit_zone_name = ""
            obj.wvl_last_edit_zone_indices = ""
            self.report({"INFO"}, "Cleared all vertex lock groups.")
        else:
            for group in obj.wvl_lock_groups:
                group.locked = False
            self.report({"INFO"}, "Disabled all vertex lock groups without deleting them.")
        return {"FINISHED"}




CLASSES = (
    WVL_LockGroup,
    WVL_UL_lock_groups,
    WVL_OT_toggle_guard,
    WVL_OT_lock_selected,
    WVL_OT_create_edit_zone,
    WVL_OT_select_edit_zone_interior,
    WVL_OT_mirror_shape_area,
    WVL_OT_apply_sculpt_mask_from_locks,
    WVL_OT_clear_sculpt_mask,
    WVL_OT_refresh_mesh_normals,
    WVL_OT_unlock_selected,
    WVL_OT_toggle_selected,
    WVL_OT_group_toggle_lock,
    WVL_OT_select_group,
    WVL_OT_delete_group,
    WVL_OT_unlock_all,
)



def _safe_delete_rna_property(owner, name):
    if hasattr(owner, name):
        try:
            delattr(owner, name)
        except Exception:
            pass


def register_rna():
    import bpy
    from bpy.props import BoolProperty, CollectionProperty, EnumProperty, FloatProperty, IntProperty, StringProperty

    bpy.types.Object.wvl_lock_groups = CollectionProperty(type=WVL_LockGroup)
    bpy.types.Object.wvl_active_group = IntProperty(default=0)
    bpy.types.Object.wvl_last_edit_zone_name = StringProperty(default='')
    bpy.types.Object.wvl_last_edit_zone_indices = StringProperty(default='')

    bpy.types.WindowManager.wvl_guard_enabled = BoolProperty(default=False, description='Turn on to lock vertices outside designated area. Turn off to unlock protected vertices.')
    bpy.types.WindowManager.wvl_guard_interval = FloatProperty(
        name='Guard Interval',
        default=0.05,
        min=0.02,
        max=2.0,
        soft_min=0.03,
        soft_max=0.15,
        description='How often locked vertices are restored while the guard is enabled',
    )
    bpy.types.WindowManager.wvl_zone_name = StringProperty(name='Zone Name', default='', description='Name your protected zone.')
    bpy.types.WindowManager.wvl_clear_existing_on_zone = BoolProperty(
        name='Clear Existing Locks First',
        default=True,
        description='Remove old lock groups before creating a new protected edit zone',
    )
    bpy.types.WindowManager.wvl_mirror_direction = EnumProperty(
        name='Direction',
        items=(
            ('POS_TO_NEG', '+X to -X', 'Copy selected +X shape to the -X side'),
            ('NEG_TO_POS', '-X to +X', 'Copy selected -X shape to the +X side'),
        ),
        default='POS_TO_NEG',
    )
    bpy.types.WindowManager.wvl_mirror_selected_target_only = BoolProperty(
        name='Selected Target Only',
        default=False,
        description='Only move already-selected vertices on the target side',
    )
    bpy.types.WindowManager.wvl_mirror_preserve_locked = BoolProperty(
        name='Preserve Locked',
        default=True,
        description='Do not mirror from or onto currently locked vertices',
    )
    bpy.types.WindowManager.wvl_mirror_max_distance = FloatProperty(
        name='Max Match Distance',
        default=0.25,
        min=0.0,
        soft_min=0.0,
        soft_max=1.0,
        description='Maximum distance allowed when matching the mirrored target vertex. Use 0 for unlimited.',
    )


def unregister_rna():
    global _TIMER_RUNNING
    _TIMER_RUNNING = False
    for name in (
        'wvl_mirror_max_distance',
        'wvl_mirror_preserve_locked',
        'wvl_mirror_selected_target_only',
        'wvl_mirror_direction',
        'wvl_clear_existing_on_zone',
        'wvl_zone_name',
        'wvl_guard_interval',
        'wvl_guard_enabled',
    ):
        _safe_delete_rna_property(bpy.types.WindowManager, name)
    for name in (
        'wvl_last_edit_zone_indices',
        'wvl_last_edit_zone_name',
        'wvl_active_group',
        'wvl_lock_groups',
    ):
        _safe_delete_rna_property(bpy.types.Object, name)
