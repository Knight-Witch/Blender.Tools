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

## Current development findings

### Analyze Mesh

The user tested Dev_v2.11.1 Analyze Mesh in Blender 5.0.1 against Blender's original 3D Print Toolbox on the same `_CAP 3` mesh.

Original Toolbox: `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`.
Dev_v2.11.1 Witch Tools: `0 / 0 / 0 / 1 / 0 / 0 / 73 / 1 / 1 / 80`.

Dev_v2.11.2 replaced the simplified analyzer approximations with Toolbox-equivalent semantics. Runtime parity retest is still pending.

### STL Export

The user then reported in Blender 5.0.1 that, after selecting an export folder, pressing `Export STL` produced no visible result/file.

Inspection showed the integrated exporter called Blender's STL operator and then reported success without checking the returned operator status or verifying that a file had actually been written. The exact runtime reason Blender's operator failed/cancelled is not yet established.

Dev_v2.11.3 changes the export path so it:
- validates the chosen folder and selected mesh set;
- tries Blender's current native STL exporter first;
- checks for `FINISHED` and verifies an STL file was actually created;
- tries the legacy STL operator as a compatibility path where available;
- falls back to a self-contained binary STL writer if Blender's exporters are unavailable or cancel;
- writes selected evaluated meshes with modifiers, world transforms, triangulation, and negative-transform winding correction;
- reports a real error if all export paths fail instead of silently appearing successful.

The simple Export UI remains unchanged: folder selector + `Export STL`, fixed STL format.

## Advanced Clean state retained

Dev_v2.11.1 restored the intended Instant Clean-style interaction model:
- Repair / Manifold / Topology / Normals / Dissolve are separate collapsible child sections.
- Each header has an enable toggle and individual play button.
- Main Clean runs enabled sections; a section play button runs only that section.
- Shift selection-only behavior applies to both paths.
- Explicit user-requested compact layout changes remain; Object Data and Make Planar remain removed; Dissolve remains last.

## Current known-working/runtime-observed state

Observed in Blender 5.0.1 on the prior candidate:
- Witch Tools 3D Print Tools panel rendered.
- Analyze Mesh Check All executed and populated Results.
- Direct Analyze comparison exposed the known parity mismatch.
- Export STL was user-tested and failed to produce the expected file/result.

Not established yet:
- Dev_v2.11.3 STL export/re-import success;
- Dev_v2.11.2/2.11.3 Analyze detector parity;
- Advanced Clean section execution/Shift behavior;
- Transform coordinate editing;
- Make Manifold / Auto Fix / Advanced Clean topology safety;
- Dev_v2.10.1 Magic Branch/Inject/Object Snap regression in this integrated candidate;
- Blender 4.5 secondary compatibility for Dev_v2.11.3.

## Active problems / limitations

1. Dev_v2.11.3 Export STL must be runtime-tested in Blender 5.0.1 with one selected mesh and multiple selected meshes, then re-imported for dimension/orientation verification.
2. The fallback writer is source/static work until Blender runtime testing confirms evaluated mesh extraction and resulting STL behavior.
3. Analyze must be rerun on the same `_CAP 3` fixture; expected Toolbox reference counts remain `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`.
4. After Analyze count parity, offending-element identity must be compared before Witch Tools click-to-select is implemented.
5. Advanced Clean section actions and topology-changing operations still require Undo/Redo, mode, normals/winding, material/edge/custom-data, manifold, malformed-selection, and failure-safety testing.
6. Transform Edit Mode coordinate editing remains runtime-untested.
7. Dev_v2.10.1 Magic Branch/Inject/Object Snap fixes still require regression retest after integration.
8. Blender 4.5 secondary compatibility remains unverified for Dev_v2.11.3.

## Next exact implementation step

Package Dev_v2.11.3 as a full installable ZIP and install it in Blender 5.0.1.

First, select one normal mesh, choose a real folder, press `Export STL`, confirm the `.stl` appears, and re-import it to verify dimensions/orientation. Then test a multi-object selection and one object with an unapplied modifier. If export still fails, capture the new explicit error message.

After export is confirmed, rerun Analyze on `_CAP 3` and compare all ten counts against the original Toolbox before beginning click-to-select work.

## Files changed for Dev_v2.11.3

Source:
- `print3d_tools.py`
- `__init__.py`
- `state.py`
- `CHANGELOG.md`

Documentation/build files are updated with this state, test plan, compatibility record, and packaging metadata.

## Test status

- Prior Blender 5.0.1 3D Print Tools panel rendering: user-observed
- Prior Blender 5.0.1 Analyze execution: user-observed
- Prior direct Toolbox Analyze comparison: performed; parity failed on 4 of 10 fields
- Prior Export STL runtime attempt: user-observed failure/no output
- Dev_v2.11.3 export source correction: implemented
- Dev_v2.11.3 Blender 5.0.1 runtime: not yet performed
- Dev_v2.11.3 Blender 4.5 runtime: not performed
- Public release branches changed: no
