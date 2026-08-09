# Witch Tools UI Map

Last updated: 2026-08-08  
Current development candidate: `Dev_v2.10.0`

## Edit Tools — default order

Top-level sections are now preference-backed and reorderable. Default:

1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Object Snap
5. Inject New
6. Magic Branch
7. Edge Doctor
8. Vertex Lock
9. Selection Slots

`Reorder Tools` switches the panel to compact rows with a drag grip and explicit up/down arrow fallback. The saved order lives in Witch Tools add-on preferences, not the `.blend` scene.

## Coordinate Copy

Three-step workflow retained from Dev_v2.9.0:

1. Global / Local, X/Y/Z, Location/Rotation/Scale.
2. Capture one vertex/edge/face source.
3. Select independent targets and Apply Copied Coordinates.

Default Apply shortcut: `Ctrl+Shift+C`.

## Planar Edit

Retained as an independent top-level tool because it is a separate precision workflow.

- Plane Lock: X/Y/Z object-local axis locks, partial unlock, clear all.
- Level: capture one source point, assign exact enabled world coordinates to every target vertex.

## Vertex Snap / Object Snap

Existing operator contracts and controls remain unchanged.

## Inject New

Four-step UI:

### 1. Initial Setup

- Solo
- Branch
- Slide

### 2. Movement

Solo/Branch:

- independent X / Y / Z toggles;
- optional `Use Captured Rail`;
- Magnetic Snap;
- Branch-only Auto-Merge.

Slide:

- select one or more edges;
- all inserted vertices share one relative rail factor;
- the selected edge nearest the cursor is the driver rail.

### 3. New Element

Solo/Branch: Vertex / Edge / Face.  
Slide: Vertex only.

### 4. Select Source and Inject

`Inject New` starts modal placement. Magnetic targets highlight in the viewport. Hold MMB to pause placement and orbit around the live injection; release MMB to resume.

Canonical operators:

- `mesh.wt_inject_new_capture_rail_end`
- `mesh.wt_inject_new_clear_rail`
- `mesh.wt_inject_new`

## Magic Branch

### Tool Mode

- Persistent toggle (dedicated hotkeyable operator)
- OFF = Single Branch
- ON = remain armed after a completed branch

### Branch Type

- Vertex
- Edge
- Face

Face adds:

- Paver: repeat equal-size source-derived tiles;
- Organic: one connected adaptable face.

### Drag / Snap

- X / Y / Z independent toggles, XYZ default;
- Magnetic Snap;
- Auto-Merge.

`Start Magic Branch` arms the viewport. Click-drag geometry of the chosen type. Hold MMB during a drag to orbit around live branch geometry.

Canonical operators:

- `mesh.wt_magic_branch`
- `mesh.wt_magic_branch_toggle_persistent`

## Edge Doctor

Parent repair section containing:

### Missing Vertex / Edge Injector

Former Edge / Vertex Inject A/B/C repair plus new two-edge L mode.

- A/B/C: select A, B, C individually; C active last. Existing projection solver remains canonical.
- L mode: select two edges sharing one corner; infer the fourth parallelogram corner and create/reuse the missing vertex and outer edges.

Canonical wrapper: `mesh.wt_edge_doctor_missing_inject`.

### Alignment Fixer

Former `Align Vertices / Edges / Faces` / Guided Align UI, renamed and nested. Backend operators remain the existing `mesh.wt_guided_align_*` contracts.

### Curvature Sync

Existing Curvature Sync workflow, nested unchanged under Edge Doctor.

## Vertex Lock

Existing Vertex Locks / Protected Edit Zone controls retained and renamed at top-level UI to singular `Vertex Lock`.

## Selection Slots

Existing saved mesh-selection workflow retained.

## Magnetic target behavior

Shared by Inject New and Magic Branch:

1. vertex cursor target wins;
2. otherwise edge;
3. otherwise face.

Hover highlight must correspond to the target actually used by placement.

- vertex/edge: nearest compatible new endpoint is aligned while copied shape stays rigid;
- face: live endpoints solve independently along parallel travel lines to the face/boundary.

Auto-Merge supports conservative vertex/edge materialization/welding. Arbitrary face-interior retopology is not automatically invented in the Dev_v2.10.0 candidate.

## Persistence / backend contract

- Coordinate/Level transient capture state: `Scene.wt_precision_edit`.
- Plane Lock values: BMesh custom layers.
- Edit Tools order/disclosure state: add-on preferences.
- topology drag/magnetic logic: `precision_edit_drag.py` + `precision_edit_topology.py`.
- Witch Dock / Quickbar is not modified in Dev_v2.10.0; future exposure must remain a thin wrapper over Witch Tools.

## Dev_v2.10.1 UI corrections

- Inject New Edge Solo/Branch accepts one or more Edge sources.
- Magic Branch Step 1 now has explicit ON/OFF; Persistent is only stay-armed behavior.
- Magic Branch Branch Type buttons also switch Blender Vertex/Edge/Face selection mode.
- Plain MMB changes the live pivot only while dragging; modifier MMB keeps normal viewport navigation.
- Paver can grow along an enabled out-of-plane axis, including the Z-only floor-to-wall case.
