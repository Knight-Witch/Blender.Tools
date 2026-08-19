# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate — Dev_v2.11.3

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
- Dev_v2.11.2 replaced the approximations with 3D Print Toolbox-equivalent algorithms/default thresholds; Dev_v2.11.3 retains this.
- Immediate Analyze gate: rerun `_CAP 3` and match `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`, then compare exact offending-element identity.

### WT-PRINT-002 — Clean & Repair

- Status: active candidate.
- Make Manifold, Auto Fix, Advanced Clean.
- Global Fix precedes Local Fix.
- Advanced Clean retains Instant Clean-style child sections, per-section play actions, requested compact controls, no Object Data/Make Planar, Dissolve last.
- Remaining: Blender 5.0.1 execution tests plus topology/attribute/Undo safety validation.

### WT-PRINT-003 — STL Export

- Status: active hotfix candidate.
- UI remains folder + fixed STL export.
- Prior Blender 5.0.1 runtime attempt produced no expected output.
- Dev_v2.11.3 validates native exporter completion/file creation, attempts legacy export compatibility, and provides a direct evaluated-mesh binary STL fallback with transactional file replacement.
- Remaining: Blender 5.0.1 one/multi-object/modifier/transform/failure/re-import validation and Blender 4.5 secondary compatibility smoke test.

### WT-PRINT-004 — Analyze click-to-select parity

- Status: planned required follow-up.
- Add exact result-element selection/highlighting only after analyzer count and offending-element parity are established.

### WT-MBR-001 — Magic Branch

- Status: active retained baseline.
- Dev_v2.10.1 runtime-fix candidate remains pending regression retest for multi-contact merge, navigation, Paver axis growth/return-path merge, selection-mode sync, and Object Snap Undo.

### WT-VINJ-002 — Inject New magnetic expansion

- Status: active retained baseline.
- Solo/Branch/multi-edge Slide, XYZ, Magnetic Snap, Auto-Merge; Dev_v2.10.1 corrections retained.

### WT-EDOC-001 — Edge Doctor

- Status: active retained baseline.
- Missing Vertex / Edge Injector, Alignment Fixer, Curvature Sync remain nested under Edge Doctor.

### WT-UI-001 — Reorderable Edit Tools

- Status: active retained baseline.

### WT-PREC-001 / 002 — Coordinate Copy / Planar Edit

- Status: active retained baseline.

## Validation gate

Primary Blender 5.0.1 tests:
1. register/unregister and panel order;
2. Export STL physical-file/re-import validation, including one/multi-object, modifiers, transforms and failure reporting;
3. Analyze `_CAP 3` exact parity, then broader detector identity tests;
4. Advanced Clean headers and main/per-section execution including Shift behavior;
5. Transform object/edit behavior;
6. Make Manifold / Auto Fix / Advanced Clean topology safety;
7. Undo/Redo, mode restoration, normals/winding, materials/custom data, malformed selections, safe failures;
8. Dev_v2.10.1 Magic Branch/Inject/Edge Doctor/Object Snap/Edit Tools regression.

Secondary Blender 4.5 tests follow for shared/BG3 workflows that still require 4.5.

## Deferred / research

- Curved/polyline Inject rails: research.
- Branch extrusion/side-face mode: deferred.
- Multi-object topology creation: deferred.
- Plane Lock world-frame mode: research.
- Dynamic hover-added Slide fan: deferred.
- Arbitrary face-interior Auto-Merge retopology: research.
- A/B/C repair viewport labels: deferred QoL.
- 3D-print threshold/preferences expansion: deferred.
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

- Dev_v2.11.x is based on current Dev_v2.10.1.
- Current direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`.
- Public release branches and Witch Dock/Quickbar remain unchanged.
- Integration into `Blender_Dev` remains planned only after runtime acceptance.

## Immediate next step

Package/install Dev_v2.11.3 in Blender 5.0.1 and validate Export STL first. Then rerun Analyze parity before click-to-select work or scope expansion.
