# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-18

## Dev_v2.11.0 — 3D Print Tools + Transform integration

- Corrected the development baseline: the new feature is now integrated onto Dev_v2.10.1 / `feature/witch-tools-magic-branch` rather than the older Dev_v2.9.0 precision-edit branch.
- Added top-level Transform below Mode Switcher with object Location/Rotation/Scale and selected-mesh local Location editing.
- Added top-level 3D Print Tools above Edit Tools with simplified STL Export, consolidated Analyze Mesh, Make Manifold, Auto Fix, and Advanced Clean.
- Preserved current Magic Branch, Inject New, Edge Doctor, Object Snap, and Edit Tools-order source while wiring the new modules.
- Added the `print3d_transform` spec/state/roadmap/test plan and updated project state, roadmap, and UI map.
- Recorded Analyze click-to-select parity as a required follow-up after detector counts are validated against Blender's original 3D Print Toolbox.
- Candidate: `Dev_v2.11.0`; target Blender `4.5.0`; Blender runtime validation pending.
