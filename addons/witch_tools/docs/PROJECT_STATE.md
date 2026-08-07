# Witch Tools Project State

Last updated: 2026-08-07

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh-operator backend
- Development branch: `feature/witch-tools-precision-edit`
- Parent development baseline: `feature/witch-tools-guided-align` at commit `fc94b7c27d0b850699e79b973a0548a2193eb525`
- Intended integration branch: `Blender_Dev`
- Development package: `Witch_Tools_Dev`
- Default target Blender version: `4.5.0`

## Current candidate

- Version: `Dev_v2.9.0`
- Scope: Coordinate Copy, Planar Edit, Inject New, plus retained Dev_v2.8.0 Guided Align and earlier Witch Tools functionality
- Package folder: `Witch_Tools_Dev`
- Declared target: Blender `4.5.0`
- Runtime status: source candidate; Blender 4.5 registration, panel, mesh, modal, undo/redo, and save/reopen validation pending
- Installable ZIP: not cut from this branch yet
- Public/release branches modified: no

## Baseline and source recovery

The repository's older Dev_v2.7.0 snapshot cannot be reconstructed from the committed files because its source parts are truncated relative to their manifest. Dev_v2.8.0 re-established an auditable direct source tree from the verified Dev_v2.6.1 baseline and added Guided Align.

This Dev_v2.9.0 work branches directly from the verified Dev_v2.8.0 Guided Align source commit:

- `fc94b7c27d0b850699e79b973a0548a2193eb525`

Current direct source:

- `addons/witch_tools/dev/Witch_Tools_Dev/`

The public/default release path remains unchanged.

## Current implementation

### Coordinate Copy

Edit Tools now begins with **Coordinate Copy**.

Implemented source behavior:

- Global / Local coordinate type;
- X/Y/Z masks;
- Location / Rotation / Scale toggles;
- exact one-element source capture for vertex, edge, or face;
- source selection clears after capture;
- Global converts through world space per object, allowing different object origins/transforms;
- Local copies numeric object-local values;
- vertices apply independently;
- disconnected selected edge or face components apply independently;
- no selection-wide target median;
- geometry-frame Rotation/Scale semantics for mesh elements;
- transaction-first target planning;
- existing Vertex Lock and new Plane Lock preflight;
- default Mesh keymap shortcut `Ctrl+Shift+C` for Apply.

### Planar Edit

**Plane Lock**:

- stores X/Y/Z lock masks and values in persistent BMesh custom layers;
- locks selected vertices directly; edge/face selections therefore lock participating vertices;
- supports combined axes, partial unlock, and clear all;
- uses a lightweight Edit Mode guard to restore locked object-local coordinates.

**Level**:

- captures one source vertex coordinate, edge midpoint, or face center in world space;
- applies exact source world X/Y/Z coordinates to every selected target vertex independently;
- converts each result back into the target object's local mesh coordinates;
- supports multi-object Edit Mode;
- preflights Vertex Locks and Plane Locks before mutation.

### Inject New

Edit Tools now contains **Inject New** immediately below Vertex Snap.

Implemented source behavior:

- Setup: Solo / Branch / Slide;
- Solo: duplicate one selected vertex, edge, or face with no connection back to source;
- Branch: duplicate one selected vertex, edge, or face and create source-to-copy branch edges;
- Slide: split exactly one selected edge and insert one new vertex into that edge;
- Solo/Branch movement: global X, Y, Z, or a captured straight Rail endpoint;
- Rail endpoint capture accepts a vertex, edge midpoint, or face center;
- Slide uses the selected source edge itself as its rail;
- modal mouse placement with left-click/Enter commit and Esc/right-click cancel;
- existing Vertex Lock references are snapshotted/restored across topology changes;
- Vertex Lock and Plane Lock guards are suspended during the modal topology operation, then restored;
- newly created vertices do not inherit Plane Lock masks;
- shape-key meshes with multiple keys are rejected;
- finish checks for zero-area faces.

Slide is intentionally vertex-only. Branch creates branch edges, not extrusion side faces.

### Existing auto-aligned inject

The previous **Edge / Vertex Inject** A/B/C → D repair workflow remains a separate existing section and operator. It is not replaced or duplicated by Inject New.

## Current Edit Tools UI order

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

## Witch Dock / Quickbar status

Not modified in this pass. Witch Tools remains the canonical backend. Thin Witch Dock / Quickbar exposure is deferred until Dev_v2.9.0 behavior is accepted in Blender 4.5.

## Last completed work

- Read root repository rules, architecture docs, add-on-local rules, current project state/roadmap, baseline source, current version, target Blender, and relevant existing Edit Tools operators before implementation.
- Confirmed Dev_v2.8.0 Guided Align commit `fc94b7c...` as the direct parent baseline.
- Created `feature/witch-tools-precision-edit` without modifying the Guided Align branch or public release branches.
- Added modular property, common math/protection, geometry-frame, Coordinate Copy, Planar Edit, Inject New, and panel modules.
- Registered the new operator/property families and Plane Lock guard.
- Added `Ctrl+Shift+C` Coordinate Copy Apply default keymap.
- Added compact step-based UI and hover help.
- Bumped development metadata to `Dev_v2.9.0` targeting Blender 4.5.
- Created `/docs/features/precision_edit/` with specification, decisions, state, roadmap, and a topology-aware Blender 4.5 test plan.
- Updated UI map and roadmap for the new candidate.
- Compared the branch against the exact parent baseline; the branch is strictly ahead and contains only the intended source/docs candidate work.

## Current known-working state

Previously user-validated in Blender 4.5:

- Dev_v2.5.2 Curvature Sync production collar workflow.
- Quickbar Dev_v1.4.0 Selection Slots workflow.

Dev_v2.9.0 validation completed in this implementation environment:

- branch starts from the exact Dev_v2.8.0 candidate commit;
- branch compare reports no behind commits relative to that baseline;
- authored new precision-edit Python modules parsed/compiled during implementation;
- source operator/property/UI contracts were reviewed while wiring registration and panel calls;
- no Blender executable is available in this environment.

Do not infer runtime success from the static checks above.

## Active problems and limitations

1. Blender 4.5 registration and panel rendering are untested.
2. Coordinate Copy edge/face Rotation/Scale geometry-frame behavior requires real-mesh acceptance testing, especially under mirrored/non-uniform object transforms.
3. Plane Lock timer enforcement must be validated during actual Blender transforms and save/reopen.
4. Level multi-object behavior must be measured in Blender with differently transformed objects.
5. Inject New modal mouse projection requires camera-angle testing.
6. Inject New cancel rollback, especially Slide edge reconstruction, must be proven in Blender.
7. Inject New operates on one active mesh at a time.
8. Rail is a straight source-to-end segment only.
9. Branch creates loose branch edges rather than side faces and therefore does not promise a manifold result.
10. Slide topology must be tested for normals/winding, material/edge attributes, zero-length edges, zero-area faces, duplicate topology, and manifold safety.
11. Undo/redo and save/reopen are untested for the new systems.
12. `Ctrl+Shift+C` must be checked against the user's Blender keymap for conflicts.
13. No additional Blender version has been tested or verified for Dev_v2.9.0.
14. Inherited documentation conflict: the Dev_v2.8.0 roadmap references `/docs/features/align_selection/`, but that directory is absent on the branch. This pass records the gap and does not fabricate historical files.
15. Witch Dock / Quickbar exposure is deferred.

## Next exact implementation step

Install the Dev_v2.9.0 source candidate in Blender 4.5 and execute `/addons/witch_tools/docs/features/precision_edit/TEST_PLAN.md` in order:

1. registration/unregistration and Edit Tools panel rendering/order;
2. Coordinate Copy Global Location with multiple target vertices;
3. Coordinate Copy multi-object Global vs Local with different object transforms;
4. Coordinate Copy Edge/Face Rotation/Scale;
5. Plane Lock axis combinations, unlock, clear, transform guard, and persistence;
6. Level on same-object and multi-object targets;
7. Inject New Solo Vertex/Edge/Face on X/Y/Z and Rail;
8. Inject New Branch Vertex/Edge/Face on X/Y/Z and Rail;
9. Inject New Slide on boundary/interior/loose/special-data edges;
10. cancel rollback, malformed selections, Vertex Locks, Plane Locks, and shape keys;
11. undo/redo, save/reopen, normals/winding, attributes, zero geometry, and manifold checks.

Fix only failures found in that validation pass. Do not broaden scope into curved rails, extrusion side faces, world-frame Plane Lock, multi-object topology Inject, viewport previews, or Witch Dock/Quickbar integration unless explicitly promoted.

## Files changed for Dev_v2.9.0 source candidate

New source modules:

- `precision_edit_props.py`
- `precision_edit_common.py`
- `precision_edit_frames.py`
- `operators_coordinate_copy.py`
- `operators_planar_edit.py`
- `operators_inject_new.py`
- `panel_precision_edit.py`

Modified source modules:

- `__init__.py`
- `state.py`
- `registration.py`
- `keymaps.py`
- `operators_ui.py`
- `panel_edit_tools.py`

Documentation additions/updates are tracked in `NOTES_CHANGELOG.md` and `NOTES_CHANGELOG_FULL.md`.

## Test status

- Parent baseline/branch ancestry: passed
- Authored new-module Python parse/compile: passed during implementation
- Source registration/panel/operator contract review: performed
- Blender executable in implementation environment: unavailable
- Blender 4.5 registration/unregistration: not performed
- Blender 4.5 panel rendering/icons/tooltips: not performed
- Coordinate Copy real-mesh execution: not performed
- Plane Lock real transform enforcement: not performed
- Level real-mesh execution: not performed
- Inject New real modal/topology execution: not performed
- Undo/redo: not performed
- Save/reopen: not performed
- Additional Blender versions: not tested
- Witch Dock/Quickbar updated: no
- Public release branches/URLs modified: no
