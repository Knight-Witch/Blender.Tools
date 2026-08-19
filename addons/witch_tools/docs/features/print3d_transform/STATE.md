# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.4`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Primary runtime target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`
- `bl_info` minimum: Blender `4.5.0`

## Runtime findings leading to Dev_v2.11.4

The user retested Dev_v2.11.3 in Blender 5.0.1 on the same `_CAP 3` object.

Original 3D Print Toolbox:
- Non-manifold Edges: 0
- Bad Contiguous Edges: 0
- Intersect Faces: 0
- Shells: 1
- Zero Faces: 0
- Zero Edges: 0
- Non-flat Faces: 98
- Thin Faces: 0
- Sharp Edges: 0
- Overhang Faces: 79

Witch Tools Dev_v2.11.3:
- Non-manifold Edges: 0
- Bad Contiguous Edges: 0
- Intersect Faces: 0
- Shells: 1
- Zero Faces: 0
- Zero Edges: 0
- Non-flat Faces: 73
- Thin Faces: 0
- Sharp Edges: 0
- Overhang Faces: 80

Therefore the local Analyze implementation remained unacceptable even after the Dev_v2.11.2 parity rewrite.

The same user test confirmed the Dev_v2.11.3 STL export hotfix now produces the STL file successfully in Blender 5.0.1.

## Dev_v2.11.4 Analyze architecture

Witch Tools no longer implements its own Analyze detector.

`Check All` now:
1. invokes the installed 3D Print Toolbox `mesh.print3d_check_all` operator;
2. reads the report produced by that same installed extension;
3. maps the live report entries into the compact Witch Tools Results box.

In Edit Mode, non-empty result entries invoke the original Toolbox `mesh.print3d_select_report` operator with the original report index. This restores the original click-to-select pipeline rather than re-creating selection logic.

There is intentionally no alternate Witch Tools detector fallback. If the 3D Print Toolbox backend/report cannot be found, Analyze returns a visible error. Exact parity takes priority over maintaining two implementations.

## Analyze dependency

- Required for Analyze: installed and enabled 3D Print Toolbox extension.
- Not required for: Transform, STL Export, Make Manifold, Auto Fix, Advanced Clean, or other Witch Tools features.

## STL Export state

Dev_v2.11.3 export reliability fix is retained unchanged and is user-confirmed to create an STL in Blender 5.0.1.

The exporter:
- validates folder and selected mesh set;
- verifies Blender exporter completion and physical file creation;
- tries legacy export where available;
- has a direct evaluated-mesh binary STL fallback;
- uses world transforms, triangulation, and negative-transform winding correction;
- writes fallback output transactionally through a temporary file.

Full re-import/dimension/orientation matrix is still pending.

## Advanced Clean state

Dev_v2.11.1 Instant Clean-style section structure and execution design remain retained unchanged.

## Runtime validation status

Performed in Blender 5.0.1:
- 3D Print Tools panel rendering: passed on prior candidates.
- Analyze execution: passed on prior candidates, but local detector parity failed through Dev_v2.11.3.
- STL file creation: user-confirmed passed on Dev_v2.11.3.

Not yet performed on Dev_v2.11.4:
- direct Toolbox-backed Analyze count parity;
- direct Toolbox click-to-select parity in Edit Mode;
- Advanced Clean execution/Shift behavior;
- Transform editing;
- Make Manifold / Auto Fix safety;
- Blender 4.5 compatibility.

## Next exact step

Install the full Dev_v2.11.4 package in Blender 5.0.1 with 3D Print Toolbox enabled.

On the unchanged `_CAP 3` object:
1. run the original 3D Print Toolbox `Check All`;
2. run Witch Tools `Check All`;
3. verify every displayed count is identical;
4. enter Edit Mode and click the original Toolbox Non-flat result, record/observe its selected faces;
5. rerun `Check All` if required, click the Witch Tools Non-flat result, verify the exact same faces are selected;
6. repeat for Overhang and another non-zero/selectable diagnostic where available.

If the counts differ after Dev_v2.11.4, investigate report-module resolution/mapping only; do not reintroduce a parallel detector.
