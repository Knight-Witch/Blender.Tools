# Precision Edit — Feature State

Last updated: 2026-08-08

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Branch: `feature/witch-tools-magic-branch`
- Direct parent branch: `feature/witch-tools-precision-edit`
- Parent head at branch creation: `a5fe4bbccc954b25ac645489f2092b3d3d7618c5`
- Current candidate: Witch Tools `Dev_v2.10.0`
- Intended Blender target: `4.5.0`

## Dev_v2.9 systems retained

- Coordinate Copy Global/Local, XYZ, Location/Rotation/Scale, independent targets, multi-object conversion.
- Plane Lock custom-layer constraints and guard.
- Level exact per-target world-coordinate assignment.
- Coordinate Copy Apply default `Ctrl+Shift+C` shortcut.

## Dev_v2.10 Inject New expansion

- Solo / Branch / Slide retained.
- Solo/Branch movement changed to independent X/Y/Z toggles; any non-empty combination is allowed.
- straight captured Rail remains available.
- Magnetic Snap highlights vertex/edge/face targets.
- vertex/edge magnetic placement rigidly aligns the nearest compatible new endpoint.
- face magnetic placement solves each endpoint along its own travel line.
- Branch Auto-Merge welds supported vertex/edge contacts and materializes interior edge split points.
- multiple selected Slide edges receive one inserted vertex each at one shared relative factor.
- nearest selected rail under the cursor acts as Slide driver.
- MMB pauses live placement and passes viewport orbit through after assigning the live injection as the pivot candidate.
- zero-length edge and zero-area face validation added through the shared topology backend.

## Shared backend

- `precision_edit_drag.py`: projection, hover picking/highlight, magnetic solves, merge materialization, MMB pivot helper.
- `precision_edit_topology.py`: duplication/branch primitives, Paver/Organic primitives, geometry validation.
- These modules are also canonical for Magic Branch; no duplicate magnetic implementation is intended.

## Static checks performed

- authored Dev_v2.10 Python modules compile with Python syntax compilation in the implementation environment;
- source/version/registration wiring has been reviewed while integrating files;
- stale branch-specific Dev_v2.9 packaging workflow was replaced with a Dev_v2.10 workflow targeting this feature branch.

## Runtime status

No Blender executable is available in the implementation environment. The following remain untested in Blender 4.5:

- registration/unregistration;
- panel/icon/GPU hover rendering;
- Coordinate Copy and Plane Lock inherited runtime acceptance;
- magnetic snap from practical camera angles;
- target-edge split/weld behavior;
- multi-edge Slide cancellation and data preservation;
- MMB orbit pivot/resume behavior;
- Undo/Redo;
- save/reopen;
- additional Blender versions.

## Current limitations

- topology creation is active-object-only;
- Rail is straight only;
- Branch creates branch edges, not automatic side faces;
- arbitrary face-interior Auto-Merge retopology is intentionally not invented;
- Slide dynamically drives only the preselected edge set; unselected fan edges are not added solely by hover in this candidate.

## Next exact step

Run `TEST_PLAN.md` plus `/docs/features/magic_branch/TEST_PLAN.md` in Blender 4.5. Fix only failures observed during that validation before any Witch Dock / Quickbar wrapper work.
