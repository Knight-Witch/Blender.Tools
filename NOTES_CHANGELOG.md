# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Update: Witch Tools Dev_v2.5.0 Curvature Sync MVP

- Inspected the supplied Witch Tools Dev_v2.4.0 source and existing Vertex Lock / Protected Edit Zone data model.
- Implemented the first functional Curvature Sync MVP directly in Witch Tools.
- Added explicit A/M/Z anchor capture, automatic selection clearing, circular XY/XZ/YZ fitting, exact middle-axis normalization, equal segment counts per side, multi-chain/multi-object synchronization, missing-vertex injection, and optional shared-face column construction.
- Added copied-BMesh preflight, branched/ambiguous selection rejection, shape-key injection protection, unresolved-column reporting, and lock/edit-zone/anchor index remapping.
- Fixed a pre-existing Vertex Locks unregister failure caused by a missing safe RNA-property deletion helper.
- Packaged `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip` with SHA-256 `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`.
- Added the add-on changelog entry, README workflow, quick-start guide, latest/full notes, and compatibility entry.
- Tested registration/unregistration, synthetic repair, lock/protected-zone behavior, strict failure without mutation, and a 21-chain two-object collar repair using Blender Python 5.2.0 LTS.
- Updated Curvature Sync state, Witch Tools state, project state, build registry, and Blender compatibility records.

## Public compatibility

No public branch, Quickbar update destination, package identity, operator namespace, external release link, or asset path was changed.

## Testing limitation

Exact Blender 4.5 UI, installed-package behavior, and interactive undo/redo remain pending user validation. The supplied original collar file was not overwritten.