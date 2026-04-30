from .actions import last_switcher_choice, mirror_pivot_mode, rotation_degrees
from .config import (
    MODE_BUTTON_KEYS,
    ORIGIN_GROUPS,
    TOOL_KEYS,
    TOOL_TITLES,
    mode_order,
    ordered_mode_buttons,
    save_mode_order,
    save_tool_order,
    tool_open,
    tool_order,
)
from .utils import addon_preferences, current_mode


RESIZE_HANDLE = 5
MIN_EXTRA_HEIGHT = 0


def current_mode_key(context):
    mode = current_mode(context)
    last_target = last_switcher_choice(context)
    if mode == 'EDIT' and last_target == 'UV_DATA':
        return 'UV_DATA'
    return mode


def supported_transform_mode(context):
    return current_mode(context) in {'OBJECT', 'EDIT'}


def supported_mirror_mode(context):
    return current_mode(context) == 'OBJECT'


def build_layout(context):
    prefs = addon_preferences(context)
    scale = prefs.dock_scale if prefs else 1.0
    region = context.region
    x = float(prefs.dock_x if prefs else 48)
    top_offset = float(prefs.dock_y if prefs else 36)

    drag_h = int(18 * scale)
    margin = int(7 * scale)
    gap = int(5 * scale)
    small_gap = int(2 * scale)
    group_gap = int(12 * scale)
    title_h = int(22 * scale)
    row_h = int(34 * scale)
    footer_h = int(28 * scale)
    footer_btn = int(24 * scale)
    lock_btn = int(15 * scale)
    btn = int(31 * scale)
    chev_w = int(14 * scale)
    step_w = int(47 * scale)
    axis_w = int(25 * scale)
    pair_w = int(62 * scale)
    pivot_w = int(55 * scale)
    mirror_btn_w = int(128 * scale)

    mode_buttons = ordered_mode_buttons(prefs)
    mode_buttons_w = len(mode_buttons) * btn + (len(mode_buttons) - 1) * small_gap
    mode_w = margin * 2 + max(int(240 * scale), mode_buttons_w)
    rotate_w = margin * 2 + max(int(160 * scale), step_w + small_gap + axis_w * 3 + small_gap * 2)
    mirror_w = margin * 2 + max(int(240 * scale), pivot_w * 2 + mirror_btn_w + small_gap * 3)
    origin_w = margin * 2 + max(int(240 * scale), len(ORIGIN_GROUPS) * 2 * pair_w + 2 * group_gap + 3 * small_gap)
    footer_w = margin * 2 + footer_btn * 2 + small_gap + int(120 * scale)
    min_panel_w = max(mode_w, rotate_w, mirror_w, origin_w, footer_w, int(390 * scale))
    stored_w = int(getattr(prefs, 'dock_width', 0) or 0) if prefs else 0
    panel_w = max(min_panel_w, stored_w)

    y_top = region.height - top_offset
    content_h = drag_h + margin + title_h + row_h + gap + title_h + margin
    if prefs and prefs.more_tools_open:
        for key in tool_order(prefs):
            content_h += title_h
            if tool_open(prefs, key):
                content_h += row_h
            content_h += gap
        content_h -= gap
        content_h += margin
    content_h += gap + footer_h
    extra_h = max(MIN_EXTRA_HEIGHT, int(getattr(prefs, 'dock_height_extra', 0) or 0)) if prefs else 0
    total_h = content_h + extra_h

    y = y_top - drag_h
    drag = {'x': x, 'y': y, 'w': panel_w, 'h': drag_h, 'kind': 'drag', 'tooltip': 'Drag Quickbar'}

    rows = []
    buttons = []
    sections = []
    mode_button_items = []

    lock_icon = 'locked' if prefs and prefs.locked else 'unlocked'
    lock_tooltip = 'Unlock Quickbar' if prefs and prefs.locked else 'Lock Quickbar'
    buttons.append({
        'x': x + int(5 * scale),
        'y': y + max(1, int((drag_h - lock_btn) / 2)),
        'w': lock_btn,
        'h': lock_btn,
        'action': 'TOGGLE_LOCK',
        'icon': lock_icon,
        'tooltip': lock_tooltip,
        'enabled': True,
        'active': bool(prefs and prefs.locked),
        'group': 'titlebar',
        'style': 'title_icon',
    })

    y -= margin + title_h
    rows.append({'name': 'mode_title', 'title': 'Mode', 'x': x + margin, 'y': y, 'w': panel_w - margin * 2, 'h': title_h, 'title_pos': 'center', 'box': 'title'})

    y -= row_h
    rows.append({'name': 'mode_tools', 'title': '', 'x': x + margin, 'y': y, 'w': panel_w - margin * 2, 'h': row_h, 'title_pos': 'none', 'box': 'row'})
    bx = x + (panel_w - mode_buttons_w) / 2
    current_key = current_mode_key(context)
    for action, icon, tooltip, target in mode_buttons:
        mode_key = action.split(':', 1)[1]
        button = {
            'x': bx,
            'y': y + 3,
            'w': btn,
            'h': row_h - 6,
            'action': action,
            'icon': icon,
            'tooltip': tooltip,
            'enabled': True,
            'active': bool(target and current_key == target),
            'group': 'mode',
            'style': 'icon',
            'mode_key': mode_key,
        }
        buttons.append(button)
        mode_button_items.append(button)
        bx += btn + small_gap

    y -= gap + title_h
    rows.append({'name': 'more_tools_title', 'title': 'More Tools', 'x': x + margin, 'y': y, 'w': panel_w - margin * 2, 'h': title_h, 'title_pos': 'center', 'box': 'major_title'})
    buttons.append({'x': x + margin, 'y': y + 2, 'w': chev_w, 'h': title_h - 4, 'action': 'TOGGLE_MORE_TOOLS', 'icon': 'chevron', 'tooltip': 'Show/Hide More Tools', 'enabled': True, 'active': False, 'style': 'bare'})

    if prefs and prefs.more_tools_open:
        for key in tool_order(prefs):
            y -= gap + title_h
            title = TOOL_TITLES[key]
            row = {'name': f'{key}_title', 'key': key, 'title': title, 'x': x + margin, 'y': y, 'w': panel_w - margin * 2, 'h': title_h, 'title_pos': 'center', 'box': 'tool_title'}
            rows.append(row)
            sections.append(row)
            buttons.append({'x': x + margin, 'y': y + 2, 'w': chev_w, 'h': title_h - 4, 'action': f'TOGGLE_TOOL:{key}', 'icon': 'chevron', 'tooltip': f'Show/Hide {title}', 'enabled': True, 'active': False, 'style': 'bare', 'tool_key': key})
            buttons.append({'x': x + margin + chev_w + small_gap, 'y': y + 1, 'w': panel_w - margin * 2 - chev_w - small_gap, 'h': title_h - 2, 'action': f'DRAG_TOOL:{key}', 'tooltip': f'Drag to reorder {title}', 'enabled': True, 'active': False, 'style': 'drag_zone', 'tool_key': key})

            if not tool_open(prefs, key):
                continue

            y -= row_h
            rows.append({'name': f'{key}_tools', 'key': key, 'title': '', 'x': x + margin, 'y': y, 'w': panel_w - margin * 2, 'h': row_h, 'title_pos': 'none', 'box': 'row'})
            if key == 'rotate':
                rot_ok = supported_transform_mode(context)
                deg = rotation_degrees(context)
                total_buttons_w = step_w + small_gap + axis_w * 3 + small_gap * 2
                bx = x + (panel_w - total_buttons_w) / 2
                buttons.append({'x': bx, 'y': y + 4, 'w': step_w, 'h': row_h - 8, 'action': 'ROTATE_TOGGLE', 'text': f'{deg}°', 'tooltip': 'Toggle 90° / 180°', 'enabled': True, 'active': deg == 180, 'group': 'rotate', 'style': 'text'})
                bx += step_w + small_gap
                for axis in ('X', 'Y', 'Z'):
                    buttons.append({'x': bx, 'y': y + 4, 'w': axis_w, 'h': row_h - 8, 'action': f'ROTATE:{axis}', 'text': axis, 'tooltip': f'Rotate {deg}° around {axis}', 'enabled': rot_ok, 'active': False, 'group': 'rotate compact', 'style': 'text'})
                    bx += axis_w + small_gap
            elif key == 'mirror':
                mirror_ok = supported_mirror_mode(context)
                pivot = mirror_pivot_mode(context)
                total_buttons_w = pivot_w * 2 + mirror_btn_w + small_gap * 3
                bx = x + (panel_w - total_buttons_w) / 2
                buttons.append({'x': bx, 'y': y + 4, 'w': pivot_w, 'h': row_h - 8, 'action': 'MIRROR_PIVOT:CURSOR', 'text': 'Cursor', 'tooltip': 'Mirror pivot: 3D Cursor', 'enabled': True, 'active': pivot == 'CURSOR', 'group': 'mirror', 'style': 'text'})
                bx += pivot_w + small_gap
                buttons.append({'x': bx, 'y': y + 4, 'w': pivot_w, 'h': row_h - 8, 'action': 'MIRROR_PIVOT:WORLD', 'text': 'World', 'tooltip': 'Mirror pivot: World Origin', 'enabled': True, 'active': pivot == 'WORLD', 'group': 'mirror', 'style': 'text'})
                bx += pivot_w + small_gap * 3
                buttons.append({'x': bx, 'y': y + 4, 'w': mirror_btn_w, 'h': row_h - 8, 'action': 'MIRROR_OBJECTS', 'text': 'Mirror Selected', 'tooltip': 'Duplicate selected mesh objects and mirror them on X', 'enabled': mirror_ok, 'active': False, 'group': 'mirror', 'style': 'text'})
            elif key == 'origin':
                total_buttons_w = sum(len(g) * pair_w + (len(g) - 1) * small_gap for g in ORIGIN_GROUPS) + group_gap * (len(ORIGIN_GROUPS) - 1)
                bx = x + (panel_w - total_buttons_w) / 2
                for group in ORIGIN_GROUPS:
                    for action, pair, tooltip in group:
                        buttons.append({'x': bx, 'y': y + 4, 'w': pair_w, 'h': row_h - 8, 'action': action, 'pair': pair, 'tooltip': tooltip, 'enabled': True, 'active': False, 'group': 'origin', 'style': 'pair'})
                        bx += pair_w + small_gap
                    bx += group_gap - small_gap

    footer_y = y_top - content_h + extra_h
    if extra_h:
        footer_y = y_top - content_h
    y = footer_y
    rows.append({'name': 'footer', 'title': '', 'x': x + margin, 'y': y, 'w': panel_w - margin * 2, 'h': footer_h, 'title_pos': 'none', 'box': 'footer'})
    footer_total_w = footer_btn * 2 + small_gap
    bx = x + panel_w - margin - footer_total_w
    buttons.append({'x': bx, 'y': y + 3, 'w': footer_btn, 'h': footer_h - 6, 'action': 'OPEN_PREFERENCES', 'icon': 'key_command', 'tooltip': 'Open shortcut preferences', 'enabled': True, 'active': False, 'group': 'footer', 'style': 'footer_icon'})
    bx += footer_btn + small_gap
    buttons.append({'x': bx, 'y': y + 3, 'w': footer_btn, 'h': footer_h - 6, 'action': 'CHECK_UPDATES', 'icon': 'import', 'tooltip': 'Check for updates', 'enabled': True, 'active': False, 'group': 'footer', 'style': 'footer_icon'})

    panel_y = y_top - total_h
    resize_handles = [
        {'x': x - RESIZE_HANDLE / 2, 'y': panel_y, 'w': RESIZE_HANDLE, 'h': total_h, 'kind': 'resize', 'edge': 'left', 'tooltip': 'Resize Quickbar'},
        {'x': x + panel_w - RESIZE_HANDLE / 2, 'y': panel_y, 'w': RESIZE_HANDLE, 'h': total_h, 'kind': 'resize', 'edge': 'right', 'tooltip': 'Resize Quickbar'},
        {'x': x, 'y': panel_y - RESIZE_HANDLE / 2, 'w': panel_w, 'h': RESIZE_HANDLE, 'kind': 'resize', 'edge': 'bottom', 'tooltip': 'Resize Quickbar'},
    ]

    return {
        'x': x,
        'y': panel_y,
        'top': y_top,
        'w': panel_w,
        'h': total_h,
        'content_h': content_h,
        'min_w': min_panel_w,
        'drag': drag,
        'rows': rows,
        'buttons': buttons,
        'sections': sections,
        'mode_buttons': mode_button_items,
        'resize_handles': resize_handles,
        'scale': scale,
        'row_h': row_h,
    }


def point_in(item, mx, my):
    return item['x'] <= mx <= item['x'] + item['w'] and item['y'] <= my <= item['y'] + item['h']


def button_at(layout, mx, my):
    for button in reversed(layout['buttons']):
        if button.get('style') == 'drag_zone' and point_in(button, mx, my):
            return button
    for button in reversed(layout['buttons']):
        if button.get('style') != 'drag_zone' and point_in(button, mx, my):
            return button
    if point_in(layout['drag'], mx, my):
        return layout['drag']
    return None


def resize_at(layout, mx, my):
    for handle in layout.get('resize_handles', []):
        if point_in(handle, mx, my):
            return handle
    return None


def drop_mode_key(layout, mx, my):
    items = sorted(layout.get('mode_buttons', []), key=lambda item: item['x'])
    if not items:
        return ''
    for item in items:
        if mx < item['x'] + item['w'] / 2:
            return item.get('mode_key', '')
    return '__append__'


def apply_mode_drop(prefs, dragged, target_key):
    if dragged not in MODE_BUTTON_KEYS or target_key == dragged:
        return
    order = mode_order(prefs)
    if dragged in order:
        order.remove(dragged)
    if target_key == '__append__' or target_key not in order:
        order.append(dragged)
    else:
        order.insert(order.index(target_key), dragged)
    save_mode_order(prefs, order)


def drop_section_key(layout, mx, my):
    sections = layout.get('sections', [])
    if not sections:
        return ''
    for section in sections:
        if section['y'] - 2 <= my <= section['y'] + section['h'] + 2:
            return section.get('key', '')
    ordered = sorted(sections, key=lambda s: s['y'], reverse=True)
    if my > ordered[0]['y'] + ordered[0]['h']:
        return ordered[0].get('key', '')
    if my < ordered[-1]['y']:
        return '__append__'
    nearest = min(ordered, key=lambda s: abs((s['y'] + s['h'] / 2) - my))
    return nearest.get('key', '')


def apply_section_drop(prefs, dragged, target_key):
    if dragged not in TOOL_KEYS:
        return
    order = tool_order(prefs)
    if dragged in order:
        order.remove(dragged)
    if target_key == '__append__' or target_key not in order:
        order.append(dragged)
    else:
        order.insert(order.index(target_key), dragged)
    save_tool_order(prefs, order)
