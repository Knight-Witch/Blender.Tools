# Align Vertices / Edges / Faces State

Last updated: 2026-08-05

## Status

- Feature ID: `WT-ALIGN-001`
- Current implementation: Witch Tools `Dev_v2.8.0` candidate
- Canonical owner: Witch Tools
- Witch Dock/Quickbar role: deferred thin wrapper after backend validation
- Target Blender version: `4.5.0`
- Runtime status: static candidate; Blender 4.5 validation pending

## Source baseline

The repository's committed Dev_v2.7.0 snapshot parts are truncated and do not match the recorded manifest. The documented Dev_v2.7.1 source cannot be reconstructed from that snapshot.

Dev_v2.8.0 was implemented from the verified complete Dev_v2.6.1 source and recorded as:

- direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`
- patch record: `addons/witch_tools/dev/patches/Dev_v2_8_0/`
- feature branch: `feature/witch-tools-guided-align`

## Implemented

- Four-step Witch Tools Edit section.
- Parent capture from vertex, edge, face, and mixed selections.
- Active Element and Median parent references.
- World X/Y/Z coordinate masks.
- Custom Guide start/end numeric fields.
- Guide point capture from selected geometry.
- Copy parent reference to guide start.
- Custom-frame matching.
- Projection to guide line.
- Free-coordinate movement.
- Straight captured edge rails.
- One Anchor to All.
- Paired by Rail.
- Rigid relative-spacing/shape preservation.
- Whole Selection and Per Selected Island grouping.
- Optional rail extent clamping.
- Multi-object world/local conversion.
- Parent exclusion from movement.
- Vertex Lock preflight.
- Multiple-shape-key rejection.
- Stale parent/rail count detection.
- Ambiguous rail and impossible-constraint rejection.
- Non-mutating Analyze.
- Transaction-first Apply and rollback attempt on unexpected failure.

## Build identity

- Artifact: `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip`
- Size: 138,473 bytes
- SHA-256: `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`
- Package: `Witch_Tools_Dev`
- Python files: 48
- Total files: 63
- Generated cache files: 0
- Source-tree SHA-256: `076912ce5d84115adb803ebfa793e04117053fe9af45d459cd4cbdb7be853504`

## Testing completed

- Parsed and compiled all 48 Python files.
- Duplicate identifier scan passed across 99 operator/panel IDs.
- Confirmed seven Guided Align operators.
- Confirmed panel UI-state names exist in preferences.
- Ran seven pure constraint-math assertions covering component matching, deltas, custom-frame conversion, valid rail solving, and incompatible rail rejection.
- Verified compressed patch decoding and SHA-256.
- Applied patch to a pristine Dev_v2.6.1 reconstruction.
- Verified patched source tree matches the packaged candidate source.
- Verified ZIP integrity, safe relative paths, single package root, and generated-cache exclusion.

## Testing pending

- Blender 4.5 registration/unregistration.
- N-panel rendering and disclosure persistence.
- Capture behavior for vertex, edge, face, and mixed modes.
- Screenshot world-axis case.
- Slide-only rail case.
- Paired parent/child rail case.
- Custom 45-degree guide.
- Shape-preserving groups and multiple islands.
- Multi-object Edit Mode with different transforms.
- Locks, stale markers, impossible constraints, malformed rails, shape keys, and rollback.
- Undo/redo.
- Save/reopen.
- Witch Dock/Quickbar integration and overlay regression.

## Known limitations

- Rails must be straight.
- Paired rails require exactly one captured parent vertex per rail component.
- A subordinate island touching more than one rail is rejected.
- Multiple shape keys are unsupported.
- Linked objects sharing a Mesh datablock share markers.
- Captured-marker objects must participate in the current Edit Mode context.
- Topology edits may require recapture.

## Next exact step

Run the ordered Blender 4.5 test plan. Do not begin Witch Dock/Quickbar work until the backend workflow and contract are accepted.
