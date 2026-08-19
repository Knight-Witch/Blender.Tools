bl_info = {
    'name': 'Witch Tools Dev_v2.10.0',
    'author': 'Knight Witch',
    'version': (2, 10, 0),
    'blender': (4, 5, 0),
    'location': 'View3D > Sidebar > Witch Tools',
    'description': 'Workflow-organized Blender tools with integrated transform, 3D-print analysis, repair, cleanup, BG3, weight, modifier, and modeling workflows',
    'category': 'Mesh',
}

from .registration import register, unregister
