# Witch Tools Project State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Current candidate: `Dev_v2.11.4`
- Primary runtime/development target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`, primarily for BG3 and workflows that still require it
- Add-on minimum (`bl_info['blender']`): Blender `4.5.0`
- Package folder: `Witch_Tools_Dev`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Current artifact

- Full installable ZIP: `Witch_Tools_Dev_v2_11_4_3D_Print_Transform_Blender_5_0_1.zip`
- SHA-256: `787f3f529c1b7960380e06bc007f0e584cfb84b1335dffd47a3c41f1a0775f52`
- Package reconstructed from the previously verified full Dev_v2.11.3 package plus the exact current Dev_v2.11.4 source files from this branch.
- Independent post-package extraction verified the changed files against their current Git blob hashes.
- Python files parsed: 67
- UI/operator IDs scanned: 145
- Duplicate IDs: none
- Dev_v2.11.4 version/minimum-Blender metadata: verified
- Advanced Clean routing contracts: verified
- Exact Toolbox bridge contracts: verified
- Parallel/local Analyze detector tokens: absent
- Dev_v2.11.3 STL export reliability contracts: retained/verified
- Cache/package hygiene: passed
- ZIP integrity: passed
- Blender runtime validation of Dev_v2.11.4: pending

## Latest Blender 5.0.1 runtime findings

### STL Export

The user confirmed the Dev_v2.11.3 STL export hotfix now produces the expected STL file. The exporter reliability correction is retained unchanged in Dev_v2.11.4.

Still pending for Export:
- re-import dimension/orientation verification;
- multi-object export;
- unapplied modifier evaluation;
- negative-scale/winding fixture;
- explicit fallback-path runtime test where safe;
- Blender 4.5 secondary smoke test.

### Analyze Mesh

The user retested Dev_v2.11.3 against the original 3D Print Toolbox on the same unchanged `_CAP 3` object.

Original Toolbox:
`0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`

Dev_v2.11.3 Witch Tools:
`0 / 0 / 0 / 1 / 0 / 0 / 73 / 0 / 0 / 80`

The remaining mismatches — Non-flat 73 vs 98 and Overhang 80 vs 79 — prove that the locally reconstructed Analyzer still was not the same implementation as the installed current Toolbox. This supersedes the Dev_v2.11.2 assumption that reproducing historical Toolbox semantics locally was sufficient.

## Dev_v2.11.4 implementation

Analyze no longer has a parallel Witch Tools detector.

`print3d_tools.py` now:
- invokes `bpy.ops.mesh.print3d_check_all`, i.e. the operator registered by the installed 3D Print Toolbox;
- resolves the installed Toolbox report module and reads its live report entries;
- maps those report entries into the compact Witch Tools result fields;
- refuses to invent/fallback to alternate diagnostics if the Toolbox backend/report cannot be resolved.

`panel_print3d.py` now:
- in Edit Mode, renders non-empty selectable result counts as buttons;
- invokes the original `mesh.print3d_select_report` operator;
- passes the original live Toolbox report index;
- therefore delegates selection mode and element-index selection to the same Toolbox pipeline as the original panel.

### Analyze dependency

Dev_v2.11.4 Analyze requires 3D Print Toolbox to be installed and enabled. This dependency is deliberate to guarantee version-exact parity with the extension actually running in Blender. Transform, STL Export, Make Manifold, Auto Fix, Advanced Clean, and other Witch Tools functionality remain independent.

If a future self-contained build must eliminate this dependency, obtain and vendor the exact current Toolbox source package first. Do not recreate the detector algorithms by hand again.

## Advanced Clean state retained

Dev_v2.11.1 restored the intended Instant Clean-style interaction model:
- Repair / Manifold / Topology / Normals / Dissolve are separate collapsible child sections.
- Each header has an enable toggle and individual play button.
- Main Clean runs enabled sections; a section play button runs only that section.
- Shift selection-only behavior is intended for both paths.
- Explicit user-requested compact layout changes remain; Object Data and Make Planar remain removed; Dissolve remains last.

## Current known-working/runtime-observed state

Observed in Blender 5.0.1:
- 3D Print Tools panel renders.
- Analyze executes on prior candidates.
- Dev_v2.11.3 local Analyze parity failed on Non-flat and Overhang.
- Dev_v2.11.3 Export STL now creates the output file.

Dev_v2.11.4 itself has not yet been run in Blender. Static/package success must not be treated as runtime parity.

## Active problems / limitations

1. Dev_v2.11.4 exact Analyze bridge must be runtime-tested with the installed current 3D Print Toolbox in Blender 5.0.1.
2. Original Toolbox and Witch Tools Check All must display identical counts on `_CAP 3` and broader fixtures.
3. Edit Mode result buttons must select the exact same element sets as the original Toolbox buttons.
4. The report-module resolver must be tested against the actual Blender 5.0.1 extension package namespace.
5. Analyze deliberately requires 3D Print Toolbox enabled; missing backend/report must fail explicitly.
6. Advanced Clean execution/Shift behavior remains runtime-untested.
7. Make Manifold / Auto Fix / Advanced Clean topology-changing paths require Undo/Redo, mode, normals/winding, materials/custom-data, manifold, malformed-selection, and safe-failure tests.
8. Transform Edit Mode coordinate editing remains runtime-untested.
9. Dev_v2.10.1 Magic Branch/Inject/Object Snap fixes require regression retest after integration.
10. Blender 4.5 secondary compatibility is not established for Dev_v2.11.4.

## Next exact implementation step

Install the full Dev_v2.11.4 package in Blender 5.0.1 while 3D Print Toolbox is enabled.

On unchanged `_CAP 3`:
1. run original Toolbox Check All;
2. run Witch Tools Check All;
3. confirm all ten displayed values are identical;
4. enter Edit Mode and compare the original Toolbox and Witch Tools Non-flat result buttons for exact face selection;
5. repeat for Overhang and another non-zero selectable diagnostic.

If counts differ, debug only the Toolbox report-resolution/mapping bridge. Do not reintroduce a local Analyze implementation.

## Files changed for Dev_v2.11.4

Source:
- `dev/Witch_Tools_Dev/print3d_tools.py`
- `dev/Witch_Tools_Dev/panel_print3d.py`
- `dev/Witch_Tools_Dev/__init__.py`
- `dev/Witch_Tools_Dev/state.py`
- `dev/Witch_Tools_Dev/CHANGELOG.md`
- `dev/Witch_Tools_Dev/Blender_Version_Compatability.md`
- `dev/Witch_Tools_Dev/NOTES_CHANGELOG.md`

Build/compatibility:
- `.github/workflows/package-witch-tools-v2-11.yml`
- `docs/COMPATIBILITY_DEV_v2.11.4.md`

Documentation:
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/UI_MAP.md`
- `docs/NOTES_CHANGELOG.md`
- `docs/NOTES_CHANGELOG_FULL.md`
- `docs/features/print3d_transform/SPEC.md`
- `docs/features/print3d_transform/STATE.md`
- `docs/features/print3d_transform/ROADMAP.md`
- `docs/features/print3d_transform/DECISIONS.md`
- `docs/features/print3d_transform/TEST_PLAN.md`

## Test status

- Dev_v2.11.3 Blender 5.0.1 STL file creation: user-confirmed passed.
- Dev_v2.11.3 Blender 5.0.1 Analyze parity: user-confirmed failed on Non-flat/Overhang.
- Dev_v2.11.4 exact Toolbox bridge source implementation: complete.
- Dev_v2.11.4 local/static package validation: passed.
- Dev_v2.11.4 final ZIP integrity and independent source-hash verification: passed.
- Dev_v2.11.4 Blender 5.0.1 runtime: not yet performed.
- Dev_v2.11.4 Blender 4.5 runtime: not performed.
