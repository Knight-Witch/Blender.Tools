# Witch Tools — 3D Print Tools + Transform Test Plan

Candidate: Dev_v2.11.4  
Primary runtime target: Blender 5.0.1  
Secondary compatibility target: Blender 4.5.0

## 1. Package / registration

Run in Blender 5.0.1 first:
1. Install the full ZIP over the existing `Witch_Tools_Dev` package.
2. Enable Witch Tools.
3. Confirm no traceback during registration.
4. Disable/re-enable once; confirm clean unregister/register.
5. Confirm existing Dev_v2.10.1 Magic Branch, Edge Doctor, Inject New, Object Snap, and Edit Tools ordering still exist.
6. Confirm the official 3D Print Toolbox extension is installed and enabled for Analyze testing.

Repeat shared registration smoke test in Blender 4.5 before claiming secondary compatibility.

## 2. Top-level UI order

Confirm default order begins:
1. Mode Switcher
2. Transform
3. Auto Mirror
4. 3D Print Tools
5. Edit Tools

Expand every new nested panel at narrow and wide N-panel widths. Confirm no clipped controls, invalid icon errors, or blank-panel failures.

## 3. Transform — Object Mode

On a mesh object:
- edit X/Y/Z Location and confirm exact values;
- edit Rotation in Euler mode;
- switch Rotation Mode and confirm UI remains valid;
- edit Scale;
- Undo/Redo each change.

## 4. Transform — Mesh Edit Mode

Single vertex:
- select one vertex;
- confirm Location equals its object-local coordinate;
- edit X only and verify only X changes.

Multiple vertices:
- select a non-symmetric group;
- record pairwise distances;
- edit Location X/Y/Z;
- verify the group translates rigidly and pairwise distances remain unchanged;
- Undo/Redo.

## 5. Analyze Mesh — immediate Dev_v2.11.4 exact-backend gate

Use the same unchanged `_CAP 3` object from the runtime screenshots.

Known original Toolbox reference on this object:
- Non-manifold Edges: 0
- Bad Contiguous Edges: 0
- Intersect Faces: 0
- Shells: 1
- Zero Faces: 0
- Zero Edges: 0
- Non-flat Faces: 98
- Thin Faces: 0
- Sharp Edges: 0
- Overhang Faces: 79

Dev_v2.11.3 incorrectly returned Non-flat 73 and Overhang 80.

### Exact count test

1. In the original 3D Print Toolbox tab, press `Check All`.
2. Record/screenshot all ten displayed values.
3. Without changing the object, mode, transforms, geometry, or Toolbox settings, press Witch Tools `Check All`.
4. Compare every value.

Pass condition: all ten displayed values are identical. Dev_v2.11.4 invokes the original `mesh.print3d_check_all`, so any mismatch after this change is a report-resolution/mapping bug and must be fixed without reintroducing local detector logic.

### Click-to-select parity

Test in Edit Mode with a non-empty report such as Non-flat Faces and Overhang Faces:
1. Run original Toolbox Check All.
2. Click its result button and observe/record the selected face indices or a stable visual selection.
3. Rerun Check All if selection changes invalidate the report.
4. Click the equivalent Witch Tools result button.
5. Confirm the exact same element type, mesh selection mode, and element set are selected.
6. Repeat for at least one edge diagnostic when a fixture provides a non-zero edge result.

Pass condition: Witch Tools selection is produced by the original `mesh.print3d_select_report` and is identical to the original Toolbox result button.

### Backend dependency failure

Temporarily disable the 3D Print Toolbox extension only if safe:
- Witch Tools Analyze must return a clear error.
- Witch Tools must not manufacture a different set of Analyze counts.
- Re-enable the Toolbox afterward.

### Broader parity fixtures

After `_CAP 3`, repeat exact count/selection comparison on:
- clean watertight mesh;
- known non-manifold mesh;
- degenerate mesh;
- intersecting mesh;
- thin-wall fixture;
- sharp-edge fixture;
- rotated/non-uniformly-scaled print mesh.

## 6. Make Manifold

Run on duplicate test files only.

Test boundary holes, duplicate/coincident vertices, loose geometry, degenerate geometry, and an already-manifold mesh. Verify topology, normals/winding, materials/edge attributes where applicable, Undo/Redo, mode restoration, and failure without partial mutation.

## 7. Auto Fix — Global Fix

Individually test Tri Mesh, Quad Mesh, Face Normal, Noise Shells, Spikes, Intersect Face, Intersect Volumes, Fill Holes, then representative combinations.

Verify no unintended zero geometry, expected manifold state, normals/winding, materials/custom edge data, Undo/Redo, and safe failure on malformed input. Treat Intersect Volumes as destructive/rebuilding until proven otherwise.

## 8. Auto Fix — Local Fix

In Edit Mode test Select More/Less, Face Orientation, Unify/Flip, Refine, Remesh, Smooth, Reduce. Verify selection scope and unrelated-island safety.

## 9. Advanced Clean

UI:
- one main Clean button;
- separate Repair / Manifold / Topology / Normals / Dissolve child sections;
- each section header has enable toggle + play action;
- Object Data and Make Planar absent;
- Dissolve last;
- requested compact Manifold/Topology/Normals controls present.

Behavior:
- main Clean runs only enabled sections;
- each section play button runs only that section even when its enable toggle is off;
- Shift applies selection-only behavior to both paths.

For topology-changing actions test Undo/Redo, Object/Edit restoration, normals/winding, materials, Seam/Sharp/UV/custom edge data where applicable, manifold safety, multi-object behavior where supported, malformed selections, and failure without partial destructive changes.

## 10. STL export

Dev_v2.11.3 user testing confirmed that the export hotfix creates an STL in Blender 5.0.1. Retest in Dev_v2.11.4 for regression, then complete the remaining matrix.

### Basic one-object export
- Select one normal mesh.
- Choose writable folder.
- Export and confirm physical `.stl` output.
- Re-import into a clean scene and compare dimensions/orientation.

### Multiple selected meshes
- Export two separated meshes as one STL.
- Confirm both components and world relationship after re-import.

### Evaluated modifiers
- Export an object with unapplied geometry-changing modifier.
- Confirm re-import reflects evaluated modifier geometry.

### Object transforms / negative scale
- Test translation, rotation, non-uniform scale, and a negative/mirrored scale fixture.
- Inspect re-imported dimensions/orientation/winding.

### Edit Mode
- Make an Edit Mode geometry change and export.
- Confirm current edited geometry is present.

### Overwrite / failure handling
- Export same filename twice; confirm complete replacement and no `.wt_tmp` residue.
- Test a safe failure path where possible.
- Test empty/no-triangle mesh failure.
- Verify failed fallback cannot replace destination with partial data.

### Native vs fallback
- Record whether Blender native export or Witch Tools fallback handled the normal case if diagnostics expose it.
- If fallback cannot be forced safely, retain it as runtime-untested rather than claiming it works.

## 11. Regression — Dev_v2.10.1 baseline

Smoke test Magic Branch activation/selection-mode sync, Inject New Edge Solo/Branch/Slide, one magnetic merge case, Edge Doctor, Object Snap Undo, and Edit Tools reorder controls.

## 12. Blender 4.5 secondary compatibility

After Blender 5.0.1 primary validation, test at minimum:
- register/unregister;
- basic Transform;
- confirm the 4.5-installed 3D Print Toolbox exposes the expected Check All/report/select operator pipeline or record incompatibility;
- one safe Advanced Clean Repair action;
- one-object STL export/re-import;
- BG3 workflows still expected in 4.5;
- Magic Branch/Inject/Edge Doctor if expected there.

Do not claim 4.5 compatibility for paths not actually tested there.

## Acceptance

Dev_v2.11.4 is accepted only after:
- exact Toolbox-backed Analyze count parity is observed in Blender 5.0.1;
- click-to-select parity is observed in Edit Mode;
- unavailable-Toolbox behavior fails explicitly;
- STL export regression remains successful and re-import checks are completed as required;
- remaining Transform/Clean & Repair/baseline regression tests are recorded;
- relevant Blender 4.5 secondary checks are separately recorded.

Static/package validation alone is not runtime validation.
