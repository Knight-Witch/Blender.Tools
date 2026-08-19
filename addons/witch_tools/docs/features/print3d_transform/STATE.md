# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.0`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Target Blender: `4.5.0`

## Artifact

- Full ZIP: `Witch_Tools_Dev_v2_11_0_3D_Print_Transform_Blender_4_5.zip`
- SHA-256: `d15ec5393c82bdf1fa4027fc161edcbda2fb0b426e5802a64b107f37d78e50d7`
- GitHub Actions: passed
- 67 Python files parsed
- 145 unique UI/operator IDs scanned; no duplicate `bl_idname` values
- cache/package hygiene: passed
- ZIP integrity: passed
- Blender runtime: pending

## Baseline correction

The first 3D Print/Transform integration pass was created from the older Dev_v2.9.0 precision-edit branch. That is not the current Witch Tools baseline. Dev_v2.11.0 ports the feature modules onto the newer Dev_v2.10.1 Magic Branch source so the newer Magic Branch, Edge Doctor, Edit Tools ordering, and topology fixes are retained.

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
- `CHANGELOG.md`

## Static/package validation performed

GitHub Actions and a second local inspection of the downloaded artifact verified:
- Python AST parsing across 67 Python files;
- 145 unique `bl_idname` values with zero duplicates;
- Dev_v2.11.0 / Blender 4.5 metadata;
- required Transform/3D Print and retained Magic Branch/Edge Doctor source presence;
- no `__pycache__`, `.pyc`, or `.pyo` files;
- ZIP integrity;
- SHA-256 match.

## Runtime validation not performed

Still untested in Blender 4.5:
- add-on register/unregister;
- nested panel rendering and icon validity;
- Transform UI edits and Undo/Redo;
- exact Analyze Mesh count parity with Blender's original 3D Print Toolbox;
- selection-highlight behavior (planned after detector parity; not implemented in Dev_v2.11.0);
- Make Manifold;
- Auto Fix, especially Intersect Volumes;
- Advanced Clean selection-only and topology-changing paths;
- STL export/reimport;
- normals/winding;
- material/edge/custom-data preservation;
- manifold safety;
- malformed selections;
- failure without partial destructive changes;
- Dev_v2.10.1 Magic Branch/Inject/Object Snap/Edge Doctor regression.

## Known design limitations

- Edit-mode mesh vertices expose editable Location only. Rotation and Scale in that mode are object transforms because vertices do not have independent rotation/scale properties.
- Analyze Mesh currently provides result counts, not the original toolbox's click-to-select result buttons. Click-to-select is now a required follow-up once detector parity is confirmed.
- Thin Faces and intersection detection must be compared against the original toolbox before equivalence is claimed.
- Intersect Volumes is intentionally topology-rebuilding and must be validated on duplicate files before routine use.

## Next exact step

Install the full Dev_v2.11.0 ZIP in Blender 4.5 and begin with registration, panel order/rendering, Transform Location, and Check All parity. Fix failures found there before adding result click-to-select or broadening the feature.
