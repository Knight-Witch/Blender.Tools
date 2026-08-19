# Witch Tools — 3D Print Tools + Transform Test Plan

Candidate: Dev_v2.11.3  
Primary runtime target: Blender 5.0.1  
Secondary compatibility target: Blender 4.5.0

## 1. Package / registration

Run in Blender 5.0.1 first:
1. Install the full ZIP over the existing `Witch_Tools_Dev` package.
2. Enable Witch Tools.
3. Confirm no traceback during registration.
4. Disable/re-enable once; confirm clean unregister/register.
5. Confirm existing Dev_v2.10.1 Magic Branch, Edge Doctor, Inject New, Object Snap, and Edit Tools ordering still exist.

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

## 5. Analyze Mesh parity

Use the same `_CAP 3` object from the Blender 5.0.1 parity-failure screenshots, without changing transforms or geometry.

Original Toolbox reference:
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

Dev_v2.11.3 retains the Dev_v2.11.2 parity correction and passes this first gate only if all ten counts match.

Then compare a clean watertight mesh, known non-manifold mesh, degenerate mesh, intersecting mesh, thin-wall threshold fixture, sharp convex/concave fixture, and rotated/non-uniformly-scaled curved print mesh.

Once counts match, compare actual offending-element identity using the original Toolbox selection buttons. Click-to-select inside Witch Tools remains gated on this validation.

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

## 10. STL export — immediate Dev_v2.11.3 gate

The prior runtime issue was that choosing a folder and pressing Export STL produced no expected output. Dev_v2.11.3 must prove both success and failure paths.

### Basic one-object export

1. Select one normal mesh object with faces.
2. Choose an existing writable folder.
3. Press `Export STL`.
4. Confirm a `.stl` physically appears in that exact folder using the object's cleaned name.
5. Confirm Blender/Witch Tools reports success only after the file exists.
6. Confirm file size is greater than the 84-byte binary STL header/count minimum for a non-empty mesh.
7. Re-import into a clean scene and compare dimensions, orientation, and position/geometry expectations.

### Multiple selected meshes

- Select two separated mesh objects and export.
- Confirm one combined STL named from the active object with `_selection` suffix.
- Re-import and verify both components are present in their correct world relationship.

### Evaluated modifiers

- Use a mesh with a visible unapplied modifier that changes geometry.
- Export without applying the modifier manually.
- Re-import and confirm the exported STL reflects evaluated modifier geometry.

### Object transforms and negative scale

- Test translation, rotation, and non-uniform scale.
- Test one negative/mirrored scale fixture.
- Re-import and inspect dimensions, orientation, triangle winding/surface orientation, and obvious inversion artifacts.

### Edit Mode

- With an edited mesh in Edit Mode, make an unsaved-in-mode geometry change and export.
- Confirm the exported geometry reflects current Edit Mode data.

### Overwrite and failure handling

- Export to the same expected filename twice and confirm the second complete export replaces/updates the file without leaving a `.wt_tmp` file.
- Use an unwritable/invalid destination if safe to reproduce and confirm a visible error is reported.
- Invoke with no selected mesh through any reachable path and confirm it refuses safely.
- Test an empty mesh/no exportable triangles and confirm it fails rather than accepting an empty STL.
- After any fallback failure, confirm the temporary `.wt_tmp` file is removed and an existing destination is not replaced by a partial fallback file.

### Native vs fallback path

- Normal test should establish whether Blender's native exporter succeeds in Blender 5.0.1.
- If a controlled development setup can make the native/legacy operator unavailable or return cancellation without risking the user's work, explicitly test the direct Witch Tools fallback and re-import its output.
- If the fallback cannot be forced safely, record it as source/static validated but runtime-untested rather than claiming it works.

## 11. Regression — Dev_v2.10.1 baseline

Smoke test Magic Branch activation/selection-mode sync, Inject New Edge Solo/Branch/Slide, one magnetic merge case, Edge Doctor, Object Snap Undo, and Edit Tools reorder controls.

## 12. Blender 4.5 secondary compatibility

After Blender 5.0.1 primary validation, test at minimum:
- register/unregister;
- basic Transform;
- Analyze parity fixture/equivalent;
- one safe Advanced Clean Repair action;
- one-object STL export/re-import;
- BG3 workflows still expected in 4.5;
- Magic Branch/Inject/Edge Doctor if expected there.

Do not claim 4.5 compatibility for paths not actually tested there.

## Acceptance

Dev_v2.11.3 is accepted only after the primary Blender 5.0.1 checks are recorded, Analyze parity is established, STL export creates and re-imports valid files, and relevant Blender 4.5 secondary checks are separately recorded. Static/package validation alone is not runtime validation.
