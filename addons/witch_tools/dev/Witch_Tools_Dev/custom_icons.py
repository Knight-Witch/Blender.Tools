import os

import bpy.utils.previews

_PREVIEWS = None

_ICON_FILES = {
    "github": "github.png",
    "patreon": "patreon.png",
    "kofi": "kofi.png",
    "paypal": "paypal.png",
    "nexus": "nexus.png",
    "website": "website.png",
}


def register_custom_icons():
    global _PREVIEWS
    if _PREVIEWS is not None:
        return _PREVIEWS
    pcoll = bpy.utils.previews.new()
    base_dir = os.path.join(os.path.dirname(__file__), "icons")
    for key, filename in _ICON_FILES.items():
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            pcoll.load(key, path, 'IMAGE')
    _PREVIEWS = pcoll
    return _PREVIEWS


def unregister_custom_icons():
    global _PREVIEWS
    if _PREVIEWS is not None:
        bpy.utils.previews.remove(_PREVIEWS)
        _PREVIEWS = None


def get_icon_id(key, fallback=0):
    if _PREVIEWS is None:
        return fallback
    icon = _PREVIEWS.get(key)
    return icon.icon_id if icon else fallback
