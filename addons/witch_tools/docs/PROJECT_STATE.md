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
- Inspected `Collar_DESIGN_v6 - Copy.blend` after manual edge creation and identified eight stale unsplit-face cases.
- Produced a file-specific Blender 4.5 repair script plus optional BAT launcher that splits those faces along the existing edge network and saves a new file without overwriting the original.
- Added transactional baseline validation and geometry-integrity checks to that repair script.
- Added `WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces` to the roadmap for generalized Witch Tools integration.
- Preserved the original uploaded collar file and all public compatibility surfaces.

## Current known-working state

Under Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed
- synthetic target-edge injection placed D at the exact expected position
- C-D face splitting produced two valid faces from one quad
- result selection retained C and D
- Curvature Sync synthetic regression passed
- the exact-file unsplit-face repair found and split eight stale faces
- repair vertex and edge counts remained unchanged
- repaired face count increased by exactly eight
- no new zero-length edges, zero-area faces, duplicate faces, boundary changes, or overlinked-edge-count changes were introduced

The previous actual-collar Curvature Sync harness result remains documented, but standalone Vertex Inject and the repair script still require manual Blender 4.5 execution.

## Active problems

1. Exact Blender 4.5 installation and UI test are pending for Dev_v2.5.1.
2. Interactive undo/redo is unverified because background-mode undo is unavailable.
3. Real collar A/B/C selection and target-chain inference require immediate user validation.
4. The file-specific unsplit-face repair must be executed inside Blender 4.5 so its saved output remains Blender 4.5-compatible.
5. Bulk standalone injection and curvature-aware single injection are not yet exposed.
6. Curvature Sync still has unresolved-column and missing-Middle limitations.
7. Generalized embedded-edge repair is documented but not yet integrated into the add-on.
8. The full Dev_v2.5.1 source tree has not yet been imported into the final canonical repository source location.

## Next exact implementation step

Run `repair_collar_unsplit_faces.py` against the uploaded `Collar_DESIGN_v6 - Copy.blend` in Blender 4.5. Open the newly saved `_REPAIRED_UNSPLIT_FACES.blend` output and visually verify the eight repaired locations.

Then continue the urgent collar workflow:

1. test Edge / Vertex Inject on any remaining required A/B/C locations;
2. inspect D placement and C-D face splitting;
3. test undo/redo;
4. run Curvature Sync after the required correspondence vertices are present;
5. inspect topology and print-critical surfaces before slicing.

Patch only the required injector, Curvature Sync, or cleanup behavior in response to the Blender 4.5 result.

## Test status

- ZIP integrity and package layout: passed
- Python syntax: passed for all 45 add-on source files
- Blender Python 5.2 registration/unregistration: passed
- synthetic Vertex Inject topology test: passed
- Curvature Sync synthetic regression: passed
- exact-file unsplit-face repair under Blender Python 5.2: passed
- Blender 4.5 add-on runtime: not performed
- Blender 4.5 repair-script execution: not performed
- interactive undo/redo: not verified
- public release/update behavior: not modified or tested

## Known remaining issues

Dev_v2.5.1 and the collar repair script are urgent development tools, not public releases. Use them only on backups until Blender 4.5 manual validation is complete.
