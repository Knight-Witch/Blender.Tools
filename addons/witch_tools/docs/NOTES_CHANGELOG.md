# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-05

## Dev_v2.8.0 — Align Vertices / Edges / Faces

- Added **Edit Tools > Align Vertices / Edges / Faces** as a four-step workflow: capture parent, choose alignment target, choose permitted movement, select subordinates and apply.
- Added parent capture from vertices, edges, faces, and mixed selections with Active Element or Median reference.
- Added explicit world X/Y/Z matching. Coordinates left disabled remain unchanged.
- Added editable arbitrary-angle Custom Guide start/end coordinates, selection capture, parent-to-start copy, custom-frame matching, and projection to the guide line.
- Added free-coordinate movement and straight captured slide rails.
- Added one-parent-to-all and explicit paired-by-rail parent/child mapping.
- Added rigid relative-spacing/shape preservation, whole-selection/per-island grouping, rail extent clamping, and Vertex Lock preflight.
- Added non-mutating Analyze and transaction-first Apply behavior.
- Added failures for stale captures, curved/zero rails, impossible multi-axis rail constraints, out-of-range clamped solutions, ambiguous pairing, multiple shape keys, locked targets, and non-invertible transforms.
- Witch Dock/Quickbar was deliberately not modified; it remains a later thin-wrapper task after backend validation.

## Source recovery

- The committed Dev_v2.7.0 snapshot parts are truncated and do not match their manifest, so the documented Dev_v2.7.1 source cannot be reconstructed from the repository snapshot.
- Dev_v2.8.0 was implemented from the last verified complete Dev_v2.6.1 source baseline.
- Added the direct unpacked source at `addons/witch_tools/dev/Witch_Tools_Dev/` and a reproducible patch record at `addons/witch_tools/dev/patches/Dev_v2_8_0/`.

## Candidate artifact

- File: `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip`
- Size: 138,473 bytes
- SHA-256: `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`
- Target Blender: `4.5.0`

## Testing

Passed:

- 48 Python files parsed and compiled;
- duplicate scan across 99 operator/panel identifiers;
- seven expected Guided Align operator IDs;
- UI-state preference declaration consistency;
- seven pure constraint-math assertions;
- source patch dry-run/application and source-tree equality;
- ZIP integrity, safe paths, package root, and cache exclusion.

Not performed:

- Blender 4.5 registration or panel rendering;
- real BMesh alignment cases;
- undo/redo;
- save/reopen;
- Witch Dock/Quickbar regression.
