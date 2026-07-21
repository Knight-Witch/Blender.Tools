# Selection Slots Roadmap

Last updated: 2026-07-21

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development scope

### SS-CORE-001 — Persistent mesh Selection Slots

- Status: implemented development build; Blender 4.5 runtime validation pending
- Witch Tools build: `Dev_v2.6.0`
- Scope:
  - vertex/edge/face and combined-domain save;
  - multi-object Edit Mode;
  - scene records plus mesh custom-data markers;
  - overwrite, reselect, clear, remove, add, rename, reorder, Clear All;
  - `.blend` persistence.

### SS-UI-001 — Witch Tools N-panel

- Status: implemented development build; Blender 4.5 UI validation pending
- Location: Edit Tools immediately below Curvature Sync
- Current reorder UI: up/down controls
- Remaining: verify compact sizing, native icon enums, field expansion, and tooltip behavior in Blender 4.5.

### SS-QB-001 — Quickbar Select tab

- Status: implemented development build; Blender 4.5 overlay validation pending
- Quickbar build: `Dev_v1.4.0`
- Scope:
  - optional Witch Tools operator integration;
  - custom supplied icon assets;
  - rename dialog;
  - responsive names and full-name tooltips;
  - grip drag reorder;
  - unavailable-backend state.

### SS-TEST-001 — Runtime validation

- Status: active/pending user test
- Required:
  - install/register/unregister;
  - each mesh selection domain;
  - multi-object Edit Mode;
  - save/reopen;
  - overwrite and empty-save rejection;
  - clear versus remove;
  - reorder and naming;
  - topology change behavior;
  - undo/redo;
  - Quickbar draw/input/pass-through/resize/file-load tests.

## Next release candidates

### SS-DIAG-001 — Slot health diagnostics

- Status: planned after runtime validation
- Possible scope:
  - show missing object count;
  - compare stored and surviving element counts;
  - indicate topology-propagated extra markers;
  - select/report incomplete slots without silently rewriting them.

### SS-MODE-001 — Additive/subtractive reselect modes

- Status: deferred
- Current behavior replaces the current selection.
- Possible later modes: Replace, Add, Subtract, Intersect.

### SS-OBJECT-001 — Object Mode selection slots

- Status: deferred
- Must remain distinct from mesh-element Selection Slots.

### SS-UV-001 — Independent UV selection storage

- Status: research
- Requires explicit UV-loop identity and synchronization rules; mesh selection alone is insufficient.

### SS-TRANSFER-001 — Cross-file export/import

- Status: research
- Requires a stable topology matching strategy; raw object pointers and mesh custom layers are file-local.

### SS-STABLE-ID-001 — Immutable topology identity

- Status: research
- Explore whether explicit element UUID attributes provide meaningful advantages over current custom markers without causing severe data bloat or propagation ambiguity.

## Rejected for the current build

- storing transient BMesh indices as persistent identity;
- silently rebuilding selections after deleted topology;
- duplicating the canonical backend inside Quickbar;
- forcing hidden objects visible during reselect;
- unlimited slot creation;
- treating slot names as unique identifiers.
