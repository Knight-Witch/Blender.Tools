# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.2`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Primary runtime target: Blender `5.0.1`
- Secondary compatibility target: Blender `4.5.0`
- `bl_info` minimum remains Blender `4.5.0`

## Blender 5.0.1 runtime result that triggered Dev_v2.11.2

The user ran Dev_v2.11.1 Analyze Mesh and Blender's original 3D Print Toolbox Check All on the same object in Blender 5.0.1.

Matching results:
- Non-manifold Edges: 0 / 0
- Bad Contiguous Edges: 0 / 0
- Intersect Faces: 0 / 0
- Shells: 1 / 1
- Zero Faces: 0 / 0
- Zero Edges: 0 / 0

Mismatched results:
- Non-flat Faces: Toolbox 98; Witch Tools 73
- Thin Faces: Toolbox 0; Witch Tools 1
- Sharp Edges: Toolbox 0; Witch Tools 1
- Overhang Faces: Toolbox 79; Witch Tools 80

This establishes a real parity failure in Dev_v2.11.1; the Witch Tools values were not accepted as equivalent.

## Dev_v2.11.2 source correction

`print3d_tools.py` now replaces the simplified analyzer approximations with Toolbox-equivalent check semantics:
- untransformed mesh for solid/degenerate/shell analysis;
- Toolbox BVH self-intersection epsilon/overlap semantics;
- 0.1 mm degenerate threshold for both Zero Faces and Zero Edges;
- world-transformed loop-normal test for Non-flat Faces at 5 degrees;
- world-transformed triangulated six-sample backwards-ray Thickness test at 1 mm, mapping hits back to original faces;
- world-transformed signed manifold-edge angle test for Sharp at 160 degrees;
- world-transformed downward-normal Overhang test at 45 degrees.

The UI remains intentionally simplified: the Toolbox threshold grid is still hidden because the user explicitly does not need those controls.

## Advanced Clean state retained from Dev_v2.11.1

- Repair / Manifold / Topology / Normals / Dissolve are individual collapsible sections.
- Each header has an enable toggle and individual play button.
- Main Clean runs enabled sections; a section play button runs only that section.
- Shift selection-only behavior applies to both paths.
- Requested layout customizations remain intact.

## Runtime validation status

Performed in Blender 5.0.1 on Dev_v2.11.1:
- Witch Tools 3D Print Tools panel rendered.
- Analyze Mesh Check All executed and populated results.
- Direct count comparison against the original Toolbox exposed the parity mismatch above.

Not yet performed on Dev_v2.11.2:
- rerun the exact same mesh and verify all ten counts match;
- exact offending-element identity comparison after count parity;
- Advanced Clean section execution/Shift behavior;
- Transform runtime behavior;
- Make Manifold / Auto Fix topology safety;
- STL export/reimport;
- Blender 4.5 compatibility regression.

## Known limitations

- Analyze click-to-select is still not implemented. It remains the next required follow-up after detector/count and offending-element parity are confirmed.
- Thickness parity uses the original Toolbox-style temporary mesh/ray-cast method and therefore needs runtime verification in both Blender 5.0.1 and 4.5 before compatibility is claimed.
- Intersect Volumes remains topology-rebuilding and requires destructive-operation validation.
- Edit-mode Transform Location remains object-local.

## Next exact step

Install Dev_v2.11.2 in Blender 5.0.1 and run Check All on the same `_CAP 3` mesh used for the parity failure. Expected Toolbox reference values from the user's screenshot are:
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

If every count matches, compare the actual selected offending geometry for Non-flat and Overhang before implementing click-to-select inside Witch Tools. If any count still differs, fix that detector before moving on.
