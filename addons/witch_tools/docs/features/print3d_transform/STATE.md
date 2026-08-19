# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.3`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Primary runtime target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`
- `bl_info` minimum remains Blender `4.5.0`

## Analyze Mesh state

Blender 5.0.1 comparison on the same `_CAP 3` object established that Dev_v2.11.1 did not match Blender's original 3D Print Toolbox on four checks:
- Non-flat: Toolbox 98 / Witch Tools 73
- Thin: Toolbox 0 / Witch Tools 1
- Sharp: Toolbox 0 / Witch Tools 1
- Overhang: Toolbox 79 / Witch Tools 80

The other six displayed counts matched on that fixture.

Dev_v2.11.2 replaced the simplified analyzer approximations with Toolbox-equivalent check semantics and default thresholds. Runtime retest of the corrected analyzer is still pending and remains part of Dev_v2.11.3 validation.

## Dev_v2.11.3 STL Export correction

User runtime report in Blender 5.0.1: after choosing a folder, pressing Witch Tools `Export STL` did not produce the expected file/result.

The previous source invoked Blender's STL exporter but did not inspect the returned operator status and did not verify that a file actually existed before reporting success. This explains how a cancelled/failed exporter path could present as a no-op, but the precise Blender-side reason for the failed runtime call is not yet known.

Dev_v2.11.3 source changes:
- validate the folder and selected mesh objects;
- prefer Blender's current `wm.stl_export` path;
- require a `FINISHED` return and an actual STL output file before accepting success;
- try the legacy `export_mesh.stl` path when available;
- if Blender exporters fail/cancel, write a binary STL directly from the selected evaluated meshes;
- the fallback applies evaluated modifiers, object world transforms, triangulates polygons, and corrects winding for negative transforms;
- write the fallback through a temporary file and replace the target only after successful completion;
- report explicit failure details if no path succeeds.

The UI remains folder + `Export STL`; STL is still the fixed format.

## Advanced Clean state retained

- Repair / Manifold / Topology / Normals / Dissolve remain individual collapsible sections.
- Each header has an enable toggle and individual play button.
- Main Clean runs enabled sections; each section play button runs only that section.
- Shift selection-only behavior applies to both paths.
- Requested compact layout changes remain intact.

## Runtime validation status

Performed in Blender 5.0.1 on prior candidates:
- 3D Print Tools panel rendered;
- Analyze Mesh executed and exposed the known parity issue;
- Export STL was attempted and user reported no output.

Not yet performed on Dev_v2.11.3:
- STL export/re-import after the new native-result validation and fallback writer;
- exact `_CAP 3` Analyze parity retest;
- offending-element Analyze identity comparison;
- Advanced Clean section execution/Shift behavior;
- Transform runtime behavior;
- Make Manifold / Auto Fix topology safety;
- Blender 4.5 compatibility regression.

## Known limitations

- The new direct binary STL fallback has not yet been executed in Blender.
- Analyze click-to-select remains gated on detector/count and offending-element parity.
- Intersect Volumes remains topology-rebuilding and requires destructive-operation validation.
- Edit-mode Transform Location remains object-local.

## Next exact step

Package and install Dev_v2.11.3 in Blender 5.0.1. Test Export STL first with one selected mesh, then multiple selected meshes, then a mesh with an unapplied modifier. Re-import the resulting STL and compare dimensions/orientation. If export fails, use the new explicit error report to identify the runtime path.

Then rerun Analyze on `_CAP 3`; expected Toolbox reference values remain `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`.
