from bpy.types import Panel
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .print3d_tools import RESULT_FIELDS


def _narrow(context, pixels=360):
    region = getattr(context, 'region', None)
    return bool(region and region.width < pixels)


def _toggle_row(layout, props, fields, narrow=False, split_at=3):
    groups = (fields[:split_at], fields[split_at:]) if narrow and len(fields) > split_at else (fields,)
    for group in groups:
        if not group: continue
        row = layout.row(align=True)
        for prop_name, label in group: row.prop(props, prop_name, text=label, toggle=True)


class VIEW3D_PT_wt_print3d(Panel):
    bl_label = '3D Print Tools'; bl_idname = 'VIEW3D_PT_wt_print3d'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['PRINT3D']; bl_description = 'Analyze, repair, clean, and export meshes for 3D printing.'
    def draw(self, context):
        obj = context.active_object
        self.layout.label(text=obj.name, icon='MESH_DATA') if obj and obj.type == 'MESH' else self.layout.label(text='Select a mesh object', icon='INFO')


class VIEW3D_PT_wt_print3d_export(Panel):
    bl_label = 'Export'; bl_idname = 'VIEW3D_PT_wt_print3d_export'; bl_parent_id = 'VIEW3D_PT_wt_print3d'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY; bl_order = 0
    def draw(self, context):
        props = context.scene.wt_print3d
        self.layout.prop(props, 'export_directory', text='')
        row = self.layout.row(); row.scale_y = 1.15; row.operator('witch_tools.print3d_export_stl', text='Export STL', icon='EXPORT')


class VIEW3D_PT_wt_print3d_analyze(Panel):
    bl_label = 'Analyze Mesh'; bl_idname = 'VIEW3D_PT_wt_print3d_analyze'; bl_parent_id = 'VIEW3D_PT_wt_print3d'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY; bl_order = 1
    def draw(self, context):
        props = context.scene.wt_print3d
        row = self.layout.row(); row.scale_y = 1.1; row.operator('witch_tools.print3d_analyze', text='Check All', icon='CHECKMARK')
        box = self.layout.box(); box.label(text='Results', icon='INFO')
        for prop_name, label in RESULT_FIELDS:
            row = box.row(align=True); row.label(text=label); row.label(text=str(getattr(props, prop_name)))
        if props.last_analyzed_object and context.active_object and props.last_analyzed_object != context.active_object.name:
            self.layout.label(text='Results are from a different object', icon='ERROR')


class VIEW3D_PT_wt_print3d_clean_repair(Panel):
    bl_label = 'Clean & Repair'; bl_idname = 'VIEW3D_PT_wt_print3d_clean_repair'; bl_parent_id = 'VIEW3D_PT_wt_print3d'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY; bl_order = 2
    def draw(self, context):
        row = self.layout.row(); row.scale_y = 1.15; row.operator('witch_tools.print3d_make_manifold', text='Make Manifold', icon='MOD_REMESH')


class VIEW3D_PT_wt_print3d_auto_fix(Panel):
    bl_label = 'Auto Fix'; bl_idname = 'VIEW3D_PT_wt_print3d_auto_fix'; bl_parent_id = 'VIEW3D_PT_wt_print3d_clean_repair'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY; bl_order = 0
    def draw(self, context): self.layout.label(text='Global Fix first; Local Fix below.', icon='HAND')


class VIEW3D_PT_wt_print3d_global_fix(Panel):
    bl_label = 'Global Fix'; bl_idname = 'VIEW3D_PT_wt_print3d_global_fix'; bl_parent_id = 'VIEW3D_PT_wt_print3d_auto_fix'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY; bl_order = 0
    def draw(self, context):
        layout = self.layout; props = context.scene.meshfixtool_properties; full = props.tri_boolean or props.quad_boolean
        row = layout.row(align=True); row.prop(props,'tri_boolean',text='Tri Mesh',icon='MOD_TRIANGULATE',toggle=True); row.prop(props,'quad_boolean',text='Quad Mesh',icon='MESH_GRID',toggle=True)
        layout.prop(props,'face_normal_boolean',text='Face Normal',icon='ORIENTATION_NORMAL',toggle=True)
        row = layout.row(align=True); row.prop(props,'minor_parts_boolean',text='Noise Shells',icon='UNLINKED',toggle=True); row.prop(props,'minor_parts_threshold',text='Min %',slider=True)
        row = layout.row(align=True); row.enabled=full; row.prop(props,'spikes_boolean',text='Spikes',icon='SHARPCURVE',toggle=True); row.prop(props,'spikes_angle_limit',text='Min Angle',slider=True)
        row = layout.row(align=True); row.enabled=full; row.prop(props,'intersection_boolean',text='Intersect Face',icon='MOD_SOLIDIFY',toggle=True); row.prop(props,'intersection_angle_limit',text='Min Angle',slider=True)
        row = layout.row(align=True); row.enabled=full; row.prop(props,'volume_intersection_boolean',text='Intersect Volumes',icon='SELECT_EXTEND',toggle=True); row.prop(props,'holes_boolean',text='Fill Holes',icon='HOLDOUT_ON',toggle=True)
        row = layout.row(); row.scale_y=1.2; row.enabled=full or props.face_normal_boolean or props.minor_parts_boolean
        row.operator('witch_tools.mr_auto_fix', text='Auto Fix' if not props.meshfixing else 'Calculating…', icon='HAND' if not props.meshfixing else 'SORTTIME')
        if props.statistics_boolean:
            box=layout.box(); box.label(text='Last Auto Fix',icon='TEXT'); box.label(text=f'Verts: {props.sum_vertices}'); box.label(text=f'Edges: {props.sum_edges}'); box.label(text=f'Faces: {props.sum_faces}')
            if props.volume_intersection_boolean: box.label(text=f'Intersect Volumes: {props.sum_volumes}')
            if props.holes_boolean: box.label(text=f'Holes: {props.sum_holes}')


class VIEW3D_PT_wt_print3d_local_fix(Panel):
    bl_label = 'Local Fix'; bl_idname = 'VIEW3D_PT_wt_print3d_local_fix'; bl_parent_id = 'VIEW3D_PT_wt_print3d_auto_fix'; bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = PANEL_CATEGORY; bl_order = 1
    def draw(self, context):
        layout=self.layout; edit=context.mode=='EDIT_MESH'
        row=layout.row(align=True); row.enabled=edit; row.operator('mesh.select_more',text='Select More',icon='ADD'); row.operator('mesh.select_less',text='Select Less',icon='REMOVE')
        row=layout.row(align=True); row.enabled=edit; overlay=getattr(context.space_data,'overlay',None)
        if overlay: row.prop(overlay,'show_face_orientation',text='Face Normal',toggle=True)
        row.operator('witch_tools.mr_local_face_normal',text='Unify/Flip',icon='ORIENTATION_NORMAL'); row.operator('witch_tools.mr_refine_local',text='Refine',icon='MESH_ICOSPHERE')
        row=layout.row(align=True); row.enabled=edit; row.operator('witch_tools.mr_remesh_local',text='Remesh',icon='MOD_REMESH'); row.operator('witch_tools.mr_smooth_local',text='Smooth',icon='MOD_SMOOTH'); row.operator('witch_tools.mr_reduce_local',text='Reduce',icon='MOD_DECIM')


class VIEW3D_PT_wt_print3d_advanced_clean(Panel):
    bl_label='Advanced Clean'; bl_idname='VIEW3D_PT_wt_print3d_advanced_clean'; bl_parent_id='VIEW3D_PT_wt_print3d_clean_repair'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category=PANEL_CATEGORY; bl_order=1
    def draw(self, context):
        cats=context.scene.wt_ic_categories; row=self.layout.row(); row.scale_y=1.25; row.operator('witch_tools.advanced_clean',text='Clean',icon='BRUSH_DATA')
        _toggle_row(self.layout,cats,[('repair','Repair'),('manifold','Manifold'),('topology','Topology'),('normals','Normals'),('dissolve','Dissolve')],narrow=_narrow(context),split_at=3)
        self.layout.label(text='Shift + Clean: selection only',icon='EVENT_SHIFT')


class VIEW3D_PT_wt_print3d_clean_repair_settings(Panel):
    bl_label='Repair'; bl_idname='VIEW3D_PT_wt_print3d_clean_repair_settings'; bl_parent_id='VIEW3D_PT_wt_print3d_advanced_clean'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category=PANEL_CATEGORY; bl_order=0
    def draw(self, context):
        pg=context.scene.wt_ic_repair; col=self.layout.column(align=True)
        row=col.row(align=True); row.prop(pg,'loose',text='Loose',toggle=True); sub=row.row(align=True); sub.enabled=pg.loose; sub.prop(pg,'loose_verts',text='',icon='VERTEXSEL',toggle=True); sub.prop(pg,'loose_edges',text='',icon='EDGESEL',toggle=True); sub.prop(pg,'loose_faces',text='',icon='FACESEL',toggle=True)
        row=col.row(align=True); row.prop(pg,'doubles',text='Doubles',toggle=True); sub=row.row(); sub.enabled=pg.doubles; sub.prop(pg,'doubles_dst',text='Max Distance')
        row=col.row(align=True); row.prop(pg,'zero_faces',text='Zero Faces',toggle=True); sub=row.row(); sub.enabled=pg.zero_faces; sub.prop(pg,'zero_faces_area',text='Max Area')
        row=col.row(align=True); row.prop(pg,'dispensables',text='Dispensables',toggle=True); sub=row.row(); sub.enabled=pg.dispensables; sub.prop(pg,'dispensables_ang',text='Max Angle')


class VIEW3D_PT_wt_print3d_clean_manifold_settings(Panel):
    bl_label='Manifold'; bl_idname='VIEW3D_PT_wt_print3d_clean_manifold_settings'; bl_parent_id='VIEW3D_PT_wt_print3d_advanced_clean'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category=PANEL_CATEGORY; bl_order=1
    def draw(self, context):
        pg=context.scene.wt_ic_manifold; row=self.layout.row(align=True); row.prop(pg,'fill_holes',text='Fill Holes',toggle=True); sub=row.row(); sub.enabled=pg.fill_holes; sub.prop(pg,'fill_holes_max_sides',text='Max Sides')
        self.layout.label(text='Remove Non-Manifold:'); _toggle_row(self.layout,pg,[('non_manifold_faces','Faces'),('non_manifold_verts','Vertices'),('wire_geo','Wire')])


class VIEW3D_PT_wt_print3d_clean_topology_settings(Panel):
    bl_label='Topology'; bl_idname='VIEW3D_PT_wt_print3d_clean_topology_settings'; bl_parent_id='VIEW3D_PT_wt_print3d_advanced_clean'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category=PANEL_CATEGORY; bl_order=2
    def draw(self, context):
        pg=context.scene.wt_ic_topology; self.layout.prop(pg,'type',text='')
        if pg.type=='TRIS':
            row=self.layout.row(align=True); row.prop(pg,'quad_method',text='Quads'); row.prop(pg,'ngon_method',text='NGons')
        else:
            if _narrow(context): self.layout.prop(pg,'quad_max_face_ang'); self.layout.prop(pg,'quad_max_shape_ang')
            else:
                row=self.layout.row(align=True); row.prop(pg,'quad_max_face_ang',text='Face Angle'); row.prop(pg,'quad_max_shape_ang',text='Shape Angle')
            self.layout.label(text='Compare'); _toggle_row(self.layout,pg,[('compare_sharp','Sharp'),('compare_seam','Seam'),('compare_uv','UV'),('compare_material','Material'),('compare_vcol','VCol')],narrow=_narrow(context),split_at=3)


class VIEW3D_PT_wt_print3d_clean_normals_settings(Panel):
    bl_label='Normals'; bl_idname='VIEW3D_PT_wt_print3d_clean_normals_settings'; bl_parent_id='VIEW3D_PT_wt_print3d_advanced_clean'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category=PANEL_CATEGORY; bl_order=3
    def draw(self, context):
        pg=context.scene.wt_ic_normals
        row=self.layout.row(align=True); row.prop(pg,'recalculate',text='Recalculate',toggle=True); sub=row.row(); sub.enabled=pg.recalculate; sub.prop(pg,'recalculate_orientation',text='')
        row=self.layout.row(align=True); row.prop(pg,'auto_smooth',text='Smooth by Angle',toggle=True); sub=row.row(); sub.enabled=pg.auto_smooth; sub.prop(pg,'auto_smooth_ang',text='Max Angle')
        self.layout.prop(pg,'weighted_normals',text='Weighted Normals',toggle=True); self.layout.label(text='Clear Data'); _toggle_row(self.layout,pg,[('clear_custom_split_normals','Split Normals'),('clear_sharp_edges','Sharp Edges')])


class VIEW3D_PT_wt_print3d_clean_dissolve_settings(Panel):
    bl_label='Dissolve'; bl_idname='VIEW3D_PT_wt_print3d_clean_dissolve_settings'; bl_parent_id='VIEW3D_PT_wt_print3d_advanced_clean'; bl_space_type='VIEW_3D'; bl_region_type='UI'; bl_category=PANEL_CATEGORY; bl_order=4
    def draw(self, context):
        pg=context.scene.wt_ic_dissolve; row=self.layout.row(align=True); row.prop(pg,'max_angle'); row.prop(pg,'boundaries',toggle=True); self.layout.label(text='Protect')
        _toggle_row(self.layout,pg,[('protect_sharp','Sharp'),('protect_seam','Seam'),('protect_uv','UV'),('protect_materials','Materials')],narrow=_narrow(context),split_at=2)


PANELS=(VIEW3D_PT_wt_print3d,VIEW3D_PT_wt_print3d_export,VIEW3D_PT_wt_print3d_analyze,VIEW3D_PT_wt_print3d_clean_repair,VIEW3D_PT_wt_print3d_auto_fix,VIEW3D_PT_wt_print3d_global_fix,VIEW3D_PT_wt_print3d_local_fix,VIEW3D_PT_wt_print3d_advanced_clean,VIEW3D_PT_wt_print3d_clean_repair_settings,VIEW3D_PT_wt_print3d_clean_manifold_settings,VIEW3D_PT_wt_print3d_clean_topology_settings,VIEW3D_PT_wt_print3d_clean_normals_settings,VIEW3D_PT_wt_print3d_clean_dissolve_settings)
