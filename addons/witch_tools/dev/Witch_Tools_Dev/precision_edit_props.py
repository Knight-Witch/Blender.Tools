from bpy.props import BoolProperty, EnumProperty, FloatVectorProperty, StringProperty
from bpy.types import PropertyGroup


def _sync_inject_mode(self, _context):
    if self.inject_new_mode == 'SLIDE':
        self.inject_new_element_type = 'VERT'
        self.inject_new_use_rail = False


class WTPrecisionEditProperties(PropertyGroup):
    # Section disclosure
    show_coordinate_copy: BoolProperty(name='Coordinate Copy', default=True)
    show_planar_edit: BoolProperty(name='Planar Edit', default=True)
    show_inject_new: BoolProperty(name='Inject New', default=True)
    show_magic_branch: BoolProperty(name='Magic Branch', default=True)

    # Coordinate Copy
    coordinate_copy_space: EnumProperty(
        name='Coordinate Space',
        description='Global applies one world-space coordinate/frame across objects with different origins. Local copies numeric object-local values into each target object',
        items=[
            ('GLOBAL', 'Global', 'Capture and apply in world space; use this to line up different objects exactly'),
            ('LOCAL', 'Local', 'Capture object-local values and apply those same local values in each target object'),
        ],
        default='GLOBAL',
    )
    coordinate_copy_axis_x: BoolProperty(name='X', description='Copy the enabled transform components on X', default=True)
    coordinate_copy_axis_y: BoolProperty(name='Y', description='Copy the enabled transform components on Y', default=True)
    coordinate_copy_axis_z: BoolProperty(name='Z', description='Copy the enabled transform components on Z', default=True)
    coordinate_copy_use_location: BoolProperty(name='Location', description='Copy source position on the enabled X/Y/Z axes', default=True)
    coordinate_copy_use_rotation: BoolProperty(
        name='Rotation',
        description='Match the source geometry frame rotation on the enabled X/Y/Z components. Vertices use their normal; edges/faces use deterministic geometry frames',
        default=False,
    )
    coordinate_copy_use_scale: BoolProperty(
        name='Scale',
        description='Match source geometric extent on the enabled X/Y/Z components. Vertices have unit extent; edges use length; faces use frame-aligned bounds',
        default=False,
    )
    coordinate_copy_source_location: FloatVectorProperty(size=3, subtype='XYZ', precision=6)
    coordinate_copy_source_rotation: FloatVectorProperty(size=3, subtype='EULER', precision=5)
    coordinate_copy_source_scale: FloatVectorProperty(size=3, subtype='XYZ', default=(1.0, 1.0, 1.0), precision=5)
    coordinate_copy_source_type: StringProperty(default='', options={'HIDDEN'})
    coordinate_copy_source_object_name: StringProperty(default='', options={'HIDDEN'})
    coordinate_copy_captured_space: StringProperty(default='', options={'HIDDEN'})
    coordinate_copy_has_source: BoolProperty(default=False, options={'HIDDEN'})
    coordinate_copy_source_label: StringProperty(default='No source captured')
    coordinate_copy_last_report: StringProperty(default='Select one source element and Capture Source.')

    # Planar Edit — Plane Lock
    planar_lock_axis_x: BoolProperty(name='X', description='Freeze selected vertices at their current object-local X coordinate', default=False)
    planar_lock_axis_y: BoolProperty(name='Y', description='Freeze selected vertices at their current object-local Y coordinate', default=False)
    planar_lock_axis_z: BoolProperty(name='Z', description='Freeze selected vertices at their current object-local Z coordinate', default=True)

    # Planar Edit — Level
    planar_level_axis_x: BoolProperty(name='X', description='Set every target to the source world X coordinate', default=False)
    planar_level_axis_y: BoolProperty(name='Y', description='Set every target to the source world Y coordinate', default=False)
    planar_level_axis_z: BoolProperty(name='Z', description='Set every target to the source world Z coordinate', default=True)
    planar_level_source_location: FloatVectorProperty(size=3, subtype='XYZ', precision=6)
    planar_level_has_source: BoolProperty(default=False, options={'HIDDEN'})
    planar_level_source_label: StringProperty(default='No level source captured')
    planar_edit_last_report: StringProperty(default='Choose Plane Lock axes or capture a Level source.')

    # Inject New
    inject_new_mode: EnumProperty(
        name='Setup',
        description='Choose how the newly injected geometry relates to the source',
        items=[
            ('SOLO', 'Solo', 'Duplicate the source without creating any connection back to it'),
            ('BRANCH', 'Branch', 'Duplicate the source and create source-to-copy branch edges'),
            ('SLIDE', 'Slide', 'Insert a new vertex into every selected source edge; all inserted vertices share one relative slide position'),
        ],
        default='SOLO',
        update=_sync_inject_mode,
    )
    inject_new_move: EnumProperty(
        name='Legacy Move Along',
        items=[('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', ''), ('RAIL', 'Rail', '')],
        default='X',
        options={'HIDDEN'},
    )
    inject_new_axis_x: BoolProperty(name='X', description='Allow mouse placement to move on global X', default=True)
    inject_new_axis_y: BoolProperty(name='Y', description='Allow mouse placement to move on global Y', default=False)
    inject_new_axis_z: BoolProperty(name='Z', description='Allow mouse placement to move on global Z', default=False)
    inject_new_use_rail: BoolProperty(
        name='Rail',
        description='Use the captured straight source-to-end rail instead of free XYZ mouse movement',
        default=False,
    )
    inject_new_magnetic_snap: BoolProperty(
        name='Magnetic Snap',
        description='Highlight hovered vertices, edges, and faces and magnetically align the new injection to the hovered target',
        default=True,
    )
    inject_new_auto_merge: BoolProperty(
        name='Auto-Merge',
        description='In Branch mode, weld magnetic vertex/edge contacts into the target topology on commit. A vertex branch dropped on an existing vertex becomes a direct source-to-target edge',
        default=False,
    )
    inject_new_element_type: EnumProperty(
        name='Element',
        description='Geometry type to duplicate in Solo or Branch mode. Slide always injects vertices into the selected edges',
        items=[
            ('VERT', 'Vertex', 'Duplicate one selected vertex'),
            ('EDGE', 'Edge', 'Duplicate one selected edge and its endpoints'),
            ('FACE', 'Face', 'Duplicate one selected face and its boundary'),
        ],
        default='VERT',
    )
    inject_new_rail_end: FloatVectorProperty(size=3, subtype='XYZ', precision=6)
    inject_new_rail_end_set: BoolProperty(default=False, options={'HIDDEN'})
    inject_new_rail_target_label: StringProperty(default='No rail endpoint captured')
    inject_new_last_report: StringProperty(default='Choose Setup, movement, and element type; then select a source.')

    # Magic Branch
    magic_branch_persistent: BoolProperty(
        name='Persistent',
        description='Stay armed after each completed branch so another click-drag can immediately create the next branch. Turn off for one branch then exit',
        default=False,
    )
    magic_branch_element_type: EnumProperty(
        name='Branch Element',
        items=[
            ('VERT', 'Vertex', 'Click-drag a source vertex to branch a new edge'),
            ('EDGE', 'Edge', 'Click-drag a source edge to branch a copied edge with source-to-copy connections'),
            ('FACE', 'Face', 'Click-drag a source face to grow adjacent face geometry from the edge nearest the drag direction'),
        ],
        default='VERT',
    )
    magic_branch_axis_x: BoolProperty(name='X', description='Allow Magic Branch movement on global X', default=True)
    magic_branch_axis_y: BoolProperty(name='Y', description='Allow Magic Branch movement on global Y', default=True)
    magic_branch_axis_z: BoolProperty(name='Z', description='Allow Magic Branch movement on global Z', default=True)
    magic_branch_magnetic_snap: BoolProperty(
        name='Magnetic Snap',
        description='Highlight hovered mesh elements and magnetically align the live branch to them',
        default=True,
    )
    magic_branch_auto_merge: BoolProperty(
        name='Auto-Merge',
        description='On commit, weld compatible magnetic vertex/edge contacts into the existing topology',
        default=False,
    )
    magic_branch_face_mode: EnumProperty(
        name='Face Build',
        items=[
            ('PAVER', 'Paver', 'Repeat equal-size face tiles outward from the source edge as the mouse travels'),
            ('ORGANIC', 'Organic', 'Create one connected face whose outer edge follows the mouse and magnetic target'),
        ],
        default='PAVER',
    )
    magic_branch_last_report: StringProperty(default='Configure Magic Branch, then press Start and click-drag geometry in the viewport.')


CLASSES = (WTPrecisionEditProperties,)
