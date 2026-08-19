import bpy
import bmesh
from itertools import chain
from bpy.types import Operator, PropertyGroup
from bpy.props import BoolProperty, FloatProperty, IntProperty, EnumProperty, PointerProperty


CLEAN_TARGET_ITEMS = (
    ('ENABLED', 'Enabled Sections', 'Run every Advanced Clean section currently enabled in the section headers'),
    ('REPAIR', 'Repair', 'Run only Repair'),
    ('MANIFOLD', 'Manifold', 'Run only Manifold'),
    ('TOPOLOGY', 'Topology', 'Run only Topology'),
    ('NORMALS', 'Normals', 'Run only Normals'),
    ('DISSOLVE', 'Dissolve', 'Run only Dissolve'),
)


class WTInstantCleanCategories(PropertyGroup):
    repair: BoolProperty(name='Repair', default=True)
    manifold: BoolProperty(name='Manifold', default=True)
    topology: BoolProperty(name='Topology', default=True)
    normals: BoolProperty(name='Normals', default=True)
    dissolve: BoolProperty(name='Dissolve', default=True)


class WTInstantCleanRepair(PropertyGroup):
    loose: BoolProperty(name='Loose', default=True, description='Unconnected geometry')
    loose_verts: BoolProperty(name='Loose Verts', default=True)
    loose_edges: BoolProperty(name='Loose Edges', default=True)
    loose_faces: BoolProperty(name='Loose Faces', default=True)
    doubles: BoolProperty(name='Doubles', default=True)
    doubles_dst: FloatProperty(name='Max Distance', default=0.0001, subtype='DISTANCE', min=0.0)
    zero_faces: BoolProperty(name='Zero Faces', default=True)
    zero_faces_area: FloatProperty(name='Max Area', default=0.0001, subtype='DISTANCE', min=0.0)
    dispensables: BoolProperty(name='Dispensables', default=True)
    dispensables_ang: FloatProperty(name='Max Angle', default=0.0875, subtype='ANGLE', min=0.0)


class WTInstantCleanManifold(PropertyGroup):
    non_manifold_faces: BoolProperty(name='Faces', default=True, description='Remove interior/non-manifold faces')
    non_manifold_verts: BoolProperty(name='Vertices', default=True, description='Split zero-size non-manifold vertex connections')
    wire_geo: BoolProperty(name='Wire', default=True, description='Remove geometry not connected to faces')
    fill_holes: BoolProperty(name='Fill Holes', default=False)
    fill_holes_max_sides: IntProperty(name='Max Sides', default=4, min=0)


class WTInstantCleanTopology(PropertyGroup):
    type: EnumProperty(name='Type', items=[('TRIS','Tris','','MOD_TRIANGULATE',0),('QUADS','Quads','','MESH_GRID',1)], default='TRIS')
    quad_method: EnumProperty(name='Quad Method', items=[('BEAUTY','Beauty',''),('FIXED','Fixed',''),('FIXED_ALTERNATE','Fixed Alternate',''),('SHORTEST_DIAGONAL','Shortest Diagonal',''),('LONGEST_DIAGONAL','Longest Diagonal','')], default='BEAUTY')
    ngon_method: EnumProperty(name='NGon Method', items=[('BEAUTY','Beauty',''),('CLIP','Clip','')], default='BEAUTY')
    quad_max_face_ang: FloatProperty(name='Max Face Angle', subtype='ANGLE', default=0.698123, min=0.0, max=3.14159)
    quad_max_shape_ang: FloatProperty(name='Max Shape Angle', subtype='ANGLE', default=0.698123, min=0.0, max=3.14159)
    compare_sharp: BoolProperty(name='Sharp', default=True)
    compare_seam: BoolProperty(name='Seam', default=True)
    compare_vcol: BoolProperty(name='VCol', default=True)
    compare_uv: BoolProperty(name='UV', default=True)
    compare_material: BoolProperty(name='Material', default=True)


class WTInstantCleanNormals(PropertyGroup):
    recalculate: BoolProperty(name='Recalculate', default=True)
    recalculate_orientation: EnumProperty(name='Orientation', items=[('OUTSIDE','Outside',''),('INSIDE','Inside','')], default='OUTSIDE')
    auto_smooth: BoolProperty(name='Smooth by Angle', default=True)
    auto_smooth_ang: FloatProperty(name='Max Angle', subtype='ANGLE', default=0.785398, min=0.0, max=3.14159)
    weighted_normals: BoolProperty(name='Weighted Normals', default=False)
    clear_custom_split_normals: BoolProperty(name='Split Normals', default=True)
    clear_sharp_edges: BoolProperty(name='Sharp Edges', default=True)


class WTInstantCleanDissolve(PropertyGroup):
    max_angle: FloatProperty(name='Max Angle', default=0.0875, subtype='ANGLE', min=0.0, max=3.14159)
    boundaries: BoolProperty(name='Boundaries', default=False)
    protect_sharp: BoolProperty(name='Sharp', default=True)
    protect_seam: BoolProperty(name='Seam', default=True)
    protect_uv: BoolProperty(name='UV', default=True)
    protect_materials: BoolProperty(name='Materials', default=True)


def _valid(bmeshes):
    return [bm for bm in bmeshes if bm and bm.is_valid]


def _repair(context, objects, bmeshes):
    pg = context.scene.wt_ic_repair
    if pg.doubles: bpy.ops.mesh.remove_doubles(threshold=pg.doubles_dst)
    if pg.loose:
        bpy.ops.mesh.delete_loose(use_verts=pg.loose_verts, use_edges=pg.loose_edges, use_faces=pg.loose_faces)
        bpy.ops.mesh.select_all(action='SELECT')
    if pg.zero_faces: bpy.ops.mesh.dissolve_degenerate(threshold=pg.zero_faces_area)
    if pg.dispensables:
        for bm in _valid(bmeshes):
            verts = [v for v in bm.verts if v.select and len(v.link_edges) == 2 and v.calc_edge_angle(0) < pg.dispensables_ang]
            if verts: bmesh.ops.dissolve_verts(bm, verts=verts)


def _manifold(context, objects, bmeshes):
    pg = context.scene.wt_ic_manifold
    if pg.non_manifold_faces:
        bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        bpy.ops.mesh.select_interior_faces(); bpy.ops.mesh.delete(type='FACE')
    if pg.non_manifold_verts:
        bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=False, use_multi_face=False, use_non_contiguous=False, use_verts=True)
        for bm in _valid(bmeshes):
            for nm_v in [v for v in bm.verts if v.select and v.is_valid and v.link_edges and all(e.link_faces for e in v.link_edges)]:
                merge_co = nm_v.co.copy(); parts = []; prev_edge = nm_v.link_edges[0]; parts.append({prev_edge})
                while sum(len(p) for p in parts) != len(nm_v.link_edges):
                    used = set(chain.from_iterable(parts))
                    linked = [e for e in nm_v.link_edges if e not in used and any(f in prev_edge.link_faces for f in e.link_faces)]
                    if linked:
                        prev_edge = linked[0]; parts[-1].add(prev_edge)
                    else:
                        remaining = [e for e in nm_v.link_edges if e not in used]
                        if not remaining: break
                        prev_edge = remaining[0]; parts.append({prev_edge})
                for part in parts:
                    res = bmesh.ops.bisect_edges(bm, edges=list(part), cuts=1)
                    new_verts = [i for i in res.get('geom_split', []) if isinstance(i, bmesh.types.BMVert)]
                    if len(new_verts) > 1:
                        for other in new_verts[1:]:
                            if new_verts[0].is_valid and other.is_valid:
                                bmesh.ops.pointmerge(bm, verts=[new_verts[0], other], merge_co=merge_co)
    if pg.wire_geo:
        bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.select_non_manifold(extend=False, use_wire=True, use_boundary=False, use_multi_face=False, use_non_contiguous=False, use_verts=False)
        bpy.ops.mesh.delete(type='EDGE')
    if pg.fill_holes:
        bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=False)
        bpy.ops.mesh.fill_holes(sides=pg.fill_holes_max_sides)


def _topology(context):
    pg = context.scene.wt_ic_topology; bpy.ops.mesh.select_all(action='SELECT')
    if pg.type == 'TRIS': bpy.ops.mesh.quads_convert_to_tris(quad_method=pg.quad_method, ngon_method=pg.ngon_method)
    else:
        bpy.ops.mesh.tris_convert_to_quads(face_threshold=pg.quad_max_face_ang, shape_threshold=pg.quad_max_shape_ang, uvs=pg.compare_uv, vcols=pg.compare_vcol, seam=pg.compare_seam, sharp=pg.compare_sharp, materials=pg.compare_material)


def _ensure_smooth_by_angle(context, obj, angle):
    if bpy.app.version < (4, 1, 0):
        obj.data.use_auto_smooth = True; obj.data.auto_smooth_angle = angle; return
    name = '(Witch Tools) Smooth by Angle'
    mod = next((m for m in obj.modifiers if m.type == 'NODES' and m.name == name), None) or obj.modifiers.new(name=name, type='NODES')
    group = bpy.data.node_groups.get('Smooth by Angle')
    if group is None:
        try:
            context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add_node_group(asset_library_type='ESSENTIALS', asset_library_identifier='', relative_asset_identifier='geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle')
            created = obj.modifiers[-1]; group = created.node_group; obj.modifiers.remove(created)
        except Exception: group = None
    if group:
        mod.node_group = group
        try: mod['Input_1'] = angle
        except Exception: pass
    else:
        try: obj.modifiers.remove(mod)
        except Exception: pass


def _normals(context, objects, bmeshes):
    pg = context.scene.wt_ic_normals
    if pg.recalculate:
        bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.normals_make_consistent(inside=pg.recalculate_orientation == 'INSIDE')
    if pg.auto_smooth:
        bpy.ops.mesh.select_all(action='SELECT')
        try: bpy.ops.mesh.faces_shade_smooth()
        except Exception: pass
        for obj in objects: _ensure_smooth_by_angle(context, obj, pg.auto_smooth_ang)
    if pg.weighted_normals:
        for obj in objects:
            if not any(m.type == 'WEIGHTED_NORMAL' for m in obj.modifiers):
                mod = obj.modifiers.new(name='(Witch Tools) Weighted Normals', type='WEIGHTED_NORMAL'); mod.keep_sharp = True
    if pg.clear_custom_split_normals:
        for obj in objects:
            context.view_layer.objects.active = obj
            try: bpy.ops.mesh.customdata_custom_splitnormals_clear()
            except Exception: pass
    if pg.clear_sharp_edges:
        for bm in _valid(bmeshes):
            for edge in bm.edges: edge.smooth = True


def _dissolve(context):
    pg = context.scene.wt_ic_dissolve; delimiter = {'NORMAL'}
    if pg.protect_materials: delimiter.add('MATERIAL')
    if pg.protect_seam: delimiter.add('SEAM')
    if pg.protect_sharp: delimiter.add('SHARP')
    if pg.protect_uv: delimiter.add('UV')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.dissolve_limited(angle_limit=pg.max_angle, use_dissolve_boundaries=pg.boundaries, delimit=delimiter)


def _enabled_targets(categories):
    targets = set()
    if categories.repair: targets.add('REPAIR')
    if categories.manifold: targets.add('MANIFOLD')
    if categories.topology: targets.add('TOPOLOGY')
    if categories.normals: targets.add('NORMALS')
    if categories.dissolve: targets.add('DISSOLVE')
    return targets


class WT_OT_advanced_clean(Operator):
    bl_idname = 'witch_tools.advanced_clean'; bl_label = 'Clean'; bl_options = {'REGISTER','UNDO'}
    bl_description = 'Clean the enabled Advanced Clean sections, or run one section from its play button. Hold Shift to clean only the current selection.'

    target: EnumProperty(name='Clean Target', items=CLEAN_TARGET_ITEMS, default='ENABLED', options={'HIDDEN', 'SKIP_SAVE'})
    selection_only: BoolProperty(name='Selection Only', default=False, options={'HIDDEN', 'SKIP_SAVE'})

    @classmethod
    def poll(cls, context): return bool(context.selected_objects or context.objects_in_mode)

    def invoke(self, context, event):
        self.selection_only = bool(event.shift)
        return self.execute(context)

    def execute(self, context):
        prev_mode = context.mode; prev_active = context.view_layer.objects.active
        objects = [o for o in (context.objects_in_mode if context.mode == 'EDIT_MESH' else context.selected_objects) if o.type == 'MESH']
        if not objects:
            self.report({'ERROR'}, 'Select at least one mesh object.')
            return {'CANCELLED'}

        categories = context.scene.wt_ic_categories
        targets = _enabled_targets(categories) if self.target == 'ENABLED' else {self.target}
        if not targets:
            self.report({'WARNING'}, 'No Advanced Clean sections are enabled.')
            return {'CANCELLED'}

        if not prev_active or prev_active.type != 'MESH': context.view_layer.objects.active = objects[0]
        if context.mode != 'EDIT_MESH': bpy.ops.object.mode_set(mode='EDIT')
        bmeshes = [bmesh.from_edit_mesh(o.data) for o in objects]; hidden = []
        try:
            if self.selection_only:
                for bm in bmeshes: hidden.append({v for v in bm.verts if v.hide})
                bpy.ops.mesh.hide(unselected=True)
            else:
                bpy.ops.mesh.select_all(action='SELECT')

            if 'REPAIR' in targets: _repair(context, objects, bmeshes)
            if 'MANIFOLD' in targets: _manifold(context, objects, bmeshes)
            if 'TOPOLOGY' in targets: _topology(context)
            if 'NORMALS' in targets: _normals(context, objects, bmeshes)
            if 'DISSOLVE' in targets: _dissolve(context)

            for obj in objects: bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)
            if self.selection_only:
                bpy.ops.mesh.reveal(select=False)
                for bm, old_hidden in zip(bmeshes, hidden):
                    for v in old_hidden:
                        if v.is_valid: v.hide_set(True)
            return {'FINISHED'}
        except Exception as exc:
            self.report({'ERROR'}, f'Advanced Clean failed: {exc}')
            return {'CANCELLED'}
        finally:
            try:
                if prev_mode == 'OBJECT' and context.mode == 'EDIT_MESH': bpy.ops.object.mode_set(mode='OBJECT')
            except Exception: pass
            if prev_active: context.view_layer.objects.active = prev_active


CLASSES = (WTInstantCleanCategories, WTInstantCleanRepair, WTInstantCleanManifold, WTInstantCleanTopology, WTInstantCleanNormals, WTInstantCleanDissolve, WT_OT_advanced_clean)


def register_props():
    bpy.types.Scene.wt_ic_categories = PointerProperty(type=WTInstantCleanCategories)
    bpy.types.Scene.wt_ic_repair = PointerProperty(type=WTInstantCleanRepair)
    bpy.types.Scene.wt_ic_manifold = PointerProperty(type=WTInstantCleanManifold)
    bpy.types.Scene.wt_ic_topology = PointerProperty(type=WTInstantCleanTopology)
    bpy.types.Scene.wt_ic_normals = PointerProperty(type=WTInstantCleanNormals)
    bpy.types.Scene.wt_ic_dissolve = PointerProperty(type=WTInstantCleanDissolve)


def unregister_props():
    for name in ('wt_ic_dissolve','wt_ic_normals','wt_ic_topology','wt_ic_manifold','wt_ic_repair','wt_ic_categories'):
        if hasattr(bpy.types.Scene, name): delattr(bpy.types.Scene, name)
