# Witch Tools UI Map

Last updated: 2026-08-18  
Current development candidate: `Dev_v2.10.0`  
Target Blender: `4.5.0`

## Top-level 3D View sidebar order

1. **Mode Switcher**
2. **Transform**
3. **Auto Mirror**
4. **3D Print Tools**
5. **Edit Tools**
6. Quick Modifiers
7. Head Tools
8. Body Tools
9. Armour Tools
10. Hair Tools
11. Weight Tools
12. Armature Tools
13. Shape Key Tools
14. Export Tools
15. Troubleshooting Tools
16. Footer

The new panels are inserted without changing the existing internal Edit Tools ordering or canonical operator ownership.

## Transform

Top-level icon behavior uses Blender-native controls and remains available whenever an active object exists.

Child panels:

### Location

Object Mode:

- direct active-object X / Y / Z location editing.

Mesh Edit Mode:

- shows the local-space median of selected vertices;
- editing an axis translates all selected vertices by the corresponding delta;
- edge/face selections work through their selected participating vertices.

### Rotation

- Rotation Mode selector;
- Euler / Quaternion / Axis Angle fields according to the object rotation mode;
- in Mesh Edit Mode this is explicitly the active object's rotation.

### Scale

- direct active-object X / Y / Z scale;
- in Mesh Edit Mode this is explicitly the active object's scale.

## 3D Print Tools

### Export

- folder field;
- **Export STL** button;
- STL is fixed and no separate format/options panel is exposed.

### Analyze Mesh

- **Check All**
- Results box:
  - Non-manifold Edges
  - Bad Contiguous Edges
  - Intersect Faces
  - Shells
  - Zero Faces
  - Zero Edges
  - Non-flat Faces
  - Thin Faces
  - Sharp Edges
  - Overhang Faces

Not exposed:

- Volume / Area statistics;
- individual Solid / Intersections / Shells filters;
- source threshold grid;
- Hollow;
- Bisect;
- Align XY;
- Scale To.

Current candidate displays result counts only. Result click-to-select/highlight parity is deferred until Blender 4.5 count validation.

### Clean & Repair

Top action:

- **Make Manifold**

Subsections:

1. **Auto Fix**
2. **Advanced Clean**

#### Auto Fix

Order:

1. Global Fix
2. Local Fix

Global Fix controls:

- Tri Mesh / Quad Mesh toggle row
- Face Normal
- Noise Shells + Min %
- Spikes + Min Angle
- Intersect Face + Min Angle
- Intersect Volumes
- Fill Holes
- Auto Fix
- Last Auto Fix statistics

Local Fix controls:

- Select More / Select Less
- Face Orientation display
- Unify / Flip
- Refine
- Remesh
- Smooth
- Reduce

#### Advanced Clean

Top controls:

- **Clean**
- Repair / Manifold / Topology / Normals / Dissolve category toggles
- Shift + Clean = selection only

Subsection order:

1. Repair
2. Manifold
3. Topology
4. Normals
5. Dissolve

Repair retains Loose, Doubles, Zero Faces, and Dispensables controls.

Manifold:

- Fill Holes + Max Sides;
- **Remove Non-Manifold:** Faces / Vertices / Wire toggle row;
- Make Planar is omitted.

Topology:

- Tris / Quads mode;
- conversion-method controls;
- Quads Max Face Angle + Max Shape Angle share a row when space permits and stack when narrow;
- Compare Sharp / Seam / UV / Material / VCol uses compact toggle rows that split when narrow.

Normals:

- Recalculate + Orientation;
- Smooth by Angle + Max Angle;
- Weighted Normals;
- Clear Data: Split Normals / Sharp Edges compact toggle row.

Dissolve:

- Max Angle;
- Boundaries;
- Protect Sharp / Seam / UV / Materials.

Instant Clean Object Data is omitted.

## Edit Tools — retained Dev_v2.9.0 order

1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Inject New
5. Object Snap
6. Edge / Vertex Inject
7. Curvature Sync
8. Align Vertices / Edges / Faces
9. Selection Slots
10. Vertex Locks / remaining Edit Tools controls

All Dev_v2.9.0 precision-edit contracts remain canonical and are not duplicated by the new Transform or 3D Print panels.

## New operator/property contracts in Dev_v2.10.0

3D Print:

- `witch_tools.print3d_analyze`
- `witch_tools.print3d_make_manifold`
- `witch_tools.print3d_export_stl`
- `Scene.wt_print3d`

Auto Fix:

- `witch_tools.mr_auto_fix`
- `witch_tools.mr_local_face_normal`
- `witch_tools.mr_refine_local`
- `witch_tools.mr_remesh_local`
- `witch_tools.mr_smooth_local`
- `witch_tools.mr_reduce_local`
- `Scene.meshfixtool_properties`

Advanced Clean:

- `witch_tools.advanced_clean`
- `Scene.wt_ic_categories`
- `Scene.wt_ic_repair`
- `Scene.wt_ic_manifold`
- `Scene.wt_ic_topology`
- `Scene.wt_ic_normals`
- `Scene.wt_ic_dissolve`

Transform:

- `Scene.wt_transform_state`

## Responsive-layout rule

The integrated 3D Print UI checks the sidebar region width. Wide toggle groups are split into smaller rows below roughly 360 px instead of relying on Blender to clip unavailable controls.
