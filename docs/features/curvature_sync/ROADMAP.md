# Curvature Sync Roadmap

Last updated: 2026-07-21

## Current urgent MVP

### CS-BASE-001 — Establish Witch Tools baseline

- Status: completed for implementation; canonical repository source import remains pending
- Baseline used: Witch Tools `Dev_v2.4.0`
- Current derivative build: Witch Tools `Dev_v2.5.1`

### CS-VINJ-001 — Standalone Auto-Aligned Vertex Inject

- Status: MVP implemented; Blender 4.5 user validation pending
- Implemented:
  - ordered A/B/C selection
  - A-B and B-C edge validation
  - ideal D calculation from `C + (A - B)`
  - target-chain inference and straightest-continuation traversal
  - ambiguous fork rejection
  - projected target-edge split
  - existing-vertex reuse
  - default C-D connect and shared-face split
  - copied-BMesh preflight
  - lock/edit-zone/anchor remapping
  - shape-key and degenerate-face rejection
- Remaining:
  - bulk standalone injection
  - curvature-guide-aware single injection
  - richer preview/diagnostics
  - multiple-object single-inject workflow

### CS-CURV-001 — Circular multi-chain curvature solve

- Status: MVP implemented; Blender 4.5 user validation pending
- Implemented:
  - explicit A/M/Z per selected chain
  - XY/XZ/YZ circular fitting
  - exact middle-axis normalization
  - equal per-side segment count
  - multiple parallel chains
  - transition-anchor preservation
- Remaining:
  - persistent repair groups
  - shared-center/master-chain controls
  - automatic missing-Middle creation
  - generalized non-circular support

### CS-BULK-001 — Bulk missing correspondence injection

- Status: Curvature Sync internal MVP partially implemented
- Implemented:
  - canonical target slots
  - selected-chain edge splitting
  - optional corresponding-column construction
  - unresolved-column reporting
- Remaining:
  - automatic chain/correspondence discovery
  - reuse of the new standalone Vertex Inject backend
  - surplus-vertex analysis
  - richer preflight and preview

### CS-XOBJ-001 — Multi-object synchronization

- Status: MVP implemented; user validation pending
- Implemented:
  - multi-object Edit Mode participation
  - shared target segment count
  - upper/lower collar interface alignment test
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
  - protected dissolve policies

### CS-UI-001 — Witch Tools N-panel integration

- Status: MVP implemented
- Current UI:
  - Edge / Vertex Inject section
  - Connect & Split Face toggle
  - projection and existing-vertex tolerances
  - Curvature Sync A/M/Z controls and settings
- Remaining:
  - preview overlays
  - richer diagnostics
  - persistent repair-group UI

### CS-TEST-001 — MVP validation

- Status: partially completed
- Completed:
  - package syntax and registration tests
  - synthetic standalone vertex injection
  - synthetic face split
  - Curvature Sync regression test
  - prior protected-anchor and actual collar harness tests
- Pending:
  - Blender 4.5 installation and panel rendering
  - real collar manual A/B/C injection
  - interactive undo/redo
  - production topology and print-fit inspection

## Next exact patch scope

1. User-test Dev_v2.5.1 Vertex Inject in Blender 4.5.
2. Patch only selection-history, chain-inference, projection, face-split, or undo failures required by that test.
3. Use Vertex Inject to prepare the collar anchors/topology required by Curvature Sync.
4. User-test Curvature Sync on the repaired topology.
5. Add automatic missing-Middle and bulk correspondence improvements after the urgent print workflow succeeds.

## Later development

### CS-VINJ-002 — Curvature-aware single inject

- Status: planned
- Dependency: Dev_v2.5.1 user validation

### CS-GROUP-001 — Persistent repair-group data

- Status: planned

### CS-PREVIEW-001 — Ghost/lattice preview

- Status: planned after urgent MVP stabilization

### CS-CLEAN-001 — Safe surplus-vertex handling

- Status: deferred
- Default remains leave existing surplus topology unchanged

### CS-VINJ-003 — Manual/local-frame inject

- Status: deferred

### CS-SPLINE-001 — Generic spline/non-circular repair

- Status: research

### CS-AUTO-001 — Automatic chain and curved-region discovery

- Status: research
- Must remain conservative and abort on ambiguity

## Rejected for current MVP

- one-click automatic remesh
- silent topology dissolution
- fitting from every malformed vertex
- movement outside A/Z
- protected-coordinate drift
- Quickbar-first implementation

## Milestone status

### Urgent MVP development build

- Produced: Dev_v2.5.1
- Runtime-tested environment: Blender Python 5.2.0 LTS
- Blender 4.5 verification: pending

### Alpha exit criteria

- standalone Vertex Inject succeeds on the actual collar
- user completes collar Curvature Sync workflow in Blender 4.5
- interactive undo/redo verified
- no partial destructive failures
- unresolved topology clearly reported

### Stable integration

- acceptance criteria pass
- Blender 4.5 verified
- source imported canonically
- documentation and changelog complete
- public compatibility separately audited
