# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current release / baseline recovery

### WT-BASE-001 — Import latest Witch Tools development baseline

- Status: active
- Priority: critical
- Current implementation baseline: Dev_v2.4.0 imported locally and used to produce Dev_v2.5.x builds
- Remaining deliverable: canonical repository source import with hash, version, package name, branch ancestry, and Blender target recorded
- Acceptance: installs in Blender 4.5 and matches recorded artifact contents

### WT-BASE-002 — Build current UI and operator registries

- Status: planned
- Dependency: canonical WT-BASE-001 source import
- Deliverable: `UI_MAP.md`, `FEATURE_REGISTRY.md`, and `OPERATOR_REGISTRY.md`

### WT-BASE-003 — Audit public/update compatibility

- Status: planned
- Dependency: WT-BASE-001
- Deliverable: exact URLs, package identifiers, external references, and upgrade behavior

## Current topology development project

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: active MVP; Blender 4.5 user validation pending
- Current build: Dev_v2.5.1
- Priority: high
- Scope: select source A/B and target C; inject D; connect C-D; split original face into two; preserve winding, normals, material, smoothing, and edge attributes
- Feature relationship: prerequisite for Curvature Sync correspondence repair

### WT-VINJ-002 — Manual Vertex Inject with local triangulated movement

- Status: deferred
- Scope: modal placement using a locally derived frame and selectable axis restrictions

### WT-VINJ-003 — Bulk Missing Correspondence Injection

- Status: partially implemented inside Curvature Sync; standalone workflow planned
- Scope: propagate missing vertices and connecting edges across multiple parallel chains
- Dependency: WT-VINJ-001

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: active MVP; Blender 4.5 user validation pending
- Current build: Dev_v2.5.1
- Priority: high
- Scope: A/M/Z anchors, shared angular lattice, multiple parallel chains, protected straight spans, multiple objects/islands, matching split print components
- Feature packet: `/docs/features/curvature_sync/`

### WT-CURV-002 — Cross-object column synchronization

- Status: MVP implemented; production validation pending
- Dependency: WT-CURV-001 and WT-VINJ-003

### WT-CURV-003 — Generic spline/non-circular mode

- Status: research
- Not current scope. Circular planar arcs are the deterministic first target.

### WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces

- Status: planned for Witch Tools integration
- Priority: high cleanup utility
- Production discovery: creating edges with `F` can leave zero-face wire edges lying across an older unsplit face
- Required behavior:
  - detect wire edges whose endpoints belong to exactly one existing face
  - split that face along the existing edge instead of deleting the edge network
  - preserve material, smoothing, loop/custom data, winding, and normals
  - reject ambiguous candidates rather than guessing
  - operate transactionally and report unresolved loose edges separately
- Current reference case: `Collar_DESIGN_v6 - Copy.blend`
- Ad hoc result: exact-file repair script identified two stale face splits on `COLLAR - UPPER.002` and six on `RIGHT EXTENSION`; Blender 4.5 user execution remains pending
- Future UI location: Edit Tools > Cleanup / Topology Repair

## Protection infrastructure

### WT-PROT-001 — Audit existing Vertex Lock implementation

- Status: complete for the Dev_v2.5.x topology MVP

### WT-PROT-002 — Protected/ignored zone permissions

- Status: active partial implementation
- Required distinctions:
  - block movement
  - block deletion/dissolve
  - exclude from curvature fitting
  - allow boundary connection/split when explicitly permitted

## Later work

General BG3, modeling, weighting, cleanup, and print-oriented roadmap items will be imported from existing project documents and dev sources. They must not be reconstructed incompletely from memory.

## Deferred/rejected policy

No discussed idea is automatically current-release scope. New ideas must be placed in the appropriate section with status and dependencies.
