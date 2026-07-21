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
- Automated runtime tested: Blender Python `5.2.0 LTS`
- Blender 4.5 installed production workflow: user-validated for Curvature Sync Apply on the supplied collar

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
- User installed Dev_v2.5.2 in Blender 4.5, ran the corrected Curvature Sync workflow on the supplied pre-curvature collar file, and reported that the result worked beautifully.
- Updated feature, build, compatibility, project-state, roadmap, and notes documentation.
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

Under the user's Blender 4.5 environment:

- the add-on installed and the Curvature Sync UI was usable;
- the saved A/M/Z and chain selection workflow restored from the supplied file;
- Analyze/Apply completed on the production collar;
- the user visually confirmed that the corrected curvature and column topology worked beautifully.

Pre-existing wire, boundary, overlinked, and intersection conditions remain in the collar files. The patch corrects column correspondence and does not claim to clean unrelated pre-existing topology.

## Active problems

1. Interactive undo/redo has not yet been reported by the user.
2. Formal normals, face-winding, manifold, and print-fit inspection remain pending before slicing.
3. Only safe two-face interior misaligned edges are replaced; special-data and ambiguous cases abort.
4. Surplus chain vertices and automatic missing-Middle creation remain outside the current MVP.
5. Standalone Vertex Inject remains active-object based and aborts on ambiguous forks.
6. The full Dev_v2.5.2 source tree has not yet been imported into the final canonical repository source location.
7. Source-derived UI and operator registries remain pending.

## Next exact implementation step

1. Save the successful corrected collar under a new versioned filename.
2. Test interactive undo/redo in Blender 4.5.
3. Inspect normals, face winding, non-manifold selections, and print-critical surfaces before slicing.
4. Record any remaining unrelated topology problems separately from Curvature Sync.
5. Import the complete Dev_v2.5.2 source into the canonical Witch Tools repository tree and generate UI/operator registries.

## Test status

- ZIP integrity and package layout: passed
- Python syntax: passed for all 45 source files
- Blender Python 5.2 registration/unregistration: passed
- actual collar correspondence repair: passed in automated runtime
- geometry-coordinate regression against Dev_v2.5.1: passed
- degeneracy/duplicate/boundary-count checks: passed
- special-data cancellation without real-mesh mutation: passed
- save/reopen: passed
- Blender 4.5 installed Curvature Sync production run: user-reported passed
- Blender 4.5 visual curvature/column result: user-reported passed
- interactive undo/redo: not yet reported
- formal normals/manifold/print-fit validation: pending
- public release/update behavior: not modified or tested

## Known remaining issues

Dev_v2.5.2 remains a development build rather than a public release. The primary collar repair workflow is now user-validated in Blender 4.5, but final print preparation still requires topology and surface inspection.
