import bpy
from bpy.types import PropertyGroup


def _exclusive(prop_self, prop):
    if getattr(prop_self, prop):
        other = 'quad_boolean' if prop == 'tri_boolean' else 'tri_boolean'
        if getattr(prop_self, other):
            setattr(prop_self, other, False)


def update_tri(self, context): _exclusive(self, 'tri_boolean')
def update_quad(self, context): _exclusive(self, 'quad_boolean')


class MFTProperties(PropertyGroup):
    meshfixing: bpy.props.BoolProperty(name='Fixing Status', default=False)
    sum_vertices: bpy.props.IntProperty(default=0)
    sum_edges: bpy.props.IntProperty(default=0)
    sum_faces: bpy.props.IntProperty(default=0)
    sum_holes: bpy.props.IntProperty(default=0)
    sum_volumes: bpy.props.IntProperty(default=0)

    tri_boolean: bpy.props.BoolProperty(name='Tri Mesh', description='Triangulate mesh', default=True, update=update_tri)
    quad_boolean: bpy.props.BoolProperty(name='Quad Mesh', description='Convert triangles to quads after repair', default=False, update=update_quad)
    face_normal_boolean: bpy.props.BoolProperty(name='Face Normal', description='Recalculate face normals outside', default=False)
    minor_parts_boolean: bpy.props.BoolProperty(name='Noise Shells', description='Remove small disconnected mesh parts', default=False)
    minor_parts_threshold: bpy.props.FloatProperty(name='', default=1.0, description='Loose parts face threshold as percent of total faces', min=0.1, max=5.0, precision=1, step=0.1)
    spikes_boolean: bpy.props.BoolProperty(name='Spikes', description='Dissolve vertices forming extreme face-normal angles', default=False)
    spikes_angle_limit: bpy.props.FloatProperty(name='', default=10.0, description='Minimum spike angle', min=1.0, max=60.0, precision=1, step=1.0)
    intersection_boolean: bpy.props.BoolProperty(name='Intersect Face', description='Dissolve vertices around non-manifold / extreme intersecting faces', default=False)
    intersection_angle_limit: bpy.props.FloatProperty(name='', default=10.0, description='Minimum intersection angle', min=1.0, max=60.0, precision=1, step=1.0)
    volume_intersection_boolean: bpy.props.BoolProperty(name='Intersect Volumes', description='Union overlapping disconnected volumes; destructive to some mesh data', default=False)
    holes_boolean: bpy.props.BoolProperty(name='Fill Holes', description='Fill boundary holes', default=False)
    statistics_boolean: bpy.props.BoolProperty(name='Statistics', default=True)
