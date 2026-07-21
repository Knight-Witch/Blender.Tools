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
- Selection Slot name, reselect, save, clear, remove, add, and Clear All hit targets must remain distinct.
- Disabled Selection Slot actions must not invoke fallback or neighboring operators.

## Drag threshold

A click must not become a drag from minor pointer movement. Dragging begins only after a defined threshold and only from permitted handles/title areas.

## Resize

- left, right, and bottom resize regions must remain distinct
- resize must clamp to valid dimensions
- release must end the modal interaction immediately
- no resize handle may capture input while the dock is locked if the current design disables resizing under lock
- widening the dock must grow Selection Slot name hit targets without overlapping icon controls

## Section, tab, mode, and Selection Slot reorder

- reorder begins only from the intended grip/title area
- ordinary button or name clicks must not start reorder
- canceled reorder restores the original order
- state/data order persists only after a successful drop
- Selection Slot grip drag must call the canonical Witch Tools move operator rather than directly editing mesh marker data
- Selection Slot drag state must be cleared on release, cancel, file change, stop, and unregister

## Display controls

Open/Close and Maximize Open/Close must retain separate assignable hitboxes and keymaps. Default fallback shortcuts must not overwrite an explicitly assigned user shortcut.

## Mode switching

- unavailable modes must not trap Cycle Modes on the same target
- disabled cycle targets are skipped
- entering Pose Mode from a linked mesh may select the relevant armature only according to documented behavior
- mode actions must preserve usable active-object context

## Selection Slots operator routing

Dev_v1.4.0 Select-tab controls route through dedicated Quickbar operators, which invoke Witch Tools Dev_v2.6.0+ `mesh.wt_selection_slot_*` operators.

- Name click opens the Quickbar rename dialog, then commits through the Witch Tools rename operator.
- Grip drag computes target order in Quickbar, then commits one-step moves through the Witch Tools move operator.
- Save/reselect/clear/remove/add/Clear All use the canonical operator family.
- When the backend is unavailable, controls are disabled and the overlay continues to pass unrelated events through.

## Undo contract

Scene/data-changing actions use dedicated operators. UI-only actions—including collapse, tab/section reorder, resize, display state, and lock—must not pollute Blender scene undo history.

Selection Slot save, clear, Clear All, and remove alter persistent Witch Tools scene/mesh data. Runtime tests must verify their Blender undo behavior. Selection Slot name/order presentation changes must not create geometry mutations.

Immediate expected behavior after a scene-changing action:

1. invoke the action;
2. press Ctrl+Z;
3. Blender immediately undoes that action when the canonical operator declares undo support.

## File changes and handlers

After opening a new file:

- stale overlay/input runtime is stopped
- Selection Slot drag state is canceled
- runtime restarts only when prior state/preferences require it
- duplicate handlers or gizmos are not registered
- the Select tab queries the new scene rather than retaining stale slot objects

## Unregister

Disabling the add-on must immediately restore normal viewport input. No modal, draw handler, timer, gizmo, keymap, or Selection Slot drag state may remain active.

## Test matrix requirements

Test:

- click each control
- rapid repeated clicks
- drag then cancel
- Selection Slot drag upward/downward and release outside a row
- resize from every handle
- long/short Selection Slot names at minimum and expanded width
- locked and unlocked behavior
- overlapping UI regions
- pass-through selection and navigation around the dock
- Witch Tools enabled, disabled, and unregistered while Quickbar remains enabled
- all hotkey assignments and clearing
- Ctrl+Z/Ctrl+Shift+Z after scene actions
- file open/new/reset
- add-on disable/enable
- multiple 3D View areas where supported
