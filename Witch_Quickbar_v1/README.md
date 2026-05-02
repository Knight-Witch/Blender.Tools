# Witch Quickbar v1.0.2

**Witch Quickbar** is a floating quick-access toolbar for Blender. It provides compact viewport controls for mode switching, rotation shortcuts, origin/cursor snapping, object mirroring workflows, and fast display-state control.

## Development Build Note

Public v1.0.2 was produced from internal build 1.2.8.

This build focuses on UI polish for the floating dock: cleaner tooltip behavior, mirror-tool icons, a darker/larger closed launcher emblem, and an expandable footer hotkey section.

## Current Tools

- Floating draggable quickbar in the 3D View
- Lock/unlock position control
- Left/right/bottom resize handles
- Minimize to Mode-only bar
- Maximize to full tool view
- Close to a small draggable launcher button
- Open/Close display hotkey support
- Maximize Open/Close hotkey support
- Mode Switcher
- Custom mode button order
- Cycle Modes shortcut support
- Cycle inclusion filter in preferences
- Last Mode Used shortcut support
- More Tools collapsible container
- Reorderable More Tools sections
- Rotate tools for Object/Edit Mode
- Origins & Cursor tools
- Mirror Objects tool with Cursor/World pivot
- Expandable footer hotkey controls
- Settings footer button
- GitHub update/check footer button

## Display States

Witch Quickbar has three display states:

- **Full**: normal full quickbar with Mode and More Tools visible.
- **Minimized**: header plus Mode switcher only.
- **Closed Launcher**: a small draggable launcher icon near the lower-left of the 3D View.

The closed launcher restores the quickbar to its last open state.

## Hotkeys

Display hotkeys are available for:

- **Open/Close**: cycles from Full → Minimized → Closed Launcher, and restores from Closed Launcher to the last open state.
- **Maximize Open/Close**: opens the tool to Full view, or expands all More Tools sections if already Full.

The footer hotkey icon opens an inline shortcut section for quick assignment and clearing of:

- Open/Close
- Maximize Open/Close
- Cycle Modes
- Last Mode Used

When assigning the Open/Close hotkey, the Maximize hotkey defaults to the same key with Ctrl added if it has not already been customized.

## Undo Behavior Target

The More Tools buttons that change the scene are dedicated undoable operators:

- Rotate X/Y/Z
- Origin to Geometry
- Origin to Cursor
- Cursor to Selected
- Cursor to Grid
- Selection to Cursor
- Selection to Grid
- Mirror Selected

Expected behavior: click the tool, press Ctrl+Z, and Blender should immediately undo the action like a normal Blender operation.

## Troubleshooting

If the quickbar ever appears but stops responding after loading a new project, disable and re-enable the add-on in Blender Preferences. The tool also includes file-load recovery logic intended to restart the overlay after a new file is opened.
