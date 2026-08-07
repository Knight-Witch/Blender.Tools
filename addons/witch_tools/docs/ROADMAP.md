# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate

### WT-PREC-001 — Coordinate Copy

- Status: active candidate in Witch Tools `Dev_v2.9.0`; Blender 4.5 validation pending
- Priority: urgent/high
- Feature packet: `/docs/features/precision_edit/`
- Target Blender: `4.5.0`
- Implemented source behavior:
  - Global / Local coordinate capture and application;
  - X/Y/Z component masks;
  - Location / Rotation / Scale geometry-frame copying;
  - vertex, edge, and face source capture;
  - independent target application rather than one selection median;
  - multi-object world/local conversion for different object origins/transforms;
  - Vertex Lock and Plane Lock preflight;
  - default `Ctrl+Shift+C` Apply shortcut.
- Remaining:
  - Blender 4.5 registration/UI validation;
  - exact world/local location tests;
  - edge/face rotation/scale acceptance tests;
  - undo/redo and keymap-conflict validation.

### WT-PREC-002 — Planar Edit: Plane Lock / Level

- Status: active candidate in Witch Tools `Dev_v2.9.0`; Blender 4.5 validation pending
- Plane Lock stores object-local X/Y/Z lock coordinates in persistent BMesh custom layers and restores them through an Edit Mode guard.
- Level captures a source vertex/edge/face point in world space and assigns each target vertex exact enabled coordinates.
- Remaining: transform guard behavior, persistence, multi-object Level, protection interaction, undo/redo, and save/reopen.

### WT-VINJ-002 — Manual Inject New

- Status: active candidate in Witch Tools `Dev_v2.9.0`; promoted from deferred by explicit user request
- Implemented source behavior:
  - Solo and Branch for vertex/edge/face sources;
  - Slide as a vertex-only subdivide-like insertion into one selected edge;
  - global X/Y/Z modal placement;
  - captured arbitrary straight Rail endpoint for Solo/Branch;
  - selected-edge rail for Slide;
  - modal commit/cancel;
  - existing Vertex Lock reference restoration and Plane Lock guard coordination.
- Remaining:
  - Blender 4.5 modal interaction;
  - exact cancel rollback;
  - undo/redo;
  - normals/winding/material/edge-attribute tests;
  - Slide manifold/zero-geometry tests.

### WT-PREC-003 — Blender 4.5 production validation

- Status: planned immediate
- Execute `/docs/features/precision_edit/TEST_PLAN.md` before integration or thin-wrapper work.

## Guided Align — retained from Dev_v2.8.0

### WT-ALIGN-001 — Align Vertices / Edges / Faces

- Status: active candidate retained in Witch Tools `Dev_v2.9.0`; Blender 4.5 validation pending
- Priority: urgent/high
- Documented feature-packet path in the inherited roadmap: `/docs/features/align_selection/`
- Documentation conflict: that directory is not present on the current branch; do not fabricate its missing historical contents.
- Target Blender: `4.5.0`
- Retained behavior:
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

### WT-ALIGN-002 — Blender 4.5 production validation

- Status: planned after/alongside current Dev_v2.9.0 validation

### WT-ALIGN-003 — Witch Dock / Quickbar thin wrapper

- Status: deferred until Witch Tools backend validation passes
- Witch Dock/Quickbar may expose canonical Witch Tools operator/property contracts only.
- It must not duplicate alignment, coordinate-copy, plane-lock, leveling, or injection backend logic.

### WT-ALIGN-004 — Curved/polyline movement rails

- Status: research

### WT-ALIGN-005 — Guided Align rotation and scale matching

- Status: deferred
- Separate from Coordinate Copy's element-frame Rotation/Scale semantics.

### WT-ALIGN-006 — Surface projection and nearest-point modes

- Status: research

### WT-ALIGN-007 — Capture diagnostics and viewport visualization

- Status: planned after runtime validation

## Precision Edit follow-up scope

### WT-PREC-004 — Curved/polyline Inject New rails

- Status: research

### WT-PREC-005 — Branch side-face / extrusion mode

- Status: deferred
- Requires separate manifold, winding, material, and attribute rules.

### WT-PREC-006 — Multi-object topology Inject New

- Status: deferred
- Current modal topology operator intentionally edits one active mesh.

### WT-PREC-007 — Plane Lock world-frame mode

- Status: research
- Current candidate stores object-local lock coordinates.

### WT-PREC-008 — Precision viewport previews / gizmos

- Status: research

### WT-PREC-009 — Witch Dock / Quickbar thin wrappers

- Status: deferred until Dev_v2.9.0 Witch Tools behavior is accepted in Blender 4.5

## Baseline preservation

### WT-BASE-001 — Restore auditable direct Witch Tools source

- Status: complete
- Dev_v2.7.0 snapshot conflict: committed parts are truncated and do not match the manifest.
- Recovery baseline: verified complete Dev_v2.6.1 snapshot.
- Dev_v2.8.0 Guided Align source baseline commit for this work: `fc94b7c27d0b850699e79b973a0548a2193eb525`.
- Current direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`.
- Public branches and official release paths remain unchanged.

### WT-BASE-002 — Audit integration into `Blender_Dev`

- Status: planned after Blender runtime validation
- Compare the accepted feature branch against `Blender_Dev`, resolve documentation/build-registry conflicts, then merge only an accepted source and test record.

### WT-BASE-003 — Audit public/update compatibility

- Status: planned before any official release

## Selection infrastructure

### WT-SEL-001 — Persistent mesh Selection Slots

- Status: active; Dev_v2.6.1 implementation retained in Dev_v2.9.0
- Remaining: Blender 4.5 N-panel confirmation, save/reopen, multi-object restore, topology marker propagation, and undo/redo.

### WT-SEL-002 — Selection Slot diagnostics

- Status: planned

### WT-SEL-003 — Additive/subtractive restore modes

- Status: deferred

## Topology development

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: active MVP; retained as the separate **Edge / Vertex Inject** section in Dev_v2.9.0

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: active MVP; primary production workflow user-validated in Blender 4.5
- Remaining: formal undo/redo, normals/manifold/print-fit validation, and broader missing/surplus topology support.

### WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces

- Status: planned for Witch Tools integration

## Protection infrastructure

### WT-PROT-001 — Existing Vertex Lock integration

- Status: active; reused by Guided Align and Dev_v2.9.0 Precision Edit preflight

### WT-PROT-002 — Protected/ignored zone permissions

- Status: active partial implementation

### WT-PROT-003 — Plane Lock axis constraints

- Status: active candidate in Dev_v2.9.0; Blender 4.5 validation pending

## Immediate next step

User-test Witch Tools Dev_v2.9.0 in Blender 4.5 using the Precision Edit test plan. Fix failures found there without broadening the candidate scope. Do not begin Witch Dock/Quickbar integration until the canonical Witch Tools backend behavior is accepted.

## Scope policy

No discussed feature automatically enters an official release. Dev_v2.9.0 remains a development candidate. Curved rails, branch extrusion/side faces, multi-object topology injection, world-frame Plane Lock, viewport previews, and Witch Dock/Quickbar integration remain separate follow-up scopes.
