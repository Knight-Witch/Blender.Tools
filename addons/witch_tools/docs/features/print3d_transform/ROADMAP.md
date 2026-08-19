# 3D Print Tools + Transform Roadmap

Statuses: `active`, `planned`, `deferred`, `research`, `rejected`, `complete`.

## Current candidate — Dev_v2.11.2

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
- Dev_v2.11.2 replaces the simplified approximations with Toolbox-equivalent transformed-mesh, signed-angle, BVH, degenerate-threshold, and six-sample thickness semantics.
- Remaining: rerun the same `_CAP 3` mesh and verify all ten counts match; then compare offending-element identity for selectable results.

### WT-PRINT-002 — Clean & Repair consolidation

- Status: active candidate.
- Make Manifold.
- Auto Fix: Global Fix before Local Fix.
- Advanced Clean: Repair, Manifold, Topology, Normals, Dissolve.
- Dev_v2.11.1 restored the Instant Clean-style section layout: each Advanced Clean section is independently collapsible, has its own enable toggle, and has its own play button for running only that section.
- The main Clean button runs the set of enabled section toggles.
- Original-style body layout is preserved except for the user-approved compact changes: Manifold Remove Non-Manifold toggle bar, responsive Topology angle/Compare layout, Normals Clear Data toggle bar, removal of Make Planar/Object Data, and Dissolve moved last.
- Remaining: Blender 5.0.1 rendering/interaction test plus topology safety and attribute-preservation validation.

### WT-PRINT-003 — Simplified STL export

- Status: active candidate.
- Folder + Export STL; fixed STL format.
- Remaining: Blender 5.0.1 export/re-import validation, then Blender 4.5 compatibility check if needed.

### WT-PRINT-004 — Analyze result selection/highlight parity

- Status: planned required follow-up after analyzer parity.
- Make actionable result counts select/highlight the exact offending vertices/edges/faces, matching the workflow value of Blender's original 3D Print Toolbox.
- Do not implement until count/detection parity and offending-element identity are verified so selection is not attached to an incorrect detector.

## Baseline preservation

### WT-BASE-PRINT-001 — Port onto current Magic Branch baseline

- Status: complete at source-integration level.
- The initial stale Dev_v2.9.0-based feature branch is not the authoritative candidate.
- Dev_v2.11.x is based on Dev_v2.10.1 / `feature/witch-tools-magic-branch` and retains Magic Branch, Edge Doctor, Edit Tools ordering, and the current registration surface.

## Validation gate

Before acceptance:
- Blender 5.0.1 register/unregister and required panel order;
- Advanced Clean header layout and individual section execution;
- main Clean enabled-section execution;
- Shift selection-only behavior for both global and individual section actions;
- Transform editing;
- Analyze count parity and offending-element parity;
- STL export/re-import;
- Make Manifold / Auto Fix / Advanced Clean;
- Undo/Redo;
- mode handling;
- normals and winding;
- material and edge/custom-data preservation;
- manifold safety where applicable;
- malformed selections;
- failure without partial destructive changes;
- regression test of Dev_v2.10.1 Magic Branch/Inject/Edge Doctor behavior;
- secondary Blender 4.5 compatibility checks for shared/BG3 workflows that still require 4.5.

## Deferred / research

### WT-PRINT-005 — Threshold/preferences pass

- Status: deferred.
- Keep the standard Toolbox thresholds hidden unless the user later demonstrates a real need to edit them inside Witch Tools.

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

Package/install Dev_v2.11.2 in Blender 5.0.1 and rerun Analyze Mesh on the exact `_CAP 3` mesh used for the parity failure. The target result is the original Toolbox count set: `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`. Fix any remaining detector mismatch before WT-PRINT-004 click-to-select work.
