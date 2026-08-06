import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, UIList

from .utils_context import ensure_view3d_override, mode_set
from .utils_mirror import (
    backup_group,
    build_mirror_map,
    clear_group,
    detect_active_suffix_pair,
    is_same_name_candidate,
    vertex_group_weight_map,
    weight_group_names,
)


class WTM_OT_scan_groups(Operator):
    bl_idname = 'wtm.scan_groups'
    bl_label = 'Scan Vertex Groups'
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.witch_tools
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, 'Active object must be a mesh')
            return {'CANCELLED'}

        left_suffix, right_suffix = detect_active_suffix_pair(obj, props)
        props.wtm_detected_left_suffix = left_suffix
        props.wtm_detected_right_suffix = right_suffix
        source_suffix = left_suffix if props.wtm_source_suffix == 'LEFT' else right_suffix
        target_suffix = right_suffix if props.wtm_source_suffix == 'LEFT' else left_suffix

        props.wtm_groups.clear()
        paired_sources, paired_targets = set(), set()
        names = weight_group_names(obj)

        for name in sorted(names):
            if not name.endswith(source_suffix):
                continue
            pair = name[:-len(source_suffix)] + target_suffix
            if pair in names:
                item = props.wtm_groups.add()
                item.source_name = name
                item.target_name = pair
                item.kind = 'PAIRED'
                item.enabled = True
                paired_sources.add(name)
                paired_targets.add(pair)

        if props.wtm_include_single:
            for name in sorted(names):
                if name in paired_sources or name in paired_targets:
                    continue
                if is_same_name_candidate(name, left_suffix, right_suffix):
                    item = props.wtm_groups.add()
                    item.source_name = name
                    item.target_name = name
                    item.kind = 'SINGLE'
                    item.enabled = False

        props.wtm_active_index = 0
        self.report({'INFO'}, f'Scanned {len(props.wtm_groups)} groups using {left_suffix} / {right_suffix}')
        return {'FINISHED'}


class WTM_OT_select_defaults(Operator):
    bl_idname = 'wtm.select_defaults'
    bl_label = 'Select Defaults'
    bl_options = {'REGISTER'}

    mode: EnumProperty(items=[('ALL', 'All', ''), ('NONE', 'None', ''), ('PAIRED', 'Paired', ''), ('SINGLE', 'Single', '')])

    def execute(self, context):
        groups = context.scene.witch_tools.wtm_groups
        for item in groups:
            if self.mode == 'ALL':
                item.enabled = True
            elif self.mode == 'NONE':
                item.enabled = False
            elif self.mode == 'PAIRED':
                item.enabled = item.kind == 'PAIRED'
            elif self.mode == 'SINGLE':
                item.enabled = item.kind == 'SINGLE'
        return {'FINISHED'}


class WTM_OT_restore_backups(Operator):
    bl_idname = 'wtm.restore_backups'
    bl_label = 'Restore Backups'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, 'Active object must be a mesh')
            return {'CANCELLED'}
        restored = 0
        for vg in list(obj.vertex_groups):
            if not vg.name.endswith('__WTM_BAK'):
                continue
            original_name = vg.name[:-10]
            target = obj.vertex_groups.get(original_name) or obj.vertex_groups.new(name=original_name)
            clear_group(target, len(obj.data.vertices))
            for vidx, weight in vertex_group_weight_map(obj, vg.index).items():
                target.add([vidx], weight, 'REPLACE')
            restored += 1
        self.report({'INFO'}, f'Restored {restored} groups')
        return {'FINISHED'}


class WTM_OT_mirror_selected(Operator):
    bl_idname = 'wtm.mirror_selected'
    bl_label = 'Mirror Selected Weights'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.witch_tools
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, 'Active object must be a mesh')
            return {'CANCELLED'}
        enabled = [item for item in props.wtm_groups if item.enabled]
        if not enabled:
            self.report({'ERROR'}, 'No enabled groups to mirror')
            return {'CANCELLED'}

        mapping = build_mirror_map(obj, props.wtm_mirror_tolerance)
        if not mapping:
            self.report({'ERROR'}, 'No mirrored vertex pairs found')
            return {'CANCELLED'}

        vertex_count = len(obj.data.vertices)
        half_sign = -1 if props.wtm_single_source_half == 'NEGATIVE_X' else 1
        success, skipped = 0, 0

        for item in enabled:
            src = obj.vertex_groups.get(item.source_name)
            if src is None:
                item.status = 'Missing source'
                skipped += 1
                continue

            if props.wtm_backup_groups:
                backup_group(obj, item.target_name)

            if item.kind == 'PAIRED':
                dst = obj.vertex_groups.get(item.target_name) or obj.vertex_groups.new(name=item.target_name)
                clear_group(dst, vertex_count)
                assigned = 0
                for src_index, weight in vertex_group_weight_map(obj, src.index).items():
                    dst_index = mapping.get(src_index)
                    if dst_index is None:
                        continue
                    dst.add([dst_index], weight, 'REPLACE')
                    assigned += 1
                item.status = f'{assigned} verts'
                success += 1
            else:
                mirrored = []
                for src_index, weight in vertex_group_weight_map(obj, src.index).items():
                    vert = obj.data.vertices[src_index]
                    if half_sign < 0 and vert.co.x >= -props.wtm_center_epsilon:
                        continue
                    if half_sign > 0 and vert.co.x <= props.wtm_center_epsilon:
                        continue
                    dst_index = mapping.get(src_index)
                    if dst_index is None:
                        continue
                    mirrored.append((dst_index, weight))
                for dst_index, weight in mirrored:
                    src.add([dst_index], weight, 'REPLACE')
                item.status = f'{len(mirrored)} verts'
                success += 1

        if props.wtm_normalize_after:
            try:
                mode_before = obj.mode
                mode_set(context, obj, 'WEIGHT_PAINT')
                override = ensure_view3d_override(context, obj)
                if override is not None:
                    with context.temp_override(**override):
                        bpy.ops.object.vertex_group_normalize_all(lock_active=False)
                mode_set(context, obj, 'EDIT' if mode_before == 'EDIT_MESH' else mode_before)
            except Exception:
                pass

        self.report({'INFO'}, f'Mirrored {success} groups, skipped {skipped}')
        return {'FINISHED'}


class WTM_UL_group_list(UIList):
    def draw_item(self, _context, layout, _data, item, _icon, _active_data, _active_propname, _index):
        row = layout.row(align=True)
        row.prop(item, 'enabled', text='')
        row.label(text=f'{item.source_name} -> {item.target_name}' if item.kind == 'PAIRED' else item.source_name)
        row.label(text=item.kind.title())
        if item.status:
            row.label(text=item.status)
