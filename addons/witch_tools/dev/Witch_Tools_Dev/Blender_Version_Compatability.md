# Blender Version Compatibility

## Current development candidate — Dev_v2.11.3

- Add-on: Witch Tools
- Primary runtime/development target: Blender 5.0.1
- Secondary compatibility target: Blender 4.5.0
- Add-on minimum declared in `bl_info`: Blender 4.5.0
- Current branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: Dev_v2.10.1 / `feature/witch-tools-magic-branch`
- Public/release branches modified: no

### Runtime evidence

Blender 5.0.1 user testing on prior Dev_v2.11.x candidates established:
- the integrated 3D Print Tools panel renders;
- Analyze Mesh executes, but Dev_v2.11.1 mismatched the original 3D Print Toolbox on Non-flat/Thin/Sharp/Overhang; Dev_v2.11.2 contains a source correction and still requires parity retest;
- Export STL was attempted after selecting a folder and produced no expected file/result; Dev_v2.11.3 contains the export reliability correction and still requires runtime retest.

Dev_v2.11.3 has not yet been runtime-confirmed in Blender 5.0.1 or Blender 4.5.0. Source/package validation is not a compatibility claim.

### Dev_v2.11.3 export compatibility work

- validates native Blender STL operator completion and actual file creation;
- attempts legacy STL export where available;
- includes a direct binary STL fallback using selected evaluated mesh geometry if Blender's operator paths fail/cancel;
- fallback is intended to include modifiers, world transforms, triangulation, and negative-transform winding correction;
- explicit Blender 5.0.1 and 4.5.0 export/re-import testing remains required.

## Recent development history

| Release | Primary target | Secondary target | Runtime status / notes |
|---|---|---|---|
| Dev_v2.11.3 | Blender 5.0.1 | Blender 4.5 | STL export hotfix source implemented; runtime export/re-import pending. Analyze parity retest also pending. |
| Dev_v2.11.2 | Blender 5.0.1 | Blender 4.5 | Analyze parity source correction after 5.0.1 mismatch; corrected analyzer not yet runtime-retested. |
| Dev_v2.11.1 | Blender 4.5 authoring baseline | Blender 5.0.1 observed UI environment | Restored Instant Clean-style Advanced Clean structure; 3D Print UI and Analyze were exercised in 5.0.1. |
| Dev_v2.11.0 | Blender 4.5 | none confirmed | Initial Transform + 3D Print integration. |
| Dev_v2.10.1 | Blender 4.5 | none confirmed | Magic Branch/Inject/Object Snap runtime-fix candidate; retest pending. |
| Dev_v2.10.0 | Blender 4.5 | none confirmed | Magnetic Inject New, Magic Branch, Edge Doctor regrouping/L repair, reorderable Edit Tools. |
| Dev_v2.9.0 | Blender 4.5 | none confirmed | Coordinate Copy, Plane Lock/Level, Inject New Solo/Branch/Slide. |
| Dev_v2.8.0 | Blender 4.5 | none confirmed | Guided Align source/static validation; Blender runtime pending. |
| Dev_v2.6.1 | Blender 4.5 | none confirmed | Selection Slots N-panel hotfix; exact runtime validation pending. |
| Dev_v2.5.2 | Blender 4.5 target | Blender Python 5.2.0 LTS test runtime | Curvature Sync column repair; actual collar regression passed in test runtime, exact 4.5 pending. |
| Dev_v2.5.1 | Blender 4.5 target | Blender Python 5.2.0 LTS test runtime | Auto-Aligned Vertex Inject; exact 4.5 pending. |
| Dev_v2.5.0 | Blender 4.5 target | Blender Python 5.2.0 LTS test runtime | Curvature Sync MVP runtime checks in test runtime; exact 4.5 interactive validation pending. |

Older compatibility history remains available in repository history and cumulative project changelogs.
