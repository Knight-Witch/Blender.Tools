# Witch Tools Project State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Current candidate: `Dev_v2.11.2`
- Primary runtime/development target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`, primarily for BG3 and workflows that still require it
- Add-on minimum (`bl_info['blender']`): Blender `4.5.0`
- Package folder: `Witch_Tools_Dev`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Current development finding

The user tested Dev_v2.11.1 Analyze Mesh in Blender 5.0.1 against Blender's original 3D Print Toolbox on the same `_CAP 3` mesh.

Original Toolbox:
- Non-manifold 0
- Bad Contiguous 0
- Intersect Faces 0
- Shells 1
- Zero Faces 0
- Zero Edges 0
- Non-flat 98
- Thin 0
- Sharp 0
- Overhang 79

Dev_v2.11.1 Witch Tools:
- Non-manifold 0
- Bad Contiguous 0
- Intersect Faces 0
- Shells 1
- Zero Faces 0
- Zero Edges 0
- Non-flat 73
- Thin 1
- Sharp 1
- Overhang 80

The six matching counts validate those specific observed outputs only. The four mismatches prove the initial Analyze implementation was not equivalent to the Toolbox.

## Dev_v2.11.2 source correction

`print3d_tools.py` now follows the original 3D Print Toolbox check semantics instead of simplified approximations:
- Toolbox 0.1 mm degenerate threshold for Zero Faces / Zero Edges;
- Toolbox-style BVH self-intersection overlap handling;
- world-transformed loop-normal Non-flat check at 5 degrees;
- world-transformed triangulated six-sample backwards-ray Thin check at 1 mm;
- world-transformed signed manifold-edge Sharp check at 160 degrees;
- world-transformed downward-normal Overhang check at 45 degrees.

The threshold/settings UI remains hidden as requested. Analyze click-to-select remains deferred until both count parity and offending-element identity are verified.

## Blender target change

The user clarified that Blender 5.0.1 is their normal/general-use Blender environment. Blender 4.5 is used mainly for BG3 modding or other workflows where older Collada/tooling constraints require it.

Therefore:
- Blender 5.0.1 is now the primary Witch Tools target.
- Blender 4.5 remains a secondary compatibility target.
- One installable package should remain usable in 4.5 where technically possible, so the add-on minimum stays 4.5.0 until a real incompatibility requires a split.
- Compatibility claims must still be based on actual runtime testing per feature/path.

## Advanced Clean state retained

Dev_v2.11.1 restored the intended Instant Clean-style interaction model:
- Repair / Manifold / Topology / Normals / Dissolve are separate collapsible child sections.
- Each header has an enable toggle and individual play button.
- Main Clean runs the enabled sections.
- A section play button runs only that section, even if its enable toggle is off.
- Shift selection-only behavior applies to both paths.
- Explicit user-requested compact layout changes remain; Object Data and Make Planar remain removed; Dissolve remains last.

## Current known-working/runtime-observed state

Observed in Blender 5.0.1 on Dev_v2.11.1:
- Witch Tools 3D Print Tools panel rendered.
- Analyze Mesh Check All executed and populated the Results box.
- Direct parity comparison was performed and exposed the mismatch above.

Not established yet:
- Dev_v2.11.2 analyzer parity;
- Advanced Clean section execution/Shift behavior;
- Transform coordinate editing;
- Make Manifold / Auto Fix / Advanced Clean topology safety;
- STL export/reimport;
- Dev_v2.10.1 Magic Branch/Inject/Object Snap regression in this integrated candidate;
- Blender 4.5 secondary compatibility for Dev_v2.11.2.

## Active problems / limitations

1. Dev_v2.11.2 Analyzer must be rerun on the same `_CAP 3` mesh. Expected reference counts are `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`.
2. After count parity, offending-element identity must be compared using the original Toolbox selection buttons before Witch Tools click-to-select is implemented.
3. Analyze click-to-select is required but still deferred until detector identity is confirmed.
4. Thickness parity uses the original Toolbox temporary-mesh/ray-cast method; Blender 5.0.1 runtime verification is required and 4.5 compatibility must be tested separately.
5. Advanced Clean section headers/actions still need runtime behavior tests.
6. Topology-changing repair/clean operations require Undo/Redo, mode, normals/winding, material/edge/custom-data, manifold, malformed-selection, and failure-safety testing.
7. Transform Edit Mode coordinate editing remains runtime-untested.
8. Auto Fix/Make Manifold/STL export remain runtime-untested.
9. Dev_v2.10.1 Magic Branch/Inject/Object Snap fixes still require regression retest after integration.

## Next exact implementation step

Package Dev_v2.11.2 as a full installable ZIP and test it in Blender 5.0.1 on the same `_CAP 3` parity fixture. Do not move to Analyze click-to-select until all ten counts match and the actual selected error geometry is compared.

After primary 5.0.1 validation, run the explicitly required secondary Blender 4.5 compatibility smoke tests for shared/BG3 workflows.

## Files changed for Dev_v2.11.2

Source:
- `print3d_tools.py`
- `__init__.py`
- `state.py`
- `CHANGELOG.md`

Build/compatibility:
- `.github/workflows/package-witch-tools-v2-11.yml`
- compatibility documentation

Documentation:
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/NOTES_CHANGELOG.md`
- `docs/NOTES_CHANGELOG_FULL.md`
- `docs/features/print3d_transform/SPEC.md`
- `STATE.md`
- `ROADMAP.md`
- `TEST_PLAN.md`
- `DECISIONS.md`

## Test status

- Dev_v2.11.1 Blender 5.0.1 3D Print Tools panel rendering: user-observed
- Dev_v2.11.1 Blender 5.0.1 Analyze execution: user-observed
- Dev_v2.11.1 direct Toolbox count comparison: performed; parity failed on 4 of 10 fields
- Dev_v2.11.2 source correction: implemented
- Dev_v2.11.2 static/package validation: pending packaging run
- Dev_v2.11.2 Blender 5.0.1 runtime: not yet performed
- Dev_v2.11.2 Blender 4.5 runtime: not performed
- Public release branches changed: no
