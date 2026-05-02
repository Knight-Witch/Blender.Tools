# Changelog

## Public v1.0.2

Release correlation: public v1.0.2 was produced from internal build 1.2.8.


### v1.0.2 public release

- Fixed footer shortcut assignment hitboxes so Maximize Open/Close can be assigned independently from Open/Close.
- Changed the automatic Maximize fallback from Ctrl + Open/Close to Alt + Open/Close.
- Preserved manual Maximize shortcut assignment when already set.


## v1.0.2

- Tooltip and compact mode polish.
- Removed the Mode title row for a more compact minimized state.
- Fixed Origins & Cursor button tooltips so every button reports its own action.
- Enlarged and spaced the Mirror Selected button icon/text.


- Removed generic/native hover tooltip noise from the dock drag area and More Tools reorder hit areas.
- Replaced the generic `Run a Witch Quickbar interface action` tooltip behavior with action-specific descriptions where needed.
- Added lock-button hover text: `Lock/unlock dock position`.
- Added dedicated Cursor/World pivot icons to Mirror Objects.
- Added a mirror icon to the Mirror Selected button.
- Reworked Mirror Objects layout to use a compact `Pivot:` label, flush Cursor/World icon buttons, and a separate Mirror Selected button.
- Restored the footer hotkey/quick-access icon and reserved the Knight Witch emblem only for the closed launcher state.
- Added a cog/settings footer button using the preferences icon.
- Added an expandable footer hotkey section for Open/Close, Maximize Open/Close, Cycle Modes, and Last Mode Used shortcut assignment.
- Enlarged the More Tools reorder grip in section title bars.
- Updated footer/version metadata to `v1.0.2`.

## Dev_v1.2.3

- Increased the emblem size inside the closed launcher button.
- Darkened the closed launcher button background so the white emblem reads more clearly.

## Dev_v1.2.2

- Removed the 3D View N-panel/sidebar tab; controls now live in the floating overlay and add-on preferences only.

## Dev_v1.2.0

Release correlation: development build based on `Dev_v1.1.2`.

- Added header minimize button.
- Added header maximize button.
- Added header close button.
- Added a Closed Launcher display state with a draggable launcher button near the lower-left of the 3D View.
- Added persistent display state preferences.
- Added persistent last-open-state tracking so the closed launcher restores to the previous open state.
- Added launcher position preferences.
- Added Open/Close hotkey target.
- Added Maximize Open/Close hotkey target.
- Open/Close cycles Full → Minimized → Closed Launcher and restores from Closed Launcher to the last open state.
- Maximize opens the tool to Full view and expands all More Tools sections when used while already Full.
- Assigning Open/Close defaults Maximize to Alt + the same key when Maximize has not already been customized.

## Dev_v1.1.2

- Fixed Cycle Modes getting stuck when disabled modes were encountered in the Mode button order.
- Cycle Modes now walks forward through the visual Mode order until it finds the next enabled mode.
- If an enabled target mode is unavailable in the current context, the cycler continues to the next enabled candidate instead of repeatedly failing on the same target.

## Dev_v1.1.1

- Corrected Mode button tooltip behavior after the v1.1.0 gizmo-input rewrite.
- Mode button native hover text now resolves to the specific mode/tool name instead of the generic mode-button operator description.
- Suppressed the custom drawn tooltip for Mode buttons to prevent a stale mode-name bubble after clicking a mode.

## Dev_v1.1.0

Release correlation: development repair build based on public `v1.0.4`.

- Rebuilt the input/overlay layer.
- Removed normal button handling from the always-running modal operator architecture.
- Added a View3D gizmo input layer for quickbar hit targets.
- Kept the custom drawn floating overlay visuals.
- Added dedicated undoable scene operators for Rotate, Origin, Snap, and Mirror Selected actions.
- Kept UI-only actions out of Blender's object undo history.
- Kept short-lived modal operators only for dragging, resizing, and reorder interactions.

## Public v1.0.4

- Attempted modal-detach undo dispatch for scene-changing More Tools actions.
- This did not fully resolve delayed/crossed undo behavior and was superseded by `Dev_v1.1.0`.

## Public v1.0.3

- Attempted timer-queued undo dispatch for scene-changing overlay buttons.
- Superseded by later input-layer repair work.

## Public v1.0.2

- Added file-load recovery for overlay/input handler restart after opening new Blender projects.

## Public v1.0.1

- Added an undoable generic action wrapper for scene-changing commands.

## Public v1.0.0

Release correlation: public v1.0.0 was produced from internal build v1.3.10.

- First public release.