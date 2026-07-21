# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v2.5.2 — Blender 4.5 production collar validation

- The user installed Dev_v2.5.2 in Blender 4.5 and reopened the supplied pre-curvature collar file.
- The saved A/M/Z anchors and curvature-chain selection were available for the test.
- Curvature Sync Analyze/Apply completed with **Replace Misaligned Column Edges** enabled.
- The user reported that the corrected result worked beautifully, confirming the intended curvature and visible same-slot column topology in the actual production workflow.
- This validates the primary installed Blender 4.5 workflow that remained pending after automated Blender Python 5.2.0 LTS tests.

## Remaining validation

- interactive undo/redo has not yet been reported;
- formal normals, face-winding, manifold, and print-fit inspection remain pending before slicing;
- public release installation/upgrade and update behavior remain untested.

No public branch, Quickbar URL, package identity, operator namespace, asset path, or public release location changed.
