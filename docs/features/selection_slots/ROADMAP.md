# Selection Slots Roadmap

Last updated: 2026-07-21

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development scope

### SS-CORE-001 — Persistent mesh Selection Slots

- Status: implemented development backend; Blender 4.5 behavioral validation active
- Current Witch Tools build: `Dev_v2.6.1`
- Scope:
  - vertex/edge/face and combined-domain save;
  - multi-object Edit Mode;
  - scene records plus mesh custom-data markers;
  - overwrite, reselect, clear, remove, add, rename, reorder, Clear All;
  - `.blend` persistence.

### SS-UI-001 — Witch Tools N-panel

- Status: hotfix implemented in Dev_v2.6.1; Blender 4.5 validation pending
- Location: Edit Tools immediately below Curvature Sync
- Dev_v2.6.0 finding: header and Clear All rendered, but expanding did not reveal slot rows
- Dev_v2.6.1 correction:
  - no Scene mutation inside `Panel.draw()`;
  - safe empty-scene Slot 1 initialization through an operator;
  - clickable disclosure arrow and title;
  - row-level draw failure containment.
- Remaining:
  - verify expanded rows in Blender 4.5;
  - verify compact sizing, icon enums, field expansion, and native tooltip behavior;
  - verify panel collapse/minimal-view regression.

### SS-QB-001 — Quickbar Select tab

- Status: user-reported working in Blender 4.5 for the tested Select workflow
- Quickbar build: `Dev_v1.4.0`
- Scope:
  - optional Witch Tools operator integration;
  - custom supplied icon assets;
  - rename dialog;
  - responsive names and full-name tooltips;
  - grip drag reorder;
  - unavailable-backend state.
- Remaining:
  - full overlay regression: pass-through, resize, lock, file-load recovery, undo/redo, and dependency-absent behavior.

### SS-TEST-001 — Runtime validation

- Status: active
- Completed:
  - Dev_v2.6.0 Quickbar Select workflow user-reported working;
  - Dev_v2.6.0 N-panel expansion failure reproduced by user report;
  - Dev_v2.6.1 static and simulated panel-layout validation passed.
- Required next:
  - Dev_v2.6.1 install/register/unregister;
  - N-panel expand/collapse and Slot 1 display;
  - each mesh selection domain;
  - multi-object Edit Mode;
  - save/reopen;
  - overwrite and empty-save rejection;
  - clear versus remove;
  - reorder and naming;
  - topology-change behavior;
  - undo/redo;
  - Quickbar complete overlay regression.

## Next release candidates

### SS-DIAG-001 — Slot health diagnostics

- Status: planned after runtime validation
- Possible scope:
  - missing object count;
  - stored versus surviving element counts;
  - topology-propagated marker indication;
  - incomplete-slot report without silent rewriting.

### SS-MODE-001 — Additive/subtractive reselect modes

- Status: deferred
- Current behavior: Replace Selection.

### SS-OBJECT-001 — Object Mode selection slots

- Status: deferred

### SS-UV-001 — Independent UV selection storage

- Status: research

### SS-TRANSFER-001 — Cross-file export/import

- Status: research

### SS-STABLE-ID-001 — Immutable topology identity

- Status: research

## Rejected for the current build

- transient BMesh indices as persistent identity;
- silent reconstruction of deleted topology;
- duplicate canonical backend inside Quickbar;
- forcing hidden objects visible;
- unlimited slots;
- slot names as unique identifiers.