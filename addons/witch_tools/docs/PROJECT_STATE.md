# Witch Tools Project State

Last updated: 2026-08-08

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh-operator backend
- Development branch: `feature/witch-tools-magic-branch`
- Direct parent: `feature/witch-tools-precision-edit` at `a5fe4bbccc954b25ac645489f2092b3d3d7618c5`
- Earlier Guided Align baseline: `fc94b7c27d0b850699e79b973a0548a2193eb525`
- Intended integration branch: `Blender_Dev`
- Development package: `Witch_Tools_Dev`
- Target Blender: `4.5.0`

## Current candidate

- Version: `Dev_v2.10.0`
- Scope: Dev_v2.9 Precision Edit retained + magnetic Inject New, Magic Branch, Edge Doctor regrouping/L repair, and persistent Edit Tools ordering.
- Runtime status: source/static candidate; Blender 4.5 validation pending.
- Public/release branches modified: no.
- Witch Dock/Quickbar modified: no.

## Current Edit Tools default order

1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Object Snap
5. Inject New
6. Magic Branch
7. Edge Doctor
8. Vertex Lock
9. Selection Slots

Users can reorder these top-level sections through `Reorder Tools`. Saved order lives in add-on preferences. The reorder UI exposes a drag grip plus up/down fallback and Reset Default.

Planar Edit remains top-level immediately after Coordinate Copy because it was an explicit earlier feature and was not requested to be removed; it may be moved by the user.

## Dev_v2.9 functionality retained

### Coordinate Copy

- Global/Local;
- X/Y/Z;
- Location/Rotation/Scale geometry-frame copying;
- vertex/edge/face source capture;
- independent targets rather than one selection median;
- multi-object world/local conversion;
- Vertex Lock / Plane Lock preflight;
- default Ctrl+Shift+C Apply shortcut.

### Planar Edit

- persistent object-local Plane Lock custom layers and guard;
- exact per-target world-space Level operation;
- multi-object Level support;
- protection preflight.

## Inject New — Dev_v2.10 changes

- Solo / Branch / Slide retained.
- Solo/Branch X/Y/Z are independent toggles; any non-empty combination is allowed.
- captured straight Rail remains optional.
- Magnetic Snap highlights hovered vertex, edge, or face.
- vertex/edge snapping aligns the nearest compatible new endpoint while preserving rigid copied shape.
- face snapping moves each endpoint along its own travel line to the hovered face/boundary.
- Branch Auto-Merge welds supported vertex/edge contacts; target edge is split at an interior contact when needed.
- arbitrary face-interior Auto-Merge retopology is intentionally not invented.
- Slide accepts one or more preselected edges, injects one vertex into each, and applies a shared relative factor; cursor-nearest selected rail is the driver.
- Slide does not automatically add completely unselected fan edges merely by hover in this candidate.
- MMB pauses modal placement, assigns current live geometry as the orbit pivot candidate, passes navigation through, and resumes after release.
- shared finish validation rejects zero-length edges and zero-area faces.

## Magic Branch

New source candidate with:

- Single Branch / Persistent;
- dedicated hotkeyable Persistent-toggle operator;
- Vertex / Edge / Face click-drag branching;
- X/Y/Z independent axes, all enabled by default;
- shared Magnetic Snap / Auto-Merge behavior;
- MMB orbit around live branch geometry;
- Face Paver and Organic modes.

Paver repeats equal source-derived tiles and does not stretch the final tile to force an arbitrary off-grid endpoint. Organic creates one adaptable connected face.

Persistent attempts to establish per-branch Undo boundaries, but that modal Undo behavior is explicitly unverified until Blender testing.

## Edge Doctor

New parent UI group containing:

1. Missing Vertex / Edge Injector
2. Alignment Fixer
3. Curvature Sync

Missing Injector preserves the existing A/B/C solver and adds a two-edge L mode. Two selected edges sharing one corner infer D as `A + C - B`, reuse a vertex within the existing tolerance where possible, then create missing A-D / C-D edges.

Alignment Fixer is the existing Guided Align backend with a clearer UI name; canonical `mesh.wt_guided_align_*` operator IDs remain unchanged.

A/B/C viewport letter overlays are deferred QoL and are not part of Dev_v2.10.0 source.

## Shared architecture

- `precision_edit_drag.py`: viewport projection, hover target picking, GPU highlighting, magnetic solve, edge materialization/welding, orbit-pivot helper.
- `precision_edit_topology.py`: duplicate/branch primitives, Organic/Paver creation, zero-geometry validation.
- Inject New and Magic Branch both call these backends; neither owns a duplicate magnetic implementation.

## Last completed work

- Re-read repository rules, architecture, add-on rules/state/specs and current source before changes.
- Confirmed current precision-edit head and created `feature/witch-tools-magic-branch` from exact SHA `a5fe4bbccc954b25ac645489f2092b3d3d7618c5`.
- Bumped source metadata to Dev_v2.10.0 / Blender 4.5.
- Implemented the shared drag/snap and topology layers.
- Reworked Inject New for magnetic placement, Auto-Merge, multi-axis movement, multi-edge Slide, and MMB navigation.
- Added Magic Branch.
- Added Edge Doctor wrapper/L repair while preserving old repair/alignment/curvature backends.
- Added preference-backed Edit Tools ordering.
- Replaced the inherited branch-specific v2.9 packaging workflow with a v2.10 workflow for this branch.
- Added `/docs/features/magic_branch/` specification, decisions, state, roadmap and Blender test plan.
- Updated Precision Edit specification/state, UI map and parent roadmap.

## Current known-working state

Previously user-validated in Blender 4.5 from earlier candidates:

- Dev_v2.5.2 Curvature Sync production collar workflow.
- Quickbar Dev_v1.4.0 Selection Slots workflow.

Dev_v2.10 implementation-environment checks:

- authored/modified local Python candidate modules compiled successfully with Python syntax compilation;
- version and registration wiring reviewed;
- feature docs contain explicit acceptance criteria/test matrices;
- no Blender executable is available here.

Do not infer Blender runtime success from static compilation.

## Active problems / limitations

1. Blender 4.5 registration/unregistration and panel rendering untested.
2. GPU hover drawing and vertex/edge/face selection priority untested in Blender.
3. Magnetic solves need camera-angle and transformed-object validation.
4. target edge split/weld Auto-Merge needs topology/attribute validation.
5. MMB `view_location` pivot behavior must be tested for natural orbit/resume behavior.
6. Persistent Magic Branch per-branch Undo must be proven.
7. N-panel drag-grip reorder must be proven; arrow fallback is available in source.
8. multi-edge Slide cancel/Undo and special edge-data preservation must be proven.
9. active-object-only topology creation.
10. straight Inject Rail only.
11. Branch does not auto-create side faces.
12. arbitrary face-interior Auto-Merge retopology deferred.
13. Paver preserves equal tiles and will not stretch an off-grid final tile.
14. hover-only dynamic addition of unselected Slide fan edges deferred.
15. A/B/C viewport letters deferred.
16. inherited missing `/docs/features/align_selection/` historical packet remains unresolved.
17. no additional Blender version has been tested.
18. Witch Dock/Quickbar exposure deferred.

## Next exact implementation step

1. Obtain the Dev_v2.10.0 static package from the branch packaging workflow if it passes.
2. Install in Blender 4.5.
3. Execute `/docs/features/precision_edit/TEST_PLAN.md` and `/docs/features/magic_branch/TEST_PLAN.md`.
4. Prioritize: registration/UI/GPU -> Inject magnetic -> Auto-Merge -> multi-edge Slide -> MMB orbit -> Magic Branch Vertex/Edge -> Organic/Paver -> Persistent Undo -> Edge Doctor regression -> locks/attributes/normals/manifold/cancel/Undo.
5. Fix only observed failures before considering integration.
6. Do not begin Witch Dock/Quickbar wrappers until canonical Witch Tools behavior is accepted.

## Files changed for Dev_v2.10.0

New source modules:

- `precision_edit_drag.py`
- `precision_edit_topology.py`
- `operators_magic_branch.py`
- `operators_edge_doctor.py`
- `operators_edit_tool_order.py`
- `panel_edit_sections.py`

Major modified source modules:

- `operators_inject_new.py`
- `precision_edit_props.py`
- `panel_precision_edit.py`
- `panel_edit_tools.py`
- `preferences.py`
- `registration.py`
- `operators_ui.py`
- `__init__.py`
- `state.py`

Packaging:

- `.github/workflows/package-witch-tools-v2-10.yml`
- stale v2.9 branch-packaging workflow removed from this feature branch.

Documentation additions/updates are tracked by the project/source notes changelogs.

## Test status

- Python syntax compile of authored Dev_v2.10 modules: passed.
- Source-level architecture/registration review: performed.
- Blender executable available here: no.
- Blender 4.5 registration/UI/GPU/modal/topology tests: not performed.
- Undo/Redo: not performed.
- Save/reopen: not performed.
- Additional Blender versions: not tested.
- Public release branches: unchanged.
- Witch Dock/Quickbar: unchanged.
