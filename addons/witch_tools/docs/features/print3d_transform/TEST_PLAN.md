# Witch Tools — 3D Print Tools + Transform Test Plan

Candidate: Dev_v2.11.2  
Primary runtime target: Blender 5.0.1  
Secondary compatibility target: Blender 4.5.0

## 1. Package / registration

Run in Blender 5.0.1 first:
1. Install the full ZIP over the existing `Witch_Tools_Dev` package.
2. Enable Witch Tools.
3. Confirm no traceback during registration.
4. Disable/re-enable once; confirm clean unregister/register.
5. Confirm existing Dev_v2.10.1 Magic Branch, Edge Doctor, Inject New, Object Snap, and Edit Tools ordering still exist.

Pass: no registration errors and no current-baseline tools disappear.

Repeat the shared registration smoke test in Blender 4.5 before claiming secondary compatibility.

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

Confirm Rotation/Scale are clearly object transforms, not fabricated per-vertex values.

## 5. Analyze Mesh parity — immediate Dev_v2.11.2 gate

Use the same `_CAP 3` object from the Blender 5.0.1 parity-failure screenshots, without changing transforms or geometry.

Original 3D Print Toolbox reference from the user:
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

Dev_v2.11.1 Witch Tools incorrectly returned:
- Non-flat Faces: 73
- Thin Faces: 1
- Sharp Edges: 1
- Overhang Faces: 80

Dev_v2.11.2 passes this first gate only if all ten counts exactly match the original Toolbox reference above.

The integrated backend intentionally uses the Toolbox default thresholds while hiding their UI:
- Degenerate: 0.1 mm
- Non-Planar: 5 degrees
- Thickness: 1 mm
- Sharp: 160 degrees
- Overhang: 45 degrees

After the `_CAP 3` count test, compare at least:
- a known clean watertight print mesh;
- a mesh with known non-manifold boundaries;
- a mesh with zero/degenerate geometry;
- a mesh with known intersecting faces;
- a thin-wall mesh near the 1 mm threshold;
- a mesh containing convex and concave very-sharp manifold edges;
- a rotated/non-uniformly-scaled curved print mesh to verify world-transform handling.

For every mesh, record both count sets. Any mismatch is a failure to investigate.

Once counts match, use the original Toolbox's result-selection buttons to inspect the actual offending elements. Count parity alone does not establish detector identity. Compare at minimum Non-flat, Thin, Sharp, Overhang, Intersections and degenerate results where nonzero.

Click-to-select inside Witch Tools remains gated on this detector identity validation.

## 6. Make Manifold

Run on duplicate test files only.

Test:
- boundary hole;
- duplicate/coincident vertices;
- loose edge/vertex;
- degenerate edge/face;
- already-manifold mesh.

For each:
- inspect resulting topology;
- check normals/winding;
- verify material assignments where faces survive;
- verify edge attributes where applicable;
- run Undo and Redo;
- ensure mode is restored predictably;
- ensure failure does not leave a partially modified mesh.

## 7. Auto Fix — Global Fix

Individually test Tri Mesh, Quad Mesh, Face Normal, Noise Shells, Spikes, Intersect Face, Intersect Volumes, Fill Holes, then representative combinations.

For topology-changing cases verify:
- no zero-length edges;
- no zero-area faces;
- expected manifold state;
- normals/winding;
- materials;
- seams/sharp/other custom edge data where preservation is expected;
- Undo/Redo;
- malformed/unsupported geometry fails safely.

Intersect Volumes must be treated as destructive/rebuilding until proven otherwise. Compare before/after vertex/edge/face counts and inspect attribute loss explicitly.

## 8. Auto Fix — Local Fix

In Edit Mode test:
- Select More / Less;
- Face Orientation display;
- Unify/Flip;
- Refine;
- Remesh;
- Smooth;
- Reduce.

Verify operations respect the intended selection scope and do not unexpectedly modify unrelated mesh islands.

## 9. Advanced Clean — UI and execution model

First test the layout before destructive behavior:
- Advanced Clean has one main Clean button at the top.
- Repair, Manifold, Topology, Normals, Dissolve are separate collapsible child sections in that order.
- Each child header shows a section-name enable toggle and a play button.
- Object Data is absent.
- Make Planar is absent.
- Dissolve is last.
- Repair visually retains the original-style Remove group and checkbox/numeric-row structure.
- Manifold shows Fill Holes plus compact `Remove Non-Manifold: [Faces] [Vertices] [Wire]`.
- Topology retains Convert To and Methods, with responsive angle/Compare layout when converting to quads.
- Normals retains original-style main controls with compact Clear Data toggles.
- Dissolve retains the original-style Max Angle / Boundaries / Protect body.

Execution behavior:
1. Disable all section toggles except Repair. Click main Clean. Confirm only Repair runs.
2. Repeat with only Manifold, Topology, Normals, then Dissolve enabled.
3. Enable a representative combination and confirm main Clean runs exactly those enabled sections.
4. Disable a section toggle, then press that section's play button. Confirm the individual play action still runs only that section and does not invoke the other enabled sections.
5. Press each section play button and confirm only that section executes.
6. Hold Shift with main Clean and each individual play button; confirm selection-only behavior applies.

Then run topology-safety tests with each section individually and representative combinations:
- Undo/Redo;
- Object/Edit Mode restoration;
- normals/winding;
- material assignments;
- Seam/Sharp/UV/custom edge data where preservation is expected;
- manifold safety where applicable;
- multi-object behavior where supported;
- malformed/ambiguous selections;
- failure without partial destructive changes.

## 10. STL export

- choose a folder;
- export one selected mesh;
- export multiple selected meshes;
- confirm `.stl` output name/path;
- re-import into a clean Blender scene;
- compare dimensions and orientation;
- verify no unexpected non-mesh objects are exported.

## 11. Regression — Dev_v2.10.1 baseline

Smoke test:
- Magic Branch activation and Branch Type selection-mode sync;
- Inject New Edge Solo/Branch and Slide;
- magnetic target highlighting/merge on one known case;
- Edge Doctor parent and nested tools;
- Object Snap Undo;
- Edit Tools reorder controls.

This feature must not be accepted if integrating 3D Print/Transform regresses the newer baseline.

## 12. Blender 4.5 secondary compatibility

After the Blender 5.0.1 primary pass, test in Blender 4.5 at minimum:
- register/unregister;
- Transform panel rendering and basic Object/Edit coordinate edit;
- Analyze `_CAP 3` or an equivalent saved parity fixture;
- Advanced Clean headers and one safe Repair action;
- the BG3-specific workflows the user still performs in 4.5;
- Magic Branch/Inject/Edge Doctor smoke tests if those workflows are expected in 4.5.

Do not claim 4.5 compatibility for paths not actually tested there.

## Acceptance

Dev_v2.11.2 is accepted only after the primary Blender 5.0.1 checks are recorded, Analyze count/offending-element parity is established, and the relevant Blender 4.5 secondary checks are separately recorded. Static AST/package validation alone is not runtime validation.
