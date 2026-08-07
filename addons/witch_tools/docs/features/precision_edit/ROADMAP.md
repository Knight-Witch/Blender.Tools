# Precision Edit — Feature Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current candidate

### PE-001 — Coordinate Copy

- Status: active candidate in `Dev_v2.9.0`
- Implemented source workflow: Global/Local, XYZ, Location/Rotation/Scale, source capture, independent target Apply, multi-object world conversion, Vertex Lock/Plane Lock preflight, hotkeyable Apply.
- Remaining: Blender 4.5 acceptance testing and any fixes discovered there.

### PE-002 — Plane Lock

- Status: active candidate in `Dev_v2.9.0`
- Implemented source workflow: persistent object-local X/Y/Z locks, partial-axis unlock, clear-all, edit guard, integration with precision operators.
- Remaining: Blender transform, undo/redo, persistence, topology-change interaction, and performance validation.

### PE-003 — Level

- Status: active candidate in `Dev_v2.9.0`
- Implemented source workflow: source vertex/edge/face capture, world X/Y/Z masks, per-target exact leveling across multiple objects.
- Remaining: Blender 4.5 multi-object and protection-system validation.

### PE-004 — Inject New: Solo / Branch / Slide

- Status: active candidate in `Dev_v2.9.0`
- Implemented source workflow: Vertex/Edge/Face Solo and Branch, Vertex Slide, global X/Y/Z modal placement, captured straight Rail endpoint, commit/cancel, existing lock-reference restoration.
- Remaining: Blender 4.5 modal/topology/undo/attribute/manifold tests.

### PE-005 — Dev_v2.9.0 Blender 4.5 production validation

- Status: planned immediate
- Execute `TEST_PLAN.md` before merging or exposing through Witch Dock / Quickbar.

## Follow-up scope

### PE-006 — Witch Dock / Quickbar thin wrappers

- Status: deferred until PE-005 passes
- Must call canonical Witch Tools operators and preserve the overlay architecture.

### PE-007 — Curved/polyline Inject rails

- Status: research
- Requires path parameterization, junction rules, and deterministic mouse projection.

### PE-008 — Branch side-face / extrusion mode

- Status: deferred
- Requires explicit manifold, winding, material, and edge-attribute contracts. It is not implied by current Branch.

### PE-009 — Multi-object Inject New topology

- Status: deferred
- Current topology-changing modal operator intentionally edits one active mesh.

### PE-010 — Plane Lock world-frame option

- Status: research
- Current candidate intentionally stores object-local lock coordinates. A world-frame mode would need explicit behavior when object transforms change outside Edit Mode.

### PE-011 — Coordinate Copy viewport preview / frame gizmos

- Status: research
- Useful only after the core source/target semantics are accepted in Blender.

## Scope policy

None of the follow-up ideas above are part of Dev_v2.9.0 unless explicitly promoted after runtime validation. The candidate scope is the three requested Edit Tools sections and their current backend contracts only.
