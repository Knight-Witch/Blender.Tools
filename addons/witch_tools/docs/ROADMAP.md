# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate — Dev_v2.11.2

Primary runtime target: Blender `5.0.1`  
Secondary compatibility target: Blender `4.5.0`  
Branch: `feature/witch-tools-3d-print-transform-v2-11`  
Parent baseline: Dev_v2.10.1 Magic Branch

### WT-XFORM-001 — Transform panel

- Status: active candidate.
- Top-level under Mode Switcher.
- Object Location/Rotation/Scale; selected-mesh local Location.
- Remaining: Blender 5.0.1 UI/Undo/save-reopen validation, then relevant 4.5 compatibility checks.

### WT-PRINT-001 — Analyze Mesh

- Status: active parity-fix candidate.
- Dev_v2.11.1 Blender 5.0.1 comparison matched 6 of 10 Toolbox counts but failed Non-flat, Thin, Sharp, and Overhang.
- Dev_v2.11.2 replaces those approximations and related detector internals with 3D Print Toolbox-equivalent algorithms/default thresholds.
- Immediate gate: rerun `_CAP 3` and match the original `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79` result set.
- After count parity, compare exact offending-element identity before click-to-select work.

### WT-PRINT-002 — Clean & Repair

- Status: active candidate.
- Make Manifold, Auto Fix, Advanced Clean.
- Global Fix precedes Local Fix.
- Advanced Clean retains the Dev_v2.11.1 Instant Clean-style child-section structure and per-section play actions.
- Original-style bodies are retained except for the explicitly requested compact Manifold, Topology, and Normals changes; Object Data/Make Planar stay removed and Dissolve stays last.
- Remaining: Blender 5.0.1 custom-header/execution tests plus full topology/attribute/Undo safety validation.

### WT-PRINT-003 — STL Export

- Status: active candidate.
- Folder + fixed STL export.
- Remaining: Blender 5.0.1 export/re-import validation and secondary 4.5 check if required.

### WT-PRINT-004 — Analyze click-to-select parity

- Status: planned required follow-up.
- Add exact result-element selection/highlighting only after analyzer count and offending-element parity are established.

### WT-MBR-001 — Magic Branch

- Status: active retained baseline.
- Dev_v2.10.1 runtime-fix candidate remains pending regression retest for multi-contact merge, navigation, Paver axis growth/return-path merge, selection-mode sync, and Object Snap Undo.

### WT-VINJ-002 — Inject New magnetic expansion

- Status: active retained baseline.
- Solo/Branch/multi-edge Slide, XYZ, Magnetic Snap, Auto-Merge.
- Dev_v2.10.1 multi-edge/merge corrections retained and require regression test after Dev_v2.11 integration.

### WT-EDOC-001 — Edge Doctor

- Status: active retained baseline.
- Missing Vertex / Edge Injector, Alignment Fixer, Curvature Sync remain nested under Edge Doctor.

### WT-UI-001 — Reorderable Edit Tools

- Status: active retained baseline.
- Preference-backed Edit Tools ordering; integration regression check required.

### WT-PREC-001 / 002 — Coordinate Copy / Planar Edit

- Status: active retained baseline.
- Existing Dev_v2.9+ functionality remains canonical and unchanged by Dev_v2.11.2.

## Validation gate

Primary Blender 5.0.1 tests:
1. register/unregister and panel order;
2. Analyze `_CAP 3` exact parity, then broader detector identity tests;
3. Advanced Clean Instant Clean-style headers/body layout;
4. main Clean enabled-section execution and per-section play execution, including Shift-selection behavior;
5. Transform object/edit behavior;
6. Make Manifold;
7. Auto Fix and Advanced Clean topology safety;
8. STL export/re-import;
9. Undo/Redo, mode restoration, normals/winding, materials and edge/custom data, manifold safety, malformed selections, safe failures;
10. Dev_v2.10.1 Magic Branch/Inject/Edge Doctor/Object Snap/Edit Tools-order regression.

Secondary Blender 4.5 tests follow for shared/BG3 workflows that still require 4.5. Do not claim a path compatible until it is actually tested there.

## Guided Align / Alignment Fixer

- Status: active retained; nested under Edge Doctor.
- Canonical `mesh.wt_guided_align_*` backend remains unchanged.
- Curved/polyline rails remain research.

## Deferred / research

- Curved/polyline Inject rails: research.
- Branch extrusion/side-face mode: deferred.
- Multi-object topology creation: deferred.
- Plane Lock world-frame mode: research.
- Dynamic hover-added Slide fan: deferred.
- Arbitrary face-interior Auto-Merge retopology: research.
- A/B/C repair viewport labels: deferred QoL.
- 3D-print threshold/preferences expansion: deferred; current backend uses the standard Toolbox defaults without exposing the grid.
- Transform mesh world/local display switch: research.

## Explicit Dev_v2.11.x exclusions

- 3D Print Toolbox Volume / Area
- separate Solid / Intersections / Shells controls
- Hollow
- Bisect
- Align XY
- Scale To
- export options UI
- Instant Clean Object Data
- Instant Clean Make Planar

## Baseline preservation

- Dev_v2.11.x is based on current Dev_v2.10.1, not the stale earlier Dev_v2.9.0 feature baseline.
- Current direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`.
- Public release branches and Witch Dock/Quickbar remain unchanged.
- Integration into `Blender_Dev` remains planned only after runtime acceptance.

## Immediate next step

Package and install Dev_v2.11.2 in Blender 5.0.1 and rerun Analyze on the same `_CAP 3` mesh. Fix any remaining parity mismatch before implementing WT-PRINT-004 click-to-select or broadening scope.
