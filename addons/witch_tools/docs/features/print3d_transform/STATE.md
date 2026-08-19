# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.3`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Primary runtime target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`
- `bl_info` minimum: Blender `4.5.0`

## Artifact

- Full installable ZIP: `Witch_Tools_Dev_v2_11_3_3D_Print_Transform_Blender_5_0_1.zip`
- SHA-256: `67b884b75bf594273930b016a5d62601e16318b745b568eb13bc9ea6be8b7cf0`
- GitHub Actions run: `32215145944` — passed
- Static source/package validation: passed
- ZIP integrity and independent local SHA verification: passed
- Blender runtime: pending

## Analyze Mesh state

Dev_v2.11.1 Blender 5.0.1 comparison on `_CAP 3` failed parity against the original 3D Print Toolbox on Non-flat/Thin/Sharp/Overhang. Dev_v2.11.2 replaced the approximations with Toolbox-equivalent semantics; Dev_v2.11.3 retains that correction. Corrected runtime parity is still unverified.

Expected `_CAP 3` Toolbox reference: `0 / 0 / 0 / 1 / 0 / 0 / 98 / 0 / 0 / 79`.

## STL Export state

User runtime report: in Blender 5.0.1, choosing an export folder and pressing `Export STL` produced no expected output.

The old integration did not validate the Blender export operator result or output file. Dev_v2.11.3 now validates folder/selection, checks native exporter completion and output, attempts the legacy exporter where available, and has a direct binary STL fallback from selected evaluated meshes.

Fallback design:
- evaluated modifiers;
- world transforms;
- loop-triangle export;
- negative-transform winding correction;
- temporary file + atomic replacement;
- explicit failure if no exportable triangles or all paths fail.

This implementation is source/static validated but not yet run in Blender.

## Advanced Clean state

Dev_v2.11.1 Instant Clean-style section structure and execution design remain retained unchanged.

## Runtime validation status

Performed on prior candidate(s) in Blender 5.0.1:
- 3D Print Tools panel rendering;
- Analyze execution/comparison;
- prior Export STL attempt, which failed/no-output.

Not yet performed on Dev_v2.11.3:
- STL export/re-import;
- corrected Analyze parity;
- Advanced Clean execution/Shift behavior;
- Transform editing;
- Make Manifold / Auto Fix safety;
- Blender 4.5 compatibility.

## Next exact step

Install Dev_v2.11.3 in Blender 5.0.1 and test Export STL first on one ordinary mesh into a known writable folder. Confirm the file appears and re-imports correctly. Then test multi-object and unapplied-modifier cases. If export fails, capture the explicit error text now produced.

Then rerun `_CAP 3` Analyze parity before implementing result click-to-select.
