# Curvature Sync State

Last updated: 2026-07-21

## Identity

- Feature family: Curvature Sync and Edge / Vertex Inject
- Canonical owner: Witch Tools
- Current implementation status: urgent MVP development build produced
- Current build: Witch Tools `Dev_v2.5.1`
- Target Blender version: `4.5`
- Development branch: `Blender_Dev`

## Current build

Artifact:

`Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`

SHA-256:

`fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`

Package identity remains `Witch_Tools_Dev`.

## Implemented: Auto-Aligned Vertex Inject

- explicit ordered A, B, C vertex selection using Blender selection history
- requirement that A-B and B-C are existing edges
- ideal relation `D = C + (A - B)`
- target-chain inference from A in the B-to-C row direction
- straightest-continuation traversal with ambiguous-fork rejection
- projection of the ideal D relation onto an actual target-chain edge
- configurable projection tolerance
- existing-vertex reuse tolerance to prevent near-duplicates
- target-edge split when D is missing
- default optional C-D connect and shared-face split
- copied-BMesh preflight before real mutation
- shape-key rejection
- zero-area-face rejection
- Vertex Lock, Protected Edit Zone, and Curvature Sync anchor-index remapping after topology changes
- C and D left selected for inspection

## Implemented: Curvature Sync MVP

- explicit A / Middle / Z capture per selected chain
- open non-branching chain validation
- circular XY, XZ, and YZ fitting
- exact middle-axis normalization
- equal segment counts on both sides of Middle
- missing vertex injection and optional cross-column face construction
- multiple parallel chains and aligned objects
- copied-BMesh preflight
- Vertex Lock / Protected Edit Zone integration
- unresolved-column reporting instead of unsafe forced connections

## Validation completed

Using Blender Python `5.2.0 LTS`:

- complete package syntax parse passed for 45 Python files
- registration and unregistration passed
- synthetic Auto-Aligned Vertex Inject split the target edge at the exact calculated position
- synthetic C-D connection split one quad into two valid faces
- no zero-area faces were produced
- full Curvature Sync synthetic regression test passed after the Vertex Inject addition
- previous actual collar Curvature Sync test remains valid for Dev_v2.5.0 behavior

## Testing limitation

The available automated runtime is Blender Python `5.2.0 LTS`, not Blender `4.5`. Blender 4.5 installation, panel rendering, interactive selection behavior, and undo/redo remain pending user validation.

## Current limitations

- Auto-Aligned Vertex Inject currently operates on the active mesh object
- the user must select A, then B, then C individually; C must be active last
- A-B and B-C must be real mesh edges
- target-chain traversal aborts on ambiguous forks
- bulk standalone injection is not yet exposed
- Curvature Sync remains circular-planar and requires explicit A/M/Z anchors
- no surplus-vertex dissolution

## Next exact step

User-test Dev_v2.5.1 in Blender 4.5 on a backup collar file:

1. install and enable the package;
2. open Edit Tools > Edge / Vertex Inject;
3. select A, B, and C individually in that order;
4. run Inject Auto-Aligned Vertex with Connect & Split Face enabled;
5. inspect C-D, face winding, normals, and surrounding topology;
6. test interactive undo/redo;
7. report any chain-inference or projection error before proceeding to Curvature Sync.

After urgent user validation, import the complete source tree into the canonical Witch Tools development location and continue bulk correspondence and missing-middle work.
