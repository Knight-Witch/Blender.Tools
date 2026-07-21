# Witch Tools Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit
- Default target Blender version: 4.5
- Development package identity: `Witch_Tools_Dev`

## Current development build

- Version: `Dev_v2.5.1`
- Artifact: `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`
- SHA-256: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Package folder: `Witch_Tools_Dev`
- Declared Blender target: `4.5.0`
- Python source files: 45
- PNG assets: 6
- Generated cache files: none
- Static Python syntax audit: passed
- Runtime environment tested: Blender Python `5.2.0 LTS`
- Exact Blender 4.5 runtime: pending user test

Dev_v2.5.1 was produced from Dev_v2.5.0 without changing package identity, existing operator namespaces, assets, or the Witch Tools footer URL.

## Current implementation

Dev_v2.5.1 retains all Dev_v2.5.0 Curvature Sync MVP behavior and adds Edit Tools > Edge / Vertex Inject:

- ordered A/B/C vertex selection
- A-B source-column and B-C row-edge validation
- ideal D relation from `C + (A - B)`
- target-chain inference from A
- strict straightest-continuation traversal and fork rejection
- projection tolerance and existing-vertex reuse tolerance
- target-edge splitting
- default optional C-D connection and shared-face split
- copied-BMesh preflight
- shape-key and zero-area-face rejection
- Vertex Lock, Protected Edit Zone, and Curvature Sync anchor remapping
- C and D selected after success

Curvature Sync remains available with explicit A/M/Z circular multi-chain and multi-object repair.

## Last completed work

- Implemented and packaged Auto-Aligned Vertex Inject as Dev_v2.5.1.
- Added a dedicated Edit Tools section and user controls.
- Added `VERTEX_INJECT_QUICK_START.md` and package changelog/compatibility updates.
- Ran full package syntax, registration/unregistration, synthetic vertex-injection, face-split, and Curvature Sync regression tests.
- Preserved the original uploaded collar file and all public compatibility surfaces.

## Current known-working state

Under Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed
- synthetic target-edge injection placed D at the exact expected position
- C-D face splitting produced two valid faces from one quad
- result selection retained C and D
- Curvature Sync synthetic regression passed
- no zero-area faces were produced in the injection test

The previous actual-collar Curvature Sync harness result remains documented, but standalone Vertex Inject has not yet been manually exercised on the actual collar topology.

## Active problems

1. Exact Blender 4.5 installation and UI test are pending.
2. Interactive undo/redo is unverified because background-mode undo is unavailable.
3. Real collar A/B/C selection and target-chain inference require immediate user validation.
4. The injector currently acts on the active object and aborts on ambiguous topology forks.
5. Bulk standalone injection and curvature-aware single injection are not yet exposed.
6. Curvature Sync still has unresolved-column and missing-Middle limitations.
7. The full Dev_v2.5.1 source tree has not yet been imported into the final canonical repository source location.

## Next exact implementation step

Install Dev_v2.5.1 in Blender 4.5 on a backup collar file. Test Edge / Vertex Inject before Curvature Sync:

1. click A, B, and C individually in that order;
2. keep Connect & Split Face enabled;
3. run Inject Auto-Aligned Vertex;
4. inspect D placement, C-D topology, normals, and face winding;
5. test undo and redo;
6. report any error message or incorrect target-chain choice.

Patch only the required injector files in response to that test. Once the collar has the required missing vertices/columns, continue with Curvature Sync.

## Test status

- ZIP integrity and package layout: passed
- Python syntax: passed for all 45 source files
- Blender Python 5.2 registration/unregistration: passed
- synthetic Vertex Inject topology test: passed
- Curvature Sync synthetic regression: passed
- Blender 4.5 runtime: not performed
- interactive undo/redo: not verified
- actual collar standalone injection: pending
- public release/update behavior: not modified or tested

## Known remaining issues

Dev_v2.5.1 is an urgent development build, not a public release. Use it only on a backup until Blender 4.5 manual validation is complete.
