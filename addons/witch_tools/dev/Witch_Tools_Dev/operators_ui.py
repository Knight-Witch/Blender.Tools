import json

import bpy
from bpy.props import StringProperty
from bpy.types import Operator

from .state import ADDON_PACKAGE, UI_STATE_PROPS
from .utils_context import addon_preferences


def _tag_redraw_all(context):
    wm = getattr(context, 'window_manager', None)
    if wm is None:
        return
    for window in wm.windows:
        screen = window.screen
        if screen is None:
            continue
        for area in screen.areas:
            try:
                area.tag_redraw()
            except Exception:
                pass


HELP_TOPICS = {
    'coordinate_copy_title': (
        'Copy exact coordinates from one source vertex, edge, or face to one or more independent targets.\n\n'
        '1. Choose Global or Local space\n2. Enable X/Y/Z and Location, Rotation, and/or Scale\n'
        '3. Select exactly one source and Capture Source\n4. Select target geometry and Apply\n\n'
        'Global converts through world space, so targets on different mesh objects can line up even when their object origins differ. '
        'Vertices are applied individually; connected selected edge/face regions are applied as independent groups, never as one global median.'
    ),
    'planar_edit_title': (
        'Plane Lock and Level are absolute precision-edit helpers.\n\n'
        'Plane Lock freezes the enabled object-local X/Y/Z coordinates of selected vertices while leaving other axes editable. '
        'Edges and faces lock their vertices.\n\n'
        'Level captures one source point in world space, then sets every selected target vertex to the source coordinate on the enabled axes. '
        'This levels each target exactly rather than moving the selection median.'
    ),
    'inject_new_title': (
        'Fast one-shot topology creation and placement.\n\n'
        'Solo duplicates one selected vertex/face or one or more selected edges without a source connection. Branch duplicates them and creates source-to-copy branch edges. '
        'Slide injects one vertex into every selected edge and moves all injected vertices to the same relative position along their own rails.\n\n'
        'Solo/Branch allow any combination of global X/Y/Z, or a captured straight Rail. Magnetic Snap highlights the vertex, edge, or face under the cursor. '
        'Vertex/edge targets rigidly align the nearest corresponding injected vertex; face targets solve each injected vertex along its own travel line. '
        'Branch Auto-Merge checks every new vertex on commit: coincident vertices weld, and a contact inside an existing edge subdivides that target edge before welding so no stale unsplit edge remains.\n\n'
        'During placement, plain MMB pauses placement and orbits around the live injection. Shift/Ctrl+MMB remain normal Blender navigation.'
    ),
    'magic_branch_title': (
        'Drag-and-drop mesh building without restarting an operator for every branch.\n\n'
        'Magic Branch has an explicit ON/OFF control. Single Branch turns OFF after one completed click-drag; Persistent stays armed for the next branch. Both ON/OFF and Persistent are hotkeyable operators.\n\n'
        'Vertex creates a new vertex and source-to-new edge. Edge creates a copied edge with source-to-copy connections. Face grows from the source-face edge nearest the drag direction. '
        'Paver repeats equal-size face tiles and can turn out of the source face plane when the enabled axes require it (for example, Z-only can grow a wall from a horizontal face). Organic creates one adaptable connected face.\n\n'
        'X/Y/Z are independent movement toggles; all three enabled is free mouse movement. Magnetic Snap highlights targets and Auto-Merge reintegrates every supported overlapping new vertex/edge contact. Branch Type also switches Blender Vertex/Edge/Face selection mode. Plain MMB changes the orbit pivot only during a live drag.'
    ),
    'edge_doctor_title': (
        'Topology repair tools grouped in one place.\n\n'
        'Missing Vertex / Edge Injector repairs regular-grid gaps from either ordered A/B/C vertices or two selected edges that form an L. '
        'Alignment Fixer moves subordinate geometry to an anchor or custom guide. Curvature Sync repairs and synchronizes parallel curved chains.'
    ),
    'weight_transfer_single': 'Transfer weights from one source mesh to one target mesh.',
    'weight_transfer_batch': 'Transfer weights across stored source and target sets by matching base names.',
    'vertex_snap_title': (
        'Snap one vertex to another in one click.\n\nSingle-Snap:\n1. Select main (anchor) vertex\n2. Shift+select second vertex\n3. Press Snap Vertices (button or hotkey)\n\n'
        'Multi-Snap:\n1. Shift+select main (anchor) vertices in order 1-by-1\n2. Shift+select second set of vertices in order\n3. Requires equal numbers of vertices\n4. Press Snap or hotkey.'
    ),
    'object_snap_title': (
        'Move an entire target object or disconnected mesh island into alignment.\n\n1. Select the source vertex, edge, or face\n2. Shift-select the target anchor last\n'
        '3. For separate objects, keep the target mesh active\n4. Press Vertex, Edge, or Face\n\nEdge and Face can optionally match orientation. Opposing normals is the default.'
    ),
    'vertex_inject_title': (
        'Repair a missing vertex/edge pattern without manually measuring the missing corner.\n\n'
        'A/B/C mode: click A, then B, then C individually; C must be active last. A-B defines the source column relationship and B-C defines row direction. '
        'The solver projects the missing D position onto the inferred parallel target chain, reuses or splits that target, and can connect/split the shared face.\n\n'
        'L mode: select exactly two edges sharing one corner. The tool infers the fourth parallelogram corner from the two legs, reuses a nearby existing vertex when appropriate, and creates the missing outer edges.'
    ),
    'alignment_fixer_title': (
        'Align selected vertices, edges, or faces without guessing transform pivots.\n\n1. Select the parent anchor and Capture Anchor\n2. Choose World XYZ or define a Custom Guide\n'
        '3. Choose Free Coordinates or capture edges as Slide Rails\n4. Select subordinate geometry, Analyze, then Align\n\n'
        'Match toggles are the coordinates that become equal. Coordinates left off remain unchanged. Preserve Relative Spacing moves each target group as one rigid shape. Paired by Rail maps each subordinate island to the captured parent on its rail.'
    ),
    # Legacy help key retained for scenes/UI code that still refers to the former name.
    'guided_align_title': 'Alignment Fixer: capture an anchor, choose world/custom guide constraints, then align selected subordinate geometry.',
    'curvature_sync_title': (
        'Repair and synchronize multiple selected curved edge chains.\n\n1. Select one A/start vertex on every curve and Capture A\n2. Select the middle/symmetry vertex on every curve and Capture Middle\n'
        '3. Select one Z/end vertex on every curve and Capture Z\n4. Select only the A-to-Z curve edges for every parallel chain\n5. Analyze, then Apply Curvature Sync\n\n'
        'The circular workflow keeps A/Z fixed, can normalize Middle, equalizes segment counts, injects missing vertices, and builds/repairs cross-column edges where selected chains bound a common face.'
    ),
    'vertex_locks_title': 'Create targeted protected mesh-edit zones and keep locked vertices fixed while you edit.',
    'vertex_locks_core_title': 'Turn Guard on or off, adjust the guard interval, and refresh locked mesh state while working in a protected edit setup.',
    'vertex_locks_groups_title': 'Manage saved lock groups, select them, disable them, or clear them entirely. This section auto-reveals after you create an edit zone.',
    'vertex_locks_sculpt_title': 'Apply or clear sculpt masks from the currently locked vertices so protected areas stay blocked while sculpting.',
    'vertex_locks_zone_title': (
        'Create an edit zone and protect/lock the vertices outside this zone while Guard is ON.\n\n1. Select all vertices within desired edit zone\n2. Name edit zone\n3. Create edit zone\n4. Select editable interior.'
    ),
    'vertex_locks_guard_interval': 'How often locked vertices are restored while the guard is enabled.',
    'vertex_locks_shape_mirror_title': 'Mirror an edited shape across the mesh without deleting or symmetrizing topology while preserving the existing mesh.',
}


class WITCHTOOLS_OT_help_tooltip(Operator):
    bl_idname = 'witch_tools.help_tooltip'
    bl_label = 'Help'
    bl_options = {'INTERNAL'}
    topic: StringProperty(default='')

    @classmethod
    def description(cls, _context, properties):
        return HELP_TOPICS.get(getattr(properties, 'topic', ''), 'Help')

    def execute(self, _context):
        return {'FINISHED'}


class WITCHTOOLS_OT_open_preferences(Operator):
    bl_idname = 'witch_tools.open_preferences'
    bl_label = 'Open Witch Tools Preferences'
    bl_options = {'INTERNAL'}
    section: StringProperty(default='GENERAL')

    @classmethod
    def description(cls, _context, properties):
        section = getattr(properties, 'section', 'GENERAL').replace('_', ' ').title()
        return f'Open Witch Tools preferences ({section}).'

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs and hasattr(prefs, 'active_section'):
            prefs.active_section = self.section or 'GENERAL'
        try:
            bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        except Exception:
            try:
                bpy.ops.screen.userpref_show()
            except Exception:
                pass
        try:
            bpy.ops.preferences.addon_show(module=ADDON_PACKAGE)
        except Exception:
            pass
        return {'FINISHED'}


class WITCHTOOLS_OT_open_link(Operator):
    bl_idname = 'witch_tools.open_link'
    bl_label = 'Open Link'
    bl_options = {'INTERNAL'}
    url: StringProperty(default='')
    label: StringProperty(default='Open Link')

    @classmethod
    def description(cls, _context, properties):
        label = getattr(properties, 'label', 'Open Link')
        url = getattr(properties, 'url', '')
        return f'{label}: {url}' if url else label

    def execute(self, _context):
        if not self.url:
            return {'CANCELLED'}
        try:
            bpy.ops.wm.url_open(url=self.url)
            return {'FINISHED'}
        except Exception:
            return {'CANCELLED'}


def _capture_ui_state(owner):
    return {name: getattr(owner, name) for name in UI_STATE_PROPS if hasattr(owner, name)}


def _apply_ui_state(owner, data):
    for name in UI_STATE_PROPS:
        if name in data and hasattr(owner, name):
            try:
                setattr(owner, name, data[name])
            except Exception:
                pass


class WITCHTOOLS_OT_toggle_minimal_view(Operator):
    bl_idname = 'witch_tools.toggle_minimal_view'
    bl_label = 'Toggle Minimal View'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def description(cls, context, _properties):
        prefs = addon_preferences(context) if context else None
        if prefs and getattr(prefs, 'ui_minimal_mode', False):
            return 'Expand tool sections.'
        return 'Collapse tool sections.'

    def execute(self, context):
        prefs = addon_preferences(context)
        if prefs is None:
            self.report({'ERROR'}, 'Witch Tools preferences are unavailable.')
            return {'CANCELLED'}
        if prefs.ui_minimal_mode:
            snapshot = {}
            if prefs.ui_state_snapshot:
                try:
                    snapshot = json.loads(prefs.ui_state_snapshot)
                except Exception:
                    snapshot = {}
            _apply_ui_state(prefs, snapshot)
            prefs.ui_minimal_mode = False
            _tag_redraw_all(context)
            self.report({'INFO'}, 'Witch Tools layout restored.')
            return {'FINISHED'}
        prefs.ui_state_snapshot = json.dumps(_capture_ui_state(prefs), separators=(',', ':'))
        for name in UI_STATE_PROPS:
            if name.startswith('show_') and hasattr(prefs, name):
                setattr(prefs, name, False)
        prefs.ui_minimal_mode = True
        _tag_redraw_all(context)
        self.report({'INFO'}, 'Witch Tools collapsed to minimal view.')
        return {'FINISHED'}
