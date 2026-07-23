# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current release / baseline recovery

### WT-BASE-001 — Preserve latest Witch Tools development baseline

- Status: complete for isolated reproducible snapshot; direct unpacked canonical source import remains active
- Priority: critical
- Current derivative build: Dev_v2.6.1
- Completed 2026-07-23:
  - development-only snapshot stored under `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/`;
  - manifest records source ZIP, ordered parts, archive, package root, and source-tree identities;
  - final reconstruction verified 60 files, 383,270 bytes, and tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`;
  - public Witch Tools source paths and branches remained unchanged.
- Remaining:
  - decide and execute the direct unpacked development source layout;
  - generate source-derived UI/operator registries;
  - preserve branch ancestry and public integration strategy.

### WT-BASE-002 — Build current UI and operator registries

- Status: planned
- Dependency: direct unpacked development source import

### WT-BASE-003 — Audit public/update compatibility

- Status: planned
- Dependency: direct unpacked development source import

## Current selection infrastructure

### WT-SEL-001 — Persistent mesh Selection Slots

- Status: active development; N-panel hotfix pending Blender 4.5 confirmation
- Current build: Dev_v2.6.1
- Priority: urgent/high
- Feature packet: `/docs/features/selection_slots/`
- Implemented backend:
  - vertex, edge, face, and combined-domain storage;
  - multi-object Edit Mode;
  - `.blend` persistence using scene records and per-mesh markers;
  - save/overwrite, reselect, clear, Clear All, add, remove, rename, reorder;
  - initial Slot 1 and maximum 20 slots;
  - stable operator family for Quickbar integration.
- Dev_v2.6.0 finding:
  - Quickbar Select workflow user-reported working;
  - Witch Tools N-panel body failed to reveal rows after expansion.
- Dev_v2.6.1 correction:
  - removed Scene mutation from `Panel.draw()`;
  - added safe operator-driven Slot 1 initialization;
  - made title and arrow clickable;
  - added row-level draw containment.
- Remaining:
  - Blender 4.5 N-panel confirmation;
  - save/reopen, multi-object, and undo/redo validation;
  - record marker behavior after delete/subdivide/duplicate;
  - direct unpacked source import and registries.

### WT-SEL-002 — Selection Slot diagnostics

- Status: planned after WT-SEL-001 validation

### WT-SEL-003 — Additive/subtractive restore modes

- Status: deferred

## Current topology development project

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: active MVP; standalone collar validation pending
- Current build: retained in Dev_v2.6.1

### WT-VINJ-002 — Manual Vertex Inject

- Status: deferred

### WT-VINJ-003 — Bulk Missing Correspondence Injection

- Status: partially implemented inside Curvature Sync; standalone workflow planned

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: active MVP; primary production workflow user-validated in Blender 4.5
- Current build: retained in Dev_v2.6.1
- Remaining: undo/redo report, formal normals/manifold/print-fit validation, missing-Middle and surplus-topology improvements

### WT-CURV-002 — Cross-object column synchronization

- Status: MVP implemented; production collar result user-validated

### WT-CURV-004 — Misaligned existing column replacement

- Status: MVP implemented and user-validated on the production collar

### WT-CURV-003 — Generic spline/non-circular mode

- Status: research

### WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces

- Status: planned for Witch Tools integration

## Protection infrastructure

### WT-PROT-001 — Audit existing Vertex Lock implementation

- Status: complete for current topology MVP

### WT-PROT-002 — Protected/ignored zone permissions

- Status: active partial implementation

## Immediate next step

Complete the isolated Quickbar Dev_v1.4.0 source snapshot, then user-test Witch Tools Dev_v2.6.1 in Blender 4.5. Confirm the Selection Slots body expands and Slot 1 renders, then test the selection workflow and panel regression matrix. Patch only failures found in that test.

## Deferred/rejected policy

No discussed idea is automatically current-release scope.
