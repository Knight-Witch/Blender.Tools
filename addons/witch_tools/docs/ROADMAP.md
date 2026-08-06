# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate

### WT-ALIGN-001 — Align Vertices / Edges / Faces

- Status: active candidate in Witch Tools `Dev_v2.8.0`; Blender 4.5 validation pending
- Priority: urgent/high
- Feature packet: `/docs/features/align_selection/`
- Target Blender: `4.5.0`
- Candidate artifact SHA-256: `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`
- Implemented:
  - parent anchor capture from vertex, edge, face, and mixed selections;
  - Active Element and Median references;
  - world X/Y/Z matching with explicit coordinate masks;
  - arbitrary Custom Guide start/end coordinates;
  - custom-frame matching and projection to guide line;
  - free movement and straight captured slide rails;
  - one-to-all and explicit paired-by-rail relationships;
  - rigid relative-shape preservation;
  - whole-selection and per-island grouping;
  - rail extent clamping;
  - multi-object world/local coordinate conversion;
  - Vertex Lock, stale capture, shape-key, transform, rail, and ambiguity preflight;
  - non-mutating Analyze and transaction-first Apply.
- Remaining:
  - Blender 4.5 UI and registration validation;
  - screenshot-case geometry tests;
  - undo/redo and save/reopen;
  - multi-object and failure-rollback tests;
  - final operator/property contract acceptance.

### WT-ALIGN-002 — Blender 4.5 production validation

- Status: planned immediate
- Test the world-axis free-move case, slide-rail case, paired parent/child case, arbitrary-angle guide, rigid shape preservation, malformed selections, locks, transforms, undo/redo, and persistence.
- Record exact Blender version, operating system, geometry setup, before/after measurements, and failures.

### WT-ALIGN-003 — Witch Dock / Quickbar thin wrapper

- Status: deferred until WT-ALIGN-002 passes
- Witch Dock/Quickbar may expose the canonical Witch Tools operator/property contract only.
- It must not duplicate alignment math, marker storage, rail solving, or pairing logic.
- Preserve overlay drawing, event routing, dragging, resizing, locking, persistence, assets, and pass-through behavior.

### WT-ALIGN-004 — Curved/polyline movement rails

- Status: research
- Current candidate intentionally accepts straight rails only.
- A future design requires arc-length parameterization, junction handling, and explicit behavior when a rigid group cannot follow a curved path without rotation/deformation.

### WT-ALIGN-005 — Rotation and scale matching

- Status: deferred
- Requires a separate operator contract and safety plan; not part of Dev_v2.8.0.

### WT-ALIGN-006 — Surface projection and nearest-point modes

- Status: research
- Not part of current scope.

### WT-ALIGN-007 — Capture diagnostics and viewport visualization

- Status: planned after runtime validation
- Potential future work: marker overlays, rail direction display, target previews, and recapture assistance.

## Baseline preservation

### WT-BASE-001 — Restore auditable direct Witch Tools source

- Status: complete on `feature/witch-tools-guided-align`
- Dev_v2.7.0 snapshot conflict: committed parts are truncated and do not match the manifest.
- Recovery baseline: verified complete Dev_v2.6.1 snapshot.
- Current direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`
- Dev_v2.8.0 patch record: `addons/witch_tools/dev/patches/Dev_v2_8_0/`
- Public branches and official release paths remain unchanged.

### WT-BASE-002 — Audit integration into `Blender_Dev`

- Status: planned after Blender runtime validation
- Compare feature branch against `Blender_Dev`, resolve documentation/build-registry conflicts, then merge only an accepted source and test record.

### WT-BASE-003 — Audit public/update compatibility

- Status: planned before any official release

## Selection infrastructure

### WT-SEL-001 — Persistent mesh Selection Slots

- Status: active; Dev_v2.6.1 implementation retained in Dev_v2.8.0
- Remaining: Blender 4.5 N-panel confirmation, save/reopen, multi-object restore, topology marker propagation, and undo/redo.

### WT-SEL-002 — Selection Slot diagnostics

- Status: planned

### WT-SEL-003 — Additive/subtractive restore modes

- Status: deferred

## Topology development

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: active MVP; retained in Dev_v2.8.0

### WT-VINJ-002 — Manual Vertex Inject

- Status: deferred

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: active MVP; primary production workflow user-validated in Blender 4.5
- Remaining: formal undo/redo, normals/manifold/print-fit validation, and broader missing/surplus topology support.

### WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces

- Status: planned for Witch Tools integration

## Protection infrastructure

### WT-PROT-001 — Existing Vertex Lock integration

- Status: implemented for Guided Align preflight; Blender runtime validation pending

### WT-PROT-002 — Protected/ignored zone permissions

- Status: active partial implementation outside Guided Align

## Immediate next step

User-test Witch Tools Dev_v2.8.0 in Blender 4.5. Do not begin Witch Dock/Quickbar integration until the backend's real mesh behavior and final workflow are accepted.

## Scope policy

No discussed feature automatically enters an official release. Dev_v2.8.0 remains a development candidate. Curved rails, rotation/scale, projection to arbitrary surfaces, viewport overlays, and Witch Dock/Quickbar integration are separate follow-up scopes.
