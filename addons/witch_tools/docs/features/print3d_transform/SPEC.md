# Witch Tools — 3D Print Tools + Transform Specification

Status: active development candidate  
Version: `Dev_v2.11.4`  
Parent baseline: Witch Tools `Dev_v2.10.1` / `feature/witch-tools-magic-branch`  
Primary runtime target: `Blender 5.0.1`  
Secondary compatibility target: `Blender 4.5.0`

## Purpose

Keep frequently used transform, 3D-print analysis, repair, cleanup, and STL-export controls inside the Witch Tools N-panel while preserving the existing Magic Branch, Edge Doctor, precision-edit, weight, modifier, and BG3 workflows.

General-purpose Witch Tools functionality remains modular. Analyze Mesh is a deliberate integration exception: exact diagnostic parity is more important than maintaining a second copy of the 3D Print Toolbox detector code, so Witch Tools invokes the installed 3D Print Toolbox backend directly.

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

UI:
- Folder selector.
- One `Export STL` action.
- Format is always STL; no options subsection is exposed.

Behavior:
- Export the currently selected mesh object(s) as one STL file into the chosen folder.
- Single-object filename uses the active/selected object name; multi-object export uses the active object name with `_selection` suffix.
- Prefer Blender's current native STL exporter and apply evaluated modifiers.
- Require a `FINISHED` result and verify that an STL file was actually created.
- Try the legacy Blender STL operator where available.
- If Blender's STL operator paths are unavailable or cancel/fail, Witch Tools may write binary STL directly from selected evaluated mesh geometry.
- Direct fallback output uses world transforms, triangulated evaluated geometry, and winding correction for negative transforms.
- Fallback output is transactional: write a temporary file and replace the target only after a complete successful write.
- A selection with no exportable triangles fails clearly.
- If all export paths fail, report a visible error with diagnostic detail instead of silently appearing to succeed.

Dev_v2.11.3 STL export was user-confirmed to create the expected STL in Blender 5.0.1 and is retained unchanged in Dev_v2.11.4.

### Analyze Mesh — exact Toolbox backend

One `Check All` action displays these results inside Witch Tools:
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

Not exposed in Witch Tools: Volume/Area statistics, separate Solid/Intersections/Shells buttons, or the threshold-control grid.

#### Source-of-truth contract

Witch Tools must **not** maintain an independently implemented Analyze detector. Dev_v2.11.1 through Dev_v2.11.3 demonstrated that a hand-copied/recreated detector can diverge from the version of 3D Print Toolbox actually installed in Blender 5.0.1.

Dev_v2.11.4 therefore:
- invokes the installed 3D Print Toolbox operator `mesh.print3d_check_all` directly;
- reads the live report produced by that same installed extension;
- mirrors the report counts into the Witch Tools Results box;
- in Edit Mode, invokes the original `mesh.print3d_select_report` operator using the original report index for non-empty selectable results;
- does not substitute Witch Tools thresholds, BMesh copies, BVH logic, normals calculations, or thickness algorithms;
- does not silently fall back to a second analyzer if the Toolbox backend is unavailable.

This makes the installed 3D Print Toolbox the single diagnostic source of truth while keeping its UI inside Witch Tools.

#### Dependency

Analyze Mesh requires 3D Print Toolbox to be installed and enabled. If `mesh.print3d_check_all` or its report data is unavailable, Witch Tools must report an explicit error. Export, Transform, Clean & Repair, and the rest of Witch Tools remain independent of this dependency.

#### Click-to-select behavior

When the original Toolbox report contains selectable element data and Blender is in Edit Mode, the Witch Tools result count becomes an actionable button using the same original report entry and `mesh.print3d_select_report`. The expected selection mode and selected vertex/edge/face indices therefore come from the Toolbox itself rather than a reconstructed Witch Tools selection map.

### Clean & Repair

Order:
1. Make Manifold
2. Auto Fix
3. Advanced Clean

Auto Fix:
- Global Fix before Local Fix.
- Global controls include Tri Mesh / Quad Mesh, Face Normal, Noise Shells + minimum %, Spikes + angle, Intersect Face + angle, Intersect Volumes, Fill Holes, Auto Fix.
- Local controls retain Select More/Less, Face Orientation, Unify/Flip, Refine, Remesh, Smooth, Reduce.

Advanced Clean preserves the Instant Clean interaction model unless a specific control was deliberately changed:
- A main Clean button remains at the top and runs every section whose section-header enable toggle is on.
- Repair, Manifold, Topology, Normals, and Dissolve are individual collapsible child sections.
- Each child-section header contains an enable toggle labeled with the section name and a play button.
- A child-section play button runs only that section, independent of the other section enable toggles.
- Holding Shift while using either the main Clean button or an individual section play button limits cleanup to the current selection.
- Repair retains the original-style Remove group with Loose/Doubles/Zero Faces/Dispensables checkbox controls and compact vertex/edge/face loose-geometry buttons.
- Manifold retains Fill Holes, removes Make Planar, and uses `Remove Non-Manifold: [Faces] [Vertices] [Wire]`.
- Topology retains the original Convert To / Methods structure. Max Face Angle and Max Shape Angle share one row when width permits and separate when narrow; Compare uses the responsive Sharp / Seam / UV / Material / VCol toggle bar.
- Normals retains original-style Recalculate / Smooth by Angle / Weighted Normals controls; Clear Data uses Split Normals / Sharp Edges toggle buttons.
- Dissolve remains the final section with Max Angle / Boundaries / Protect layout.
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

## Safety requirements

Topology-changing operations must:
- produce one coherent Undo step where applicable;
- preserve mode or restore it predictably;
- preserve normals/winding unless the operation explicitly recalculates them;
- preserve materials and edge attributes where technically applicable;
- avoid partial destructive changes on validation failure;
- be tested for malformed selections and shape/topology edge cases;
- document any operator that intentionally rebuilds topology or may discard custom data.

Export must never overwrite/replace the destination with a partial fallback file after a failed fallback write.

Analyze is non-destructive except for the original Toolbox selection operator when the user explicitly clicks a result in Edit Mode.

## Acceptance criteria

The candidate is accepted only when:
- Blender 5.0.1 registration and primary workflows are tested first;
- Blender 4.5 compatibility is separately tested for shared/BG3 workflows that need it;
- Transform and 3D Print Tools render in the required order without hiding baseline tools;
- Advanced Clean headers/body layout and individual/global execution behave as specified;
- Transform Location edits object and selected-mesh coordinates correctly;
- running original Toolbox `Check All` and Witch Tools `Check All` consecutively on the same unchanged object produces identical displayed counts because both use the same Toolbox backend;
- Witch Tools result buttons in Edit Mode select the same exact elements as the original Toolbox result buttons;
- an unavailable/disabled Toolbox produces an explicit Analyze error rather than an alternate result set;
- Make Manifold, Auto Fix, and Advanced Clean complete without unhandled exceptions on valid test meshes;
- topology-changing actions pass Undo/Redo, mode, normals/winding, material/edge-data, manifold, malformed-selection, and safe-failure tests;
- STL export creates a valid non-empty file and re-imports with expected dimensions/orientation.
