# Witch Quickbar Input and Event Contract

## Goal

Quickbar must remain responsive without blocking normal Blender viewport interaction.

## Event ownership

An event may be consumed only when:

- the pointer is inside an active Quickbar hit target; or
- a Quickbar modal drag/resize/reorder operation is actively running; or
- an assigned Quickbar hotkey is matched.

All unrelated viewport input must pass through.

## Click behavior

- Press and release must resolve to the intended control.
- Overlapping hitboxes are prohibited.
- Footer shortcut controls must not trigger neighboring assignments.
- Tooltip hit areas must match the actual button action.
- Locked dock state must block movement without blocking button use.

## Drag threshold

A click must not become a drag from minor pointer movement. Dragging begins only after a defined threshold and only from permitted handles/title areas.

## Resize

- left, right, and bottom resize regions must remain distinct
- resize must clamp to valid dimensions
- release must end the modal interaction immediately
- no resize handle may capture input while the dock is locked if the current design disables resizing under lock

## Section reorder

- reorder begins only from the intended grip/title area
- ordinary button clicks within a section must not start reorder
- canceled reorder restores the original order
- state persists only after a successful drop

## Display controls

Open/Close and Maximize Open/Close must retain separate assignable hitboxes and keymaps. Default fallback shortcuts must not overwrite an explicitly assigned user shortcut.

## Mode switching

- unavailable modes must not trap Cycle Modes on the same target
- disabled cycle targets are skipped
- entering Pose Mode from a linked mesh may select the relevant armature only according to the documented behavior
- mode actions must preserve usable active-object context

## Undo contract

Scene-changing actions use dedicated undoable operators. UI-only actions—including collapse, reorder, resize, display state, and lock—must not pollute Blender scene undo history.

Immediate expected behavior:

1. invoke scene action
2. press Ctrl+Z
3. Blender immediately undoes that action

## File changes and handlers

After opening a new file:

- stale overlay/input runtime is stopped
- runtime restarts only when prior state/preferences require it
- duplicate handlers or gizmos are not registered

## Unregister

Disabling the add-on must immediately restore normal viewport input. No modal, draw handler, timer, gizmo, or keymap may remain active.

## Test matrix requirements

Test:

- click each control
- rapid repeated clicks
- drag then cancel
- resize from every handle
- locked and unlocked behavior
- overlapping UI regions
- pass-through selection and navigation around the dock
- all hotkey assignments and clearing
- Ctrl+Z/Ctrl+Shift+Z after scene actions
- file open/new/reset
- add-on disable/enable
- multiple 3D View areas where supported