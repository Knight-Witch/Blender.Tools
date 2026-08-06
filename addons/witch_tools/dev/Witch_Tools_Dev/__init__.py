bl_info = {
    'name': 'Witch Tools Dev_v2.8.0',
    'author': 'Knight Witch',
    'version': (2, 8, 0),
    'blender': (4, 5, 0),
    'location': 'View3D > Sidebar > Witch Tools',
    'description': 'Workflow-organized BG3 Blender tools for mode switching, mirror, edit, weight, modifiers, heads, bodies, armour, hair, armatures, shape keys, export, and troubleshooting',
    'category': 'Mesh',
}

from .registration import register, unregister
