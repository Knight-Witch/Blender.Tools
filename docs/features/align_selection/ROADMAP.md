# Align Selection Roadmap

Statuses: `planned`, `active`, `deferred`, `research`, `complete`.

## Current development scope

### WT-ALIGN-001 — World-axis Align Selection

- Status: active; Dev_v2.7.1 N-panel hotfix complete, Blender 4.5 validation pending
- Includes source and target-anchor capture, Median/Active Element reference modes, Match Coordinates, Move Shape, X/Y/Z combinations, Whole Selection, Per Selected Island, multi-object conversion, Vertex Lock preflight, and local Quickbar thin integration.

### WT-ALIGN-001A — N-panel rendering hotfix

- Status: complete in Dev_v2.7.1; user confirmation pending
- Registered the missing `show_edit_align_selection` preference and replaced the invalid section icon identifier.

## Next validation scope

### WT-ALIGN-002 — Blender runtime regression

- Status: planned immediate
- First confirm that Edit Tools displays the Align Selection title, disclosure control, reference dropdown, capture controls, axis controls, operation control, grouping control, Apply, and Clear.
- Then test real vertex/edge/face capture, Figures A and B, two parallel/disconnected cavities, multi-object transforms, undo/redo, save/reopen, locks, stale captures, and shape keys.

### WT-ALIGN-003 — Quickbar reference-mode controls

- Status: planned local-only follow-up
- Add Median/Active Element exposure and clarify Match versus Preserve Shape controls without changing the canonical Witch Tools backend.
- Do not update Quickbar source on GitHub unless the user explicitly changes that instruction.

## Deferred and research

### WT-ALIGN-004 — Custom coordinate frames

- Status: research

### WT-ALIGN-005 — Rotation and scale matching

- Status: deferred

### WT-ALIGN-006 — Projection and nearest-surface alignment

- Status: research

### WT-ALIGN-007 — Marker diagnostics and recapture assistance

- Status: planned after runtime validation

## Rejected for current build

- Guessing the target anchor.
- Moving islands with no captured anchor.
- Duplicating geometry calculations in Quickbar.
- Applying partial island changes when any component fails preflight.
