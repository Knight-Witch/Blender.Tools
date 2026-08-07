# Witch Tools Notes Changelog — Latest Update

## 2026-08-07 — Dev_v2.9.0 Precision Edit

- Added **Coordinate Copy** above Vertex Snap with Global/Local space, X/Y/Z masks, Location/Rotation/Scale controls, exact source capture, independent target application, multi-object world conversion, and default `Ctrl+Shift+C` Apply shortcut.
- Added **Planar Edit** with persistent per-vertex object-local Plane Lock axes and exact world-space Level targets.
- Added **Inject New** below Vertex Snap with Solo/Branch/Slide, global X/Y/Z placement, captured straight Rail endpoints, Vertex/Edge/Face Solo/Branch sources, and vertex-only edge-splitting Slide.
- Preserved the existing A/B/C **Edge / Vertex Inject** repair workflow as a separate tool.
- Added protection-system coordination so Coordinate Copy/Level preflight Vertex Locks and Plane Locks, while Inject New suspends/restores guards around modal topology changes.
- Added step-based compact UI, hover help, `PRECISION_EDIT_QUICK_START.md`, and the repository `precision_edit` feature packet/test plan.
- Bumped development metadata to `Dev_v2.9.0`, target Blender 4.5.
- Static/source checks were performed during implementation. Blender 4.5 registration, UI, real-mesh/modal topology behavior, undo/redo, and save/reopen remain untested in this environment.
