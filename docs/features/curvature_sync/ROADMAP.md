# Curvature Sync Roadmap

Last updated: 2026-07-21

## Current urgent MVP

### CS-BASE-001 — Inspect and establish Witch Tools baseline

- Status: completed for implementation; canonical repository source import still pending
- Baseline used: Witch Tools `Dev_v2.4.0`
- Resulting build: Witch Tools `Dev_v2.5.0`

### CS-CURV-001 — Circular multi-chain curvature solve

- Status: MVP implemented; Blender 4.5 user validation pending
- Implemented:
  - explicit A/M/Z per selected chain
  - XY/XZ/YZ circular fitting
  - exact middle-axis normalization
  - equal segment count on both sides of Middle
  - multiple parallel chains
  - preservation of A/Z transition anchors
- Remaining:
  - persistent repair groups
  - explicit shared-center/master-chain controls
  - automatic missing-Middle creation
  - broader non-circular support

### CS-BULK-001 — Bulk missing correspondence injection

- Status: MVP partially implemented
- Implemented:
  - canonical slot count from selected maximum or custom per-side value
  - missing vertex injection by selected-edge split
  - optional corresponding column connection through shared faces
  - unresolved-column reporting
- Remaining:
  - automatic chain/correspondence discovery
  - standalone reusable injection backend
  - surplus-vertex analysis/dissolution
  - richer preflight diagnostics and preview

### CS-XOBJ-001 — Multi-object synchronization

- Status: MVP implemented; user validation pending
- Implemented:
  - multi-object Edit Mode participation
  - one shared target segment count across selected objects
  - actual upper/lower collar interface alignment test
- Remaining:
  - persistent master/follower group data
  - transform mismatch diagnostics
  - multiple island-specific controls

### CS-PROT-001 — Protected-zone permissions

- Status: MVP partially implemented
- Implemented:
  - enabled Vertex Lock groups respected
  - locked A/Z anchors allowed
  - already-correct locked Middle allowed
  - locked non-anchor interior vertices abort before mutation
  - lock/edit-zone/anchor indices remapped after topology injection
  - topology may connect to fixed boundary anchors
- Remaining:
  - dedicated Curvature Ignore Zone UI
  - per-operation permission matrix
  - explicit protected topology/dissolve policies

### CS-UI-001 — Witch Tools N-panel integration

- Status: MVP implemented
- Current UI:
  - Capture A / Middle / Z
  - clear anchors
  - plane selection
  - selected-maximum or custom segment count
  - exact-middle normalization toggle
  - inject missing toggle
  - build missing columns toggle
  - respect locks toggle
  - Analyze and Apply
- Remaining:
  - preview visualization
  - anchor/lattice overlays
  - richer per-chain diagnostics
  - repair-group persistence

### CS-TEST-001 — MVP validation

- Status: partially completed
- Completed:
  - full syntax/package audit
  - Blender Python 5.2.0 LTS registration/unregistration
  - synthetic mismatch repair
  - protected-anchor and locked-interior behavior
  - invalid branched selection without mutation
  - actual two-object collar repair
  - save/reopen and topology validation
- Pending:
  - Blender 4.5 installation and UI
  - interactive undo/redo
  - explicit manual-selection run by the user
  - production print-part inspection

## Next exact patch scope

1. User-test Dev_v2.5.0 in Blender 4.5 on a backup collar file.
2. Patch installation, selection, UI, topology, or unresolved-column failures only as required.
3. Add automatic creation of a missing exact Middle vertex/column.
4. Improve shared-center/master-chain controls if user-selected corresponding chains fail to align.
5. Add clearer unresolved-column selection/diagnostics.

## Later development

### CS-VINJ-001 — Standalone Auto-Aligned Vertex Inject

- Status: planned
- Note: bulk Curvature Sync contains an internal edge-split primitive, but the independently usable A/B/C → D operator remains unimplemented.
- Scope:
  - A/B/C selection order
  - ideal D calculation
  - target-edge resolution
  - edge split
  - default C-D connect and face split
  - attribute/normal preservation
  - strict failure before mutation

### CS-VINJ-002 — Curvature-aware single inject

- Status: planned
- Dependency: standalone CS-VINJ-001

### CS-GROUP-001 — Persistent repair-group data and preflight

- Status: planned
- Scope: objects, islands, ordered chains, master/followers, A/M/Z, center frame, protected zones, validation report

### CS-PREVIEW-001 — Ghost/lattice preview

- Status: planned after urgent MVP stabilization

### CS-CLEAN-001 — Safe surplus-vertex handling

- Status: deferred
- Default remains leave existing surplus topology unchanged

### CS-VINJ-003 — Manual triangulated/local-frame inject

- Status: deferred

### CS-SPLINE-001 — Generic spline/non-circular repair

- Status: research

### CS-AUTO-001 — Automatic chain and curved-region discovery

- Status: research
- Must remain conservative and abort on ambiguity

## Rejected for current MVP

- one-click automatic remesh
- silent dissolution of unmatched topology
- fitting based on every malformed vertex
- moving geometry outside A/Z
- allowing protected coordinates to drift
- Quickbar-first implementation

## Milestone status

### MVP development build

- Produced: Dev_v2.5.0
- Runtime-tested environment: Blender Python 5.2.0 LTS
- Blender 4.5 verification: pending

### Alpha exit criteria

- user completes collar workflow in Blender 4.5
- interactive undo/redo verified
- no partial destructive failures
- missing-Middle workflow implemented
- unresolved topology clearly selected/reported

### Stable integration

- all acceptance criteria pass
- Blender 4.5 verified
- source imported canonically
- documentation and changelog complete
- public release/update compatibility separately audited