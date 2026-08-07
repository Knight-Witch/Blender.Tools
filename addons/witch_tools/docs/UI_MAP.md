# Witch Tools UI Map

Last updated: 2026-08-07  
Current development candidate: `Dev_v2.9.0`

## Edit Tools

Current runtime ordering in `panel_edit_tools.py`:

1. **Coordinate Copy**
2. **Planar Edit**
3. Vertex Snap
4. **Inject New**
5. Object Snap
6. Edge / Vertex Inject
7. Curvature Sync
8. Align Vertices / Edges / Faces
9. Selection Slots
10. Vertex Locks / remaining Edit Tools controls

## Coordinate Copy

Header icon: `COPYDOWN`

The section is a three-step workflow.

### 1. Choose What to Copy

- Space: `Global` / `Local`
- Axes: X / Y / Z compact toggles
- Copy: Location / Rotation / Scale compact toggles

Global is explicit world-space capture/application with matrix conversion per target object. Local copies numeric object-local values.

### 2. Select One Source

- `Capture Source`
- clear-source `X` icon button
- captured source object/type status

Capture requires exactly one source element in the current vertex/edge/face selection mode and clears that selection afterward so targets can be selected cleanly.

### 3. Select Target(s) and Apply

- `Apply Copied Coordinates`
- shortcut hint
- persistent status/error line

Default development shortcut: `Ctrl+Shift+C` in the Mesh keymap.

Targets are never treated as one selection-wide median. Vertex targets apply independently; disconnected selected edge/face components apply independently.

## Planar Edit

Header icon: `MESH_PLANE`

### Plane Lock

- X / Y / Z lock-axis toggles
- `Lock Selected`
- `Unlock Selected`
- `Clear All Plane Locks`

Plane Lock freezes the enabled object-local coordinate components of participating vertices while leaving unlocked axes editable.

### Level

- `1. Capture Source`
- source status
- X / Y / Z toggles
- `2. Level Targets`

Level captures the source in world space and sets each selected target vertex independently to the source coordinate on enabled axes.

## Vertex Snap

Existing section and shortcut contract remain unchanged.

## Inject New

Header icon: `MOD_EDGESPLIT`

The section is a four-step workflow.

### 1. Initial Setup

- `Solo`
- `Branch`
- `Slide`

Solo creates a disconnected duplicate. Branch creates the duplicate plus source-to-copy branch edges. Slide inserts one new vertex into one selected edge.

### 2. Movement

Solo / Branch:

- X
- Y
- Z
- Rail

When Rail is active:

- `Capture Rail End`
- clear-end `X` icon button
- captured endpoint status

Slide automatically uses the selected source edge as its rail.

### 3. New Element

Solo / Branch:

- Vertex (`VERTEXSEL`)
- Edge (`EDGESEL`)
- Face (`FACESEL`)

Slide displays Vertex only because it is a subdivide-like edge insertion.

### 4. Select Source and Inject

- selection instruction appropriate to current mode
- `Inject New`
- persistent status/error line

Placement is modal: move the mouse, then left-click or Enter to commit; Esc/right-click cancels.

## Object Snap

Existing section remains unchanged.

## Edge / Vertex Inject

The existing A/B/C → D auto-aligned repair tool remains a separate section. It is not replaced by Inject New.

## Align Vertices / Edges / Faces

The existing Dev_v2.8.0 four-step Guided Align UI remains unchanged after the new precision sections are inserted above it:

1. Capture Parent Anchor.
2. Choose World XYZ or Custom Guide target.
3. Choose free movement or captured rails / mapping / shape-preservation behavior.
4. Select subordinates, Analyze, and Align.

## Canonical operator contracts added in Dev_v2.9.0

Coordinate Copy:

- `mesh.wt_coordinate_copy_capture`
- `mesh.wt_coordinate_copy_clear`
- `mesh.wt_coordinate_copy_apply`

Planar Edit:

- `mesh.wt_planar_lock_selected`
- `mesh.wt_planar_unlock_selected`
- `mesh.wt_planar_clear_all`
- `mesh.wt_planar_level_capture`
- `mesh.wt_planar_level_targets`

Inject New:

- `mesh.wt_inject_new_capture_rail_end`
- `mesh.wt_inject_new_clear_rail`
- `mesh.wt_inject_new`

## Persistence / backend contract

- Coordinate Copy and Level capture state lives on `Scene.wt_precision_edit` for the current Blender scene/session.
- Plane Lock coordinates are stored in mesh BMesh custom layers: `wt_plane_lock_mask`, `wt_plane_lock_x`, `wt_plane_lock_y`, `wt_plane_lock_z`.
- Existing Vertex Locks remain a separate protection system and are consulted by the new coordinate-changing tools.
- Witch Dock / Quickbar integration is not part of Dev_v2.9.0. Later UI must call these Witch Tools contracts rather than duplicate backend logic.
