# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-18

## Dev_v2.10.0 — Transform + 3D Print Tools consolidation

- Added the `print3d_transform` feature packet with specification, acceptance criteria, feature state, roadmap, and Blender 4.5 topology-aware test plan.
- Added **Transform** as a top-level Witch Tools panel immediately below Mode Switcher with collapsible Location / Rotation / Scale controls.
- Documented Edit Mode mesh Location as selected-vertex local-space median plus delta translation; Rotation and Scale remain object transforms because vertices do not own independent rotation/scale properties.
- Added **3D Print Tools** above Edit Tools with simplified STL Export, consolidated Analyze Mesh results, and Clean & Repair.
- Documented deliberate omissions from the original 3D Print Toolbox UI: Volume/Area, per-check filter controls, Hollow, Bisect, Align XY, Scale To, and export options.
- Added Clean & Repair layout and behavior: Make Manifold; Auto Fix with Global Fix before Local Fix; Advanced Clean with Repair / Manifold / Topology / Normals / Dissolve.
- Documented compact responsive toggle layouts for Remove Non-Manifold, Topology Compare, and Normals Clear Data.
- Recorded that Instant Clean Object Data and Make Planar are intentionally excluded.
- Bumped the development candidate to `Dev_v2.10.0`, target Blender `4.5.0`, on `feature/witch-tools-3d-print-transform`.
- Static Python parse/compile was performed for the new/modified modules. Blender 4.5 registration, UI, operator execution, topology safety, undo/redo, save/reopen, and export validation remain pending because no Blender executable is available in the implementation environment.
