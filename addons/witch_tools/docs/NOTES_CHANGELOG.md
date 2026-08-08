# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-08

## Dev_v2.10.0 — Magnetic mesh editing / Magic Branch documentation update

- Promoted the current development candidate to `Dev_v2.10.0` on `feature/witch-tools-magic-branch`, target Blender `4.5.0`.
- Added `/docs/features/magic_branch/` with specification, decisions, state, roadmap, acceptance criteria and a topology-aware Blender 4.5 test plan.
- Updated Precision Edit docs for Inject New independent XYZ movement, Magnetic Snap, Auto-Merge, multi-edge Slide and MMB orbit behavior.
- Documented shared magnetic semantics: cursor priority vertex > edge > face; vertex/edge rigid endpoint placement; face per-endpoint travel-line placement.
- Documented conservative Auto-Merge and the explicit non-goal of inventing arbitrary face-interior retopology.
- Documented Paver as equal-size repeated tiles and Organic as the arbitrary one-face reach mode.
- Reorganized the UI map around Edge Doctor and persistent user-reorderable Edit Tools sections; Planar Edit remains a separate default section directly after Coordinate Copy.
- Recorded two-edge L repair for Missing Vertex / Edge Injector while retaining the existing A/B/C solver.
- Recorded current limitations: active-object-only topology, preselected-set multi-edge Slide, deferred A/B/C viewport labels, unverified Persistent Undo, MMB pivot feel and N-panel drag-grip behavior.
- Replaced stale v2.9 branch packaging configuration with Dev_v2.10.0 packaging configuration.
- Static Python compilation passed for authored candidate modules. Blender runtime validation remains pending.
