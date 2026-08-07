# Witch Tools Precision Edit — Feature Specification

Status: development candidate  
Candidate: `Dev_v2.9.0`  
Target Blender: `4.5.0`  
Branch: `feature/witch-tools-precision-edit`

## Purpose

Add fast, explicit mesh-edit precision workflows to Witch Tools without relying on Blender selection medians or repeated manual coordinate entry.

The feature contains three Edit Tools sections:

1. **Coordinate Copy**
2. **Planar Edit**
3. **Inject New**

Witch Tools remains the canonical backend. Any later Witch Dock / Quickbar exposure must call these operators rather than duplicate geometry logic.

## Coordinate Copy

### User workflow

1. Choose `Global` or `Local` coordinate space.
2. Enable any combination of X, Y, Z.
3. Enable Location, Rotation, Scale, or a combination.
4. Select exactly one source vertex, edge, or face and press **Capture Source**.
5. Select one or more targets.
6. Press **Apply Copied Coordinates** or its hotkey.

### Coordinate semantics

- `Global`: source and targets are evaluated in world space, then every result is converted back into the target object's local mesh coordinates. This is the mode intended for lining up different mesh objects whose object origins/transforms differ.
- `Local`: the same numeric object-local source values are applied in each target object's own local frame.
- Changing Global/Local after capture invalidates the capture and requires recapture.
- Disabled X/Y/Z components remain unchanged.

### Exact-target semantics

Coordinate Copy must never use the entire target selection's median as the value being changed.

- Vertex mode: every selected target vertex is an independent target.
- Edge mode: every connected component of selected target edges is an independent target group.
- Face mode: every connected component of selected target faces is an independent target group.

### Location / rotation / scale on mesh elements

Mesh elements do not own Blender Object transform channels, so Rotation and Scale are defined as geometry-frame operations:

- Vertex: position plus a normal-derived local frame; unit geometric extent.
- Edge: midpoint, edge-direction frame, and edge length.
- Face: median center, face-normal/edge-derived frame, and frame-aligned planar extent.

Location moves each target point/group center. Rotation and scale operate around that target's own center.

### Shortcut

Default development shortcut for Apply: `Ctrl+Shift+C` in the Mesh keymap. The operator remains assignable through Blender's normal right-click shortcut workflow.

## Planar Edit

### Plane Lock

Plane Lock freezes selected geometry on one or more object-local coordinate axes while leaving the other axes editable.

- X/Y/Z may be combined.
- Selecting an edge or face locks its participating vertices.
- Lock references are stored as persistent BMesh custom layers, not transient vertex indices.
- A lightweight guard restores locked coordinates during Edit Mode transforms.
- **Unlock Selected** removes only the enabled lock axes from the current selection.
- **Clear All Plane Locks** clears this tool's locks from all participating Edit Mode meshes.
- Existing full Vertex Locks remain stronger protection and are honored by the precision-edit operators.

### Level

1. Select exactly one source vertex, edge, or face and press **Capture Source**.
2. Enable X, Y, and/or Z.
3. Select any target vertices, edges, or faces.
4. Press **Level Targets**.

The source point is captured in world space. Every selected target vertex independently receives the source world coordinate on the enabled axes. Disabled axes remain unchanged. This is an absolute per-vertex operation, not a median translation.

## Inject New

### Setup modes

- `Solo`: duplicate one selected vertex, edge, or face. The duplicate is not connected back to the source.
- `Branch`: duplicate one selected vertex, edge, or face and add source-to-copy branch edges for the duplicated source vertices. Branch does not automatically create side faces.
- `Slide`: insert one new vertex into exactly one selected edge. The original edge is split so the new vertex is already part of the topology.

Slide is deliberately vertex-only because inserting an edge or face *into* one existing edge has no unambiguous topology-preserving meaning.

### Movement modes

Solo and Branch support:

- `X`: move only along global X.
- `Y`: move only along global Y.
- `Z`: move only along global Z.
- `Rail`: capture one endpoint from a vertex, edge midpoint, or face center; the new geometry moves only on the straight segment from the source point to that endpoint.

Slide uses the selected source edge itself as its rail.

Placement is modal: move the mouse, then left-click or Enter to commit. Esc or right-click cancels.

### Scope and safety

- Inject New currently operates on one active mesh in Edit Mode.
- Meshes with multiple shape keys are rejected.
- Existing Vertex Lock references are snapshotted/restored across topology changes.
- Plane Lock enforcement is suspended during the modal operation and newly created vertices do not inherit Plane Lock masks.
- Finish rejects zero-area faces discovered after the operation.
- Cancel attempts to remove duplicated topology or dissolve the inserted Slide vertex back out.

The existing **Edge / Vertex Inject** A/B/C auto-aligned repair operator remains a separate tool and is not replaced by Inject New.

## UI order

Edit Tools candidate order:

1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Inject New
5. Object Snap
6. Edge / Vertex Inject
7. Curvature Sync
8. Align Vertices / Edges / Faces
9. Selection Slots
10. Vertex Locks / remaining Edit Tools controls

Each new section uses compact toggles/icons and an explicit numbered workflow where ordering matters.

## Acceptance criteria

### Coordinate Copy

- Global Location can align targets across two mesh objects with different origins/transforms to exactly the same enabled world coordinate.
- Local Location copies the same numeric local coordinate into targets without pretending the objects share world frames.
- Selecting multiple target vertices changes each vertex to the copied enabled coordinate, not the target median.
- Connected selected edge/face components behave independently.
- X/Y/Z masks preserve disabled components.
- Location-only, Rotation-only, Scale-only, and combined modes execute without moving unrelated components.
- Changing space after source capture is rejected until recapture.
- Protected targets fail before partial mutation.
- Ctrl+Shift+C invokes Apply in Mesh Edit Mode and can be reassigned through Blender keymaps.

### Plane Lock

- Locked X/Y/Z coordinates remain exact while ordinary transforms change unlocked coordinates.
- Multiple lock axes can be combined.
- Edge/face selection locks participating vertices.
- Unlock Selected removes only requested axes.
- Clear All removes this tool's locks.
- Locks survive ordinary Edit Mode selection changes and save/reopen when Blender preserves the custom mesh layers.

### Level

- Every selected target vertex receives the exact source world coordinate on enabled axes.
- Multi-object targets with different object origins/transforms line up in world space.
- No target-selection median is used.
- Existing Vertex Locks and Plane Locks block incompatible changes before mutation.

### Inject New

- Solo Vertex/Edge/Face creates a movable disconnected copy.
- Branch Vertex/Edge/Face creates the copy plus source-to-copy branch edges without deleting source topology.
- Slide inserts one vertex into one edge and leaves the vertex between the original endpoints.
- X/Y/Z mouse placement changes only the selected global movement axis.
- Rail movement is clamped to the source-to-end segment.
- Esc/right-click restores the pre-operation topology for all three modes.
- Commit participates in Blender Undo/Redo as one operator action.
- Existing material/edge attributes and face winding are preserved where the operation does not intentionally create new loose geometry.
- Slide does not introduce zero-length edges, zero-area faces, duplicate edges, or unexpected non-manifold changes in a previously manifold local test case.
- Failure does not leave partially injected topology.

## Out of scope for Dev_v2.9.0

- Curved/polyline Inject New rails.
- Multi-object simultaneous Inject New topology editing.
- Branch side-face generation / extrusion behavior.
- Automatically interpreting Slide as edge/face insertion.
- Surface projection rails.
- Witch Dock / Quickbar wrapper changes before Witch Tools runtime acceptance.
