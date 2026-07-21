# Curvature Sync State

Last updated: 2026-07-21

## Identity

- Feature family: Curvature Sync and Edge / Vertex Inject
- Canonical owner: Witch Tools
- Current implementation status: urgent MVP development build produced
- Current build: Witch Tools `Dev_v2.5.2`
- Target Blender version: `4.5`
- Development branch: `Blender_Dev`

## Current build

- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Package identity: `Witch_Tools_Dev`
- Supersedes: `Dev_v2.5.1`

## Implemented: Auto-Aligned Vertex Inject

- ordered A/B/C selection using Blender selection history
- A-B and B-C edge validation
- ideal relation `D = C + (A - B)`
- target-chain inference and strict ambiguous-fork rejection
- projected target-edge split and existing-vertex reuse
- default optional C-D shared-face connection/split
- copied-BMesh preflight
- shape-key and degenerate-face rejection
- lock, edit-zone, and captured-anchor remapping

## Implemented: Curvature Sync

- explicit A/M/Z capture per selected open chain
- circular XY/XZ/YZ fitting and exact middle-axis normalization
- equal segment counts on both sides of Middle
- multiple parallel chains and aligned multi-object Edit Mode
- missing-vertex injection and canonical column construction
- copied-BMesh preflight and protected-zone integration
- unresolved-column reporting instead of unsafe forced connections

## Dev_v2.5.2 correction: misaligned existing columns

The supplied post-run file confirmed that the curve coordinates were correct, but the previous build retained pre-existing cross-edges whose endpoints mapped to different canonical column slots. Those stale edges became diagonal after redistribution while new correct columns were also added.

Dev_v2.5.2 adds **Replace Misaligned Column Edges**:

- identifies existing cross-edges connecting different canonical slots;
- accepts only unambiguous two-face interior edges;
- dissolves those stale edges before canonical same-slot reconstruction;
- rejects A/Z boundary edges, non-two-face edges, Seam, Sharp, Crease, bevel/custom-data edges, and mixed-material or mixed-smoothing boundaries before real-mesh mutation;
- reports planned and completed replacement counts.

## Validation completed

Using Blender Python `5.2.0 LTS`:

- complete package syntax parse passed for 45 Python files;
- registration and unregistration passed;
- the supplied `Collar_PRE-curvature_sync.blend` processed 26 chains at 26 segments per side;
- 520 vertices were injected and 1,324 vertices were moved;
- 96 misaligned existing column edges were replaced;
- 975 canonical column edges were created;
- zero column positions remained unresolved;
- resulting vertex-coordinate multisets exactly matched the successful Dev_v2.5.1 curvature result;
- no zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced;
- material-index and flat/smooth face-state distributions remained consistent;
- a special-data edge test aborted during copied-BMesh preflight without changing real-mesh topology counts;
- save and reopen passed.

The collar files contain pre-existing wire, boundary, overlinked, and intersection conditions outside this correction. Dev_v2.5.2 did not add geometry-coordinate changes beyond the Dev_v2.5.1 result.

## Testing limitation

The automated runtime is Blender Python `5.2.0 LTS`, not Blender `4.5`. Blender 4.5 installation, panel rendering, interactive selection, normal undo/redo, and final production inspection remain pending user validation.

## Current limitations

- circular planar Curvature Sync only;
- explicit A/M/Z anchors and selected chains remain required;
- no automatic surplus-chain-vertex dissolution;
- only safe two-face interior misaligned edges are replaced;
- special edge/face data causes a strict abort rather than a destructive guess;
- standalone Vertex Inject remains active-object based and aborts on ambiguous forks.

## Next exact step

Open `Collar_PRE-curvature_sync.blend` in Blender 4.5 with Dev_v2.5.2 installed. Keep **Replace Misaligned Column Edges** enabled, run Analyze, then Apply Curvature Sync. Verify the clean column topology, interactive undo/redo, normals, and print-critical surfaces before saving or slicing.

After the urgent collar workflow is validated, import the full Dev_v2.5.2 source tree into the canonical Witch Tools repository location and generate source-derived UI/operator registries.