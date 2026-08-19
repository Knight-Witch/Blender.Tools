# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-18

## Dev_v2.11.3 — STL export reliability hotfix

- Blender 5.0.1 runtime testing exposed a second 3D Print Tools issue: after selecting a folder, `Export STL` produced no expected file/result.
- Source inspection found that the integrated exporter invoked Blender's STL operator but did not check whether the operator returned `FINISHED` or whether a file had actually been created. The precise Blender-side reason for the runtime cancellation/failure is still unknown.
- Export now validates the folder and selected meshes, tries Blender's current STL exporter, verifies completion/output, then tries the legacy exporter where available.
- Added a self-contained binary STL fallback using selected evaluated meshes, applied modifiers, world transforms, triangulation, and negative-transform winding correction.
- Fallback output is written transactionally through a temporary file and replaces the destination only after a successful complete write.
- Export now reports explicit failure details instead of silently appearing successful.
- UI remains unchanged: folder selector + Export STL, fixed STL format.
- Dev_v2.11.2 Analyze parity correction remains included and still requires the `_CAP 3` runtime parity retest.
- Primary target remains Blender 5.0.1; Blender 4.5 remains the secondary compatibility target.
- Candidate: `Dev_v2.11.3`; Blender runtime retest pending.
