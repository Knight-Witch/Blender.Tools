# Witch Tools Notes Changelog — Latest Update

## 2026-08-08 — Dev_v2.10.0 Magnetic Mesh Editing

- Expanded Inject New with independent X/Y/Z movement toggles, vertex/edge/face Magnetic Snap highlighting, Branch Auto-Merge, multi-edge Slide, and MMB orbit around the live injection.
- Added shared `precision_edit_drag.py` and `precision_edit_topology.py` backends so Inject New and Magic Branch use one canonical drag/snap/topology implementation.
- Added Magic Branch with Single/Persistent modes, Vertex/Edge/Face branch types, Paver/Organic face workflows, magnetic placement, Auto-Merge, and a hotkeyable Persistent toggle.
- Reorganized repair tools under Edge Doctor: Missing Vertex / Edge Injector, Alignment Fixer, Curvature Sync. Added two-edge L repair while retaining the original A/B/C solver.
- Added preference-backed Edit Tools ordering with compact drag-grip rows, up/down fallback, and Reset Default. Planar Edit remains independently reorderable.
- Bumped metadata to `Dev_v2.10.0`, target Blender `4.5.0`, and replaced the branch-specific v2.9 packaging workflow with a v2.10 workflow.
- Added/updated specifications, decisions, state, UI map, roadmap, acceptance criteria and Blender 4.5 topology test plans.
- Static Python compilation passed for authored Dev_v2.10 modules. Blender 4.5 registration, GPU hover drawing, modal behavior, MMB pivot, Auto-Merge, Persistent Undo, reorder drag, real topology, Undo/Redo and save/reopen remain untested in this environment.
