# Changelog

## Public v1.0.1

Release correlation: public v1.0.1 was produced from internal repair build v1.1.2.

- Rebuilt the input/overlay layer so More Tools scene actions execute through dedicated undoable operators.
- Fixed the undo behavior for Rotate, Origin, Snap, and Mirror Selected actions.
- Added View3D gizmo hit targets over the drawn quickbar UI.
- Kept short-lived modal operators only for drag, resize, and reorder interactions.
- Fixed file-load recovery so the quickbar remains interactive after opening a new Blender project.
- Fixed Mode button tooltip behavior.
- Fixed Cycle Modes traversal so disabled cycle modes are skipped instead of blocking the cycle.
- Kept UI-only controls out of Blender's object undo stack.
- Updated footer/version metadata to `v1.0.1`.

## Public v1.0.0

Release correlation: public v1.0.0 was produced from internal build v1.3.10.

- First public release.
- Added floating quickbar UI for Mode, Rotate, Origins & Cursor, and Mirror Objects workflows.
- Added draggable/reorderable mode buttons and More Tools sections.
- Added cycle-mode shortcut preferences and mode inclusion filtering.
- Added lock/unlock, resize, preferences, update-link, and version footer controls.
