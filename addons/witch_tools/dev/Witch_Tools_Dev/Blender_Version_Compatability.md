# Blender Version Compatibility

## Current development candidate — Dev_v2.11.4

- Add-on: Witch Tools
- Primary runtime/development target: Blender 5.0.1
- Secondary compatibility target: Blender 4.5.0
- Add-on minimum declared in `bl_info`: Blender 4.5.0
- Current branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: Dev_v2.10.1 / `feature/witch-tools-magic-branch`
- Public/release branches modified: no

### Blender 5.0.1 runtime evidence

User testing established:
- 3D Print Tools panel renders.
- Analyze Mesh executes in prior Dev_v2.11.x candidates.
- Dev_v2.11.3 still disagreed with the original installed 3D Print Toolbox on `_CAP 3`: Toolbox Non-flat 98 / Overhang 79 versus Witch Tools Non-flat 73 / Overhang 80.
- Dev_v2.11.3 STL export hotfix now successfully creates an STL file.

### Dev_v2.11.4 Analyze compatibility model

Analyze no longer contains a parallel Witch Tools detector. It directly invokes the 3D Print Toolbox operator registered in the running Blender installation:
- `mesh.print3d_check_all` for analysis;
- the Toolbox live report for displayed counts;
- `mesh.print3d_select_report` for selectable result entries in Edit Mode.

Therefore the Analyze compatibility target is the Toolbox extension actually installed in that Blender environment rather than a separately reconstructed snapshot of its algorithms.

Analyze dependency:
- 3D Print Toolbox must be installed and enabled.
- If the Toolbox operator/report pipeline is unavailable, Analyze fails explicitly.
- Transform, STL Export, Clean & Repair, and other Witch Tools functionality remain independent.

Dev_v2.11.4 exact count and click-selection behavior still require Blender 5.0.1 runtime retest. Blender 4.5 secondary behavior depends on the 3D Print Toolbox version installed there and is not yet tested.

## Recent development history

| Release | Primary target | Secondary target | Runtime status / notes |
|---|---|---|---|
| Dev_v2.11.4 | Blender 5.0.1 | Blender 4.5 | Analyze changed to direct installed-Toolbox backend/report/select pipeline; runtime exact parity pending. Dev_v2.11.3 STL file creation fix retained and previously user-confirmed in 5.0.1. |
| Dev_v2.11.3 | Blender 5.0.1 | Blender 4.5 | STL export hotfix user-confirmed to create file; local Analyze still mismatched Non-flat/Overhang. |
| Dev_v2.11.2 | Blender 5.0.1 | Blender 4.5 | Attempted local Analyze parity rewrite; later runtime evidence showed remaining mismatch. |
| Dev_v2.11.1 | Blender 4.5 authoring baseline | Blender 5.0.1 observed UI environment | Restored Instant Clean-style Advanced Clean structure; 3D Print UI and Analyze exercised in 5.0.1. |
| Dev_v2.11.0 | Blender 4.5 | none confirmed | Initial Transform + 3D Print integration. |
| Dev_v2.10.1 | Blender 4.5 | none confirmed | Magic Branch/Inject/Object Snap runtime-fix candidate; retest pending. |
| Dev_v2.10.0 | Blender 4.5 | none confirmed | Magnetic Inject New, Magic Branch, Edge Doctor regrouping/L repair, reorderable Edit Tools. |
| Dev_v2.9.0 | Blender 4.5 | none confirmed | Coordinate Copy, Plane Lock/Level, Inject New Solo/Branch/Slide. |
| Dev_v2.8.0 | Blender 4.5 | none confirmed | Guided Align source/static validation; Blender runtime pending. |
| Dev_v2.6.1 | Blender 4.5 | none confirmed | Selection Slots N-panel hotfix; exact runtime validation pending. |
| Dev_v2.5.2 | Blender 4.5 target | Blender Python 5.2.0 LTS test runtime | Curvature Sync column repair; actual collar regression passed in test runtime, exact 4.5 pending. |

Older compatibility history remains available in repository history and cumulative project changelogs.
