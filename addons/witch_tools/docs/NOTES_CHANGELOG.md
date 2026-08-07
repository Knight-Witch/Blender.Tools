# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-07

## Dev_v2.9.0 — Precision Edit documentation/state update

- Added the `precision_edit` feature packet with specification, implementation decisions, feature state, roadmap, acceptance criteria, and Blender 4.5 test plan.
- Updated the Witch Tools UI map for the new Edit Tools order: Coordinate Copy, Planar Edit, Vertex Snap, Inject New, then the retained existing tools.
- Recorded exact Coordinate Copy semantics for Global/Local frames, independent targets, XYZ masks, and geometry-frame Location/Rotation/Scale behavior.
- Recorded Plane Lock as persistent object-local per-vertex axis protection and Level as exact per-target world-coordinate assignment.
- Recorded Inject New Solo/Branch/Slide behavior, straight Rail semantics, vertex-only Slide, Branch edge-only connection behavior, and the retained A/B/C auto-aligned inject tool.
- Updated the project roadmap and state for the Dev_v2.9.0 source candidate and deferred Witch Dock/Quickbar integration until Blender 4.5 backend validation passes.
- Recorded the inherited documentation conflict where the Dev_v2.8.0 roadmap references a missing `/docs/features/align_selection/` directory; no historical content was fabricated.
- Target Blender remains `4.5.0`.
- Blender runtime validation remains pending because no Blender executable is available in the implementation environment.
