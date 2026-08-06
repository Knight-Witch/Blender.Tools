from .ui_helpers import draw_panel_header
from .utils_context import ui_state_owner


class WTHeaderPanelMixin:
    panel_title = ''
    panel_icon = 'NONE'
    hide_in_minimal = True

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, _context):
        draw_panel_header(self.layout, self.panel_icon, self.panel_title)
