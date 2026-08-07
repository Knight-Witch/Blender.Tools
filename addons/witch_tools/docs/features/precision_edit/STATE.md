# Precision Edit — Feature State

Last updated: 2026-08-07

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Branch: `feature/witch-tools-precision-edit`
- Parent baseline commit: `fc94b7c27d0b850699e79b973a0548a2193eb525`
- Parent candidate: Witch Tools `Dev_v2.8.0` Guided Align
- Current candidate: Witch Tools `Dev_v2.9.0`
- Intended Blender target: `4.5.0`

## Last completed work

- Added Coordinate Copy source capture and Apply operators with explicit Global/Local conversion, XYZ masks, Location/Rotation/Scale geometry-frame handling, independent target groups, multi-object world-space support, and preflight against protection systems.
- Added Plane Lock using persistent mesh custom layers plus a guard timer.
- Added Level source capture and exact per-target world-coordinate application.
- Added interactive Inject New with Solo, Branch, Slide, X/Y/Z movement, arbitrary straight Rail endpoint capture, commit/cancel behavior, and protection-system suspension/restoration.
- Added compact step-based Edit Tools UI, hover help, and a default `Ctrl+Shift+C` Coordinate Copy Apply shortcut.
- Preserved the existing A/B/C Auto-Aligned Edge / Vertex Inject as a separate tool.
- Bumped development metadata from Dev_v2.8.0 to Dev_v2.9.0.

## Current known-working state

Source implementation is committed on the feature branch and the branch is based directly on the verified Dev_v2.8.0 candidate commit.

Static syntax compilation has been performed on the authored new precision-edit modules during implementation. The final repository wiring/version/docs pass still requires final source-contract comparison before handoff.

No Blender runtime is available in the implementation environment. No claim is made that Blender 4.5 registration, panel rendering, interactive modal placement, undo/redo, topology rollback, or save/reopen has passed.

## Active problems / validation risks

1. Blender 4.5 runtime validation is pending.
2. Coordinate Copy edge/face partial Euler rotation and geometry extent behavior needs real-mesh acceptance testing, especially under mirrored/non-uniform object transforms.
3. Plane Lock's timer-based restoration must be tested during normal Blender transforms and save/reopen.
4. Inject New modal mouse projection must be tested from several camera orientations.
5. Inject New cancel rollback for Branch and especially Slide must be confirmed to restore topology exactly.
6. Inject New currently operates on one active mesh at a time.
7. Inject Rail is a straight source-to-end segment only.
8. Branch creates loose source-to-copy edges, not side faces; manifoldness is therefore not promised for Branch.
9. Slide must be tested for normals, manifold safety, edge attributes, zero geometry, and Undo/Redo.
10. `Ctrl+Shift+C` must be checked against the user's Blender keymap for conflicts.
11. The older roadmap references a missing `/docs/features/align_selection/` packet; that inherited documentation gap remains unresolved.

## Next exact implementation step

1. Finish static branch/source contract validation after documentation changes.
2. Install Dev_v2.9.0 in Blender 4.5.
3. Execute `TEST_PLAN.md` in order, beginning with registration/UI and Coordinate Copy Location tests.
4. Fix only failures found by those tests; do not broaden scope into deferred rails/extrusion/Quickbar work.
5. Once accepted, cut a versioned installable artifact and record exact size/SHA-256 plus tested Blender versions.
6. Only then consider thin Witch Dock / Quickbar exposure.

## Files added for the implementation

- `precision_edit_props.py`
- `precision_edit_common.py`
- `precision_edit_frames.py`
- `operators_coordinate_copy.py`
- `operators_planar_edit.py`
- `operators_inject_new.py`
- `panel_precision_edit.py`

## Existing source files changed

- `__init__.py`
- `state.py`
- `registration.py`
- `keymaps.py`
- `operators_ui.py`
- `panel_edit_tools.py`

## Test status

- Authored-new-module Python syntax compile: passed during implementation
- Branch ancestry / changed-file comparison: passed
- Blender executable available in implementation environment: no
- Blender 4.5 registration: not performed
- Blender 4.5 UI rendering: not performed
- Coordinate Copy real-mesh behavior: not performed
- Plane Lock real transform guard: not performed
- Level real-mesh multi-object behavior: not performed
- Inject New modal behavior: not performed
- Inject topology commit/cancel: not performed
- Undo/redo: not performed
- Save/reopen: not performed
- Additional Blender versions: not tested
