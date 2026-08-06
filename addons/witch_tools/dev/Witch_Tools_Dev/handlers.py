import bpy

from .runtime import sync_weight_paint_session, weight_paint_runtime_key
from .state import runtime_cache


@bpy.app.handlers.persistent
def wt_depsgraph_update(_scene, _depsgraph):
    context = bpy.context
    if context is None or getattr(context, 'scene', None) is None or not hasattr(context.scene, 'witch_tools'):
        return
    key = weight_paint_runtime_key(context)
    if runtime_cache.get('weight_paint_key') == key:
        return
    runtime_cache['weight_paint_key'] = key
    sync_weight_paint_session(context)


@bpy.app.handlers.persistent
def wt_load_post(_dummy):
    runtime_cache['weight_paint_key'] = None
    try:
        from .operators_selection_slots import ensure_selection_slots
        ensure_selection_slots(getattr(bpy.context, 'scene', None))
    except Exception:
        pass


def register_handlers():
    if wt_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(wt_depsgraph_update)
    if wt_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(wt_load_post)


def unregister_handlers():
    if wt_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(wt_depsgraph_update)
    if wt_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(wt_load_post)
