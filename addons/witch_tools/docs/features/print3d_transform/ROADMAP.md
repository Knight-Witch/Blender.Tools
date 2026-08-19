# 3D Print Tools + Transform Roadmap

Statuses: `active`, `planned`, `deferred`, `research`, `rejected`, `complete`.

## Current candidate — Dev_v2.11.3

Primary runtime target: Blender 5.0.1  
Secondary compatibility target: Blender 4.5.0  
Baseline: Dev_v2.10.1 Magic Branch

### WT-XFORM-001 — Persistent Transform access

- Status: active candidate.
- Top-level Transform directly below Mode Switcher.
- Object Location/Rotation/Scale.
- Selected-mesh object-local Location in Edit Mode.
- Remaining: Blender 5.0.1 interaction, Undo/Redo, save/reopen validation; later Blender 4.5 compatibility pass where needed.

### WT-PRINT-001 — Consolidated Analyze Mesh

- Status: active parity-fix candidate.
- Dev_v2.11.1 runtime comparison in Blender 5.0.1 proved mismatches against the original 3D Print Toolbox: Non-flat 73 vs 98, Thin 1 vs 0, Sharp 1 vs 0, Overhang 80 vs 79.
- Dev_v2.11.2 replaced the simplified approximations with Toolbox-equivalent transformed-mesh, signed-angle, BVH, degenerate-threshold, and six-sample thickness semantics.
- Dev_v2.11.3 retains that correction unchanged.
- Remaining: rerun the same `_CAP 3` mesh and verify all ten counts match; then compare offending-element identity for selectable results.

### WT-PRINT-002 — Clean & Repair consolidation

- Status: active candidate.
- Make Manifold.
- Auto Fix: Global Fix before Local Fix.
- Advanced Clean: Repair, Manifold, Topology, Normals, Dissolve.
- Instant Clean-style collapsible sections, individual enable toggles/play actions, main Clean enabled-section behavior, and requested compact control changes are retained.
- Remaining: Blender 5.0.1 execution/Shift tests plus topology safety and attribute-preservation validation.

### WT-PRINT-003 — Simplified STL export

- Status: active hotfix candidate.
- UI remains folder + Export STL; fixed STL format.
- User runtime test showed the prior export path could appear to do nothing after a folder was selected.
- Dev_v2.11.3 validates Blender exporter completion/output, tries current and legacy Blender STL paths, and adds a direct binary STL fallback from selected evaluated meshes.
- Remaining: Blender 5.0.1 one-object/multi-object/modifier/transform export and re-import validation; explicit failure behavior; then Blender 4.5 compatibility smoke test.

### WT-PRINT-004 — Analyze result selection/highlight parity

- Status: planned required follow-up after analyzer parity.
- Make actionable result counts select/highlight the exact offending vertices/edges/faces.
- Do not implement until count/detection parity and offending-element identity are verified.

## Baseline preservation

### WT-BASE-PRINT-001 — Port onto current Magic Branch baseline

- Status: complete at source-integration level.
- Dev_v2.11.x is based on Dev_v2.10.1 / `feature/witch-tools-magic-branch` and retains Magic Branch, Edge Doctor, Edit Tools ordering, and the current registration surface.

## Validation gate

Before acceptance:
- Blender 5.0.1 register/unregister and required panel order;
- Advanced Clean header layout and individual/main execution including Shift selection-only;
- Transform editing;
- Analyze count parity and offending-element parity;
- STL one/multi-object export, modifier evaluation, transforms, file creation, explicit failure, and re-import;
- Make Manifold / Auto Fix / Advanced Clean;
- Undo/Redo and mode handling;
- normals/winding and material/edge/custom-data preservation;
- manifold safety where applicable;
- malformed selections and failure without partial destructive changes;
- regression test of Dev_v2.10.1 Magic Branch/Inject/Edge Doctor behavior;
- secondary Blender 4.5 compatibility checks for shared/BG3 workflows that still require 4.5.

## Deferred / research

### WT-PRINT-005 — Threshold/preferences pass

- Status: deferred.
- Keep standard Toolbox thresholds hidden unless an actual workflow need appears.

### WT-XFORM-002 — Mesh world/local coordinate switch

- Status: research.
- Current Edit Mode Location is object-local.

## Explicitly excluded from current scope

- Volume / Area statistics
- separate Solid / Intersections / Shells controls
- Hollow
- Bisect
- Align XY
- Scale To
- export options UI
- Instant Clean Object Data
- Instant Clean Make Planar

## Immediate next step

Package/install Dev_v2.11.3 in Blender 5.0.1 and test Export STL first. Confirm an STL is physically written and re-imports correctly for one mesh, multiple meshes, and a modifier-evaluated mesh. Then rerun Analyze on `_CAP 3` before click-to-select work.
