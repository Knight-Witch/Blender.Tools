# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.0`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` at Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Target Blender: `4.5.0`

## Baseline correction

The first 3D Print/Transform integration pass was created from the older Dev_v2.9.0 precision-edit branch. That is not the current Witch Tools baseline. Dev_v2.11.0 ports the feature modules onto the newer Dev_v2.10.1 Magic Branch source so the newer Magic Branch, Edge Doctor, Edit Tools ordering, and topology fixes are retained.

## Implemented source candidate

- Transform top-level panel directly below Mode Switcher.
- Object Location / Rotation / Scale editing.
- Edit Mode selected-vertex local Location median with delta translation.
- 3D Print Tools top-level panel above Edit Tools.
- Simplified STL Export.
- Consolidated Analyze Mesh / Check All result counts.
- Make Manifold.
- Auto Fix with Global Fix before Local Fix.
- Advanced Clean with Repair / Manifold / Topology / Normals / Dissolve and condensed responsive controls.
- Requested unused source UI omitted: volume/area, separate check filters, Hollow, Bisect, Align XY, Scale To, export options, Object Data, Make Planar.

## Source modules added

- `panel_transform.py`
- `panel_print3d.py`
- `print3d_tools.py`
- `instant_clean_core.py`
- `mesh_repair_props.py`
- `mesh_repair_backend.py`

## Integration modules modified

- `__init__.py`
- `state.py`
- `panels.py`
- `registration.py`

The integration explicitly retains Dev_v2.10.1 `operators_magic_branch`, `operators_edge_doctor`, `operators_edit_tool_order`, and the rest of the current registration surface.

## Known inherited working state

From the Dev_v2.10.x baseline, prior Blender 4.5 user testing confirmed selected Magic Branch/Inject behavior documented in the parent project state. Dev_v2.10.1 itself still requires regression retest for its runtime fixes.

## New-feature runtime status

Blender 4.5 runtime validation has not yet been performed for Dev_v2.11.0. Static package validation is performed by the packaging workflow before a downloadable artifact is accepted.

Still requiring Blender 4.5 testing:
- register/unregister;
- top-level and nested panel rendering;
- Transform interaction;
- Analyze count parity with original 3D Print Toolbox;
- result click-to-select behavior (planned after count parity; not in this candidate);
- Make Manifold;
- Auto Fix, especially Intersect Volumes;
- Advanced Clean selection-only and topology-changing operations;
- STL export/reimport;
- Undo/Redo and mode restoration;
- normals/winding;
- materials and edge/custom-data preservation;
- manifold safety;
- malformed selections;
- failure without partial destructive changes;
- regression of Magic Branch, Edge Doctor, Inject New, Object Snap, and Edit Tools ordering.

## Known design limitations

- Mesh vertices expose editable Location only; Rotation and Scale in Edit Mode remain object transforms.
- Analyze Mesh currently provides counts only. Click-to-select result parity is now a planned required follow-up once detection parity is confirmed.
- Thin-face and intersection detection must be compared against the original 3D Print Toolbox before equivalence is claimed.
- Intersect Volumes is a topology-rebuilding path and must be treated as destructive until Blender tests establish preservation behavior.

## Next exact step

Install the full Dev_v2.11.0 ZIP in Blender 4.5. First verify registration and panel order, then Transform Location, then compare Check All against the original 3D Print Toolbox on the same meshes. Only after analyzer parity is established should result click-to-select actions be wired to the new diagnostics.
