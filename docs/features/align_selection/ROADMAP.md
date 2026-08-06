# Align Vertices / Edges / Faces Roadmap

Statuses: `planned`, `active`, `deferred`, `research`, `complete`.

## Current development scope

### WT-ALIGN-001 — Guided coordinate alignment

- Status: active candidate in Witch Tools Dev_v2.8.0
- Includes parent capture, world/custom frames, component masks, free movement, straight slide rails, one-to-all and paired mapping, shape preservation, per-island grouping, multi-object conversion, and transactional preflight.
- Static/source/package validation: complete.
- Blender 4.5 runtime validation: pending.

### WT-ALIGN-001A — Auditable source recovery

- Status: complete on feature branch
- Dev_v2.7.0 snapshot parts were confirmed truncated and non-reconstructable.
- Dev_v2.8.0 was re-established from verified Dev_v2.6.1 source.
- Direct source and reproducible patch record are present.

## Immediate validation scope

### WT-ALIGN-002 — Blender 4.5 runtime regression

- Status: planned immediate
- Test panel rendering, parent/rail capture, world-axis free movement, rail sliding, paired rails, arbitrary guide, rigid shapes, multiple islands, multi-object transforms, locks, stale markers, malformed rails, impossible constraints, shape keys, undo/redo, and save/reopen.

### WT-ALIGN-003 — Witch Dock / Quickbar presentation

- Status: deferred until WT-ALIGN-002 passes
- Add a compact step-based presentation calling the canonical Witch Tools operators and scene properties.
- Preserve the existing floating-overlay architecture and pass-through behavior.
- Do not duplicate marker storage, coordinate math, rail solving, or pairing logic.

## Deferred and research

### WT-ALIGN-004 — Curved/polyline rails

- Status: research
- Requires explicit arc-length, junction, rigid-body, and rotation/deformation decisions.

### WT-ALIGN-005 — Rotation/orientation matching

- Status: deferred

### WT-ALIGN-006 — Scale matching

- Status: deferred

### WT-ALIGN-007 — Surface projection and nearest-point alignment

- Status: research

### WT-ALIGN-008 — Viewport preview and capture visualization

- Status: planned after runtime validation

### WT-ALIGN-009 — Marker diagnostics and guided recapture

- Status: planned after runtime validation

## Rejected for the current candidate

- Guessing parent/child pairs by vertex order or nearest distance.
- Silently choosing among multiple rails touching one target island.
- Deforming a rigid target group to force an impossible rail constraint.
- Editing non-participating hidden objects that happen to contain markers.
- Moving some islands when another island fails preflight.
- Duplicating the backend in Witch Dock/Quickbar.
