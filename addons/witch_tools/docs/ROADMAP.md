# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate — Dev_v2.11.4

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

- Status: active exact-backend candidate.
- Dev_v2.11.3 runtime still disagreed with the original 3D Print Toolbox on the same `_CAP 3` object: Non-flat 73 vs 98 and Overhang 80 vs 79.
- Dev_v2.11.4 removes the independent Witch Tools detector and invokes the installed Toolbox `mesh.print3d_check_all` directly, then mirrors its live report.
- There is no alternate Analyze fallback; missing Toolbox backend/report is an explicit error.
- Immediate gate: original Toolbox Check All and Witch Tools Check All must display identical values on unchanged fixtures.

### WT-PRINT-004 — Analyze click-to-select parity

- Status: active candidate.
- In Edit Mode, non-empty Witch Tools results invoke the original Toolbox `mesh.print3d_select_report` using its live report index.
- Remaining: exact element-selection parity validation.

### WT-PRINT-002 — Clean & Repair

- Status: active candidate.
- Make Manifold, Auto Fix, Advanced Clean.
- Global Fix precedes Local Fix.
- Advanced Clean retains Instant Clean-style child sections, per-section play actions, requested compact controls, no Object Data/Make Planar, Dissolve last.
- Remaining: Blender 5.0.1 execution tests plus topology/attribute/Undo safety validation.

### WT-PRINT-003 — STL Export

- Status: active candidate with initial runtime success.
- UI remains folder + fixed STL export.
- Dev_v2.11.3 added native exporter validation plus a direct evaluated-mesh binary STL fallback.
- User confirmed the Dev_v2.11.3 hotfix now creates the STL file in Blender 5.0.1.
- Remaining: re-import dimensions/orientation, multi-object, modifier, negative-scale/fallback tests, and Blender 4.5 smoke test.

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
2. original Toolbox vs Witch Tools exact Analyze displayed-count parity;
3. original Toolbox vs Witch Tools exact Analyze result-selection parity in Edit Mode;
4. explicit Analyze failure with Toolbox disabled/unavailable;
5. STL export regression plus re-import/multi-object/modifier/transform/failure validation;
6. Advanced Clean headers and main/per-section execution including Shift behavior;
7. Transform object/edit behavior;
8. Make Manifold / Auto Fix / Advanced Clean topology safety;
9. Undo/Redo, mode restoration, normals/winding, materials/custom data, malformed selections, safe failures;
10. Dev_v2.10.1 Magic Branch/Inject/Edge Doctor/Object Snap/Edit Tools regression.

Secondary Blender 4.5 tests follow for shared/BG3 workflows that still require 4.5.

## Deferred / research

- Exact self-contained vendoring of the current 3D Print Toolbox source if Witch Tools later must Analyze without the extension installed: research/deferred. Do not hand-reimplement detectors again.
- Curved/polyline Inject rails: research.
- Branch extrusion/side-face mode: deferred.
- Multi-object topology creation: deferred.
- Plane Lock world-frame mode: research.
- Dynamic hover-added Slide fan: deferred.
- Arbitrary face-interior Auto-Merge retopology: research.
- A/B/C repair viewport labels: deferred QoL.
- 3D-print threshold/preferences expansion: deferred.
- Transform mesh world/local display switch: research.

## Explicit Dev_v2.11.x UI exclusions

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

Package/install Dev_v2.11.4 in Blender 5.0.1 with 3D Print Toolbox enabled. Verify exact count parity on `_CAP 3`, then exact click-to-select parity in Edit Mode. Do not add a second Analyze detector if the bridge has a mapping/resolution bug.
