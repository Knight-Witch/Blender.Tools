# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.10.0`
- Development branch: `feature/witch-tools-3d-print-transform`
- Parent baseline: `feature/witch-tools-precision-edit` / Witch Tools `Dev_v2.9.0`
- Target Blender: `4.5.0`

## Implemented source

- Added top-level Transform directly below Mode Switcher.
- Added editable object Location / Rotation / Scale.
- Added Edit Mode selected-vertex local Location median with delta translation.
- Added top-level 3D Print Tools above Edit Tools.
- Added simplified STL Export.
- Added consolidated Analyze Mesh / Check All results.
- Added Make Manifold.
- Added Auto Fix with Global Fix before Local Fix.
- Added Advanced Clean with Repair / Manifold / Topology / Normals / Dissolve and requested condensed toggle layouts.
- Removed the requested unused source UI from this integrated presentation: volume/area, per-check filter controls, Hollow, Bisect, Align XY, Scale To, export options, Instant Clean Object Data, and Make Planar.

## Source modules

New:

- `panel_transform.py`
- `panel_print3d.py`
- `print3d_tools.py`
- `instant_clean_core.py`
- `mesh_repair_props.py`
- `mesh_repair_backend.py`

Modified:

- `__init__.py`
- `state.py`
- `panels.py`
- `registration.py`

## Static validation performed

- New/modified Python modules were parsed with `py_compile` in the implementation environment.
- Thin-face BVH result indexing was corrected after API review.
- Branch is isolated from the public/default branches.

## Runtime validation not performed

No Blender executable is available in the implementation environment. The following remain untested in Blender 4.5:

- add-on register/unregister;
- nested panel rendering;
- icon enum validity beyond static review;
- all new operator execution;
- exact Analyze Mesh count parity with Blender's original 3D Print Toolbox;
- selection-highlight behavior (not implemented in this first candidate; counts only);
- Transform edit-mode interaction during real UI edits;
- Auto Fix Intersect Volumes topology-rebuilding path;
- Smooth by Angle handling in Advanced Clean Normals;
- STL export operator signature/runtime behavior;
- undo/redo;
- save/reopen;
- normals/winding;
- material/edge-attribute preservation;
- manifold safety;
- malformed-selection behavior;
- failure without partial destructive changes.

## Known design limitations

- Edit-mode mesh vertices expose editable Location only. Rotation and Scale in that mode are object transforms because vertices do not have independent rotation/scale properties.
- Analyze Mesh currently provides result counts, not the original toolbox's click-to-select result buttons.
- Thin Faces uses a conservative 1 mm ray-distance check and must be compared against the original toolbox on known geometry.
- Intersect Volumes is intentionally destructive and must be validated on duplicate files before routine use.

## Next exact step

Install `Dev_v2.10.0` over the current Witch Tools development baseline in Blender 4.5 and execute `TEST_PLAN.md`, beginning with registration, panel order/rendering, Transform Location, and Check All. Fix only failures found in that validation before broadening the feature.
