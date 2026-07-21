# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Update: Dev_v2.5.2 production collar validation in Blender 4.5

- The user installed Witch Tools `Dev_v2.5.2` in Blender 4.5 and reopened the supplied `Collar_PRE-curvature_sync.blend` file.
- The saved A/M/Z anchors and curvature-chain selection were available for the run.
- Curvature Sync Analyze/Apply completed with **Replace Misaligned Column Edges** enabled.
- The user reported that the corrected result worked beautifully, confirming the intended curvature and visible same-slot column topology on the production collar.
- This validates the primary installed Blender 4.5 workflow that had remained pending after automated Blender Python 5.2.0 LTS testing.
- Interactive undo/redo, formal normals/manifold checks, and final print-fit/slicer validation have not yet been reported and remain pending.
- Updated Curvature Sync state, Witch Tools state, umbrella project state, build registry, compatibility record, and latest/full notes.

## Public compatibility

No public branch, Quickbar update destination, package identity, existing operator namespace, external release link, or asset path was changed.

## Current status

`Dev_v2.5.2` remains a development build rather than a public release. The urgent production collar Curvature Sync workflow is now user-validated in Blender 4.5.
