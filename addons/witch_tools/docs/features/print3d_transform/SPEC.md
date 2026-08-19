# Witch Tools — 3D Print Tools + Transform Specification

Status: active development candidate  
Version: `Dev_v2.11.2`  
Parent baseline: Witch Tools `Dev_v2.10.1` / `feature/witch-tools-magic-branch`  
Primary runtime target: `Blender 5.0.1`  
Secondary compatibility target: `Blender 4.5.0`

## Purpose

Keep frequently used transform, 3D-print analysis, repair, cleanup, and STL-export controls inside the Witch Tools N-panel while preserving the existing Magic Branch, Edge Doctor, precision-edit, weight, modifier, and BG3 workflows.

General-purpose mesh logic remains owned by Witch Tools. The feature is modular: backend operators/properties are separate from panel drawing.

## Required top-level order

1. Mode Switcher
2. Transform
3. Auto Mirror
4. 3D Print Tools
5. Edit Tools
6. existing remaining Witch Tools panels

## Transform

Top-level Transform is always available when an active object exists and contains collapsible Location, Rotation, and Scale panels.

Object Mode:
- Location edits the active object's location.
- Rotation edits the active object's current rotation representation and exposes Rotation Mode.
- Scale edits the active object's scale.

Mesh Edit Mode:
- Location displays the object-local median of selected vertices.
- Editing Location translates all selected vertices by the delta from the previous median; it must not collapse them to one coordinate.
- With one selected vertex, Location is that vertex's local coordinate.
- Rotation and Scale remain object transforms because mesh vertices do not own independent rotation/scale values.

## 3D Print Tools

### Export

- Folder selector.
- One Export STL action.
- Format is always STL; no options subsection is exposed.

### Analyze Mesh

One Check All action populates these result counts:
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

Not exposed: Volume/Area statistics, separate Solid/Intersections/Shells buttons, or the original threshold grid.

Even though the threshold controls are hidden, Analyze must reproduce Blender's 3D Print Toolbox check semantics using its standard defaults:
- Degenerate: 0.1 mm (`0.0001` Blender units)
- Non-Planar: 5 degrees
- Thickness: 1 mm (`0.001` Blender units)
- Sharp: 160 degrees
- Overhang: 45 degrees

Parity-sensitive behavior:
- Solid/degenerate/shell counts use the untransformed mesh copy, matching Toolbox behavior.
- Intersect Faces uses Toolbox-style BVH overlap semantics and epsilon.
- Non-flat Faces uses a world-transformed mesh and loop-normal distortion test.
- Thin Faces uses the Toolbox world-transformed, triangulated, six-sample backwards-ray test and maps hits back to original faces.
- Sharp Edges uses a world-transformed mesh and signed manifold-edge face angle.
- Overhang Faces uses a world-transformed mesh and the Toolbox downward-normal angle test.

Result-count parity with Blender's original 3D Print Toolbox must be established on the same mesh before click-to-select result actions are promoted. Click-to-select parity remains a required follow-up because it is part of the user's normal workflow.

### Clean & Repair

Order:
1. Make Manifold
2. Auto Fix
3. Advanced Clean

Auto Fix:
- Global Fix before Local Fix.
- Global controls include Tri Mesh / Quad Mesh, Face Normal, Noise Shells + minimum %, Spikes + angle, Intersect Face + angle, Intersect Volumes, Fill Holes, Auto Fix.
- Local controls retain Select More/Less, Face Orientation, Unify/Flip, Refine, Remesh, Smooth, Reduce.

Advanced Clean must preserve the Instant Clean interaction model unless a specific control was deliberately changed:
- A main Clean button remains at the top and runs every section whose section-header enable toggle is on.
- Repair, Manifold, Topology, Normals, and Dissolve are individual collapsible child sections.
- Each child-section header contains an enable toggle labeled with the section name and a play button.
- A child-section play button runs only that section, independent of the other section enable toggles.
- Holding Shift while using either the main Clean button or an individual section play button limits cleanup to the current selection.
- Repair retains the original-style Remove group with Loose/Doubles/Zero Faces/Dispensables checkbox controls and the compact vertex/edge/face loose-geometry buttons.
- Manifold retains Fill Holes, removes Make Planar, and replaces the original stacked remove checkboxes with `Remove Non-Manifold: [Faces] [Vertices] [Wire]`.
- Topology retains the original Convert To / Methods structure. When converting to quads, Max Face Angle and Max Shape Angle share one row when width permits and separate at narrow widths; Compare uses the responsive Sharp / Seam / UV / Material / VCol toggle bar.
- Normals retains original-style Recalculate / Smooth by Angle / Weighted Normals controls; Clear Data uses the compact Split Normals / Sharp Edges toggle bar.
- Dissolve remains the final section and otherwise keeps its original-style Max Angle / Boundaries / Protect layout.
- Object Data is removed.

## Explicitly excluded

- Hollow
- Bisect
- Align XY
- Scale To
- export-options UI
- 3D Print Toolbox Volume / Area
- separate Solid / Intersections / Shells controls
- Instant Clean Object Data
- Instant Clean Make Planar

These exclusions are UI/scope decisions, not claims that the Blender operations are useless or impossible.

## Safety requirements

Topology-changing operations must:
- produce one coherent Undo step where applicable;
- preserve mode or restore it predictably;
- preserve normals/winding unless the operation explicitly recalculates them;
- preserve materials and edge attributes where technically applicable;
- avoid partial destructive changes on validation failure;
- be tested for malformed selections and shape/topology edge cases;
- document any operator that intentionally rebuilds topology or may discard custom data.

## Acceptance criteria

The candidate is accepted only when:
- Blender 5.0.1 registration and the primary normal-use workflows are tested first;
- Blender 4.5 compatibility is separately tested for the shared/BG3 workflows that need it;
- Transform and 3D Print Tools render in the required order without hiding Magic Branch/Edge Doctor features;
- Advanced Clean section headers visibly provide the Instant Clean-style enable toggle + individual play action and the section bodies retain the specified original-style layouts;
- the main Clean action runs only enabled sections and each section play action runs only that section;
- Transform Location edits object and selected-mesh coordinates correctly;
- Check All counts match the original 3D Print Toolbox on known meshes using the same default thresholds;
- Make Manifold, Auto Fix, and Advanced Clean complete without unhandled exceptions on valid test meshes;
- Undo/Redo, mode restoration, normals/winding, material/edge data, manifold safety, and failure behavior are tested for topology-changing actions;
- STL export succeeds and re-imports as expected.
