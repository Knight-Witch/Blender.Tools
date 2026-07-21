# Curvature Sync Roadmap

## Current implementation scope

### CS-BASE-001 — Import Witch Tools baseline

- Status: blocked
- Dependency: locate latest verified source artifact

### CS-VINJ-001 — Single Auto-Aligned Vertex Inject

- Status: planned
- Scope:
  - A/B/C selection order
  - calculate D
  - target edge resolution
  - edge split
  - optional/default C-D connect and face split
  - preserve attributes and normals
  - strict failure before mutation

### CS-VINJ-002 — Curvature-aware single inject

- Status: planned
- Dependency: CS-VINJ-001
- Scope: place C/D against an existing circular guide or A/M/Z frame rather than copying an unchanged world-space offset

### CS-PROT-001 — Protected-zone permission extension

- Status: planned
- Dependency: audit Vertex Lock
- Scope: position lock, fit exclusion, dissolve prohibition, boundary connect, adjacent face split

### CS-GROUP-001 — Repair-group data and preflight

- Status: planned
- Scope: objects, islands, ordered chains, master/followers, A/M/Z, center frame, protected zones, validation report

### CS-CURV-001 — Circular multi-chain curvature solve

- Status: planned
- Scope: shared center/axis/angular lattice, per-chain radius/height, even symmetrical spacing

### CS-BULK-001 — Bulk missing correspondence injection

- Status: planned
- Dependency: CS-VINJ-001 and CS-GROUP-001

### CS-XOBJ-001 — Multi-object synchronization

- Status: planned
- Dependency: CS-CURV-001 and CS-BULK-001
- Scope: aligned split print parts and separate islands

### CS-UI-001 — Witch Tools N-panel integration

- Status: planned
- Dependency: stable operators and tests

## Next release / later

### CS-PREVIEW-001 — Ghost/lattice preview

- Status: planned after core solve

### CS-CLEAN-001 — Safe surplus-vertex handling

- Status: deferred
- Default remains leave-and-select

### CS-VINJ-003 — Manual triangulated/local-frame inject

- Status: deferred
- Modal placement with axis/direction constraints

### CS-SPLINE-001 — Generic spline/non-circular repair

- Status: research
- Not first-version scope

### CS-AUTO-001 — Automatic chain and curved-region discovery

- Status: research
- Must remain conservative and abort on ambiguity

## Rejected for first version

- one-click automatic remesh
- silent dissolution of unmatched topology
- fitting based on every malformed vertex
- moving geometry outside A/Z
- allowing protected coordinates to drift
- Quickbar-first implementation

## Milestone exit criteria

### Prototype milestone

- single-object circular chains
- explicit chain selection and A/M/Z
- no missing topology
- preview and apply
- undo/redo and normals tests pass

### Alpha milestone

- missing correspondence injection
- multiple parallel chains
- protected zones
- synthetic fixture suite

### Beta milestone

- multiple objects/islands
- upper/lower print component synchronization
- performance and failure-path testing
- full Witch Tools UI

### Stable integration

- all acceptance criteria pass
- no known partial-destructive failures
- documentation and changelog complete
- Blender 4.5 verified
- additional compatibility only if actually tested