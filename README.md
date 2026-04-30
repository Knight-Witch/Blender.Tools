# Witch Quickbar

**Witch Quickbar** is a compact floating quick-access toolbar for Blender. It is designed for artists, modders, and mesh-editing workflows where you constantly switch modes, rotate objects, set origins, move the cursor, snap selections, or mirror left/right object sets.

The tool lives directly in the 3D View as a draggable overlay, so you do not have to keep opening the sidebar or digging through Blender menus for common actions.

## What It Does

Witch Quickbar gives you a persistent floating toolbar with fast access to high-frequency Blender actions.

Current tools include:

- Mode switching
- Custom mode cycling
- Last-used mode return
- Object/Edit rotation shortcuts
- Origin and cursor tools
- Selection and grid snapping
- Object mirroring across X
- Reorderable tool sections
- Reorderable mode buttons
- Optional hotkeys for cycle mode / last mode
- Lock/unlock positioning
- Resizable floating panel

## Mode Switcher

The Mode section provides icon buttons for quickly switching between common Blender modes:

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

The mode buttons can be drag-reordered. The order also controls the mode cycle order.

## Cycle Modes

The Cycle Modes button and hotkey let you step through your mode list in order.

In preferences, you can choose which modes are included in the cycle. This is useful if you only use certain modes regularly and want the cycle shortcut to skip the rest.

For example, you can set it to only cycle:

- Edit
- Object
- Weight Paint
- Pose

The cycle order follows the current visual order of the mode buttons.

## Last Mode Used

The Last Mode Used button returns you to the previous mode used through Witch Quickbar.

This can also be assigned to a shortcut in the add-on preferences.

## Rotate Tools

The Rotate section provides compact X/Y/Z rotation buttons.

It supports:

- 90° rotation
- 180° rotation
- X axis
- Y axis
- Z axis

Rotation tools are intended for Object Mode and Edit Mode. They are disabled in other modes.

## Origins & Cursor Tools

The Origins & Cursor section provides quick icon-pair buttons for common origin, cursor, selection, and grid operations.

Included actions:

- Origin to Geometry
- Origin to Cursor
- Cursor to Selected
- Cursor to Grid
- Selection to Cursor
- Selection to Grid

Origin to Geometry uses bounds center.

## Mirror Objects

The Mirror Objects tool is designed for left/right object mirroring workflows.

It allows you to choose a mirror pivot:

- Cursor
- World Origin

Then the Mirror Selected button duplicates the selected mesh objects and mirrors the duplicates across the X axis.

This is useful for workflows like creating matching left/right accessories, armor pieces, jewelry parts, or other symmetrical mesh elements.

The mirror operation performs the needed transform/origin steps automatically so the duplicate ends up mirrored and cleaned up without requiring the usual manual Blender sequence.

## Floating UI

Witch Quickbar appears as a floating panel in the 3D View.

The panel can be:

- Dragged by the title bar
- Locked in place
- Unlocked for movement
- Resized from the left, right, or bottom edge
- Collapsed by section
- Reordered by dragging tool section headers

The More Tools area can be collapsed entirely, leaving only the main Mode section visible.

## Preferences

Witch Quickbar includes add-on preferences for:

- Shortcut assignment
- Cycle-mode inclusion
- Toolbar behavior
- Stored layout/order settings

The shortcut preferences are used for assigning quick access hotkeys to:

- Cycle Modes
- Last Mode Used

## Installation

1. Download the latest Witch Quickbar `.zip` release.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. Click `Install`.
5. Select the downloaded `.zip`.
6. Enable Witch Quickbar.

Once enabled, the floating quickbar appears in the 3D View.

## Troubleshooting

If the tool freezes, stops responding, or prevents you from selecting things in Blender:

1. Go to `Edit > Preferences > Add-ons`.
2. Find Witch Quickbar.
3. Disable the add-on.
4. Enable it again.

This resets the floating overlay and should restore normal behavior.

## Notes

Witch Quickbar is a custom viewport overlay, not a native Blender panel. It is designed to behave like a lightweight floating utility dock while keeping the controls compact and accessible.

The tool is built for practical Blender workflow speed, especially for people who repeatedly switch modes, prep meshes, mirror object sets, and use origin/cursor operations during editing.
