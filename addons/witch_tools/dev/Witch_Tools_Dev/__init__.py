bl_info = {
    'name': 'Witch Tools Dev_v2.11.4',
    'author': 'Knight Witch',
    'version': (2, 11, 4),
    'blender': (4, 5, 0),
    'location': 'View3D > Sidebar > Witch Tools',
    'description': 'Workflow-organized Blender tools with integrated Transform, 3D-print analysis/repair/cleanup, Magic Branch, BG3, weight, modifier, and modeling workflows',
    'category': 'Mesh',
}

from .registration import register, unregister
