import bpy
import bmesh
import importlib
import os
import re
import struct
import sys
from mathutils import Vector
from bpy.types import Operator, PropertyGroup
from bpy.props import IntProperty, StringProperty, PointerProperty


RESULT_FIELDS = (
    ('non_manifold_edges', 'Non-manifold Edges'),
    ('bad_contiguous_edges', 'Bad Contiguous Edges'),
    ('intersect_faces', 'Intersect Faces'),
    ('shells', 'Shells'),
    ('zero_faces', 'Zero Faces'),
    ('zero_edges', 'Zero Edges'),
    ('non_flat_faces', 'Non-flat Faces'),
    ('thin_faces', 'Thin Faces'),
    ('sharp_edges', 'Sharp Edges'),
    ('overhang_faces', 'Overhang Faces'),
)

RESULT_ICONS = {
    'non_manifold_edges': 'EDGESEL',
    'bad_contiguous_edges': 'EDGESEL',
    'intersect_faces': 'FACESEL',
    'zero_faces': 'FACESEL',
    'zero_edges': 'EDGESEL',
    'non_flat_faces': 'FACESEL',
    'thin_faces': 'FACESEL',
    'sharp_edges': 'EDGESEL',
    'overhang_faces': 'FACESEL',
}


class WTPrint3DProperties(PropertyGroup):
    export_directory: StringProperty(name='Export Folder', subtype='DIR_PATH', default='//')
    non_manifold_edges: IntProperty(default=0, min=0)
    bad_contiguous_edges: IntProperty(default=0, min=0)
    intersect_faces: IntProperty(default=0, min=0)
    shells: IntProperty(default=0, min=0)
    zero_faces: IntProperty(default=0, min=0)
    zero_edges: IntProperty(default=0, min=0)
    non_flat_faces: IntProperty(default=0, min=0)
    thin_faces: IntProperty(default=0, min=0)
    sharp_edges: IntProperty(default=0, min=0)
    overhang_faces: IntProperty(default=0, min=0)
    last_analyzed_object: StringProperty(default='')


def _mesh_object(context):
    obj = context.active_object
    return obj if obj and obj.type == 'MESH' else None


def _field_from_report_text(text):
    text = re.sub(r'[^a-z0-9]+', ' ', str(text).lower()).strip()
    if 'non manifold' in text:
        return 'non_manifold_edges'
    if 'bad contiguous' in text or 'bad contig' in text:
        return 'bad_contiguous_edges'
    if 'intersect' in text:
        return 'intersect_faces'
    if 'shell' in text:
        return 'shells'
    if 'zero face' in text:
        return 'zero_faces'
    if 'zero edge' in text:
        return 'zero_edges'
    if 'non flat' in text or 'nonflat' in text:
        return 'non_flat_faces'
    if 'thin face' in text or text.startswith('thin '):
        return 'thin_faces'
    if 'sharp edge' in text or text.startswith('sharp '):
        return 'sharp_edges'
    if 'overhang face' in text or text.startswith('overhang '):
        return 'overhang_faces'
    return None


def _find_toolbox_report_module():
    """Find the report module belonging to the installed Blender 3D Print Toolbox extension."""
    candidates = (
        'bl_ext.blender_org.print3d_toolbox.report',
        'print3d_toolbox.report',
        'object_print3d_utils.report',
    )
    for name in candidates:
        try:
            module = importlib.import_module(name)
        except Exception:
            continue
        if callable(getattr(module, 'info', None)):
            return module

    for name, module in tuple(sys.modules.items()):
        low = name.lower()
        if 'print3d' not in low or not low.endswith('.report'):
            continue
        if module is not None and callable(getattr(module, 'info', None)):
            return module
    return None


def _toolbox_report_info():
    module = _find_toolbox_report_module()
    if module is None:
        return ()
    try:
        return tuple(module.info())
    except Exception:
        return ()


def get_toolbox_report_entry(field):
    """Return (report index, text, data) for one live 3D Print Toolbox report field."""
    for index, item in enumerate(_toolbox_report_info()):
        if not isinstance(item, (tuple, list)) or len(item) < 2:
            continue
        text, data = item[0], item[1]
        if _field_from_report_text(text) == field:
            return index, text, data
    return None


def _report_count(text, data):
    match = re.search(r'(-?\d+)\s*$', str(text).replace(',', ''))
    if match:
        return max(0, int(match.group(1)))
    if data and isinstance(data, (tuple, list)) and len(data) > 1:
        try:
            return max(0, len(data[1]))
        except Exception:
            pass
    return 0


def _run_toolbox_check_all(context):
    """Run Blender's actual installed 3D Print Toolbox analyzer and return its report verbatim."""
    try:
        op = bpy.ops.mesh.print3d_check_all
        if not op.poll():
            return None, '3D Print Toolbox Check All is unavailable in the current context'
        result = op()
    except Exception as exc:
        return None, f'3D Print Toolbox backend is unavailable: {exc}'

    if 'FINISHED' not in result:
        return None, f'3D Print Toolbox Check All returned {sorted(result)}'

    info = _toolbox_report_info()
    if not info:
        return None, '3D Print Toolbox ran, but its report data could not be read'
    return info, None


def _try_blender_stl_export(filepath):
    """Try Blender's native/current STL operator, then the legacy add-on operator."""
    errors = []

    try:
        native = getattr(bpy.ops.wm, 'stl_export', None)
        if native is not None and native.poll():
            result = native(
                filepath=filepath,
                check_existing=False,
                export_selected_objects=True,
                apply_modifiers=True,
            )
            if 'FINISHED' in result and os.path.isfile(filepath) and os.path.getsize(filepath) >= 84:
                return True, 'Blender native STL exporter'
            errors.append(f'native returned {sorted(result)}')
        else:
            errors.append('native STL exporter unavailable in current context')
    except Exception as exc:
        errors.append(f'native STL exporter: {exc}')

    try:
        legacy = getattr(bpy.ops.export_mesh, 'stl', None)
        if legacy is not None and legacy.poll():
            result = legacy(
                filepath=filepath,
                check_existing=False,
                use_selection=True,
                use_mesh_modifiers=True,
            )
            if 'FINISHED' in result and os.path.isfile(filepath) and os.path.getsize(filepath) >= 84:
                return True, 'Blender legacy STL exporter'
            errors.append(f'legacy returned {sorted(result)}')
        else:
            errors.append('legacy STL exporter unavailable in current context')
    except Exception as exc:
        errors.append(f'legacy STL exporter: {exc}')

    return False, '; '.join(errors)


def _write_binary_stl_fallback(context, filepath, selected_objects):
    """Write selected evaluated meshes directly as one binary STL if Blender's exporter fails."""
    temp_path = filepath + '.wt_tmp'
    depsgraph = context.evaluated_depsgraph_get()
    triangle_count = 0

    try:
        with open(temp_path, 'wb') as handle:
            header = b'Witch Tools STL fallback export'
            handle.write(header[:80].ljust(80, b'\0'))
            handle.write(struct.pack('<I', 0))

            for obj in selected_objects:
                if obj.mode == 'EDIT':
                    obj.update_from_editmode()

                obj_eval = obj.evaluated_get(depsgraph)
                mesh = None
                try:
                    mesh = obj_eval.to_mesh()
                    if mesh is None:
                        continue
                    mesh.calc_loop_triangles()
                    matrix = obj_eval.matrix_world.copy()
                    reverse_winding = matrix.is_negative
                    vertices = mesh.vertices

                    for tri in mesh.loop_triangles:
                        v0, v1, v2 = (matrix @ vertices[index].co for index in tri.vertices)
                        if reverse_winding:
                            v1, v2 = v2, v1

                        normal = (v1 - v0).cross(v2 - v0)
                        if normal.length_squared:
                            normal.normalize()
                        else:
                            normal = Vector((0.0, 0.0, 0.0))

                        handle.write(struct.pack(
                            '<12fH',
                            normal.x, normal.y, normal.z,
                            v0.x, v0.y, v0.z,
                            v1.x, v1.y, v1.z,
                            v2.x, v2.y, v2.z,
                            0,
                        ))
                        triangle_count += 1
                finally:
                    if mesh is not None:
                        obj_eval.to_mesh_clear()

            if triangle_count == 0:
                raise RuntimeError('Selected mesh objects contain no exportable triangles')
            if triangle_count >= 2 ** 32:
                raise RuntimeError('STL triangle count exceeds the binary STL format limit')

            handle.seek(80)
            handle.write(struct.pack('<I', triangle_count))

        os.replace(temp_path, filepath)
        return triangle_count
    except Exception:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
        raise


class WT_OT_print3d_analyze(Operator):
    bl_idname = 'witch_tools.print3d_analyze'
    bl_label = 'Check All'
    bl_options = {'REGISTER'}
    bl_description = 'Run the installed 3D Print Toolbox Check All operator and mirror its exact report'

    @classmethod
    def poll(cls, context):
        return _mesh_object(context) is not None

    def execute(self, context):
        obj = _mesh_object(context)
        props = context.scene.wt_print3d
        info, error = _run_toolbox_check_all(context)
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}

        found = {}
        for index, item in enumerate(info):
            if not isinstance(item, (tuple, list)) or len(item) < 2:
                continue
            text, data = item[0], item[1]
            field = _field_from_report_text(text)
            if field in dict(RESULT_FIELDS):
                found[field] = (_report_count(text, data), index, text, data)

        missing = [field for field, _label in RESULT_FIELDS if field not in found]
        if missing:
            self.report(
                {'ERROR'},
                '3D Print Toolbox report format did not contain: ' + ', '.join(missing),
            )
            return {'CANCELLED'}

        for field, _label in RESULT_FIELDS:
            setattr(props, field, found[field][0])
        props.last_analyzed_object = obj.name
        return {'FINISHED'}


class WT_OT_print3d_make_manifold(Operator):
    bl_idname = 'witch_tools.print3d_make_manifold'
    bl_label = 'Make Manifold'
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Merge doubles, remove degenerate/loose geometry, fill boundary holes, and recalculate normals outside'

    @classmethod
    def poll(cls, context):
        return _mesh_object(context) is not None

    def execute(self, context):
        obj = _mesh_object(context)
        prev_mode = context.mode
        try:
            if context.mode != 'EDIT_MESH':
                bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=0.0001)
            bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)
            bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(type='EDGE')
            bpy.ops.mesh.select_non_manifold(
                extend=False,
                use_wire=False,
                use_boundary=True,
                use_multi_face=False,
                use_non_contiguous=False,
                use_verts=False,
            )
            try:
                bpy.ops.mesh.fill_holes(sides=0)
            except Exception:
                pass
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)
        except Exception as exc:
            self.report({'ERROR'}, f'Make Manifold failed: {exc}')
            return {'CANCELLED'}
        finally:
            try:
                if prev_mode == 'OBJECT' and context.mode == 'EDIT_MESH':
                    bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass
        return {'FINISHED'}


class WT_OT_print3d_export_stl(Operator):
    bl_idname = 'witch_tools.print3d_export_stl'
    bl_label = 'Export STL'
    bl_options = {'REGISTER'}
    bl_description = 'Export selected mesh objects as one STL to the chosen folder'

    @classmethod
    def poll(cls, context):
        return any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        props = context.scene.wt_print3d
        folder = bpy.path.abspath(props.export_directory or '//').strip()
        if not folder:
            self.report({'ERROR'}, 'Choose an export folder first')
            return {'CANCELLED'}

        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as exc:
            self.report({'ERROR'}, f'Cannot create export folder: {exc}')
            return {'CANCELLED'}

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected:
            self.report({'ERROR'}, 'Select at least one mesh object to export')
            return {'CANCELLED'}

        active = context.active_object if context.active_object in selected else selected[0]
        filename = bpy.path.clean_name(active.name if len(selected) == 1 else f'{active.name}_selection') + '.stl'
        filepath = os.path.join(folder, filename)

        native_ok, native_detail = _try_blender_stl_export(filepath)
        if native_ok:
            self.report({'INFO'}, f'Exported STL: {filepath}')
            return {'FINISHED'}

        try:
            triangle_count = _write_binary_stl_fallback(context, filepath, selected)
        except Exception as exc:
            self.report({'ERROR'}, f'STL export failed: {exc}. Blender exporter: {native_detail}')
            return {'CANCELLED'}

        self.report(
            {'INFO'},
            f'Exported STL: {filepath} ({triangle_count} triangles; Witch Tools fallback writer)',
        )
        return {'FINISHED'}


CLASSES = (
    WTPrint3DProperties,
    WT_OT_print3d_analyze,
    WT_OT_print3d_make_manifold,
    WT_OT_print3d_export_stl,
)


def register_props():
    bpy.types.Scene.wt_print3d = PointerProperty(type=WTPrint3DProperties)


def unregister_props():
    if hasattr(bpy.types.Scene, 'wt_print3d'):
        delattr(bpy.types.Scene, 'wt_print3d')
