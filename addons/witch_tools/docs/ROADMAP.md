# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development release

### WT-ALIGN-001 — Align Selection

- Status: active; Dev_v2.7.1 N-panel hotfix complete, Blender 4.5 validation pending
- Priority: urgent/high
- Feature packet: `/docs/features/align_selection/`
- Current build: `Dev_v2.7.1`
- Implemented:
  - persistent Source and Target Anchor capture;
  - vertex, edge, face, and mixed reference selections;
  - Median and Active Element source references;
  - world-space X/Y/Z Match Coordinates;
  - shape-preserving Move Shape;
  - Whole Selection and Per Selected Island;
  - multiple disconnected cavity alignment;
  - multi-object Edit Mode conversion;
  - Vertex Lock, stale-capture, missing-anchor, shape-key, and transform preflight;
  - Witch Tools N-panel and local Quickbar thin integration.
- Dev_v2.7.1 correction:
  - registered missing `show_edit_align_selection` preference;
  - replaced invalid/unverified `ALIGN` section icon with `PIVOT_ACTIVE`.
- Remaining:
  - Blender 4.5 N-panel confirmation;
  - Figure A and Figure B production tests;
  - multi-cavity, multi-object, save/reopen, and undo/redo tests;
  - protected-zone runtime confirmation;
  - local-only Quickbar reference-mode UI.

## Baseline preservation

### WT-BASE-001 — Preserve latest Witch Tools development baseline

- Status: complete for Dev_v2.7.1 verified source patch; full archive snapshot deferred
- Patch: `addons/witch_tools/dev/patches/Dev_v2_7_1/`
- Source baseline: exact user-tested replacement Dev_v2.7.0 artifact, SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`
- Build artifact: SHA-256 `f4783b620325e6c40c156d9aa05e2479ca0e0159b06f4177138b46bbfbc4c110`
- Changed-file patch and manifest: verified
- Public branches and official release paths remain unchanged.
- Remaining:
  - decide direct unpacked development source layout;
  - build source-derived UI/operator registries;
  - create a full archive snapshot during the next broader source import/rebuild pass;
  - audit eventual public integration.

### WT-BASE-002 — Build current UI and operator registries

- Status: planned
- Dependency: approved direct unpacked development source layout

### WT-BASE-003 — Audit public/update compatibility

- Status: planned before official integration

## Selection infrastructure

### WT-SEL-001 — Persistent mesh Selection Slots

- Status: active; Dev_v2.6.1 hotfix retained in Dev_v2.7.1
- Remaining:
  - Blender 4.5 N-panel confirmation;
  - save/reopen, multi-object, topology propagation, and undo/redo;
  - marker diagnostics.

### WT-SEL-002 — Selection Slot diagnostics

- Status: planned

### WT-SEL-003 — Additive/subtractive restore modes

- Status: deferred

## Align Selection follow-up

### WT-ALIGN-002 — Quickbar reference-mode UI

- Status: planned local-only next step

### WT-ALIGN-003 — Custom/local/normal coordinate frames

- Status: research

### WT-ALIGN-004 — Rotation and scale matching

- Status: deferred; requires separate contract

### WT-ALIGN-005 — Projection and nearest-surface alignment

- Status: research

### WT-ALIGN-006 — Capture diagnostics and recapture assistance

- Status: planned after runtime validation

## Topology development

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: active MVP; retained in Dev_v2.7.1

### WT-VINJ-002 — Manual Vertex Inject

- Status: deferred

### WT-VINJ-003 — Bulk Missing Correspondence Injection

- Status: partially implemented inside Curvature Sync

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: active MVP; primary production workflow user-validated in Blender 4.5
- Current build: retained in Dev_v2.7.1
- Remaining: undo/redo report, formal normals/manifold/print-fit validation, missing-Middle and surplus-topology improvements

### WT-CURV-002 — Cross-object column synchronization

- Status: MVP implemented; production collar user-validated

### WT-CURV-004 — Misaligned existing column replacement

- Status: MVP implemented and user-validated

### WT-CURV-003 — Generic spline/non-circular mode

- Status: research

### WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces

- Status: planned for Witch Tools integration

## Protection infrastructure

### WT-PROT-001 — Audit existing Vertex Lock implementation

- Status: complete for current MVPs

### WT-PROT-002 — Protected/ignored zone permissions

- Status: active partial implementation

## Immediate next step

User-test Witch Tools Dev_v2.7.1 in Blender 4.5. First confirm the Align Selection N-panel renders fully. Then test Figures A and B, two disconnected cavities, multi-object transforms, undo/redo, locks, stale captures, and save/reopen. Patch the local Quickbar reference-mode controls only after the Witch Tools panel is confirmed.

## Scope policy

No discussed feature is automatically official-release scope. Dev_v2.7.1 and local Quickbar Dev_v1.5.0 remain development builds.
