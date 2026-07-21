# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v2.5.0 — Curvature Sync MVP

- Implemented Curvature Sync under Edit Tools against the Dev_v2.4.0 baseline.
- Added multi-chain and multi-object circular A/M/Z repair, exact middle-axis normalization, equal per-side segment counts, missing-vertex injection, and optional shared-face column construction.
- Added copied-BMesh preflight and strict failure for branched, closed, ambiguous, shape-key-incompatible, or protected-interior selections.
- Integrated Vertex Lock / Protected Edit Zone reference preservation and index remapping.
- Fixed an existing Vertex Locks unregister cleanup failure.
- Packaged `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`.
- Updated Curvature Sync state, Witch Tools project state, build registry, compatibility records, and package documentation.

## Testing

- Complete package syntax audit: passed.
- Registration/unregistration in Blender Python 5.2.0 LTS: passed.
- Synthetic topology repair and strict failure tests: passed.
- Locked-anchor / locked-interior tests: passed.
- Actual two-object collar test: completed with unresolved positions reported rather than forced.
- Exact Blender 4.5 UI and interactive undo/redo: pending user test.