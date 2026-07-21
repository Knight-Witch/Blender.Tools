# Witch Quickbar Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Baseline and compatibility work

### QB-BASE-001 — Inventory public branch source and assets

- Status: active
- Branch: `Witch_Quick_Access`
- Goal: exact file tree, package directory, asset paths, operator IDs, preference IDs, and version metadata

### QB-BASE-002 — Verify update-check URL and installed behavior

- Status: active
- Current static result: `UPDATE_URL` remains `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access` and opens a URL rather than comparing a manifest
- Remaining: launch from installed public and dev builds

### QB-BASE-003 — Import latest development artifact

- Status: active
- Candidate baseline: Dev_v1.3.18 used locally to produce Dev_v1.4.0
- Remaining: canonical repository source import and artifact comparison

### QB-BASE-004 — Build Quickbar registries and test matrix

- Status: planned
- Dependency: canonical source import

## Current Select-tab development

### QB-SEL-001 — Selection Slots Select tab

- Status: development build implemented; Blender 4.5 runtime validation pending
- Build: Dev_v1.4.0
- Required backend: Witch Tools Dev_v2.6.0+
- Implemented:
  - populated `Select` tab;
  - optional capability detection;
  - thin invocation of canonical Witch Tools operators;
  - responsive slot names and full-name tooltips;
  - rename dialog;
  - reselect, save, clear, remove, add, and Clear All;
  - grip-based drag reorder;
  - disabled explanatory state without Witch Tools;
  - supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD assets converted to PNG.
- Remaining:
  - registration and overlay rendering;
  - drag/drop and canceled-drag tests;
  - resize/name-width tests;
  - pass-through and overlapping hitbox tests;
  - dependency-present/absent tests;
  - undo separation and file-load recovery;
  - canonical source import.

### QB-SEL-002 — Selection Slot compact diagnostics

- Status: deferred until Witch Tools diagnostics exist
- Possible scope: empty/incomplete indicator and saved/surviving counts without reproducing backend logic.

## Architecture work

### QB-ARCH-001 — Preserve floating-overlay architecture during monorepo migration

- Status: active documentation and implementation constraint

### QB-ARCH-002 — Stable optional Witch Tools invocation contract

- Status: active partial implementation
- Current contract: Selection Slots calls `mesh.wt_selection_slot_*` and shows unavailable state when missing
- Remaining: formal version/capability registry and integration regression tests

### QB-BUILD-001 — Generate independent Quickbar release package from canonical source

- Status: planned
- Requires package-identity and update compatibility tests

## Known development issues/regressions to test

- Apply All Transforms in Object and Edit Mode
- Mirror Transform / Mirror Objects edit-mode handling
- Main/Edit/Select tab switching and reorder
- dynamic Selection Slot row count and gizmo capacity
- open/close, minimize/maximize, launcher, lock, resize, and file-load recovery
- pass-through outside every Select-tab control
- update/check browser launch

## Later features

- additional compact Witch Tools shortcuts after stable operator integration
- configurable tab/section visibility consistent with overlay architecture
- compact Selection Slot health indicators after canonical diagnostics exist

No later feature is current release scope until explicitly assigned.
