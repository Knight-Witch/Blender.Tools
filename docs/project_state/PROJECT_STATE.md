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

- Current urgent build: `Dev_v2.5.2`
- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Based on supplied baseline: `Dev_v2.4.0`
- Supersedes: `Dev_v2.5.1`
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

- Established repository rules, architecture, documentation tracking, and non-breaking branch safeguards on `Blender_Dev`.
- Audited supplied Witch Tools, Quickbar, and Dev Modules baselines.
- Implemented Curvature Sync MVP as Dev_v2.5.0 and Auto-Aligned Vertex Inject as Dev_v2.5.1.
- Compared the user-supplied pre/post Curvature Sync collar files.
- Confirmed the successful curvature coordinates and diagnosed retained pre-existing cross-edges mapped to different canonical slots.
- Implemented **Replace Misaligned Column Edges** and produced Dev_v2.5.2.
- Updated feature state/roadmap, Witch Tools state/roadmap, build registry, compatibility, package documentation, and root/add-on notes.
- Preserved all public branches, Quickbar URLs, package identities, operator namespaces, assets, and external release locations.

## Current known-working state

For tested Dev_v2.5.2 operations under Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed;
- static package parsing passed for 45 Python files;
- actual collar processing completed across 26 selected chains;
- 520 vertices were injected and 1,324 moved;
- 96 misaligned existing column edges were replaced;
- 975 canonical column edges were created;
- zero column positions remained unresolved;
- resulting vertex coordinates exactly matched the successful Dev_v2.5.1 curvature result;
- no zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced;
- special-data rejection occurred during copied-BMesh preflight without real-mesh topology-count changes;
- save and reopen passed.

No public compatibility surface was modified.

## Active problems

1. Dev_v2.5.2 requires immediate user testing in Blender 4.5.
2. Interactive undo/redo could not be validated in background mode.
3. Final production topology, normals, and print-fit require visual inspection before slicing.
4. Only safe two-face interior misaligned edges are replaced; ambiguous or special-data cases abort.
5. Surplus chain vertices, automatic missing-Middle creation, and fully automatic chain discovery remain incomplete.
6. Vertex Inject remains active-object based and aborts on ambiguous forks.
7. Full canonical source import and source-derived UI/operator registries are pending.
8. Public Witch Tools distribution/update strategy remains unresolved.
9. Quickbar runtime/update-link testing and Witch Core source import remain pending.

## Next exact implementation step

Install Witch Tools Dev_v2.5.2 in Blender 4.5 and open `Collar_PRE-curvature_sync.blend`. Keep **Replace Misaligned Column Edges** enabled, run Analyze, then Apply. Inspect the corrected same-slot columns, intended curvature, normals, and print-critical surfaces. Test interactive undo/redo and report only any remaining Blender 4.5 or topology failures.

After the urgent print workflow is validated, import the complete Dev_v2.5.2 source into the canonical Witch Tools repository tree and generate UI/operator registries.

## Test status

- Static ZIP/package checks: passed
- Blender Python 5.2.0 LTS runtime checks: passed for tested operations
- Actual collar correspondence repair: passed in tested runtime
- Geometry-coordinate regression: passed
- Degeneracy/duplicate/boundary-count checks: passed
- Blender 4.5 runtime: not performed
- Interactive UI and undo/redo: not verified
- Public branches modified: no
- Quickbar URLs or public compatibility surfaces modified: no

## Known remaining issues

Dev_v2.5.2 is an urgent development build, not a public release. The uploaded source collar files remain unchanged. Use the pre-curvature backup and visually inspect all topology before printing.