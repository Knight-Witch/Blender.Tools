# Witch Tools Project State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Current candidate: `Dev_v2.11.0`
- Target Blender: `4.5.0`
- Package folder: `Witch_Tools_Dev`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Current artifact

- File: `Witch_Tools_Dev_v2_11_0_3D_Print_Transform_Blender_4_5.zip`
- Full installable package: yes; not a patch
- SHA-256: `d15ec5393c82bdf1fa4027fc161edcbda2fb0b426e5802a64b107f37d78e50d7`
- GitHub Actions validation: passed
- Python source files parsed: 67
- Unique UI/operator `bl_idname` values scanned: 145; duplicate count 0
- Cache/package hygiene: passed
- ZIP integrity: passed
- Blender runtime: pending

## Baseline correction

The first 3D Print/Transform implementation was built from the older Dev_v2.9.0 precision-edit branch. That branch is not the current authoritative Witch Tools baseline. Dev_v2.11.0 instead ports the new modules onto Dev_v2.10.1 so Magic Branch, Edge Doctor, Edit Tools ordering, topology fixes, and the newer registration surface remain present.

## Current candidate scope

### Transform

- New top-level Transform immediately below Mode Switcher.
- Object Mode editable Location, Rotation, Scale.
- Mesh Edit Mode editable selected-vertex object-local Location median using rigid delta translation.
- Rotation/Scale remain object transforms in mesh Edit Mode.

### 3D Print Tools

New top-level panel above Edit Tools:
- Export: folder + fixed STL export.
- Analyze Mesh: Check All + ten consolidated result counts.
- Clean & Repair: Make Manifold; Auto Fix; Advanced Clean.
- Auto Fix orders Global Fix before Local Fix.
- Advanced Clean retains Repair, Manifold, Topology, Normals, Dissolve with requested compact/responsive controls.
- Removed from the integrated UI: Volume/Area, separate Solid/Intersections/Shells controls, Hollow, Bisect, Align XY, Scale To, export options, Instant Clean Object Data, Make Planar.

Analyze result click-to-select behavior is not yet in Dev_v2.11.0. It is a required follow-up after detector/count parity is validated against Blender's original 3D Print Toolbox.

## Retained Dev_v2.10.1 baseline

The candidate preserves the current Magic Branch / Inject New / Edge Doctor / Edit Tools ordering code and all other Dev_v2.10.1 source modules. Dev_v2.10.0 had user-confirmed Blender 4.5 behavior for several magnetic editing paths; Dev_v2.10.1 runtime-fix changes remain pending regression retest as previously documented.

## Last completed work

- Confirmed the current authoritative branch/version before rebuilding the requested feature.
- Created `feature/witch-tools-3d-print-transform-v2-11` from Dev_v2.10.1.
- Ported six modular 3D Print/Transform source modules from the isolated earlier feature work.
- Rewired registration and panel aggregation against the current Dev_v2.10.1 registration surface rather than replacing it with stale Dev_v2.9.0 wiring.
- Bumped development identity to Dev_v2.11.0 targeting Blender 4.5.
- Added/updated the 3D Print + Transform specification, state, roadmap, and topology-aware Blender test plan.
- Built a full installable ZIP through GitHub Actions.
- Validated 67 Python files, 145 unique UI/operator IDs, package hygiene, version/panel-order contracts, ZIP integrity, and SHA-256.
- Independently rechecked the downloaded ZIP locally for Python AST parsing, duplicate IDs, required files, cache hygiene, and ZIP integrity.

## Current known-working state

Inherited runtime results are only those already recorded for Dev_v2.10.0. Dev_v2.11.0 itself has not been run in Blender 4.5 yet. Static/package validation does not establish Blender runtime success.

## Active problems / limitations

1. Dev_v2.11.0 register/unregister and panel rendering require Blender 4.5 testing.
2. Transform Edit Mode coordinate editing requires runtime/Undo validation.
3. Analyze Mesh detectors require direct parity comparison with the original 3D Print Toolbox.
4. Analyze result click-to-select is intentionally deferred until detector parity is confirmed.
5. Make Manifold, Auto Fix, and Advanced Clean require full topology safety/attribute tests.
6. Intersect Volumes is a destructive topology-rebuilding path and may not preserve all custom data.
7. STL export requires Blender 4.5 export/re-import validation.
8. Dev_v2.10.1 Magic Branch/Inject/Object Snap fixes still require their existing regression retest after integration.
9. No Blender version beyond 4.5 is claimed compatible.

## Next exact implementation step

Install the full Dev_v2.11.0 ZIP in Blender 4.5. Verify registration and the top-level order first. Then test Transform Location. Then run Analyze Mesh and the original 3D Print Toolbox on the same known meshes and record count differences. Fix any detector/runtime discrepancies before adding click-to-select result actions.

## Files changed / added for Dev_v2.11.0

Source additions:
- `panel_transform.py`
- `panel_print3d.py`
- `print3d_tools.py`
- `instant_clean_core.py`
- `mesh_repair_props.py`
- `mesh_repair_backend.py`

Source integration updates:
- `__init__.py`
- `state.py`
- `panels.py`
- `registration.py`
- `CHANGELOG.md`

Documentation:
- project state, roadmap, UI map, latest/full notes;
- `docs/features/print3d_transform/` spec/state/roadmap/test plan.

## Test status

- Current Dev_v2.10.1 baseline confirmed: performed
- Branch ancestry/source port review: performed
- GitHub Actions static/package validation: passed
- Downloaded ZIP independent static/package check: passed
- Blender 4.5 runtime: not performed
- Additional Blender versions: not tested
- Public release branches changed: no
