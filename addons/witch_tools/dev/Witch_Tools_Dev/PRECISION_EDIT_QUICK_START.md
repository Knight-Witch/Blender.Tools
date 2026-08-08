# Precision Edit Quick Start — Dev_v2.10.0

Target: Blender 4.5

## Coordinate Copy

1. Enter Edit Mode on the mesh object(s).
2. Open **Witch Tools > Edit Tools > Coordinate Copy**.
3. Choose Global or Local.
4. Toggle X/Y/Z and Location/Rotation/Scale.
5. Select exactly one source vertex, edge, or face and press **Capture Source**.
6. Select targets.
7. Press **Apply Copied Coordinates** or `Ctrl+Shift+C`.

Vertices apply independently. Disconnected selected edge/face components apply independently. No selection-wide target median is used.

## Planar Edit — Plane Lock

1. Select geometry to constrain.
2. Toggle X/Y/Z under Plane Lock.
3. Press **Lock Selected**.
4. Edit normally; locked object-local coordinates are restored while unlocked axes remain editable.
5. Use **Unlock Selected** for enabled axes or **Clear All Plane Locks**.

## Planar Edit — Level

1. Select one source vertex/edge/face and press **Capture Source**.
2. Toggle X/Y/Z.
3. Select targets.
4. Press **Level Targets**.

Every target vertex independently receives the source world coordinate on enabled axes.

## Inject New — Solo / Branch

1. Choose Solo or Branch.
2. Under Movement, enable one or more X/Y/Z axes. X+Y+Z is free placement. Alternatively enable **Use Captured Rail** and capture a vertex/edge/face endpoint.
3. Toggle **Magnetic Snap** if you want hover targets to guide placement.
4. Branch only: toggle **Auto-Merge** if supported snapped contacts should become shared topology on commit.
5. Choose Vertex, Edge, or Face.
6. Select exactly one source of that type.
7. Press **Inject New** and move the mouse.
8. Hover a vertex, edge, or face to see the magnetic target highlight.
9. Left-click or Enter to commit. Esc/right-click cancels.

Magnetic behavior:

- vertex: nearest compatible new endpoint lands exactly on it;
- edge: nearest compatible new endpoint lands on the edge while the rest stays rigid;
- face: each new endpoint follows its own travel line to the face/boundary.

During placement, hold MMB to pause placement and orbit around the current live injection. Release MMB to resume.

Solo stays disconnected. Branch creates source-to-copy branch edges. Auto-Merge can weld supported Branch contacts but does not invent arbitrary face-interior retopology.

## Inject New — Multi-edge Slide

1. Choose Slide.
2. Select one or more source edges.
3. Press **Inject New**.
4. Move the mouse near any selected edge. The closest selected rail becomes the driver.
5. Every inserted vertex moves to the same relative factor on its own selected edge.
6. Left-click/Enter commits; Esc/right-click cancels.

Slide injects one vertex per preselected edge. Dev_v2.10.0 does not automatically add completely unselected fan edges just because the cursor passes over them.

## Edit Tools ordering

Press **Reorder Tools** at the top of Edit Tools. Drag a grip to move a section or use the up/down arrows. The order is stored in Witch Tools preferences and can be reset to default.

## Current candidate limits

- topology-changing tools edit one active mesh at a time;
- captured Rail is straight;
- Branch does not automatically make extrusion side faces;
- arbitrary face-interior Auto-Merge topology is deferred;
- multiple shape keys block topology-changing Inject New;
- Blender 4.5 runtime validation is still required for magnetic hover, MMB pivot, merge/cancel/Undo behavior and topology/data preservation.

See `MAGIC_BRANCH_QUICK_START.md` for the persistent drag-and-drop builder.
