import textwrap

from .keymaps import find_shortcut_text


MODE_BUTTONS = (
    ('wtm.switch_edit_mode', 'EDITMODE_HLT'),
    ('wtm.switch_object_mode', 'OBJECT_DATAMODE'),
    ('wtm.toggle_weight_paint', 'WPAINT_HLT'),
    ('wtm.toggle_pose_mode', 'POSE_HLT'),
    ('wtm.switch_sculpt_mode', 'SCULPTMODE_HLT'),
    ('wtm.switch_texture_paint_mode', 'TPAINT_HLT'),
    ('wtm.switch_vertex_paint_mode', 'VPAINT_HLT'),
    ('wtm.switch_uv_data_mode', 'UV_DATA'),
    ('wtm.cycle_mode_switcher', 'FILE_REFRESH'),
    ('wtm.return_temp_mode', 'EXPORT'),
)


MODE_BUTTON_TARGETS = {
    'wtm.switch_edit_mode': 'EDIT',
    'wtm.switch_object_mode': 'OBJECT',
    'wtm.toggle_weight_paint': 'WEIGHT_PAINT',
    'wtm.toggle_pose_mode': 'POSE',
    'wtm.switch_sculpt_mode': 'SCULPT',
    'wtm.switch_texture_paint_mode': 'TEXTURE_PAINT',
    'wtm.switch_vertex_paint_mode': 'VERTEX_PAINT',
    'wtm.switch_uv_data_mode': 'UV_DATA',
}


def draw_panel_header(layout, icon, title):
    row = layout.row(align=True)
    row.alignment = 'LEFT'
    head = row.row(align=True)
    head.label(text=title, icon=icon)
    return row


def _draw_tooltip_label(row, title, topic, icon='INFO'):
    row.alignment = 'LEFT'
    icon_cell = row.row(align=True)
    icon_cell.ui_units_x = 0.9
    icon_op = icon_cell.operator('witch_tools.help_tooltip', text='', icon=icon, emboss=False)
    icon_op.topic = topic
    text_cell = row.row(align=True)
    text_cell.alignment = 'LEFT'
    text_op = text_cell.operator('witch_tools.help_tooltip', text=title, emboss=False)
    text_op.topic = topic
    return row


def draw_help_title(layout, title, topic, icon='INFO'):
    row = layout.row(align=True)
    return _draw_tooltip_label(row, title, topic, icon=icon)




def draw_centered_disclosure(layout, data, prop_name, text='How to Use'):
    row = layout.row()
    row.alignment = 'CENTER'
    is_open = getattr(data, prop_name)
    row.prop(data, prop_name, text=text, emboss=False, icon='TRIA_DOWN' if is_open else 'TRIA_RIGHT')
    return is_open


def draw_section_toggle(layout, data, prop_name, label, section_icon='NONE', help_topic=''):
    row = layout.row(align=True)
    row.alignment = 'LEFT'
    is_open = getattr(data, prop_name)
    row.prop(data, prop_name, text='', emboss=False, icon='TRIA_DOWN' if is_open else 'TRIA_RIGHT')
    if help_topic:
        _draw_tooltip_label(row, label, help_topic, icon=section_icon if section_icon and section_icon != 'NONE' else 'INFO')
    else:
        label_row = row.row(align=True)
        label_row.alignment = 'LEFT'
        label_row.label(text=label, icon=section_icon if section_icon and section_icon != 'NONE' else 'NONE')
    return is_open


def draw_wrapped_text(layout, context, lines):
    if isinstance(lines, str):
        lines = [lines]
    region_width = getattr(getattr(context, 'region', None), 'width', 300)
    wrap_width = max(20, int((region_width - 70) / 6.5))
    for line in lines:
        for subline in textwrap.wrap(line, width=wrap_width) or ['']:
            layout.label(text=subline)


def draw_shortcut_hint(layout, operator_id, prefix='Shortcut: '):
    row = layout.row()
    row.scale_y = 0.55
    text = find_shortcut_text(operator_id)
    row.label(text=(prefix + text) if text else 'RMB shortcut')


def _mode_switcher_scale(context):
    width = max(220, int(getattr(getattr(context, 'region', None), 'width', 260)))
    return max(1.15, min(2.0, width / 240.0))


def draw_mode_switcher_row(layout, context):
    from .runtime import current_switcher_mode

    active_mode = current_switcher_mode(context)
    scale = _mode_switcher_scale(context)
    outer = layout.row()
    outer.alignment = 'CENTER'
    row = outer.row(align=True)
    row.scale_x = scale
    row.scale_y = scale
    for operator_id, icon in MODE_BUTTONS:
        target_mode = MODE_BUTTON_TARGETS.get(operator_id)
        kwargs = {
            'text': '',
            'depress': bool(target_mode and target_mode == active_mode),
        }
        try:
            row.operator(operator_id, icon=icon, **kwargs)
        except Exception:
            # Fallback so one bad icon enum cannot blank the whole switcher row.
            row.operator(operator_id, icon='QUESTION', **kwargs)
    return row


def compact_button_width(text, icon=False, min_width=0.0):
    width = 0.95 + (0.22 * len(text))
    if icon:
        width += 0.75
    return max(min_width, width)




def draw_fullwidth_operator(layout, operator_id, text, icon='NONE', emboss=True, depress=False):
    return layout.operator(operator_id, text=text, icon=icon, emboss=emboss, depress=depress)


def _inline_label_units(label, icon='NONE', explicit=0.0):
    if explicit > 0.0:
        return explicit
    base = 0.78 + (0.115 * len(label))
    if icon and icon != 'NONE':
        base += 1.15
    return max(2.1, min(base, 5.8))


def draw_inline_label_prop(layout, label, data, prop_name, icon='NONE', field_text='', label_units=0.0, field_units=0.0, expand=False):
    row = layout.row(align=True)
    lead = row.row(align=True)
    lead.alignment = 'LEFT'
    lead.ui_units_x = _inline_label_units(label, icon=icon, explicit=label_units)
    if icon and icon != 'NONE':
        lead.label(text=label, icon=icon)
    else:
        lead.label(text=label)
    field = row.row(align=True)
    if field_units > 0.0:
        field.ui_units_x = min(field_units, 7.4)
    field.prop(data, prop_name, text=field_text, expand=expand)
    return row




