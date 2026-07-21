# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current release / baseline recovery

### WT-BASE-001 — Import latest Witch Tools development baseline

- Status: blocked pending artifact location
- Priority: critical
- Deliverable: unchanged source import with hash, version, package name, branch ancestry, and Blender target recorded
- Acceptance: installs in Blender 4.5 and matches recorded artifact contents

### WT-BASE-002 — Build current UI and operator registries

- Status: planned
- Dependency: WT-BASE-001
- Deliverable: `UI_MAP.md`, `FEATURE_REGISTRY.md`, and `OPERATOR_REGISTRY.md`

### WT-BASE-003 — Audit public/update compatibility

- Status: planned
- Dependency: WT-BASE-001
- Deliverable: exact URLs, package identifiers, external references, and upgrade behavior

## Current topology development project

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: specification
- Priority: high
- Scope: select source A/B and target C; inject D; connect C-D; split original face into two; preserve winding, normals, material, smoothing, and edge attributes
- Feature relationship: prerequisite for Curvature Sync correspondence repair

### WT-VINJ-002 — Manual Vertex Inject with local triangulated movement

- Status: deferred
- Scope: modal placement using a locally derived frame and selectable axis restrictions

### WT-VINJ-003 — Bulk Missing Correspondence Injection

- Status: planned
- Scope: propagate missing vertices and connecting edges across multiple parallel chains
- Dependency: WT-VINJ-001

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: specification
- Priority: high
- Scope: A/M/Z anchors, shared angular lattice, multiple parallel chains, protected straight spans, multiple objects/islands, matching split print components
- Feature packet: `/docs/features/curvature_sync/`

### WT-CURV-002 — Cross-object column synchronization

- Status: planned
- Dependency: WT-CURV-001 and WT-VINJ-003

### WT-CURV-003 — Generic spline/non-circular mode

- Status: research
- Not current scope. Circular planar arcs are the deterministic first target.

## Protection infrastructure

### WT-PROT-001 — Audit existing Vertex Lock implementation

- Status: blocked pending baseline import

### WT-PROT-002 — Protected/ignored zone permissions

- Status: planned
- Required distinctions:
  - block movement
  - block deletion/dissolve
  - exclude from curvature fitting
  - allow boundary connection/split when explicitly permitted

## Later work

General BG3, modeling, weighting, cleanup, and print-oriented roadmap items will be imported from existing project documents and dev sources. They must not be reconstructed incompletely from memory.

## Deferred/rejected policy

No discussed idea is automatically current-release scope. New ideas must be placed in the appropriate section with status and dependencies.