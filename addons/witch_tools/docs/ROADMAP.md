# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate — Dev_v2.11.0

Target Blender: `4.5.0`  
Branch: `feature/witch-tools-3d-print-transform-v2-11`  
Parent baseline: Dev_v2.10.1 Magic Branch  
Runtime validation: pending

### WT-XFORM-001 — Transform panel

- Status: active candidate.
- Top-level under Mode Switcher.
- Object Location/Rotation/Scale; selected-mesh local Location.
- Remaining: Blender 4.5 UI/Undo/save-reopen validation.

### WT-PRINT-001 — Analyze Mesh

- Status: active candidate.
- Consolidated Check All with ten counts.
- Remaining: parity against original 3D Print Toolbox.

### WT-PRINT-002 — Clean & Repair

- Status: active candidate.
- Make Manifold, Auto Fix, Advanced Clean.
- Global Fix precedes Local Fix.
- Advanced Clean retains Repair / Manifold / Topology / Normals / Dissolve with condensed responsive UI.
- Remaining: full topology/attribute/Undo safety validation.

### WT-PRINT-003 — STL Export

- Status: active candidate.
- Folder + fixed STL export.
- Remaining: export/re-import validation.

### WT-PRINT-004 — Analyze click-to-select parity

- Status: planned required follow-up.
- Add exact result-element selection/highlighting after analyzer parity is established.

### WT-MBR-001 — Magic Branch

- Status: active retained baseline.
- Dev_v2.10.1 runtime-fix candidate remains pending Blender 4.5 retest for multi-contact merge, navigation, Paver axis growth/return-path merge, selection-mode sync, and Object Snap Undo.

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
- Existing Dev_v2.9+ functionality remains canonical and unchanged by Dev_v2.11.0.

## Validation gate

Immediate Blender 4.5 tests:
1. register/unregister and panel order;
2. Transform object/edit behavior;
3. Analyze parity;
4. Make Manifold;
5. Auto Fix and Advanced Clean topology safety;
6. STL export/re-import;
7. Undo/Redo, mode restoration, normals/winding, materials and edge/custom data, manifold safety, malformed selections, safe failures;
8. Dev_v2.10.1 Magic Branch/Inject/Edge Doctor/Object Snap/Edit Tools-order regression.

Do not broaden scope before this gate passes.

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
- 3D-print threshold/preferences expansion: deferred until actual workflow need is demonstrated.
- Transform mesh world/local display switch: research.

## Explicit Dev_v2.11.0 exclusions

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

- Dev_v2.11.0 is based on current Dev_v2.10.1, not the stale earlier Dev_v2.9.0 feature baseline.
- Current direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`.
- Public release branches and Witch Dock/Quickbar remain unchanged.
- Integration into `Blender_Dev` remains planned only after runtime acceptance.

## Immediate next step

Package and install Dev_v2.11.0 in Blender 4.5. Validate panel rendering and Analyze parity first; fix observed failures before implementing WT-PRINT-004 click-to-select results or other new scope.
