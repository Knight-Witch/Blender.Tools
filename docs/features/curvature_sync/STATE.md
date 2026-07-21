# Curvature Sync State

Last updated: 2026-07-21

## Identity

- Feature: Curvature Sync
- Canonical owner: Witch Tools
- Current implementation status: MVP development build produced
- Current feature build: Witch Tools `Dev_v2.5.0`
- Target Blender version: `4.5`
- Development branch: `Blender_Dev`

## Current implementation

The first functional circular Curvature Sync MVP has been implemented against the user-supplied Witch Tools `Dev_v2.4.0` baseline and packaged as:

`Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`

Implemented behavior:

- explicit A / Middle / Z capture per selected chain
- automatic selection clearing after anchor capture
- open non-branching selected-chain validation
- XY, XZ, and YZ circular fitting
- exact middle-axis normalization using the captured Middle point to select the apex side
- equal segment counts from A to Middle and Middle to Z
- Match Selected Maximum and Custom Per Side count modes
- missing-vertex injection by selected-edge splitting
- optional missing cross-column edge construction through shared faces
- multiple parallel chains
- multiple aligned objects in multi-object Edit Mode
- copied-BMesh preflight before real mutation
- Vertex Lock and Protected Edit Zone integration
- stored lock, edit-zone, and anchor-index remapping after injection
- shape-key injection rejection
- unresolved-column reporting instead of forced unsafe connections
- local normal update and destructive edit-mesh update where topology changes

## Validation completed

### Static

- Complete package Python syntax parse: passed
- Package root and install folder preserved as `Witch_Tools_Dev`
- Cache/generated Python files excluded from distribution

### Synthetic runtime test

Using Blender Python `5.2.0 LTS`:

- two concentric chains with mismatched segment counts
- two missing vertices injected
- two missing column edges created
- original two n-gon faces split into four valid faces
- no zero-length edges
- no zero-area faces
- expected mathematical inner-arc positions confirmed
- invalid branched selection rejected without geometry-count changes

### Vertex Lock / Protected Zone runtime test

- locked A/Z anchors accepted
- already-correct locked Middle anchors accepted
- lock data and captured anchor indices preserved after injection
- locked non-anchor interior vertex rejected before mutation

### Actual collar runtime test

Input: `Collar_Blender_DEV.blend`

- objects processed: 2
- selected chains processed by the test harness: 21
- target segments per side: 27
- vertices injected: 480
- vertices moved: 1,113
- column edges created: 747
- unresolved column positions: 41, reported and not forced
- lower object remained fully manifold
- no zero-length edges, duplicate edges, zero-area faces, or invalid faces were introduced
- no new 3D interior edge intersections were introduced
- pre-existing upper-object non-manifold/intersection conditions remained unchanged
- matching upper/lower outer interface curves aligned within floating-point tolerance after the same run
- save and reopen succeeded

## Testing limitation

The test container provides Blender Python `5.2.0 LTS`, not Blender `4.5`. Exact Blender 4.5 installation, interactive UI, and normal interactive undo/redo testing remain required before this build is treated as verified for release.

## Current MVP limitations

- circular planar arcs only
- one existing A, Middle, and Z reference required per chain
- no surplus-vertex dissolution
- column construction only where corresponding vertices can safely connect through a shared face
- unresolved positions require manual review
- automatic chain discovery and automatic missing-Middle creation are not implemented
- generalized spline/non-circular fitting is deferred

## Next exact step

User-test the `Dev_v2.5.0` package in Blender 4.5 on a backup copy of the collar file. Record:

- installation and registration result
- panel rendering
- Analyze result from explicit manual selections
- Apply result
- interactive undo/redo
- whether the intended upper/lower interface chains align
- unresolved positions or topology failures requiring the next patch

After user validation, import the full `Dev_v2.5.0` source tree into the canonical Witch Tools development location on `Blender_Dev` and continue the automatic correspondence / missing-middle workflow.