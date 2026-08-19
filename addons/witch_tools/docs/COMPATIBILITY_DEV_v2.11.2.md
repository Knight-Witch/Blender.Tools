# Witch Tools Dev_v2.11.2 Compatibility Record

- Add-on: Witch Tools
- Version: Dev_v2.11.2
- Primary development/runtime target: Blender 5.0.1
- Secondary compatibility target: Blender 4.5.0
- Add-on minimum version in `bl_info`: Blender 4.5.0
- Additional Blender versions tested for Dev_v2.11.2 itself: none yet

## Package validation

- Full installable ZIP: `Witch_Tools_Dev_v2_11_2_3D_Print_Transform_Blender_5_0_1.zip`
- SHA-256: `37493258a6a995b6fd1799e60a56d0a55c4f2afda1a772a0dfecaa13ae90daef`
- GitHub Actions validation/package job: passed
- ZIP integrity: passed
- Independent downloaded-inner-ZIP SHA-256 verification: passed
- Python AST parse: 67 Python files passed
- Required Analyze parity source contracts: present
- Cache/package hygiene: passed

Static/package success does not establish Blender runtime compatibility.

## Runtime evidence inherited from Dev_v2.11.1

User runtime environment: Blender 5.0.1.

Observed:
- Witch Tools 3D Print Tools panel rendered.
- Analyze Mesh Check All executed and populated results.
- Direct same-mesh comparison against Blender's original 3D Print Toolbox was performed.

Parity failure observed on `_CAP 3`:
- Original Toolbox: Non-flat 98 / Thin 0 / Sharp 0 / Overhang 79
- Dev_v2.11.1 Witch Tools: Non-flat 73 / Thin 1 / Sharp 1 / Overhang 80
- Other displayed counts on that fixture matched: Non-manifold 0, Bad Contiguous 0, Intersect Faces 0, Shells 1, Zero Faces 0, Zero Edges 0.

## Dev_v2.11.2 status

Source correction implemented to use 3D Print Toolbox-equivalent analyzer semantics and default thresholds.

Runtime validation still required:
- Blender 5.0.1 exact `_CAP 3` parity retest;
- broader detector/offending-element identity tests;
- Transform runtime behavior;
- Advanced Clean per-section execution and Shift-selection behavior;
- Make Manifold / Auto Fix / Advanced Clean topology safety;
- STL export/reimport;
- Dev_v2.10.1 baseline regression.

Blender 4.5 secondary compatibility is not yet tested for Dev_v2.11.2. Test shared/BG3 workflows separately before claiming them compatible.

Known compatibility limitation:
The Toolbox-equivalent Thin Faces path creates a temporary mesh/object and uses object ray casts, matching the original algorithm. This requires explicit runtime verification in both 5.0.1 and 4.5 because API/runtime behavior may differ even when the Python source parses in both versions.
