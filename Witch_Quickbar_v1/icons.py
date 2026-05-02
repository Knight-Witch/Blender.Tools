import os

import bpy
import gpu
import bpy.utils.previews
from gpu_extras.batch import batch_for_shader

ICON_FILES = {
    'mode_edit': 'mode_edit.png',
    'mode_object': 'mode_object.png',
    'mode_weight_paint': 'mode_weight_paint.png',
    'mode_pose': 'mode_pose.png',
    'mode_sculpt': 'mode_sculpt.png',
    'mode_texture_paint': 'mode_texture_paint.png',
    'mode_vertex_paint': 'mode_vertex_paint.png',
    'mode_uv_data': 'mode_uv_data.png',
    'mode_cycle': 'mode_cycle.png',
    'mode_last': 'mode_last.png',
    'chevron': 'chevron.png',
    'grip': 'grip.png',
    'origin': 'origin.png',
    'geometry': 'geometry.png',
    'cursor': 'cursor.png',
    'grid': 'grid.png',
    'selection': 'selection.png',
    'key_command': 'key_command.png',
    'import': 'import.png',
    'locked': 'locked.png',
    'unlocked': 'unlocked.png',
    'emblem': 'emblem.png',
    'pivot_cursor': 'pivot_cursor.png',
    'world': 'world.png',
    'mirror': 'mirror.png',
    'preferences': 'preferences.png',
    'zoom': 'zoom.png',
}

_images = {}
_textures = {}
_shader = None
_previews = None


def _icon_path(name):
    filename = ICON_FILES.get(name)
    if not filename:
        return None
    return os.path.join(os.path.dirname(__file__), 'icons', filename)


def _preview_collection():
    global _previews
    if _previews is None:
        _previews = bpy.utils.previews.new()
    return _previews


def preview_icon(name):
    path = _icon_path(name)
    if not path or not os.path.exists(path):
        return 0
    previews = _preview_collection()
    if name not in previews:
        try:
            previews.load(name, path, 'IMAGE')
        except Exception:
            return 0
    return previews[name].icon_id


def clear_preview_cache():
    global _previews
    if _previews is not None:
        try:
            bpy.utils.previews.remove(_previews)
        except Exception:
            pass
        _previews = None


def _image_shader():
    global _shader
    if _shader is None:
        try:
            _shader = gpu.shader.from_builtin('IMAGE')
        except Exception:
            _shader = gpu.shader.from_builtin('2D_IMAGE')
    return _shader


def get_texture(name):
    if name in _textures:
        return _textures[name]
    path = _icon_path(name)
    if not path or not os.path.exists(path):
        return None
    try:
        img = bpy.data.images.load(path, check_existing=True)
        img.alpha_mode = 'STRAIGHT'
        _images[name] = img
        tex = gpu.texture.from_image(img)
        _textures[name] = tex
        return tex
    except Exception:
        return None


def draw_icon(name, x, y, w, h):
    tex = get_texture(name)
    if tex is None:
        return False
    shader = _image_shader()
    vertices = ((x, y), (x + w, y), (x + w, y + h), (x, y + h))
    texcoords = ((0, 0), (1, 0), (1, 1), (0, 1))
    indices = ((0, 1, 2), (0, 2, 3))
    batch = batch_for_shader(shader, 'TRIS', {'pos': vertices, 'texCoord': texcoords}, indices=indices)
    gpu.state.blend_set('ALPHA')
    shader.bind()
    try:
        shader.uniform_sampler('image', tex)
    except Exception:
        shader.uniform_sampler('Image', tex)
    batch.draw(shader)
    gpu.state.blend_set('NONE')
    return True


def clear_cache():
    clear_preview_cache()
    _textures.clear()
    for img in list(_images.values()):
        try:
            if img and img.name in bpy.data.images:
                bpy.data.images.remove(img)
        except Exception:
            pass
    _images.clear()
