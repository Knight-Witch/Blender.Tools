DISPLAY_VERSION = 'v1.0.2'
UPDATE_URL = 'https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access'

MODE_SEQUENCE = (
    'EDIT',
    'OBJECT',
    'WEIGHT_PAINT',
    'POSE',
    'SCULPT',
    'TEXTURE_PAINT',
    'VERTEX_PAINT',
    'UV_DATA',
)

MODE_BUTTONS = (
    ('MODE:EDIT', 'mode_edit', 'Edit Mode', 'EDIT'),
    ('MODE:OBJECT', 'mode_object', 'Object Mode', 'OBJECT'),
    ('MODE:WEIGHT_PAINT', 'mode_weight_paint', 'Weight Paint', 'WEIGHT_PAINT'),
    ('MODE:POSE', 'mode_pose', 'Pose Mode', 'POSE'),
    ('MODE:SCULPT', 'mode_sculpt', 'Sculpt Mode', 'SCULPT'),
    ('MODE:TEXTURE_PAINT', 'mode_texture_paint', 'Texture Paint', 'TEXTURE_PAINT'),
    ('MODE:VERTEX_PAINT', 'mode_vertex_paint', 'Vertex Paint', 'VERTEX_PAINT'),
    ('MODE:UV_DATA', 'mode_uv_data', 'UV Data / Edit Mode', 'UV_DATA'),
    ('MODE:CYCLE', 'mode_cycle', 'Cycle Modes', ''),
    ('MODE:RETURN', 'mode_last', 'Last Mode Used', ''),
)

MODE_BUTTON_KEYS = tuple(item[0].split(':', 1)[1] for item in MODE_BUTTONS)
MODE_BUTTON_MAP = {item[0].split(':', 1)[1]: item for item in MODE_BUTTONS}
DEFAULT_MODE_ORDER = ','.join(MODE_BUTTON_KEYS)
DEFAULT_CYCLE_MODE_FILTER = ','.join(MODE_SEQUENCE)

ORIGIN_GROUPS = (
    (
        ('ORIGIN:GEOMETRY', ('origin', 'geometry'), 'Origin to geometry'),
        ('ORIGIN:CURSOR', ('origin', 'cursor'), 'Origin to cursor'),
    ),
    (
        ('SNAP:CURSOR_TO_SELECTED', ('cursor', 'selection'), 'Cursor to selected'),
        ('SNAP:CURSOR_TO_GRID', ('cursor', 'grid'), 'Cursor to grid'),
    ),
    (
        ('SNAP:SELECTION_TO_CURSOR', ('selection', 'cursor'), 'Selected to cursor'),
        ('SNAP:SELECTION_TO_GRID', ('selection', 'grid'), 'Selected to grid'),
    ),
)

TOOL_KEYS = ('rotate', 'origin', 'mirror')
TOOL_TITLES = {
    'rotate': 'Rotate',
    'mirror': 'Mirror Objects',
    'origin': 'Origins & Cursor',
}
DEFAULT_TOOL_ORDER = ','.join(TOOL_KEYS)
MIRROR_PIVOT_MODES = ('CURSOR', 'WORLD')

COL_PANEL = (0.18, 0.18, 0.18, 0.96)
COL_HEADER = (0.145, 0.145, 0.145, 0.98)
COL_TITLE = (0.205, 0.205, 0.205, 0.92)
COL_MAJOR_TITLE = (0.188, 0.188, 0.188, 0.94)
COL_BORDER = (0.075, 0.075, 0.075, 0.96)
COL_FOOTER_LINE = (0.42, 0.42, 0.42, 0.40)
COL_BUTTON = (0.315, 0.315, 0.315, 0.98)
COL_BUTTON_HOVER = (0.39, 0.39, 0.39, 0.99)
COL_BUTTON_ACTIVE = (0.28, 0.43, 0.70, 1.0)
COL_BUTTON_DISABLED = (0.235, 0.235, 0.235, 0.72)
COL_TEXT = (0.86, 0.86, 0.86, 1.0)
COL_TEXT_DIM = (0.52, 0.52, 0.52, 0.92)
COL_TOOLTIP = (0.045, 0.045, 0.045, 0.97)
COL_HILITE = (1.0, 1.0, 1.0, 0.05)
COL_ICON_DIM_OVERLAY = (0.08, 0.08, 0.08, 0.42)
COL_DROP_HINT = (0.52, 0.66, 0.92, 0.24)


def ordered_unique(raw, allowed):
    seen = []
    for key in (raw or '').split(','):
        key = key.strip()
        if key in allowed and key not in seen:
            seen.append(key)
    for key in allowed:
        if key not in seen:
            seen.append(key)
    return seen


def mode_order(prefs):
    raw = getattr(prefs, 'mode_order', '') if prefs else ''
    return ordered_unique(raw, MODE_BUTTON_KEYS)


def save_mode_order(prefs, order):
    prefs.mode_order = ','.join(ordered_unique(','.join(order), MODE_BUTTON_KEYS))


def ordered_mode_buttons(prefs):
    return [MODE_BUTTON_MAP[key] for key in mode_order(prefs)]


def cycle_enabled_modes(prefs):
    raw = getattr(prefs, 'cycle_mode_filter', '') if prefs else ''
    if not raw:
        return list(MODE_SEQUENCE)
    enabled = []
    for key in raw.split(','):
        key = key.strip()
        if key in MODE_SEQUENCE and key not in enabled:
            enabled.append(key)
    return enabled


def save_cycle_enabled_modes(prefs, modes):
    valid = [key for key in modes if key in MODE_SEQUENCE]
    prefs.cycle_mode_filter = ','.join(valid)


def cycle_mode_order(prefs):
    enabled = set(cycle_enabled_modes(prefs))
    return [key for key in mode_order(prefs) if key in MODE_SEQUENCE and key in enabled]


def tool_order(prefs):
    raw = getattr(prefs, 'tool_order', '') if prefs else ''
    return ordered_unique(raw, TOOL_KEYS)


def save_tool_order(prefs, order):
    prefs.tool_order = ','.join(ordered_unique(','.join(order), TOOL_KEYS))


def tool_open(prefs, key):
    if key == 'rotate':
        return bool(prefs.rotate_open)
    if key == 'mirror':
        return bool(prefs.mirror_open)
    if key == 'origin':
        return bool(prefs.tools_open)
    return True


def toggle_tool_open(prefs, key):
    if key == 'rotate':
        prefs.rotate_open = not prefs.rotate_open
    elif key == 'mirror':
        prefs.mirror_open = not prefs.mirror_open
    elif key == 'origin':
        prefs.tools_open = not prefs.tools_open
