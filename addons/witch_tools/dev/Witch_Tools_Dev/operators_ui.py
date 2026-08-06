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
    'weight_transfer_single': 'Transfer weights from one source mesh to one target mesh.',
    'weight_transfer_batch': 'Transfer weights across stored source and target sets by matching base names.',
    'vertex_snap_title': (
        'Snap one vertex to another in one click.\n\n'
        'Single-Snap:\n'
        '1. Select main (anchor) vertex\n'
        '2. Shift+select second vertex\n'
        '3. Press Snap Vertices (button or hotkey)\n\n'
        'Multi-Snap:\n'
        '1. Shift+select main (anchor) vertices in order 1-by-1\n'
        '2. Shift+select second set of vertices in order\n'
        '3. Note: requires equal number of vertices\n'
        '4. Press Snap or hotkey'
    ),
    'object_snap_title': (
        'Move an entire target object or disconnected mesh island into alignment.\n\n'
        '1. Select the source vertex, edge, or face\n'
        '2. Shift-select the target anchor last\n'
        '3. For separate objects, keep the target mesh active\n'
        '4. Press Vertex, Edge, or Face\n\n'
        'Edge and Face can optionally match orientation. Opposing normals is the default.'
    ),
    'guided_align_title': (
        'Align selected vertices, edges, or faces without guessing transform pivots.\n\n'
        '1. Select the parent anchor and Capture Anchor\n'
        '2. Choose World XYZ or define a Custom Guide\n'
        '3. Choose Free Coordinates or capture edges as Slide Rails\n'
        '4. Select the subordinate geometry, Analyze, then Align\n\n'
        'Match toggles are the coordinates that become equal. Coordinates left off remain unchanged. Preserve Relative Spacing moves each target group as one rigid shape. Paired by Rail maps each subordinate island to the single captured parent vertex on its rail.'
    ),
    'curvature_sync_title': (
        'Repair and synchronize multiple selected curved edge chains.\n\n'
        '1. Select one A/start vertex on every curve and Capture A\n'
        '2. Select the middle/symmetry vertex on every curve and Capture Middle\n'
        '3. Select one Z/end vertex on every curve and Capture Z\n'
        '4. Select only the A-to-Z curve edges for every parallel chain on every aligned object\n'
        '5. Analyze, then Apply Curvature Sync\n\n'
        'Circular MVP: keeps A/Z fixed, optionally normalizes Middle to the exact curve axis, equalizes segment counts on both sides, injects missing vertices, and builds cross-column edges where selected chains bound a common face.'
    ),
    'vertex_locks_title': 'Create a targeted mesh-edit zone, & lock all vertices outside this zone in place while you edit.',
    'vertex_locks_core_title': 'Turn Guard on or off, adjust the guard interval, and refresh locked mesh state while working in a protected edit setup.',
    'vertex_locks_groups_title': 'Manage saved lock groups, select them, disable them, or clear them entirely. This section auto-reveals after you create an edit zone.',
    'vertex_locks_sculpt_title': 'Apply or clear sculpt masks from the currently locked vertices so protected areas stay blocked while sculpting.',
    'vertex_locks_zone_title': (
        'Create an edit zone and protect/lock the vertices outside this zone while Guard is ON to prevent unwanted influence.\n\n'
        '1. Select all vertices within desired edit zone\n'
        '2. Name edit zone\n'
        '3. Create edit zone\n'
        '4. Select editable interior'
    ),
    'vertex_locks_guard_interval': 'How often locked vertices are restored while the guard is enabled.',
    'vertex_locks_shape_mirror_title': (
        'Mirror an edited shape across the mesh without deleting or symmetrizing topology.\n\n'
        'Use this to copy shape changes from one side to the other while preserving the existing mesh.'
    ),
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
