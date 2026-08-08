# Precision Edit — Blender 4.5 Test Plan

Candidate: `Witch Tools Dev_v2.10.0`  
Target: Blender `4.5.0`

No item in this plan is considered passed until executed in Blender and recorded with the exact Blender version/build.

## A. Registration and UI

1. Install/enable the add-on in Blender 4.5.
2. Confirm no registration traceback.
3. Open View3D Sidebar > Witch Tools > Edit Tools.
4. Confirm default order: Coordinate Copy, Planar Edit, Vertex Snap, Object Snap, Inject New, Magic Branch, Edge Doctor, Vertex Lock, Selection Slots; confirm custom reorder persistence.
5. Expand/collapse each new section repeatedly.
6. Hover section headers and individual properties/operators; verify useful tooltips.
7. Confirm Vertex/Edge/Face icons render in Inject New.
8. Confirm `Ctrl+Shift+C` appears for Coordinate Copy Apply and invokes it in Mesh Edit Mode.
9. Disable/re-enable the add-on and confirm registration/unregistration completes cleanly.

## B. Coordinate Copy — Location

### Same object

1. Create a mesh with several vertices at different X/Y/Z values.
2. Vertex mode: capture one source vertex.
3. Enable Global + Location + Z only.
4. Select multiple target vertices and Apply.
5. Measure each target: every target world Z must equal source world Z exactly; target X/Y must remain unchanged.
6. Undo and redo; verify exact restoration/reapplication.

### Multiple objects / different origins

1. Create two mesh objects with different object origins, translations, rotations, and non-zero local vertex coordinates.
2. Enter multi-object Edit Mode.
3. Capture source on object A using Global.
4. Select targets on A and B, apply one axis and then XYZ.
5. Verify enabled world coordinates match exactly despite different origins/transforms.
6. Repeat in Local; verify matching local numeric coordinates rather than world coordinates.

### Failure behavior

- Change Global/Local after capture: Apply must cancel and request recapture.
- Disable all axes: cancel without mutation.
- Disable Location/Rotation/Scale all together: cancel without mutation.
- Capture zero or multiple source elements: cancel without mutation.
- Apply with no targets: cancel without mutation.

## C. Coordinate Copy — Edge/Face Rotation and Scale

For each of Edge and Face mode:

1. Build source and target elements with visibly different orientation/size.
2. Capture source.
3. Test Rotation only on X, Y, Z individually and XYZ together.
4. Test Scale only on X, Y, Z individually and XYZ together.
5. Test Location + Rotation + Scale together.
6. Confirm disabled components remain unchanged within numerical tolerance.
7. Select two disconnected target components at once; verify each component transforms around its own center rather than around a combined selection median.
8. Test a mirrored/non-uniformly transformed object and record any frame ambiguity or Euler flip.

## D. Plane Lock

1. Build a simple quad/grid.
2. Lock selected vertices on Z.
3. Use G, proportional editing off, and move freely in screen space; verify Z restores exactly while X/Y can change.
4. Repeat for X only, Y only, XY, XZ, YZ, XYZ.
5. Lock using edge selection and face selection; verify participating vertices are protected.
6. Add an axis to an existing partial lock; verify prior locked axis remains.
7. Unlock only one enabled axis; verify other lock axes remain.
8. Clear All Plane Locks; verify normal editing resumes.
9. Deselect/reselect geometry; verify locks remain.
10. Save, close, reopen; verify custom-layer locks persist.
11. Undo/redo lock creation and clearing.
12. Combine Plane Lock with existing Vertex Locks and verify full Vertex Lock still prevents incompatible precision operations.

## E. Level

1. Capture source vertex; select many target vertices at different coordinates.
2. Test X, Y, Z individually and combinations.
3. Confirm each target receives exact source world coordinates on enabled axes, not a translated median.
4. Repeat with source edge and face; source point must be edge midpoint/face median center.
5. Repeat across two mesh objects with different origins/transforms.
6. Test a target protected by Plane Lock on a requested Level axis: entire operation must cancel before any target changes.
7. Test a target protected by Vertex Locks: entire operation must cancel before mutation.
8. Undo/redo.

## F. Inject New — Solo

For Vertex, Edge, Face:

1. Select exactly one source of the chosen type.
2. Test X/Y/Z singly, in pairs, and XYZ together; also test Rail.
3. Move mouse, commit with left-click; verify duplicate is disconnected and selected.
4. Repeat commit with Enter.
5. Repeat and cancel with Esc and right-click; topology/counts must match pre-operation state.
6. Test Rail: capture vertex endpoint, edge midpoint, and face-center endpoint. Verify movement is clamped to the straight source-to-end segment.
7. Undo/redo each committed case.
8. Check normals/winding/material assignment/custom edge attributes on duplicated Edge/Face geometry.

## G. Inject New — Branch

For Vertex, Edge, Face:

1. Repeat single/pair/triple X/Y/Z and Rail placement; exercise Magnetic Snap and Auto-Merge.
2. Confirm the source geometry remains.
3. Confirm corresponding source vertices have branch edges to their duplicate vertices.
4. Confirm no unintended side faces are created.
5. Cancel and verify source topology and counts exactly restore.
6. Undo/redo committed result.
7. Verify special source edge attributes remain on duplicated source edges and are not silently transferred to newly created branch edges unless Blender's normal BMesh behavior explicitly does so.

Branch intentionally creates loose/non-manifold branch geometry; therefore global manifoldness is not an acceptance condition for this mode.

## H. Inject New — Slide

1. Select one edge, then multiple parallel edges, on a manifold quad/grid and choose Slide.
2. Move mouse from one end to the other; verify the inserted vertex remains on the original edge segment.
3. Commit and confirm the original edge is divided into two edges with no stale overlapping original edge.
4. Verify face winding and normals remain correct.
5. Verify no zero-length edges, zero-area faces, duplicate edges, or unexpected non-manifold changes.
6. Verify material assignment and relevant edge custom attributes survive the split as Blender/BMesh supports them.
7. Cancel at several positions; verify exact topology/count restoration.
8. Undo/redo committed split.
9. Test boundary edge, interior manifold edge, loose edge, and an edge carrying Seam/Sharp/Crease/bevel/custom attributes; record preservation behavior.
10. Test malformed selection: zero edges and face-only selection must fail without partial topology; two or more selected edges are valid multi-edge Slide input.

## I. Protection / topology-change interactions

1. Run Solo/Branch/Slide near existing Vertex Lock groups and Protected Edit Zones.
2. Verify locked old vertices do not drift while the modal operator runs.
3. Verify lock group references remain valid after commit, cancel, undo, and redo.
4. Create Plane Locks before Inject New; verify newly injected vertices are not accidentally frozen by inherited custom-layer data.
5. Re-run Plane Lock after injection and verify it can lock the new vertices normally.

## J. Stress and failure rollback

- Repeatedly invoke/cancel Inject New 20 times and check topology counts for drift.
- Invoke Inject New with source/rail nearly camera-aligned; it should reject cleanly rather than jump unpredictably.
- Test objects with negative scale, non-uniform scale, and rotated transforms.
- Test mesh with multiple shape keys: topology-changing Inject New must reject before mutation.
- Test malformed/degenerate source geometry where practical.

## K. Print/topology sanity for Slide

On a known manifold printable test mesh:

- non-manifold edges before/after;
- zero-length edges before/after;
- zero-area faces before/after;
- face normal orientation;
- duplicate vertices/edges/faces where detectable;
- local geometry dimensions before/after except the intended subdivision.

The Slide operation must not degrade print-readiness in the tested local case.

## Result recording

For every failure record:

- exact Blender version/build;
- operating system;
- active mode/selection mode;
- object transform state;
- tool settings/toggles;
- source and target element type/count;
- before/after coordinates and topology counts;
- traceback/report text;
- whether Undo restored the original state.

## Dev_v2.10.0 magnetic / Magic Branch extension

Execute `/docs/features/magic_branch/TEST_PLAN.md` in full for Magnetic Snap, Auto-Merge, MMB orbit, multi-edge Slide, Magic Branch, Edge Doctor L repair, topology attributes, cancellation, Persistent Undo, and reorder UI validation.
