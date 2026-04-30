# Witch Quickbar v1.0.1

**Witch Quickbar** is a compact floating quick-access toolbar for Blender. It provides fast viewport controls for mode switching, rotation shortcuts, origin/cursor tools, snapping, and X-axis object mirroring workflows.

This public patch release includes the repaired input/overlay layer from the internal v1.1.2 repair build.

## Features

- Floating draggable 3D View quickbar
- Lock/unlock control in the title bar
- Resizable dock width and footer space
- Reorderable mode buttons
- Reorderable More Tools sections
- Custom mode cycling with preference-based mode inclusion
- Last-used mode return
- Object/Edit rotation shortcuts
- Origin, cursor, selection, and grid tools
- X-axis Mirror Selected workflow with Cursor or World pivot
- Shortcut assignment for Cycle Modes and Last Mode Used
- Check-for-updates button linking to the project repository

## Mode Switcher

The Mode section provides quick access to:

- Edit Mode
- Object Mode
- Weight Paint
- Pose Mode
- Sculpt Mode
- Texture Paint
- Vertex Paint
- UV Data / Edit target
- Cycle Modes
- Last Mode Used

Mode buttons can be drag-reordered. The custom cycle order follows the visible mode-button order and skips any modes disabled in preferences.

## More Tools

### Rotate

Rotate selected objects or edit-mode geometry around X, Y, or Z using the selected 90° / 180° step.

### Origins & Cursor

Includes quick-access tools for:

- Origin to Geometry
- Origin to Cursor
- Cursor to Selected
- Cursor to Grid
- Selection to Cursor
- Selection to Grid

### Mirror Objects

Duplicates selected mesh objects and mirrors the duplicates across the X axis using either the 3D Cursor or World Origin as the pivot. The tool applies the required transform/origin steps automatically and leaves the mirrored duplicates selected.

## Installation

1. Download the latest Witch Quickbar `.zip` release.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. Click `Install`.
5. Select the downloaded `.zip`.
6. Enable Witch Quickbar.

## Troubleshooting

If the tool freezes, stops responding, or prevents you from selecting things in Blender:

1. Go to `Edit > Preferences > Add-ons`.
2. Find Witch Quickbar.
3. Disable the add-on.
4. Enable it again.

This resets the floating overlay and should restore normal behavior.
