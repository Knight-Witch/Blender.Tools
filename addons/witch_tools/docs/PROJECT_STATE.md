# Witch Tools Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit
- Default target Blender version: 4.5
- Development package identity: `Witch_Tools_Dev`

## Current development build

- Version: `Dev_v2.5.2`
- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Package folder: `Witch_Tools_Dev`
- Declared Blender target: `4.5.0`
- Python source files: 45
- PNG assets: 6
- Generated cache files: none
- Static Python syntax audit: passed
- Runtime environment tested: Blender Python `5.2.0 LTS`
- Exact Blender 4.5 runtime: pending user test

Dev_v2.5.2 was produced from Dev_v2.5.1 without changing package identity, existing operator identifiers, assets, or the Witch Tools footer URL.

## Current implementation

Dev_v2.5.2 retains:

- Auto-Aligned Vertex Inject with ordered A/B/C selection, target-edge projection, optional C-D face split, and copied-BMesh preflight;
- Curvature Sync circular A/M/Z multi-chain and multi-object repair;
- Vertex Lock / Protected Edit Zone integration and reference remapping;
- the exact curve-coordinate result produced by Dev_v2.5.1 on the supplied collar.

Dev_v2.5.2 adds Curvature Sync > **Replace Misaligned Column Edges**:

- detects existing cross-edges whose endpoints map to different canonical slots;
- accepts only safe two-face interior edges;
- dissolves stale edges and rebuilds correct same-slot columns;
- rejects boundary, non-two-face, Seam, Sharp, Crease, bevel/custom-data, mixed-material, or mixed-smoothing edges before mutation;
- reports planned/replaced counts in Analyze and Apply.

## Last completed work

- Compared `Collar_PRE-curvature_sync.blend` and `Collar_POST-curvature_sync.blend`.
- Confirmed the curvature math and vertex positions were successful.
- Diagnosed 96 retained pre-existing cross-edges mapped to different canonical slots: 81 on `RIGHT EXTENSION` and 15 on `COLLAR - UPPER.002`.
- Implemented safe misaligned-column replacement and packaged Dev_v2.5.2.
- Updated package README, quick start, changelog, notes, compatibility, feature state, roadmap, build registry, and project-state documentation.
- Preserved the prior exact-file unsplit-face repair utility as separate work; no unrelated cleanup system was refactored.

## Current known-working state

Under Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed;
- package syntax passed for all 45 Python files;
- the actual pre-curvature collar processed 26 selected chains at 26 segments per side;
- 520 vertices were injected;
- 1,324 vertices were moved;
- 96 misaligned existing column edges were replaced;
- 975 canonical column edges were created;
- zero column positions remained unresolved;
- vertex-coordinate multisets exactly matched the successful Dev_v2.5.1 post-curvature file;
- no zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced;
- material index and face smoothing distributions remained consistent;
- special-data edge rejection occurred during copied-BMesh preflight without real-mesh topology-count changes;
- save and reopen passed.

Pre-existing wire, boundary, overlinked, and intersection conditions remain in the collar files. The patch corrects column correspondence and does not claim to clean unrelated pre-existing topology.

## Active problems

1. Exact Blender 4.5 installation and UI testing are pending.
2. Interactive undo/redo remains unverified because the automated runtime is background Blender Python 5.2.0 LTS.
3. The user must visually inspect the corrected production topology before slicing/printing.
4. Only safe two-face interior misaligned edges are replaced; special-data and ambiguous cases abort.
5. Surplus chain vertices and automatic missing-Middle creation remain outside the current MVP.
6. Standalone Vertex Inject remains active-object based and aborts on ambiguous forks.
7. The full Dev_v2.5.2 source tree has not yet been imported into the final canonical repository source location.
8. Source-derived UI and operator registries remain pending.

## Next exact implementation step

Install Dev_v2.5.2 in Blender 4.5 and reopen `Collar_PRE-curvature_sync.blend`. Keep **Replace Misaligned Column Edges** enabled, run Analyze, then Apply Curvature Sync. Verify:

1. the reported misaligned-edge plan;
2. clean same-slot column topology instead of retained diagonals;
3. unchanged intended curvature;
4. normals and face winding;
5. interactive undo and redo;
6. print-critical surfaces before slicing.

Patch only failures found in that Blender 4.5 test. After the urgent print workflow is validated, import the complete Dev_v2.5.2 source into the canonical Witch Tools repository tree and generate UI/operator registries.

## Test status

- ZIP integrity and package layout: passed
- Python syntax: passed for all 45 source files
- Blender Python 5.2 registration/unregistration: passed
- actual collar correspondence repair: passed in tested runtime
- geometry-coordinate regression against Dev_v2.5.1: passed
- degeneracy/duplicate/boundary-count checks: passed
- special-data cancellation without real-mesh mutation: passed
- save/reopen: passed
- Blender 4.5 runtime: not performed
- interactive undo/redo: not verified
- public release/update behavior: not modified or tested

## Known remaining issues

Dev_v2.5.2 is an urgent development build, not a public release. Use it on the pre-curvature backup and inspect the result before printing.