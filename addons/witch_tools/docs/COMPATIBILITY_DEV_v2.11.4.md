# Witch Tools Dev_v2.11.4 Compatibility

- Add-on: Witch Tools
- Version: Dev_v2.11.4
- Primary runtime/development target: Blender 5.0.1
- Secondary compatibility target: Blender 4.5.0
- Add-on minimum: Blender 4.5.0
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: Dev_v2.10.1 / `feature/witch-tools-magic-branch`

## Runtime evidence

Observed by the user in Blender 5.0.1 on Dev_v2.11.3:
- 3D Print Tools panel renders.
- STL export hotfix successfully produces an STL file.
- Analyze Mesh still differs from the installed Blender 3D Print Toolbox on the same `_CAP 3` mesh: Toolbox reports Non-flat 98 and Overhang 79, while Witch Tools reports Non-flat 73 and Overhang 80.

## Dev_v2.11.4 change

Analyze no longer reimplements or approximates any 3D Print Toolbox detector. `Check All` delegates directly to the installed 3D Print Toolbox `mesh.print3d_check_all` operator and mirrors the extension's own live report data into Witch Tools. In Edit Mode, non-empty result entries invoke the installed Toolbox `mesh.print3d_select_report` operator using the Toolbox report index, preserving its click-to-select behavior.

This guarantees that, when the installed 3D Print Toolbox backend is available, Witch Tools uses the same detector execution and selection report as the original tab rather than a parallel implementation.

## Dependency / limitation

Dev_v2.11.4 Analyze Mesh requires the Blender 3D Print Toolbox extension to be installed and enabled. If that backend is unavailable, Witch Tools reports an error instead of silently falling back to a different analyzer. This dependency is deliberate for parity. The simplified Witch Tools Export STL, Clean & Repair, Transform, and other existing Witch Tools features do not depend on 3D Print Toolbox.

## Testing status

- Dev_v2.11.4 static/package validation: pending packaging workflow.
- Blender 5.0.1 Analyze exact-count parity: pending user retest.
- Blender 5.0.1 Toolbox click-to-select parity: pending user retest in Edit Mode.
- Blender 5.0.1 STL export: prior Dev_v2.11.3 user test passed.
- Blender 4.5 secondary compatibility: not tested for Dev_v2.11.4.
