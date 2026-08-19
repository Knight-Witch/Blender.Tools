# Witch Tools Project State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Current candidate: `Dev_v2.11.3`
- Primary runtime/development target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`, primarily for BG3 and workflows that still require it
- Add-on minimum (`bl_info['blender']`): Blender `4.5.0`
- Package folder: `Witch_Tools_Dev`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Current artifact

- Full installable ZIP: `Witch_Tools_Dev_v2_11_3_3D_Print_Transform_Blender_5_0_1.zip`
- Inner ZIP SHA-256: `67b884b75bf594273930b016a5d62601e16318b745b568eb13bc9ea6be8b7cf0`
- GitHub Actions validation/package run: `32215145944`
- Artifact ID: `9352062048`
- Workflow result: success
- Python files parsed: 67
- UI/operator IDs scanned: 145
- Version/panel-order contracts: passed
- Advanced Clean source contracts: passed
- Analyze parity source contracts: passed
- STL export reliability source contracts: passed
- Package hygiene and ZIP integrity: passed
- Independent local extraction/SHA/ZIP-integrity verification: passed
- Blender runtime validation of Dev_v2.11.3: pending

## Last completed work

### Analyze Mesh

Blender 5.0.1 user testing of Dev_v2.11.1 against the original 3D Print Toolbox on `_CAP 3` established a real detector parity failure:
- Toolbox: `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`
- Witch Tools: `0 / 0 / 0 / 1 / 0 / 0 / 73 / 1 / 1 / 80`

Dev_v2.11.2 replaced the simplified detector approximations with Toolbox-equivalent semantics. Dev_v2.11.3 retains that correction. Runtime parity retest is pending.

### STL Export

The user reported in Blender 5.0.1 that choosing a folder and pressing `Export STL` produced no expected file/result.

The previous source invoked Blender's STL operator without checking the returned status or verifying that a file was written. The exact Blender-side reason the runtime export path failed/cancelled is still unknown.

Dev_v2.11.3 now:
- validates the folder and selected meshes;
- tries Blender's current native STL exporter first;
- requires `FINISHED` plus an actual STL output before accepting success;
- tries the legacy STL operator where available;
- falls back to a self-contained binary STL writer if Blender exporter paths fail/cancel;
- uses selected evaluated mesh geometry, modifiers, world transforms, triangulation, and negative-transform winding correction;
- writes fallback output through a temporary file and replaces the target only after a complete write;
- reports explicit failure details if every export path fails.

The Export UI remains folder + `Export STL`, fixed STL format.

### Advanced Clean

Dev_v2.11.1 Instant Clean-style layout/execution correction remains retained: separate Repair / Manifold / Topology / Normals / Dissolve child sections, section enable toggle + play action, main Clean runs enabled sections, and Shift selection-only behavior is intended for global and section actions.

## Current known-working/runtime-observed state

Observed in Blender 5.0.1 on prior Dev_v2.11.x candidates:
- 3D Print Tools panel rendered;
- Analyze Mesh executed;
- direct Analyze comparison exposed the known parity issue;
- the prior Export STL runtime attempt failed to produce expected output.

Dev_v2.11.3 itself has not been run in Blender. Static/package success is not runtime success.

## Active problems / limitations

1. Dev_v2.11.3 Export STL must be tested in Blender 5.0.1 with one mesh, multiple meshes, a modifier-evaluated mesh, transformed/negative-scale geometry, overwrite/failure behavior, and STL re-import.
2. The direct binary STL fallback is runtime-untested.
3. Analyze must be rerun on `_CAP 3`; expected Toolbox counts remain `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`.
4. After Analyze count parity, offending-element identity must be compared before click-to-select implementation.
5. Advanced Clean execution/Shift behavior remains runtime-untested.
6. Make Manifold / Auto Fix / Advanced Clean topology-changing paths still require Undo/Redo, mode, normals/winding, materials/custom-data, manifold, malformed-selection, and safe-failure tests.
7. Transform Edit Mode coordinate editing remains runtime-untested.
8. Dev_v2.10.1 Magic Branch/Inject/Object Snap fixes require regression retest after integration.
9. Blender 4.5 secondary compatibility is not established for Dev_v2.11.3.

## Next exact implementation step

Install the full Dev_v2.11.3 ZIP in Blender 5.0.1.

First test Export STL on one ordinary selected mesh into a known writable folder. Confirm the `.stl` physically appears, then re-import it and check dimensions/orientation. Next test multiple selected meshes and one mesh with an unapplied modifier. If any export path fails, record the new explicit error text.

After export is confirmed, rerun Analyze on `_CAP 3` and compare all ten counts before beginning click-to-select work.

## Files changed for Dev_v2.11.3

Source:
- `dev/Witch_Tools_Dev/print3d_tools.py`
- `dev/Witch_Tools_Dev/__init__.py`
- `dev/Witch_Tools_Dev/state.py`
- `dev/Witch_Tools_Dev/CHANGELOG.md`
- `dev/Witch_Tools_Dev/Blender_Version_Compatability.md`

Build/compatibility:
- `.github/workflows/package-witch-tools-v2-11.yml`
- `docs/COMPATIBILITY_DEV_v2.11.3.md`

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

- Prior Blender 5.0.1 3D Print Tools panel rendering: user-observed
- Prior Blender 5.0.1 Analyze execution/comparison: user-observed; parity failure recorded
- Prior Blender 5.0.1 Export STL attempt: user-observed failure/no output
- Dev_v2.11.3 source implementation: complete
- GitHub Actions static/package validation: passed
- ZIP integrity/SHA/package contents verification: passed
- Dev_v2.11.3 Blender 5.0.1 runtime: not performed
- Dev_v2.11.3 Blender 4.5 runtime: not performed
