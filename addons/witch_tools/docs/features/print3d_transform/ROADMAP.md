# 3D Print Tools + Transform Roadmap

Statuses: `active`, `planned`, `deferred`, `research`, `rejected`, `complete`.

## Current candidate — Dev_v2.11.0

Target: Blender 4.5.0  
Baseline: Dev_v2.10.1 Magic Branch

### WT-XFORM-001 — Persistent Transform access

- Status: active candidate.
- Top-level Transform directly below Mode Switcher.
- Object Location/Rotation/Scale.
- Selected-mesh object-local Location in Edit Mode.
- Remaining: Blender UI, interaction, Undo/Redo, save/reopen validation.

### WT-PRINT-001 — Consolidated Analyze Mesh

- Status: active candidate.
- Check All plus ten result counts.
- Remaining: exact parity testing against Blender's original 3D Print Toolbox on known meshes.

### WT-PRINT-002 — Clean & Repair consolidation

- Status: active candidate.
- Make Manifold.
- Auto Fix: Global Fix before Local Fix.
- Advanced Clean: Repair, Manifold, Topology, Normals, Dissolve.
- Responsive compact toggle rows implemented for requested controls.
- Remaining: Blender 4.5 topology safety and attribute-preservation validation.

### WT-PRINT-003 — Simplified STL export

- Status: active candidate.
- Folder + Export STL; fixed STL format.
- Remaining: Blender 4.5 export/re-import validation.

### WT-PRINT-004 — Analyze result selection/highlight parity

- Status: planned required follow-up after analyzer parity.
- Make actionable result counts select/highlight the exact offending vertices/edges/faces, matching the workflow value of Blender's original 3D Print Toolbox.
- Do not implement until count/detection parity is verified so selection is not attached to an incorrect detector.

## Baseline preservation

### WT-BASE-PRINT-001 — Port onto current Magic Branch baseline

- Status: complete at source-integration level.
- The initial stale Dev_v2.9.0-based feature branch is not the authoritative candidate.
- Dev_v2.11.0 is based on Dev_v2.10.1 / `feature/witch-tools-magic-branch` and retains Magic Branch, Edge Doctor, Edit Tools ordering, and the current registration surface.

## Validation gate

Before acceptance:
- register/unregister;
- required top-level panel order;
- Transform editing;
- Analyze parity;
- STL export/re-import;
- Make Manifold / Auto Fix / Advanced Clean;
- Undo/Redo;
- mode handling;
- normals and winding;
- material and edge/custom-data preservation;
- manifold safety where applicable;
- malformed selections;
- failure without partial destructive changes;
- regression test of Dev_v2.10.1 Magic Branch/Inject/Edge Doctor behavior.

## Deferred / research

### WT-PRINT-005 — Threshold/preferences pass

- Status: deferred.
- Only expose thresholds that prove useful in the actual print-prep workflow.

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

Install Dev_v2.11.0 in Blender 4.5, verify the new panels appear without regressing Dev_v2.10.1 features, then compare Analyze Mesh counts against the original 3D Print Toolbox. Fix observed parity/runtime failures before implementing click-to-select results.
