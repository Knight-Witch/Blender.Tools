# Witch Tools — 3D Print Tools + Transform Test Plan

Candidate: `Dev_v2.10.0`  
Target: Blender `4.5.0`

No Blender runtime validation was available in the implementation environment. Execute this plan before treating the candidate as production-working.

## 1. Registration / UI

- Install over the accepted `Witch_Tools_Dev` baseline.
- Enable the add-on in Blender 4.5.0.
- Confirm no traceback during register.
- Confirm top-level order: Mode Switcher, Transform, Auto Mirror, 3D Print Tools, Edit Tools.
- Expand/collapse every new parent/child panel.
- Narrow and widen the N-panel across approximately 300–500 px and verify compact toggle groups wrap rather than clip.
- Disable/re-enable the add-on and confirm clean unregister/re-register.

## 2. Transform — Object Mode

With a mesh object selected:

- edit X/Y/Z Location individually;
- edit Euler rotation values;
- change Rotation Mode and verify Quaternion / Axis Angle fields render appropriately;
- edit X/Y/Z Scale;
- undo and redo each change;
- save, close, reopen, and verify object transforms persist normally.

Repeat with a non-mesh object to confirm the Transform panel still behaves as normal object transforms.

## 3. Transform — Edit Mode Location

On a mesh with several non-collinear vertices:

- select one vertex; confirm shown Location equals that vertex's local coordinates;
- select multiple vertices; confirm shown Location equals selection median;
- change only X and verify every selected vertex moves by the same X delta;
- repeat Y and Z;
- confirm unselected vertices do not move;
- test vertex, edge, and face selection modes because edges/faces select participating vertices;
- undo/redo;
- test a mesh with unapplied object rotation/scale and confirm the field is explicitly local-space and behaves consistently.

Confirm Rotation and Scale fields in Edit Mode affect the object transform, not invented per-vertex values.

## 4. Analyze Mesh

Prepare meshes containing known cases:

- open boundary / non-manifold edge;
- flipped adjacent face creating bad-contiguous winding;
- self-intersecting faces;
- multiple disconnected shells;
- zero-area face;
- zero-length edge;
- distorted non-planar ngon;
- deliberately thin opposing surfaces below 1 mm;
- very sharp dihedral edge;
- downward-facing 45-degree-plus overhang.

For each:

- run Check All;
- compare counts with Blender's native diagnostics / known constructed geometry;
- verify analysis does not modify coordinates, topology, selection, materials, normals, or mode;
- run in Object Mode and Edit Mode;
- switch active object after analysis and confirm stale-results warning appears.

## 5. Make Manifold

Test independently on:

- duplicate vertices;
- zero-length edges / zero-area faces;
- loose verts/edges/faces;
- simple boundary holes;
- malformed boundary that cannot be safely filled;
- already-manifold mesh.

For every case verify:

- one undo restores the exact pre-operation mesh;
- redo restores the repaired result;
- mode is restored;
- face winding / normals point as expected;
- material slots and face material indices remain valid;
- seam/sharp/custom edge data is inspected for unintended loss;
- no new zero geometry is created;
- manifold state is checked after the repair;
- exceptions do not leave a partially continued repair sequence.

## 6. Auto Fix — Global

Test each option independently first, then common combinations:

- Tri Mesh;
- Quad Mesh;
- Face Normal;
- Noise Shells + threshold;
- Spikes + angle;
- Intersect Face + angle;
- Fill Holes;
- Intersect Volumes.

For Intersect Volumes specifically:

- use a duplicate test file;
- test two overlapping closed shells and two non-overlapping shells;
- inspect topology density and dimensions after the operation;
- verify it is clearly destructive/topology-rebuilding;
- verify undo/redo;
- check normals, materials, UVs, seam/sharp attributes, manifold state, and zero geometry.

## 7. Auto Fix — Local

In Edit Mode verify:

- Select More / Select Less;
- Face Orientation display toggle;
- Unify / Flip Normal;
- Refine;
- Remesh;
- Smooth;
- Reduce.

For Refine/Remesh/Reduce, inspect topology, normals, winding, materials, edge attributes, malformed selections, undo/redo, and failure behavior.

## 8. Advanced Clean — Repair

Test each setting alone and in combination:

- Loose: verts / edges / faces;
- Doubles + distance;
- Zero Faces + area;
- Dispensables + angle.

Verify whole-mesh Clean and Shift+Clean selection-only behavior.

## 9. Advanced Clean — Manifold

Test:

- Remove Non-Manifold Faces;
- Remove Non-Manifold Vertices;
- Remove Wire;
- Fill Holes + Max Sides.

Confirm Make Planar is absent.

Validate undo/redo, normals/winding, material/edge data, manifold outcome, malformed topology, and no partial destructive failure.

## 10. Advanced Clean — Topology

TRIS:

- all Quad Method options;
- both NGon Method options.

QUADS:

- Max Face Angle;
- Max Shape Angle;
- Compare Sharp / Seam / UV / Material / VCol individually and in combinations.

Verify responsive layout at multiple panel widths and verify compared data actually prevents inappropriate joining where expected.

## 11. Advanced Clean — Normals

Test:

- Recalculate Outside / Inside;
- Smooth by Angle + angle;
- Weighted Normals;
- Clear Data: Split Normals / Sharp Edges.

Test Blender 4.5 Smooth by Angle behavior specifically and inspect modifier/node-group handling if used.

## 12. Advanced Clean — Dissolve

Test:

- Max Angle;
- Boundaries;
- Protect Sharp / Seam / UV / Materials.

Verify protected delimiters survive and inspect manifold outcome, normals, materials, edge attributes, undo/redo, and malformed selections.

## 13. STL Export

- set an absolute folder;
- set a Blender-relative `//` folder;
- export one selected mesh;
- export multiple selected meshes;
- verify file names;
- re-import exported STL and compare dimensions/orientation;
- verify no hidden format/options UI is required;
- verify export failure reports an error without changing scene data.

## 14. Regression

Confirm retained Dev_v2.9.0 functionality still registers and its panels remain available, especially:

- Mode Switcher;
- Auto Mirror;
- Coordinate Copy;
- Planar Edit;
- Vertex Snap;
- Inject New;
- Object Snap;
- Edge / Vertex Inject;
- Curvature Sync;
- Align Vertices / Edges / Faces;
- Selection Slots;
- Vertex Locks.

## Exit criteria

The candidate is accepted only after Blender 4.5 registration/UI passes and topology-changing paths have completed the required undo/redo, mode, normals/winding, material/edge-attribute, manifold, protected-zone where applicable, malformed-selection, and failure-without-partial-destruction checks.
