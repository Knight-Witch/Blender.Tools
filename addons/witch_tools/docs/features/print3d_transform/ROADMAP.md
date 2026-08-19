# 3D Print Tools + Transform Roadmap

Statuses: `active`, `planned`, `deferred`, `research`, `rejected`, `complete`.

## Current candidate — Dev_v2.11.4

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

- Status: active exact-backend candidate.
- Dev_v2.11.1 local detector mismatch: Non-flat 73 vs Toolbox 98, Thin 1 vs 0, Sharp 1 vs 0, Overhang 80 vs 79.
- Dev_v2.11.2 attempted a Toolbox-equivalent local rewrite.
- Dev_v2.11.3 user retest still failed: Non-flat 73 vs 98 and Overhang 80 vs 79. Thin/Sharp matched 0/0.
- Dev_v2.11.4 removes the parallel detector entirely. Witch Tools invokes the installed Toolbox `mesh.print3d_check_all` and mirrors its live report.
- No alternate detector fallback is allowed; unavailable Toolbox backend is an explicit error.
- Remaining: Blender 5.0.1 exact count/display retest on `_CAP 3` and report-resolution testing.

### WT-PRINT-004 — Analyze result selection/highlight parity

- Status: active candidate in Dev_v2.11.4.
- In Edit Mode, non-empty Witch Tools result buttons invoke the original Toolbox `mesh.print3d_select_report` with the original report index.
- Remaining: verify the exact selected element set matches the original Toolbox buttons for Non-flat, Overhang, and representative edge/face diagnostics.

### WT-PRINT-002 — Clean & Repair consolidation

- Status: active candidate.
- Make Manifold.
- Auto Fix: Global Fix before Local Fix.
- Advanced Clean: Repair, Manifold, Topology, Normals, Dissolve.
- Instant Clean-style collapsible sections, individual enable toggles/play actions, main Clean enabled-section behavior, and requested compact control changes are retained.
- Remaining: Blender 5.0.1 execution/Shift tests plus topology safety and attribute-preservation validation.

### WT-PRINT-003 — Simplified STL export

- Status: active candidate with initial runtime success.
- UI remains folder + Export STL; fixed STL format.
- Dev_v2.11.3 added exporter status/file validation plus a direct binary STL fallback.
- User confirmed Dev_v2.11.3 now produces an STL in Blender 5.0.1.
- Remaining: re-import dimensions/orientation, multi-object, modifier-evaluated, negative-scale/fallback paths, then Blender 4.5 smoke test.

## Baseline preservation

### WT-BASE-PRINT-001 — Port onto current Magic Branch baseline

- Status: complete at source-integration level.
- Dev_v2.11.x is based on Dev_v2.10.1 / `feature/witch-tools-magic-branch` and retains Magic Branch, Edge Doctor, Edit Tools ordering, and the current registration surface.

## Validation gate

Before acceptance:
- Blender 5.0.1 register/unregister and required panel order;
- original Toolbox Check All vs Witch Tools Check All exact displayed-count parity on unchanged meshes;
- original Toolbox result selection vs Witch Tools result selection exact element parity in Edit Mode;
- explicit Analyze failure when the Toolbox backend is disabled/unavailable;
- Advanced Clean header layout and individual/main execution including Shift selection-only;
- Transform editing;
- STL multi-object/modifier/transform/re-import and failure-path validation;
- Make Manifold / Auto Fix / Advanced Clean;
- Undo/Redo and mode handling;
- normals/winding and material/edge/custom-data preservation;
- manifold safety where applicable;
- malformed selections and failure without partial destructive changes;
- regression test of Dev_v2.10.1 Magic Branch/Inject/Edge Doctor behavior;
- secondary Blender 4.5 compatibility checks for shared/BG3 workflows that still require 4.5.

## Deferred / research

### WT-PRINT-005 — Self-contained exact Toolbox vendoring

- Status: research/deferred.
- Current Dev_v2.11.4 Analyze deliberately calls the installed 3D Print Toolbox to guarantee parity.
- If Witch Tools later must function without the original extension installed, vendor the exact current Toolbox source package as a pinned backend. Do not hand-reimplement its detectors again.

### WT-PRINT-006 — Threshold/preferences pass

- Status: deferred.
- Threshold controls remain omitted from Witch Tools; while direct delegation is used, the installed Toolbox settings are authoritative.

### WT-XFORM-002 — Mesh world/local coordinate switch

- Status: research.
- Current Edit Mode Location is object-local.

## Explicitly excluded from current UI scope

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

Package/install Dev_v2.11.4 in Blender 5.0.1 with 3D Print Toolbox enabled. On `_CAP 3`, run the original Toolbox Check All and Witch Tools Check All consecutively and confirm every displayed value is identical. Then enter Edit Mode and compare the original and Witch Tools result buttons for exact selected-element parity.
