from bpy.types import Panel

from .panel_base import WTHeaderPanelMixin
from .state import PANEL_CATEGORY, PANEL_ORDERS
from .ui_helpers import draw_inline_label_prop, draw_section_toggle
from .utils_context import ui_state_owner


class VIEW3D_PT_wt_head_tools(WTHeaderPanelMixin, Panel):
    bl_label = ''
    bl_idname = 'VIEW3D_PT_wt_head_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_CATEGORY
    bl_order = PANEL_ORDERS['HEAD_TOOLS']
    panel_title = 'Head Tools'
    panel_icon = 'USER'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        props = context.scene.witch_tools
        ui = ui_state_owner(context)
        layout = self.layout

        if getattr(ui, 'ui_minimal_mode', False):
            return

        prep = layout.box()
        if draw_section_toggle(prep, ui, 'show_head_prep', 'Prep', section_icon='TOOL_SETTINGS'):
            draw_inline_label_prop(prep, 'Race', props, 'head_race', label_units=2.8, field_units=6.2)
            draw_inline_label_prop(prep, 'Head Name', props, 'head_name', label_units=3.8, field_units=6.2)
            prep.operator('witch_tools.head_batch_rename', text='Batch Rename', icon='SORTALPHA')
            prep.separator()
            prep.operator('witch_tools.create_head_collections', text='Create Collections', icon='OUTLINER_COLLECTION')
            prep.operator('witch_tools.join_head_collection_meshes', text='Join Head / Eyes / Mouth', icon='MOD_ARRAY')
            prep.operator('witch_tools.delete_other_head_meshes', text='Delete Other Meshes', icon='TRASH')
            prep.operator('witch_tools.beautify_armature', text='Beautify Armature', icon='SHADERFX')

        editing = layout.box()
        if draw_section_toggle(editing, ui, 'show_head_editing', 'Editing', section_icon='EDITMODE_HLT'):
            draw_inline_label_prop(editing, 'Armature', props, 'head_target_armature', label_units=3.6, field_units=6.0)
            draw_inline_label_prop(editing, 'Reference Mesh', props, 'head_target_mesh', label_units=4.6, field_units=5.8)
            draw_inline_label_prop(editing, 'Surface Offset', props, 'head_offset_distance', label_units=4.4, field_units=5.4)
            draw_inline_label_prop(editing, 'Vanilla Reference', props, 'head_reference_mesh', label_units=4.8, field_units=5.8)
            editing.operator('witch_tools.snap_ear_to_head', text='Snap Ear to Head', icon='SNAP_ON')
            editing.operator('witch_tools.snap_all_head_bones', text='Snap All Bones', icon='BONE_DATA')
            editing.operator('witch_tools.fix_armature_ears', text='Fix Armature & Ears', icon='TOOL_SETTINGS')
            editing.operator('witch_tools.fix_head_seam_normals', text='Fix Head Seam Normals', icon='BRUSH_DATA')

        finishing = layout.box()
        if draw_section_toggle(finishing, ui, 'show_head_finishing', 'Finishing', section_icon='CHECKMARK'):
            finishing.operator('witch_tools.delete_lods', text='Delete Selected LODs', icon='TRASH')
            finishing.operator('witch_tools.reset_lod_distance', text='Change All LOD Distance to 0', icon='PANEL_CLOSE')
            finishing.operator('witch_tools.cleanup_export_orders', text='Clean Up Export Orders', icon='MOD_FLUID')


PANELS = (VIEW3D_PT_wt_head_tools,)
