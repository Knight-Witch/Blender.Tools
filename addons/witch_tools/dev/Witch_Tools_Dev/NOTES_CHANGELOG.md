# Witch Tools Notes Changelog — Latest Update

## 2026-08-18 — Dev_v2.11.4 Exact 3D Print Toolbox Analyze Bridge

- User confirmed Dev_v2.11.3 STL export now creates the expected STL in Blender 5.0.1.
- Dev_v2.11.3 Analyze still differed from the installed 3D Print Toolbox on `_CAP 3`: Toolbox Non-flat 98 / Overhang 79 versus Witch Tools 73 / 80.
- Removed the parallel Witch Tools Analyze detector.
- Witch Tools Check All now invokes the installed 3D Print Toolbox `mesh.print3d_check_all` directly and mirrors its live report.
- Edit Mode result buttons invoke the original `mesh.print3d_select_report` with the original report index for exact Toolbox selection behavior.
- Analyze explicitly requires 3D Print Toolbox installed/enabled and does not silently fall back to a different detector.
- Primary target: Blender 5.0.1. Secondary compatibility target: Blender 4.5.0.
- Dev_v2.11.4 runtime exact-count and exact-selection parity retest remains required.
