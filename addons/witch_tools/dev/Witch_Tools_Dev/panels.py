from .panel_auto_mirror import PANELS as AUTO_MIRROR_PANELS
from .panel_edit_tools import PANELS as EDIT_TOOL_PANELS
from .panel_footer import PANELS as FOOTER_PANELS
from .panel_head_tools import PANELS as HEAD_TOOL_PANELS
from .panel_mode_switcher import PANELS as MODE_SWITCHER_PANELS
from .panel_modifier_tool import PANELS as MODIFIER_PANELS
from .panel_weight_tools import PANELS as WEIGHT_TOOL_PANELS
from .panel_body_tools import PANELS as BODY_TOOL_PANELS
from .panel_armour_tools import PANELS as ARMOUR_TOOL_PANELS
from .panel_hair_tools import PANELS as HAIR_TOOL_PANELS
from .panel_armature_tools import PANELS as ARMATURE_TOOL_PANELS
from .panel_shape_key_tools import PANELS as SHAPE_KEY_TOOL_PANELS
from .panel_export_tools import PANELS as EXPORT_TOOL_PANELS
from .panel_troubleshooting_tools import PANELS as TROUBLESHOOTING_TOOL_PANELS


PANELS = (
    *MODE_SWITCHER_PANELS,
    *AUTO_MIRROR_PANELS,
    *EDIT_TOOL_PANELS,
    *WEIGHT_TOOL_PANELS,
    *MODIFIER_PANELS,
    *HEAD_TOOL_PANELS,
    *BODY_TOOL_PANELS,
    *ARMOUR_TOOL_PANELS,
    *HAIR_TOOL_PANELS,
    *ARMATURE_TOOL_PANELS,
    *SHAPE_KEY_TOOL_PANELS,
    *EXPORT_TOOL_PANELS,
    *TROUBLESHOOTING_TOOL_PANELS,
    *FOOTER_PANELS,
)
