# Align Selection Roadmap

Statuses: `planned`, `active`, `deferred`, `research`, `complete`.

## Current development scope

### WT-ALIGN-001 — World-axis Align Selection

- Status: active; implementation complete for Dev_v2.7.0, Blender 4.5 validation pending
- Includes source and target-anchor capture, Match Coordinates, Move Shape, X/Y/Z combinations, Whole Selection, Per Selected Island, multi-object conversion, Vertex Lock preflight, and Quickbar thin integration.

## Next validation scope

### WT-ALIGN-002 — Blender runtime regression

- Status: planned immediate
- Test N-panel and Quickbar presentation, real vertex/edge/face capture, Figures A and B, two parallel/disconnected cavities, multi-object transforms, undo/redo, save/reopen, locks, stale captures, shape keys, and overlay pass-through.

## Deferred and research

### WT-ALIGN-003 — Active Element reference mode

- Status: deferred

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
