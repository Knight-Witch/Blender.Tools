# Blender.Tools Project State

Last updated: 2026-07-21

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Development integration branch: `Blender_Dev`
- Branch origin: `Witch_Quick_Access`
- Default repository branch: `Witch_Main_Tools`
- Default Witch Tools target Blender version: `4.5`

## Current development builds

### Witch Tools

- Current urgent build: `Dev_v2.5.0`
- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Based on supplied baseline: `Dev_v2.4.0`
- Target: Blender `4.5.0`
- Runtime tested in: Blender Python `5.2.0 LTS`
- Exact Blender 4.5 runtime: pending user test

### Witch Quickbar

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package: `witch_quickbar_dev`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Update destination: `Witch_Quick_Access` public branch
- Runtime test: pending

### Witch's Dev Modules

- Version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- Package: `witch_dev_modules`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Packaging defect: original archive contains 34 `.pyc` files
- Runtime test: pending

## Last completed work

- Established root and add-on documentation/rules architecture on `Blender_Dev`.
- Audited the supplied Witch Tools, Quickbar, and Dev Modules baselines.
- Inspected Witch Tools Dev_v2.4.0 and the existing Vertex Lock / Protected Edit Zone implementation.
- Implemented Curvature Sync MVP directly in Witch Tools and produced Dev_v2.5.0.
- Added multi-object circular chain synchronization, exact middle normalization, missing-vertex injection, shared-face column creation, copied-BMesh preflight, and protected-zone/index-remapping behavior.
- Fixed a pre-existing Vertex Locks unregister helper failure.
- Updated the Curvature Sync packet, Witch Tools state, build registry, compatibility log, and packaged add-on documentation.
- Tested the build against synthetic meshes and the supplied actual collar file in Blender Python 5.2.0 LTS.

## Current known-working state

For the tested Dev_v2.5.0 operations in Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed
- static package parsing passed
- synthetic vertex injection and face splitting passed
- invalid branched topology rejected without mutation
- protected anchors accepted and locked interior vertices rejected
- actual 21-chain / two-object collar test completed
- lower collar manifold state preserved
- no zero-length edges, duplicate edges, zero-area faces, invalid faces, or new 3D edge intersections introduced
- matching upper/lower outer interface curve positions aligned within floating-point tolerance
- save/reopen passed

No public branch, public Quickbar update destination, package identity, or external release location was changed.

## Active problems

1. Dev_v2.5.0 requires immediate user testing in Blender 4.5.
2. Interactive undo/redo could not be validated in the background Python environment.
3. The actual collar selection/result must be inspected manually before printing.
4. The Curvature Sync MVP may report unresolved column positions where a safe shared-face connection is unavailable.
5. Automatic chain discovery, missing-Middle creation, and surplus-vertex dissolution remain unimplemented.
6. Full canonical source import and source-derived UI/operator registries are still pending.
7. Public Witch Tools distribution/update strategy remains unresolved.
8. Quickbar runtime/update-link testing remains pending.
9. Witch Core source baseline remains pending.

## Next exact implementation step

The user should install Witch Tools Dev_v2.5.0 in Blender 4.5 and run Curvature Sync on a backup copy of the collar using explicit A/M/Z and curve-chain selections. Record the Analyze and Apply reports, inspect upper/lower interface alignment, and test interactive undo/redo.

Any resulting failure should be patched narrowly against Dev_v2.5.0. Once the urgent collar repair works, import the complete source into the canonical Witch Tools repository tree and generate UI/operator registries.

## Test status

- Static ZIP/package checks: passed
- Blender Python 5.2.0 LTS runtime checks: passed for tested operations
- Blender 4.5 runtime: not performed
- Interactive UI and undo/redo: not verified
- Public branches modified: no
- Quickbar URLs or public compatibility surfaces modified: no

## Known remaining issues

Dev_v2.5.0 is an urgent development MVP, not a public release. The original uploaded collar file remains untouched, and any use for print preparation requires visual/manual verification in Blender 4.5.