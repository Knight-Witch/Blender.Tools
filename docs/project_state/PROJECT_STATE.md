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

- Current urgent build: `Dev_v2.5.1`
- Artifact: `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Based on supplied baseline: `Dev_v2.4.0`
- Supersedes: `Dev_v2.5.0`
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

- Established repository rules, architecture, and documentation tracking on `Blender_Dev`.
- Audited supplied Witch Tools, Quickbar, and Dev Modules baselines.
- Implemented Curvature Sync MVP as Dev_v2.5.0.
- Added standalone Auto-Aligned Vertex Inject and produced Dev_v2.5.1.
- Added ordered A/B/C selection, target-chain projection, edge splitting, optional C-D face splitting, copied-BMesh preflight, and lock/edit-zone/anchor remapping.
- Updated feature state, roadmap, Witch Tools state, build registry, package documentation, and root/add-on notes.
- Ran syntax, registration, synthetic injection, synthetic face-split, and Curvature Sync regression tests under Blender Python 5.2.0 LTS.

## Current known-working state

For tested Dev_v2.5.1 operations under Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed
- static package parsing passed for 45 Python files
- synthetic A/B/C injection placed D exactly on the expected target edge
- optional C-D connection split one quad into two valid faces
- Curvature Sync synthetic regression passed
- previous actual-collar Curvature Sync harness results remain documented

No public branch, public Quickbar update destination, package identity, asset path, or external release location was changed.

## Active problems

1. Dev_v2.5.1 requires immediate user testing in Blender 4.5.
2. Interactive undo/redo could not be validated in background mode.
3. Real collar A/B/C selection and target-chain inference have not yet been manually validated.
4. Vertex Inject aborts on ambiguous forks and currently acts on the active mesh object.
5. Curvature Sync may still report unresolved column positions.
6. Automatic bulk correspondence, missing-Middle creation, and surplus-vertex dissolution remain incomplete.
7. Full canonical source import and source-derived UI/operator registries are pending.
8. Public Witch Tools distribution/update strategy remains unresolved.
9. Quickbar runtime/update-link testing and Witch Core source import remain pending.

## Next exact implementation step

Install Witch Tools Dev_v2.5.1 in Blender 4.5 on a backup collar file. Use Edge / Vertex Inject first by clicking A, B, and C individually in order, then inspect D placement and the optional C-D face split. Test undo/redo. Patch only any injector failure required by the real collar topology, then continue into Curvature Sync.

After the urgent print workflow works, import the complete Dev_v2.5.1 source into the canonical Witch Tools repository tree and generate UI/operator registries.

## Test status

- Static ZIP/package checks: passed
- Blender Python 5.2.0 LTS runtime checks: passed for tested operations
- Blender 4.5 runtime: not performed
- Actual collar standalone Vertex Inject: pending
- Interactive UI and undo/redo: not verified
- Public branches modified: no
- Quickbar URLs or public compatibility surfaces modified: no

## Known remaining issues

Dev_v2.5.1 is an urgent development build, not a public release. The original uploaded collar file remains untouched. Use a backup and visually inspect all topology before printing.
