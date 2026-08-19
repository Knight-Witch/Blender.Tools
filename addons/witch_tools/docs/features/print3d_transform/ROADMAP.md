# 3D Print Tools + Transform Roadmap

Statuses: `active`, `planned`, `deferred`, `research`, `rejected`, `complete`.

## Current candidate

### WT-XFORM-001 — Persistent Witch Tools Transform access

- Status: active candidate in `Dev_v2.10.0`
- Target: Blender 4.5.0
- Scope: top-level Transform panel under Mode Switcher; object Location/Rotation/Scale; selected-mesh local Location in Edit Mode.
- Remaining: Blender UI/runtime/undo/save-reopen validation.

### WT-PRINT-001 — Consolidated Analyze Mesh

- Status: active candidate in `Dev_v2.10.0`
- Scope: Check All + ten result counts only.
- Remaining: Blender 4.5 parity tests against known meshes and original toolbox behavior.

### WT-PRINT-002 — Clean & Repair consolidation

- Status: active candidate in `Dev_v2.10.0`
- Scope: Make Manifold, Mesh Repair-derived Auto Fix, Instant Clean-derived Advanced Clean.
- Remaining: complete topology safety test plan, especially Intersect Volumes and selection-only cleanup.

### WT-PRINT-003 — Simplified STL export

- Status: active candidate in `Dev_v2.10.0`
- Scope: folder + one Export STL button, fixed STL format.
- Remaining: Blender 4.5 export/reimport validation.

## Planned follow-up after runtime acceptance

### WT-PRINT-004 — Result selection/highlight parity

- Status: planned
- Add compact click-to-select/highlight behavior for actionable Analyze Mesh results if the user wants the original 3D Print Toolbox interaction preserved after count parity is validated.

### WT-PRINT-005 — Threshold/preferences pass

- Status: deferred
- Only expose thresholds that prove useful in the user's actual print-prep workflow. Do not restore the original toolbox's full settings grid by default.

### WT-XFORM-002 — Global/local mesh coordinate display mode

- Status: research
- Current Edit Mode Location is explicitly object-local. A world-coordinate switch may be useful later but is outside the current requested scope.

## Explicitly excluded from current scope

- 3D Print Toolbox Volume / Area statistics
- per-check Solid / Intersections / Shells UI
- Hollow
- Bisect
- Align XY
- Scale To
- export options UI
- Instant Clean Object Data
- Instant Clean Make Planar

These exclusions do not mean the underlying Blender operations are impossible; they are intentionally not part of `Dev_v2.10.0` because they do not currently improve the user's workflow.

## Validation gate

No further feature growth until `TEST_PLAN.md` passes the Blender 4.5 registration/UI checks and the topology-changing operations have completed undo/redo, mode handling, normals/winding, material/edge-attribute, manifold, malformed-selection, and failure-safety testing.
