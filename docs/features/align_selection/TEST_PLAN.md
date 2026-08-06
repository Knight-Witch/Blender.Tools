# Align Vertices / Edges / Faces Test Plan

Target runtime: Blender `4.5.0`.

## Static and package tests

- Parse and compile every Python file.
- Scan operator and panel identifiers for duplicates.
- Confirm exactly seven `mesh.wt_guided_align_*` operators.
- Confirm every panel UI-state property is declared in preferences.
- Run pure component, custom-frame, and rail-constraint math tests.
- Reconstruct the verified source baseline and apply the recorded patch.
- Verify resulting source-tree identity.
- Verify ZIP integrity and safe relative paths.
- Confirm one package root.
- Confirm no `__pycache__`, `.pyc`, `.pyo`, temporary, editor, or unrelated files ship.

Current result: passed outside Blender.

## Registration and UI test

1. Install `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip` over the current development install.
2. Enable the add-on in Blender 4.5.
3. Open View3D Sidebar > Witch Tools > Edit Tools.
4. Confirm **Align Vertices / Edges / Faces** appears between Curvature Sync and Selection Slots.
5. Expand and collapse it.
6. Confirm all four numbered steps render.
7. Switch World/Custom, Free/Rails, One-to-All/Paired, Preserve Shape, and grouping options; confirm dependent controls appear without draw errors.
8. Restart Blender and confirm disclosure preference persistence.
9. Disable and re-enable the add-on; confirm registration/unregistration is clean.

## Test A — world-axis free coordinate matching

Use geometry equivalent to screenshots 1–3.

1. Capture the red parent vertex.
2. Choose World XYZ.
3. Enable only Z.
4. Choose Free Coordinates.
5. Select the yellow subordinate vertices.
6. Analyze and record the report.
7. Align.
8. Verify every target world Z equals parent world Z.
9. Verify every target world X and Y are unchanged.
10. Verify topology counts and all non-coordinate mesh data are unchanged.
11. Undo once; verify exact original coordinates.
12. Redo once; verify aligned coordinates.

Repeat with parent edge, parent face, mixed parent selection, Active Element, Median, X only, Y only, and multi-axis masks.

## Test B — slide along captured straight rails

1. Restore the original geometry.
2. Capture the parent.
3. Choose Captured Rails.
4. Capture the vertical existing edges as rails.
5. Enable only Z.
6. Select subordinate endpoints.
7. Analyze and Align.
8. Verify targets moved only along the rail direction.
9. Verify each target remains on its original edge line.
10. With clamp enabled, request a target beyond a rail endpoint and verify the operation cancels without movement.
11. Disable clamp and document extension behavior.

## Test C — paired parent/child rails

Use geometry equivalent to screenshot 4.

1. Capture multiple red parent vertices.
2. Choose Paired by Rail.
3. Capture disconnected blue rail components, each containing one parent.
4. Select green subordinate endpoints/islands.
5. Enable Z or the required component.
6. Analyze and Align.
7. Verify every subordinate matched its own rail's parent, not the global median.
8. Verify rail components do not cross-map.
9. Add a second parent to one rail; verify complete cancellation.
10. Make one target island touch two rails; verify complete cancellation.
11. Remove a parent from one rail; verify complete cancellation.

## Test D — custom 45-degree guide

1. Set Guide Start and Guide End to a 45-degree world XY line.
2. Verify numeric editing.
3. Capture Start and End from vertex, edge, and face selections.
4. Test Copy Anchor to Guide Start.
5. Choose Match Anchor in Guide Frame and test custom X, Y, Z, and combinations.
6. Choose Project to Guide Line.
7. Verify resulting points lie on the line within tolerance.
8. Verify their custom X coordinate is unchanged during projection.
9. Set identical start/end points; verify cancellation without movement.

## Test E — preserve relative spacing/shape

1. Select a connected target shape.
2. Record all pairwise or edge-length distances.
3. Enable Preserve Relative Spacing / Shape.
4. Align in free mode.
5. Verify every target received one identical translation and all relative distances are unchanged.
6. Repeat with Per Selected Island and two disconnected shapes.
7. Repeat with rails when one common rail-compatible translation exists.
8. Construct an impossible rigid rail constraint and verify cancellation without deformation.

## Test F — multi-object Edit Mode

1. Use at least two mesh objects with different location, rotation, and non-uniform scale where supported.
2. Capture the parent on one object and subordinates on another.
3. Verify visible world alignment and correct local-coordinate reconstruction.
4. Test multiple target objects.
5. Construct a non-invertible transform and verify cancellation.
6. Test linked objects sharing one Mesh datablock and record the marker-sharing limitation.

## Capture and persistence tests

- Recapture replaces previous parent markers.
- Recapture replaces previous rail markers.
- Clear removes parent and rail markers and guide-set flags.
- Save and reopen valid captures.
- Delete/subdivide/duplicate captured topology; verify count mismatch requires recapture.
- Confirm capture clears the current selection as designed.
- Confirm parent vertices are excluded if reselected as subordinates.

## Safety tests

- Vertex Lock on any target cancels the complete operation when Respect Vertex Locks is enabled.
- Explicit lock bypass, if exposed, is documented and tested.
- Multiple shape keys cancel.
- Missing parent, missing rail, no subordinate selection, no enabled component, curved rail, zero rail, impossible multi-axis solution, out-of-range clamped solution, ambiguous rail, and malformed paired mapping all cancel without coordinate change.
- Force an unexpected Apply exception where safely possible and verify rollback restores original local coordinates.

## Topology and data preservation

For every successful case verify:

- vertex, edge, face, and loop counts unchanged;
- no zero-length edges or zero-area faces introduced;
- normals and face winding unchanged except normal recalculation inherent to moved geometry;
- material indices unchanged;
- UVs unchanged;
- seam, sharp, crease, bevel, and custom attributes unchanged;
- manifold state unchanged;
- unrelated objects unchanged.

## Witch Dock/Quickbar test — deferred

Do not begin until Witch Tools passes. The later wrapper must then test:

- backend-unavailable state;
- operator/property parity;
- drag, resize, lock, minimize/maximize, launcher, section reorder, persistence, and pass-through;
- UI-only actions do not pollute undo;
- Align produces one undo step;
- existing Select/Edit tools remain functional.

## Acceptance record

Record exact Blender version, OS, add-on version, artifact SHA-256, test mesh, screenshots, before/after coordinates, topology/data checks, undo/redo, save/reopen, passes, failures, and known limitations.
