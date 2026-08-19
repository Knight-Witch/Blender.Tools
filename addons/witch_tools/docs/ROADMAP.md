# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate — Dev_v2.10.0

### WT-XFORM-001 — Witch Tools Transform panel

- Status: active candidate; Blender 4.5 validation pending
- Feature packet: `/addons/witch_tools/docs/features/print3d_transform/`
- Target Blender: `4.5.0`
- Scope: top-level Transform below Mode Switcher; object Location/Rotation/Scale; selected-mesh local Location editing in Edit Mode.
- Remaining: registration/UI, interaction, undo/redo, save/reopen.

### WT-PRINT-001 — Consolidated 3D Print Analyze

- Status: active candidate; Blender 4.5 validation pending
- Scope: Check All + consolidated result counts for non-manifold, winding/contiguity, intersections, shells, zero geometry, non-flat faces, thin faces, sharp edges, and overhangs.
- Deliberately omitted: Volume/Area, individual filter buttons/settings, Hollow, Bisect, Align XY, Scale To.
- Remaining: count parity on constructed defect meshes; possible result click-to-select parity after validation.

### WT-PRINT-002 — Clean & Repair consolidation

- Status: active candidate; Blender 4.5 validation pending
- Scope: Make Manifold; Mesh Repair-derived Auto Fix; Instant Clean-derived Advanced Clean.
- UI decisions: Global Fix before Local Fix; Advanced Clean sections Repair / Manifold / Topology / Normals / Dissolve; no Object Data; no Make Planar; compact responsive toggle rows.
- Remaining: full topology safety test plan, especially Intersect Volumes, selection-only cleanup, normals/winding, attributes, and undo/redo.

### WT-PRINT-003 — Simplified STL export

- Status: active candidate; Blender 4.5 validation pending
- Scope: folder + Export STL only, fixed STL format.
- Remaining: export/re-import validation.

### WT-PRINT-004 — Result selection/highlight parity

- Status: planned after Analyze count validation
- Add compact selection/highlight actions only if they improve the user's workflow; do not restore the original toolbox's full settings surface.

### WT-PRINT-005 — Analyze threshold/preferences pass

- Status: deferred
- Expose only thresholds that prove useful in actual print-prep work.

### WT-XFORM-002 — Global/local mesh coordinate display

- Status: research
- Current Edit Mode Transform Location is object-local. A world/local switch may be considered later.

## Retained Dev_v2.9.0 Precision Edit candidate

### WT-PREC-001 — Coordinate Copy

- Status: active retained candidate; Blender 4.5 validation pending
- Feature packet: `/addons/witch_tools/docs/features/precision_edit/`
- Global / Local coordinate capture/application; XYZ masks; Location / Rotation / Scale; vertex/edge/face source capture; independent targets; multi-object conversion; protection preflight; default `Ctrl+Shift+C` Apply shortcut.

### WT-PREC-002 — Planar Edit: Plane Lock / Level

- Status: active retained candidate; Blender 4.5 validation pending
- Plane Lock stores object-local per-vertex axis constraints.
- Level applies exact source world coordinates to independent targets.

### WT-VINJ-002 — Manual Inject New

- Status: active retained candidate; Blender 4.5 validation pending
- Solo / Branch / Slide; XYZ placement; straight Rail capture; modal commit/cancel; Vertex Lock / Plane Lock coordination.
- Slide remains vertex-only; Branch remains edge-connection only.

### WT-PREC-003 — Blender 4.5 production validation

- Status: planned immediate alongside Dev_v2.10.0 validation

### WT-PREC-004 — Curved/polyline Inject New rails

- Status: research

### WT-PREC-005 — Branch side-face / extrusion mode

- Status: deferred

### WT-PREC-006 — Multi-object topology Inject New

- Status: deferred

### WT-PREC-007 — Plane Lock world-frame mode

- Status: research

### WT-PREC-008 — Precision viewport previews / gizmos

- Status: research

### WT-PREC-009 — Witch Dock / Quickbar thin wrappers

- Status: deferred until the canonical Witch Tools backend is accepted in Blender 4.5

## Guided Align — retained from Dev_v2.8.0

### WT-ALIGN-001 — Align Vertices / Edges / Faces

- Status: active retained candidate; Blender 4.5 validation pending
- Parent anchor capture; world XYZ and arbitrary Custom Guide matching; straight captured rails; mapping; rigid-shape preservation; multi-object conversion; protection preflight; non-mutating Analyze and transaction-first Apply.
- Inherited documentation gap remains: older roadmap references `/docs/features/align_selection/`, which is absent from the source branch. Do not fabricate historical files.

### WT-ALIGN-002 — Blender 4.5 production validation

- Status: planned

### WT-ALIGN-003 — Witch Dock / Quickbar thin wrapper

- Status: deferred until backend validation

### WT-ALIGN-004 — Curved/polyline movement rails

- Status: research

### WT-ALIGN-005 — Guided Align rotation and scale matching

- Status: deferred

### WT-ALIGN-006 — Surface projection and nearest-point modes

- Status: research

### WT-ALIGN-007 — Capture diagnostics and viewport visualization

- Status: planned after runtime validation

## Baseline preservation

### WT-BASE-001 — Restore auditable direct Witch Tools source

- Status: complete
- Dev_v2.7.0 committed snapshot conflict remains documented.
- Verified recovery baseline: Dev_v2.6.1.
- Dev_v2.8.0 Guided Align parent commit: `fc94b7c27d0b850699e79b973a0548a2193eb525`.
- Current direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`.

### WT-BASE-002 — Audit integration into `Blender_Dev`

- Status: planned after Blender runtime acceptance

### WT-BASE-003 — Audit public/update compatibility

- Status: planned before any official release

## Selection infrastructure

### WT-SEL-001 — Persistent mesh Selection Slots

- Status: active retained implementation
- Remaining: Blender 4.5 N-panel confirmation, save/reopen, multi-object restore, topology marker propagation, undo/redo.

### WT-SEL-002 — Selection Slot diagnostics

- Status: planned

### WT-SEL-003 — Additive/subtractive restore modes

- Status: deferred

## Topology development

### WT-VINJ-001 — Auto-Aligned Vertex Inject

- Status: active retained MVP
- Remains the separate **Edge / Vertex Inject** A/B/C → D repair workflow.

### WT-CURV-001 — Curvature Sync circular multi-chain prototype

- Status: active MVP
- Primary production collar workflow was previously user-validated in Blender 4.5.
- Remaining: formal undo/redo, normals/manifold/print-fit validation, broader missing/surplus topology support.

### WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces

- Status: planned
- Remains distinct from the imported/general cleanup tools in Dev_v2.10.0.

## Protection infrastructure

### WT-PROT-001 — Existing Vertex Lock integration

- Status: active

### WT-PROT-002 — Protected/ignored zone permissions

- Status: active partial implementation

### WT-PROT-003 — Plane Lock axis constraints

- Status: active retained candidate; Blender 4.5 validation pending

## Immediate next step

Install Witch Tools `Dev_v2.10.0` in Blender 4.5 and execute `/addons/witch_tools/docs/features/print3d_transform/TEST_PLAN.md`. Start with registration/unregistration, top-level panel rendering/order, Transform selected-vertex Location, Analyze Check All, and a simple Make Manifold case. Then run topology safety and regression tests. Fix only failures found before broadening scope.

## Scope policy

No discussed feature automatically enters an official release. Dev_v2.10.0 is a development candidate. Result-selection parity, additional Analyze thresholds, world/local Transform display, curved rails, branch extrusion/side faces, multi-object topology injection, world-frame Plane Lock, viewport previews, and Witch Dock/Quickbar integration remain separate follow-up scopes unless explicitly promoted.
