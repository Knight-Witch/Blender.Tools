# Curvature Sync Roadmap

Last updated: 2026-07-21

## Current urgent MVP

### CS-BASE-001 — Establish Witch Tools baseline

- Status: completed for implementation; canonical repository source import remains pending
- Baseline used: Witch Tools `Dev_v2.4.0`
- Current derivative build: Witch Tools `Dev_v2.5.2`

### CS-VINJ-001 — Standalone Auto-Aligned Vertex Inject

- Status: MVP implemented; actual production-topology validation remains pending
- Implemented:
  - ordered A/B/C selection
  - A-B and B-C edge validation
  - ideal D calculation from `C + (A - B)`
  - target-chain inference and strict fork rejection
  - projected target-edge split and existing-vertex reuse
  - default C-D shared-face connection/split
  - copied-BMesh preflight
  - lock/edit-zone/anchor remapping
  - shape-key and degenerate-face rejection
- Remaining:
  - production collar standalone-inject confirmation
  - bulk standalone injection
  - curvature-guide-aware single injection
  - richer preview and diagnostics
  - multi-object single-inject workflow

### CS-CURV-001 — Circular multi-chain curvature solve

- Status: production workflow user-validated in Blender 4.5; broader acceptance testing remains
- Implemented:
  - explicit A/M/Z per selected chain
  - XY/XZ/YZ circular fitting
  - exact middle-axis normalization
  - equal per-side segment count
  - multiple parallel chains and aligned objects
  - transition-anchor preservation
  - successful production collar Analyze/Apply in Blender 4.5
- Remaining:
  - interactive undo/redo confirmation
  - formal normals/manifold/print-fit inspection
  - persistent repair groups
  - shared-center/master-chain controls
  - automatic missing-Middle creation
  - generalized non-circular support

### CS-BULK-001 — Bulk correspondence repair

- Status: production collar workflow user-validated inside Curvature Sync; standalone workflow remains planned
- Implemented:
  - canonical target slots
  - selected-chain edge splitting
  - corresponding-column construction
  - unresolved-column reporting
  - detection of existing cross-edges mapped to different canonical slots
  - explicit **Replace Misaligned Column Edges** toggle
  - safe two-face interior-edge dissolution and canonical same-slot reconstruction
  - strict rejection of unsafe boundary, non-two-face, special-data, mixed-material, and mixed-smoothing edges
  - zero unresolved positions in the automated production-collar run
- Remaining:
  - automatic chain/correspondence discovery
  - reuse of the standalone Vertex Inject backend
  - surplus-chain-vertex analysis
  - richer preflight visualization

### CS-XOBJ-001 — Multi-object synchronization

- Status: production collar workflow user-validated in Blender 4.5
- Implemented:
  - multi-object Edit Mode participation
  - shared target segment count
  - upper/lower collar interface alignment
  - user-confirmed successful production result
- Remaining:
  - persistent master/follower data
  - transform mismatch diagnostics
  - island-specific controls

### CS-PROT-001 — Protected-zone permissions

- Status: MVP partially implemented
- Implemented:
  - enabled Vertex Lock groups respected
  - fixed boundary anchors may receive topology connections
  - locked moving interiors abort before mutation
  - lock/edit-zone/anchor indices remapped after injection
- Remaining:
  - dedicated Curvature Ignore Zone UI
  - explicit per-operation permission matrix
  - protected dissolve policies beyond strict current rejection

### CS-UI-001 — Witch Tools N-panel integration

- Status: primary Curvature Sync workflow user-validated in Blender 4.5
- Current UI:
  - Edge / Vertex Inject controls
  - Curvature Sync A/M/Z controls
  - plane and segment controls
  - Inject Missing Vertices
  - Build Missing Column Edges
  - Replace Misaligned Column Edges
  - Respect Vertex Locks
  - Analyze and Apply
- Remaining:
  - preview overlays
  - richer diagnostics
  - persistent repair-group UI

### CS-TEST-001 — MVP validation

- Status: primary production workflow passed; broader acceptance testing remains
- Completed under Blender Python 5.2.0 LTS:
  - package syntax and registration tests
  - synthetic standalone vertex injection and face split
  - Curvature Sync regression
  - protected-anchor and failure-without-mutation tests
  - actual supplied pre/post collar comparison
  - 96-edge misaligned-column replacement
  - exact vertex-coordinate regression against the successful Dev_v2.5.1 result
  - topology-degeneracy, duplicate, boundary-count, save/reopen, and special-data cancellation checks
- Completed in the user's Blender 4.5 environment:
  - add-on installation sufficient for the workflow
  - Curvature Sync panel and saved anchor/selection access
  - production collar Analyze/Apply
  - visible curvature and corrected same-slot column topology confirmation
- Pending:
  - interactive undo/redo
  - formal normals and face-winding inspection
  - manifold and print-fit/slicer validation
  - standalone Vertex Inject confirmation on the actual production topology

## Next exact patch scope

1. Do not change the successful Curvature Sync geometry or column-replacement behavior without a reproduced defect.
2. Record interactive undo/redo and final topology/print inspection results.
3. Patch only confirmed remaining failures.
4. Import the complete Dev_v2.5.2 source into the canonical Witch Tools repository tree.
5. Generate source-derived UI, feature, and operator registries.

## Later development

### CS-VINJ-002 — Curvature-aware single inject

- Status: planned

### CS-GROUP-001 — Persistent repair-group data

- Status: planned

### CS-PREVIEW-001 — Ghost/lattice preview

- Status: planned after urgent MVP stabilization

### CS-CLEAN-001 — Safe surplus-vertex handling

- Status: deferred
- Default remains leave surplus chain vertices unchanged and report/select them.

### CS-VINJ-003 — Manual/local-frame inject

- Status: deferred

### CS-SPLINE-001 — Generic spline/non-circular repair

- Status: research

### CS-AUTO-001 — Automatic chain and curved-region discovery

- Status: research
- Must remain conservative and abort on ambiguity.

## Rejected for current MVP

- one-click automatic remesh
- silent or unreported topology dissolution
- fitting from every malformed vertex
- movement outside A/Z
- protected-coordinate drift
- Quickbar-first implementation

The explicit Dev_v2.5.2 column-replacement toggle is not silent dissolution: it preflights, reports a count, accepts only safe two-face interior edges, and aborts on ambiguous or protected/special-data cases.

## Milestone status

### Urgent MVP development build

- Produced: Dev_v2.5.2
- Automated runtime-tested environment: Blender Python 5.2.0 LTS
- Primary Blender 4.5 production workflow: user-reported passed

### Alpha exit criteria

- Vertex Inject succeeds on the actual collar where still required: pending
- user completes Curvature Sync with corrected column topology in Blender 4.5: passed
- interactive undo/redo verified: pending
- no partial destructive failures: passed for automated tested paths
- unresolved topology clearly reported: passed in the current workflow
- formal print-preparation inspection: pending

### Stable integration

- acceptance criteria pass
- Blender 4.5 broader verification complete
- source imported canonically
- documentation and changelog complete
- public compatibility separately audited
