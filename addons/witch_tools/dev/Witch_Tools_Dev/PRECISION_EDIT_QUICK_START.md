# Precision Edit Quick Start — Dev_v2.9.0

Target: Blender 4.5

## Coordinate Copy

Use this when you want selected mesh elements to adopt exact source coordinates instead of moving the target selection median.

1. Enter Edit Mode on the mesh object(s).
2. Open **Witch Tools > Edit Tools > Coordinate Copy**.
3. Choose `Global` when different objects need to line up in world space, or `Local` when you want the same object-local values.
4. Toggle X/Y/Z.
5. Toggle Location, Rotation, and/or Scale.
6. Select exactly one source vertex, edge, or face.
7. Press **Capture Source**. The source selection clears automatically.
8. Select the target geometry.
9. Press **Apply Copied Coordinates** or `Ctrl+Shift+C`.

Vertices are applied individually. Separate selected edge/face components are applied independently; the tool does not use one selection-wide median.

For mesh elements, Rotation and Scale refer to the geometry's own derived frame/extent rather than Blender Object transform channels.

## Planar Edit — Plane Lock

Use this when part of a mesh must remain fixed on one or more axis coordinates while you continue editing it.

1. Select the vertices, edges, or faces to protect.
2. Enable X, Y, and/or Z under **Plane Lock**.
3. Press **Lock Selected**.
4. Edit normally. Locked object-local coordinates are restored while the other axes remain editable.
5. Use **Unlock Selected** to remove the currently enabled lock axes from selected geometry.
6. Use **Clear All Plane Locks** to remove every Plane Lock on the participating Edit Mode meshes.

This is separate from full Vertex Locks. Existing Vertex Locks remain stronger protection.

## Planar Edit — Level

Use this to flatten or line up many target vertices to one exact source coordinate.

1. Select exactly one source vertex, edge, or face.
2. Press **1. Capture Source**. The source selection clears.
3. Toggle X/Y/Z.
4. Select target vertices, edges, or faces.
5. Press **2. Level Targets**.

Every target vertex independently receives the source world coordinate on the enabled axes. This works across differently transformed objects in multi-object Edit Mode.

## Inject New — Solo

1. Choose `Solo`.
2. Choose X, Y, Z, or Rail movement.
3. Choose Vertex, Edge, or Face.
4. If using Rail, select one endpoint vertex/edge/face and press **Capture Rail End**; the endpoint selection clears.
5. Select exactly one source matching the chosen element type.
6. Press **Inject New**.
7. Move the mouse along the constraint.
8. Left-click or Enter to place. Esc/right-click cancels.

Solo leaves the duplicate disconnected from the source.

## Inject New — Branch

Use the same steps as Solo, but choose `Branch`.

The duplicate is created plus source-to-copy branch edges for the source vertices. Branch does not automatically create side faces.

## Inject New — Slide

1. Choose `Slide`.
2. Select exactly one source edge.
3. Press **Inject New**.
4. Move the mouse along the selected edge.
5. Left-click or Enter to place. Esc/right-click cancels.

Slide inserts one new vertex into the selected edge and divides the original edge, similar to a one-cut subdivide that can be positioned interactively.

## Current candidate limits

- Inject New edits one active mesh at a time.
- Rail is a straight source-to-end segment.
- Slide is vertex-only.
- Multiple shape keys block topology-changing Inject New.
- Branch creates loose branch edges, not an extrusion shell.
- Blender 4.5 runtime validation is still required for Dev_v2.9.0 before release/integration claims.
