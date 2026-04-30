import math

import blf
import gpu
from gpu_extras.batch import batch_for_shader

from .config import (
    COL_BORDER,
    COL_BUTTON,
    COL_BUTTON_ACTIVE,
    COL_BUTTON_DISABLED,
    COL_BUTTON_HOVER,
    COL_DROP_HINT,
    COL_FOOTER_LINE,
    COL_HEADER,
    COL_HILITE,
    COL_ICON_DIM_OVERLAY,
    COL_MAJOR_TITLE,
    COL_PANEL,
    COL_TEXT,
    COL_TEXT_DIM,
    COL_TITLE,
    COL_TOOLTIP,
    DISPLAY_VERSION,
    tool_open,
)
from .icons import draw_icon as draw_png_icon
from .layout import button_at, build_layout, drop_mode_key, drop_section_key, resize_at
from .utils import addon_preferences

FONT_ID = 0
_shader_cache = None


def _shader():
    global _shader_cache
    if _shader_cache is None:
        _shader_cache = gpu.shader.from_builtin('UNIFORM_COLOR')
    return _shader_cache


def _rounded_points(x, y, w, h, r=4, segments=6):
    r = max(0, min(r, w / 2, h / 2))
    if r <= 0:
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    corners = [
        (x + w - r, y + h - r, 0, math.pi / 2),
        (x + r, y + h - r, math.pi / 2, math.pi),
        (x + r, y + r, math.pi, math.pi * 1.5),
        (x + w - r, y + r, math.pi * 1.5, math.tau),
    ]
    points = []
    for cx, cy, start, end in corners:
        for i in range(segments + 1):
            t = start + (end - start) * (i / segments)
            points.append((cx + math.cos(t) * r, cy + math.sin(t) * r))
    return points


def draw_rect(x, y, w, h, color):
    shader = _shader()
    vertices = ((x, y), (x + w, y), (x + w, y + h), (x, y + h))
    indices = ((0, 1, 2), (0, 2, 3))
    batch = batch_for_shader(shader, 'TRIS', {'pos': vertices}, indices=indices)
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float('color', color)
    batch.draw(shader)
    gpu.state.blend_set('NONE')


def draw_rounded_rect(x, y, w, h, color, radius=4):
    points = _rounded_points(x, y, w, h, radius)
    if len(points) < 3:
        return
    shader = _shader()
    center = (x + w / 2, y + h / 2)
    vertices = [center] + points
    indices = []
    for i in range(1, len(vertices)):
        j = 1 if i == len(vertices) - 1 else i + 1
        indices.append((0, i, j))
    batch = batch_for_shader(shader, 'TRIS', {'pos': vertices}, indices=indices)
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float('color', color)
    batch.draw(shader)
    gpu.state.blend_set('NONE')


def draw_line(points, color, width=1.0):
    if len(points) < 2:
        return
    shader = _shader()
    batch = batch_for_shader(shader, 'LINES', {'pos': points})
    gpu.state.blend_set('ALPHA')
    try:
        gpu.state.line_width_set(width)
    except Exception:
        pass
    shader.bind()
    shader.uniform_float('color', color)
    batch.draw(shader)
    try:
        gpu.state.line_width_set(1.0)
    except Exception:
        pass
    gpu.state.blend_set('NONE')


def draw_polyline(points, color, width=1.0, closed=False):
    if len(points) < 2:
        return
    pts = points + ([points[0]] if closed else [])
    line_points = []
    for start, end in zip(pts[:-1], pts[1:]):
        line_points.extend([start, end])
    draw_line(line_points, color, width)


def draw_rounded_outline(x, y, w, h, color, radius=4, width=1.0):
    draw_polyline(_rounded_points(x, y, w, h, radius), color, width, closed=True)


def draw_text(text, x, y, size=12, color=COL_TEXT, align='CENTER'):
    blf.size(FONT_ID, size)
    w, h = blf.dimensions(FONT_ID, text)
    if align == 'CENTER':
        tx = x - w / 2
    elif align == 'RIGHT':
        tx = x - w
    else:
        tx = x
    blf.position(FONT_ID, tx, y - h / 2, 0)
    blf.color(FONT_ID, *color)
    blf.draw(FONT_ID, text)
    return w, h


def draw_small_chevron(cx, cy, size, color, direction='right', width=1.0):
    s = size * 0.5
    if direction == 'down':
        points = [(cx - s, cy + s * 0.3), (cx, cy - s * 0.55), (cx + s, cy + s * 0.3)]
    elif direction == 'up':
        points = [(cx - s, cy - s * 0.3), (cx, cy + s * 0.55), (cx + s, cy - s * 0.3)]
    elif direction == 'left':
        points = [(cx + s * 0.3, cy + s), (cx - s * 0.55, cy), (cx + s * 0.3, cy - s)]
    else:
        points = [(cx - s * 0.3, cy + s), (cx + s * 0.55, cy), (cx - s * 0.3, cy - s)]
    draw_polyline(points, color, width)


def draw_icon(name, cx, cy, size, enabled=True):
    x = cx - size / 2
    y = cy - size / 2
    ok = draw_png_icon(name, x, y, size, size)
    if ok and not enabled:
        draw_rounded_rect(x, y, size, size, COL_ICON_DIM_OVERLAY, 2)
    if not ok:
        draw_text('?', cx, cy, int(size * 0.55), COL_TEXT_DIM if not enabled else COL_TEXT)


def draw_chevron_icon(x, y, w, h, open_state, enabled=True):
    size = min(w, h) * 0.52
    cx = x + w / 2
    cy = y + h / 2
    if open_state:
        draw_icon('chevron', cx, cy, size, enabled)
    else:
        draw_small_chevron(cx, cy, size * 0.95, COL_TEXT_DIM if not enabled else COL_TEXT, direction='right', width=1.25)


def draw_icon_pair(pair, x, y, w, h, enabled=True):
    cy = y + h / 2
    size = min(h * 0.76, 26)
    left_x = x + w * 0.24
    right_x = x + w * 0.76
    icon_col = COL_TEXT_DIM if not enabled else COL_TEXT
    draw_icon(pair[0], left_x, cy, size, enabled)
    draw_small_chevron(x + w * 0.50, cy, min(h * 0.34, 11), icon_col, direction='right', width=1.15)
    draw_icon(pair[1], right_x, cy, size, enabled)


def draw_button(button, hovered, context, runtime):
    x, y, w, h = button['x'], button['y'], button['w'], button['h']
    prefs = addon_preferences(context)
    scale = prefs.dock_scale if prefs else 1.0
    enabled = button.get('enabled', True)
    active = button.get('active', False)
    style = button.get('style', 'icon')
    radius = max(4, int(5 * scale))

    if style == 'drag_zone':
        if hovered or (runtime.section_dragging and runtime.section_drag_key == button.get('tool_key')):
            draw_rounded_rect(x, y, w, h, (1.0, 1.0, 1.0, 0.035), max(3, radius - 1))
        return

    if runtime.mode_dragging and runtime.mode_drag_key == button.get('mode_key'):
        hovered = True

    if style not in {'bare', 'title_icon'}:
        if not enabled:
            color = COL_BUTTON_DISABLED
            text_color = COL_TEXT_DIM
        elif active:
            color = COL_BUTTON_ACTIVE
            text_color = COL_TEXT
        elif hovered:
            color = COL_BUTTON_HOVER
            text_color = COL_TEXT
        else:
            color = COL_BUTTON
            text_color = COL_TEXT

        draw_rounded_rect(x, y, w, h, color, radius)
        draw_rect(x + 1.8, y + h - 1.3, max(0.0, w - 3.6), 1, COL_HILITE)
    else:
        text_color = COL_TEXT_DIM if not enabled else COL_TEXT
        if hovered:
            draw_rounded_rect(x, y, w, h, (1.0, 1.0, 1.0, 0.04), max(3, radius - 1))

    if button.get('icon') == 'chevron':
        action = button['action']
        if action == 'TOGGLE_MORE_TOOLS':
            open_state = prefs.more_tools_open
        elif action.startswith('TOGGLE_TOOL:'):
            open_state = tool_open(prefs, action.split(':', 1)[1])
        else:
            open_state = True
        draw_chevron_icon(x, y, w, h, open_state, enabled)
    elif 'pair' in button:
        draw_icon_pair(button['pair'], x + 1, y, w - 2, h, enabled)
    elif 'icon' in button:
        if style == 'footer_icon':
            multiplier = 0.84
        elif style == 'title_icon':
            multiplier = 0.92
        else:
            multiplier = 0.78
        size = min(w, h) * multiplier
        draw_icon(button['icon'], x + w / 2, y + h / 2, size, enabled)
    else:
        draw_text(button.get('text', ''), x + w / 2, y + h / 2 + 0.5, int(13 * scale), text_color)


def draw_drag_handle(layout, context):
    drag = layout['drag']
    draw_rounded_rect(drag['x'], drag['y'], drag['w'], drag['h'], COL_HEADER, 7)
    draw_rect(drag['x'], drag['y'], drag['w'], 1, COL_BORDER)
    prefs = addon_preferences(context)
    scale = prefs.dock_scale if prefs else 1.0
    grip_size = int(14 * scale)
    title_size = int(11 * scale)
    draw_text("Witch's Quickbar", drag['x'] + drag['w'] / 2, drag['y'] + drag['h'] / 2 + 0.5, title_size, COL_TEXT_DIM, align='CENTER')
    draw_icon('grip', drag['x'] + drag['w'] - int(15 * scale), drag['y'] + drag['h'] / 2, grip_size, not (prefs and prefs.locked))


def draw_tooltip(context, button, runtime):
    if not button or runtime.dragging or runtime.resizing or runtime.section_dragging or runtime.mode_dragging:
        return
    if button.get('group') == 'mode':
        return
    label = button.get('tooltip', '')
    if not label:
        return
    blf.size(FONT_ID, 12)
    tw, th = blf.dimensions(FONT_ID, label)
    pad = 6
    x = runtime.mouse_x + 12
    y = runtime.mouse_y - 24
    region = context.region
    if x + tw + pad * 2 > region.width:
        x = runtime.mouse_x - tw - pad * 2 - 12
    if y < 4:
        y = runtime.mouse_y + 16
    draw_rounded_rect(x, y, tw + pad * 2, th + pad * 2, COL_TOOLTIP, 4)
    draw_rounded_outline(x, y, tw + pad * 2, th + pad * 2, COL_BORDER, 4, 1.0)
    draw_text(label, x + pad, y + pad + th / 2, 12, COL_TEXT, align='LEFT')


def draw_drop_hints(layout, runtime):
    if runtime.mode_dragging:
        target = drop_mode_key(layout, runtime.mouse_x, runtime.mouse_y)
        items = sorted(layout.get('mode_buttons', []), key=lambda item: item['x'])
        if items:
            if target == '__append__':
                hint_x = items[-1]['x'] + items[-1]['w'] + 2
            else:
                target_item = next((item for item in items if item.get('mode_key') == target), items[0])
                hint_x = target_item['x'] - 2
            y1 = items[0]['y'] + 3
            y2 = items[0]['y'] + items[0]['h'] - 3
            draw_rect(hint_x, y1, 2, y2 - y1, COL_DROP_HINT)

    if runtime.section_dragging:
        target = drop_section_key(layout, runtime.mouse_x, runtime.mouse_y)
        for section in layout.get('sections', []):
            if target == section.get('key') or (target == '__append__' and section is layout.get('sections', [])[-1]):
                y = section['y'] + section['h'] + 2 if target != '__append__' else section['y'] - 2
                draw_rect(section['x'] + 8, y, section['w'] - 16, 2, COL_DROP_HINT)
                break


def draw_overlay(context, runtime):
    if not runtime.running or not context.area or context.area.type != 'VIEW_3D':
        return
    prefs = addon_preferences(context)
    if prefs is None:
        return

    layout = build_layout(context)
    draw_rounded_rect(layout['x'], layout['y'], layout['w'], layout['h'], COL_PANEL, 8)
    draw_rounded_outline(layout['x'], layout['y'], layout['w'], layout['h'], COL_BORDER, 8, 1.0)
    draw_rect(layout['x'] + 1, layout['top'] - 1, layout['w'] - 2, 1, (1.0, 1.0, 1.0, 0.08))
    draw_drag_handle(layout, context)

    hovered = button_at(layout, runtime.mouse_x, runtime.mouse_y) or resize_at(layout, runtime.mouse_x, runtime.mouse_y)
    for row in layout['rows']:
        if row.get('box') in {'major_title', 'tool_title'}:
            color = COL_TITLE if row.get('box') == 'tool_title' else COL_MAJOR_TITLE
            draw_rounded_rect(row['x'], row['y'] + 1, row['w'], row['h'] - 2, color, 5)
        elif row.get('box') == 'footer':
            draw_rect(row['x'] + 2, row['y'] + row['h'] - 1, row['w'] - 4, 1, COL_FOOTER_LINE)
            draw_text(f'Version: {DISPLAY_VERSION}', row['x'] + 5, row['y'] + row['h'] / 2 - 1, int(10 * layout['scale']), COL_TEXT_DIM, align='LEFT')

        if row.get('title'):
            draw_text(row['title'], row['x'] + row['w'] / 2, row['y'] + row['h'] / 2 + 0.5, int(13 * layout['scale']), COL_TEXT, align='CENTER')
            if row.get('box') == 'tool_title':
                draw_icon('grip', row['x'] + row['w'] - int(12 * layout['scale']), row['y'] + row['h'] / 2, int(10 * layout['scale']), True)

    draw_drop_hints(layout, runtime)
    for button in layout['buttons']:
        draw_button(button, button is hovered, context, runtime)
    draw_tooltip(context, hovered, runtime)
