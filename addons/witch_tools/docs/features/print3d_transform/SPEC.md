# Witch Tools — 3D Print Tools + Transform Specification

Status: active development candidate  
Version: `Dev_v2.10.0`  
Target Blender: `4.5.0`

## Purpose

Consolidate the user's frequently used 3D-print analysis, repair/cleanup, STL export, and transform controls inside the existing **Witch Tools** N-panel so normal work does not require switching N-panel tabs.

The implementation is intentionally modular: generic mesh repair/cleanup logic belongs to Witch Tools and UI code remains separate from geometry logic.

## Top-level panel order

1. Mode Switcher
2. Transform
3. Auto Mirror
4. 3D Print Tools
5. Edit Tools
6. remaining existing Witch Tools panels

## Transform

A top-level **Transform** panel sits immediately below Mode Switcher and contains collapsible Location, Rotation, and Scale child panels.

### Object Mode

- Location directly edits the active object's location.
- Rotation directly edits the active object's current rotation representation and exposes Rotation Mode.
- Scale directly edits the active object's scale.

### Mesh Edit Mode

- Location shows the local-space median coordinate of the currently selected vertices.
- Editing Location translates the selected vertices by the delta from the previous median, matching Blender's normal selection-transform behavior rather than collapsing all vertices onto one point.
- Rotation and Scale remain the active object's transform values because mesh vertices do not own independent rotation or scale properties.

## 3D Print Tools

### Export

- Folder picker only.
- One **Export STL** button.
- Format is fixed to STL.
- No inherited export-options subsection.
- Selected mesh objects export together; a single selected object uses its object name.

### Analyze Mesh

Only the consolidated workflow is exposed:

- **Check All**
- Results box containing:
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

Explicitly omitted from the UI:

- Volume / Area statistics
- individual Solid / Intersections / Shells filter buttons
- threshold-control grid from the original 3D Print Toolbox
- Hollow
- Bisect
- Align XY
- Scale To

The initial candidate keeps these as result counts only. Selection/highlight parity with the original toolbox is a possible follow-up after Blender 4.5 validation.

### Clean & Repair

Contains:

1. **Make Manifold**
2. **Auto Fix**
3. **Advanced Clean**

#### Make Manifold

Runs a conservative sequence intended for print prep: merge by distance, dissolve degenerate geometry, delete loose geometry, fill boundary holes where Blender can do so safely, and recalculate normals outside.

#### Auto Fix

Derived from the user-supplied Mesh Repair workflow and intentionally ordered **Global Fix first, Local Fix second**.

Global Fix retains the practical controls:

- Tri Mesh / Quad Mesh toggle row
- Face Normal
- Noise Shells + Min %
- Spikes + Min Angle
- Intersect Face + Min Angle
- Intersect Volumes
- Fill Holes
- Auto Fix action
- last-run statistics

Local Fix retains:

- Select More / Select Less
- Face Orientation display
- Unify / Flip Normal
- Refine
- Remesh
- Smooth
- Reduce

#### Advanced Clean

Derived from the user-supplied Instant Clean workflow.

Top action:

- Clean
- category toggles: Repair / Manifold / Topology / Normals / Dissolve
- Shift + Clean limits cleanup to the current selection

Subsections:

- Repair
- Manifold
- Topology
- Normals
- Dissolve

Explicitly omitted:

- Object Data
- Manifold Make Planar

Manifold uses a compact **Remove Non-Manifold:** toggle bar for Faces / Vertices / Wire.

Topology uses responsive layout: angle inputs share a row when the panel is wide enough and stack when narrow. Compare options Sharp / Seam / UV / Material / VCol use compact toggle rows that split when narrow.

Normals Clear Data uses a compact Split Normals / Sharp Edges toggle bar.

Dissolve is the final Advanced Clean subsection.

## Responsive UI requirement

Compact option groups must not be clipped when the N-panel narrows. The candidate uses the current `context.region.width` to split wide toggle rows into smaller rows below approximately 360 px.

## Safety requirements

Topology-changing operations must:

- be a single Blender undo step where practical;
- restore the user's prior object/edit mode when the operator temporarily changes mode;
- fail without intentionally continuing after an exception;
- avoid touching unrelated objects unless explicitly selected/targeted;
- preserve existing Witch Tools systems and panel ordering outside this requested insertion.

The more destructive **Intersect Volumes** option remains opt-in and must be treated as topology-rebuilding behavior.

## Acceptance criteria

1. Add-on registers and unregisters cleanly in Blender 4.5.0.
2. Transform appears directly under Mode Switcher.
3. 3D Print Tools appears above Edit Tools.
4. Object Location/Rotation/Scale fields update the active object immediately.
5. Edit-mode Location reflects selected-vertex median and editing it translates the selection correctly.
6. Check All produces all ten result values without changing mesh geometry.
7. Make Manifold completes as one undoable operation and does not leave the mesh in an unexpected mode.
8. Auto Fix Global and Local controls render in the requested order and invoke their integrated Witch Tools operators.
9. Advanced Clean contains Repair, Manifold, Topology, Normals, Dissolve in that order and omits Object Data / Make Planar.
10. Manifold, Topology Compare, and Normals Clear Data use compact toggle rows; narrow panel widths do not clip controls.
11. STL export requires no format/options configuration and writes an STL into the selected folder.
12. Existing Dev_v2.9.0 precision/edit tools still register and render unchanged below the inserted panels.
13. Undo/redo, normals/winding, material/edge attribute preservation, manifold safety, malformed selections, and failure-without-partial-destruction are tested for topology-changing paths before this candidate is called validated.
