# Witch Tools Project State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-3d-print-transform`
- Parent candidate: `feature/witch-tools-precision-edit` / `Dev_v2.9.0`
- Intended integration branch: `Blender_Dev`
- Development package: `Witch_Tools_Dev`
- Default target Blender version: `4.5.0`
- Public/default release branches modified: no

## Current candidate

- Version: `Dev_v2.10.0`
- Scope: Transform N-panel consolidation plus integrated 3D Print Tools, retaining all `Dev_v2.9.0` Precision Edit and earlier functionality
- Source: `addons/witch_tools/dev/Witch_Tools_Dev/`
- Installable full ZIP: not yet cut from this branch
- Runtime status: source candidate; Blender 4.5 validation pending

## Current implementation

### Transform

A new top-level **Transform** panel sits directly below Mode Switcher.

- Object Mode: editable Location, Rotation Mode/Rotation, and Scale.
- Mesh Edit Mode Location: reads the local-space median of selected vertices and translates the selected vertices by the edited delta.
- Mesh Edit Mode Rotation / Scale: edits the active object transform; no invented per-vertex rotation/scale model is introduced.
- Location / Rotation / Scale are collapsible child panels.

### 3D Print Tools

A new top-level **3D Print Tools** panel sits above Edit Tools.

#### Export

- folder picker;
- one Export STL button;
- STL fixed format;
- no source export-options UI.

#### Analyze Mesh

- Check All only;
- consolidated result counts for Non-manifold Edges, Bad Contiguous Edges, Intersect Faces, Shells, Zero Faces, Zero Edges, Non-flat Faces, Thin Faces, Sharp Edges, and Overhang Faces.

Intentionally omitted from the integrated UI:

- Volume / Area statistics;
- individual Solid / Intersections / Shells filter controls;
- source threshold-control grid;
- Hollow;
- Bisect;
- Align XY;
- Scale To.

Current limitation: result counts are implemented; original-tool click-to-select/highlight parity is deferred until count validation.

#### Clean & Repair

Order:

1. Make Manifold
2. Auto Fix
3. Advanced Clean

**Auto Fix** is based on the user-supplied Mesh Repair workflow, with Global Fix before Local Fix. It retains Tri/Quad, Face Normal, Noise Shells, Spikes, Intersect Face, Intersect Volumes, Fill Holes, and local Select/Normal/Refine/Remesh/Smooth/Reduce controls.

**Advanced Clean** is based on the user-supplied Instant Clean workflow and contains Repair, Manifold, Topology, Normals, and Dissolve. Object Data and Make Planar are deliberately omitted. Requested compact toggle bars and narrow-panel wrapping are implemented.

## Source files changed for Dev_v2.10.0

New source modules:

- `panel_transform.py`
- `panel_print3d.py`
- `print3d_tools.py`
- `instant_clean_core.py`
- `mesh_repair_props.py`
- `mesh_repair_backend.py`

Modified source modules:

- `__init__.py`
- `state.py`
- `panels.py`
- `registration.py`

New feature documentation:

- `docs/features/print3d_transform/SPEC.md`
- `docs/features/print3d_transform/STATE.md`
- `docs/features/print3d_transform/ROADMAP.md`
- `docs/features/print3d_transform/TEST_PLAN.md`

Updated project documentation:

- `docs/PROJECT_STATE.md`
- `docs/UI_MAP.md`
- `docs/NOTES_CHANGELOG.md`

## Retained current functionality

The existing Dev_v2.9.0 Edit Tools order and contracts are retained:

1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Inject New
5. Object Snap
6. Edge / Vertex Inject
7. Curvature Sync
8. Align Vertices / Edges / Faces
9. Selection Slots
10. Vertex Locks / remaining Edit Tools controls

Previously user-validated production behavior retained from earlier builds includes the Dev_v2.5.2 Curvature Sync collar workflow and Quickbar Selection Slots workflow. Those prior validations do not imply the new Dev_v2.10.0 code has been validated.

## Static validation performed

- New/modified Python source modules parse/compile successfully with Python `py_compile` in the implementation environment.
- The candidate is isolated on a feature branch created from the current Dev_v2.9.0 source candidate.
- Thin-face BVH ray result indexing was corrected after API review.
- Target remains Blender 4.5.0.

## Runtime validation not performed

No Blender executable is available in the implementation environment. Do not claim the Dev_v2.10.0 candidate works in Blender until the feature test plan is executed.

Pending:

1. register/unregister;
2. panel order, nested child rendering, icons, and responsive wrapping;
3. Transform object and selected-vertex interaction;
4. Check All parity on known defect meshes;
5. Make Manifold execution and undo/redo;
6. Auto Fix Global and Local execution;
7. Advanced Clean category execution and selection-only behavior;
8. Intersect Volumes destructive topology path;
9. Smooth by Angle behavior in Blender 4.5;
10. STL export/re-import;
11. topology-changing undo/redo;
12. normals and face winding;
13. material and edge-attribute preservation;
14. manifold safety;
15. protected-zone behavior where applicable;
16. malformed or ambiguous selections;
17. failure without partial destructive changes;
18. save/reopen;
19. regression against retained Dev_v2.9.0 tools.

## Known limitations / decisions

- Edit-mode mesh Location is object-local in this candidate.
- Mesh vertices do not expose independent rotation/scale fields; those panels remain object transforms in Edit Mode.
- Analyze Mesh currently exposes counts rather than selectable result buttons.
- Thin Faces currently uses a conservative 1 mm proximity check and requires original-tool parity testing.
- Intersect Volumes is opt-in topology rebuilding and should be tested on duplicate files before routine use.
- Hollow is not included: it can be useful for intentionally making a solid shell hollow/material-saving, but it is not part of the user's routine inspection/repair workflow.
- Bisect is not included: it is a plane-cut utility and duplicates normal Blender editing workflows.
- Align XY is not included: it is primarily print-bed orientation/alignment and overlaps the user's existing/general alignment workflows.

## Next exact implementation step

Install the Dev_v2.10.0 candidate in Blender 4.5 and execute `docs/features/print3d_transform/TEST_PLAN.md` in order. Begin with register/unregister, top-level panel order/rendering, Transform Location, Analyze Mesh Check All, and one simple Make Manifold case. Fix only failures found in that validation pass before adding result-selection parity or any additional print tools.
