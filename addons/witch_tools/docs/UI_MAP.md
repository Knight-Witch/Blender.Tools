# Witch Tools UI Map

Last updated: 2026-08-18  
Current development candidate: `Dev_v2.11.0`

## Top-level N-panel default order

1. Mode Switcher
2. Transform
3. Auto Mirror
4. 3D Print Tools
5. Edit Tools
6. Weight Tools
7. Quick Modifiers
8. Head Tools
9. Body Tools
10. Armour Tools
11. Hair Tools
12. Armature Tools
13. Shape Key Tools
14. Export Tools
15. Troubleshooting Tools
16. Footer

## Transform

Parent: `Transform`

Child panels:
- Location
- Rotation
- Scale

Object Mode:
- Location / Rotation / Scale map directly to active-object transforms.

Mesh Edit Mode:
- Location shows selected-vertex object-local median and translates the selection by delta when edited.
- One selected vertex therefore displays/edits that vertex coordinate.
- Rotation / Scale remain active-object transforms.

## 3D Print Tools

Parent: `3D Print Tools`

### Export

- folder selector
- `Export STL`

No format selector or export-options subsection; STL is fixed.

### Analyze Mesh

- `Check All`
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

Dev_v2.11.0 exposes counts only. Exact click-to-select result behavior is planned after detector parity is validated against Blender's original 3D Print Toolbox.

### Clean & Repair

- `Make Manifold`

#### Auto Fix

Global Fix first:
- Tri Mesh / Quad Mesh
- Face Normal
- Noise Shells + Min %
- Spikes + Min Angle
- Intersect Face + Min Angle
- Intersect Volumes
- Fill Holes
- Auto Fix

Local Fix:
- Select More / Less
- Face Orientation
- Unify/Flip
- Refine
- Remesh
- Smooth
- Reduce

#### Advanced Clean

- Clean
- Repair
- Manifold
- Topology
- Normals
- Dissolve

Requested condensed controls:
- Manifold `Remove Non-Manifold:` Faces / Vertices / Wire toggle row.
- Topology face/shape angle controls share a row when width permits and split at narrow widths.
- Topology Compare: Sharp / Seam / UV / Material / VCol responsive toggle row.
- Normals Clear Data: Split Normals / Sharp Edges toggle row.
- Dissolve remains at the bottom.

Not exposed in this integrated UI:
- Volume/Area
- separate Solid/Intersections/Shells controls
- Hollow
- Bisect
- Align XY
- Scale To
- export options
- Instant Clean Object Data
- Make Planar

## Edit Tools — retained Dev_v2.10.1 baseline

Default preference-backed order:
1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Object Snap
5. Inject New
6. Magic Branch
7. Edge Doctor
8. Vertex Lock
9. Selection Slots

`Reorder Tools` remains preference-backed with compact drag-grip/up/down controls.

### Coordinate Copy

Global/Local; X/Y/Z; Location/Rotation/Scale; capture one vertex/edge/face source; apply to independent targets. Default Apply shortcut: `Ctrl+Shift+C`.

### Planar Edit

- Plane Lock: persistent object-local X/Y/Z vertex constraints.
- Level: capture source point and assign exact enabled world coordinates to targets.

### Inject New

- Solo / Branch / Slide.
- XYZ movement, optional captured rail, Magnetic Snap, Branch Auto-Merge.
- Dev_v2.10.1 multi-edge Edge source and merge corrections retained.

### Magic Branch

- explicit ON/OFF plus separate Persistent behavior.
- Vertex / Edge / Face.
- Face Paver / Organic.
- XYZ, Magnetic Snap, Auto-Merge.
- Branch Type synchronizes Blender selection mode in the Dev_v2.10.1 candidate.

### Edge Doctor

Contains:
- Missing Vertex / Edge Injector
- Alignment Fixer
- Curvature Sync

### Vertex Lock / Selection Slots

Existing protection and saved-selection workflows retained.

## Persistence / backend contracts

- Transform transient UI property: `Scene.wt_transform_state`.
- 3D Print analyzer/export state: `Scene.wt_print3d`.
- Advanced Clean property groups: `Scene.wt_ic_*`.
- Mesh Repair Auto Fix state: `Scene.meshfixtool_properties`.
- Precision Edit state: `Scene.wt_precision_edit`.
- Existing Edit Tools order/disclosure state: add-on preferences.
- Existing magnetic topology/drag logic remains in the Dev_v2.10.1 precision-edit backend.

Witch Dock / Quickbar is not modified by Dev_v2.11.0.
