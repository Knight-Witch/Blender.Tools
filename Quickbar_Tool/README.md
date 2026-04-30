# Witch Quickbar v1.0.0

Witch Quickbar is a floating 3D View quick-access overlay for Blender. It is built to coexist with Witch Tools while keeping its own operator namespace, preference state, and package files.

Release correlation: public v1.0.0 was produced from internal build v1.3.10.

## Current Layout

The dock has a draggable title bar labeled **Witch's Quickbar**, with a lock/unlock icon on the left side.

The left, right, and bottom borders can be dragged to resize the dock. Locking the quickbar prevents both movement and resizing.

The **Mode** section is always visible and supports drag/drop reordering of mode buttons.

The **More Tools** section is collapsible. Its subsections can also be collapsed individually and reordered by dragging their title rows.

Current More Tools subsections:

- **Rotate**: 90° / 180° toggle plus compact X/Y/Z rotation buttons. Rotation is only active in Object Mode and Edit Mode.
- **Origins & Cursor**: Origin to Geometry, Origin to Cursor, Cursor to Selected, Cursor to Grid, Selection to Cursor, and Selection to Grid.
- **Mirror Objects**: Cursor / World pivot toggle plus Mirror Selected. The operation is Object Mode only and mirrors selected mesh-object duplicates across X using the selected pivot.

The footer includes:

- Version text: `Version: v1.0.0`
- Shortcut/preferences button
- Check-for-updates button linking to the Witch Quick Access GitHub branch

## Shortcut Targets

These operators are exposed for shortcut assignment:

- `witch_quickbar.cycle_modes`
- `witch_quickbar.last_mode`

Shortcut assignment is handled in the add-on preferences UI.

## Cycle Mode Filtering

The add-on preferences include a Cycle Modes icon row. The icons appear in the same order as the floating Mode row. Active icons are included when using the Cycle Modes button or its assigned shortcut; inactive icons are skipped. The order follows the user's custom Mode row order.

## Notes

The quickbar is a custom floating viewport overlay, not a native Blender UILayout panel. Icon assets are bundled PNGs rasterized from Blender-style SVGs supplied for this build.

The entire top strip acts as the drag handle. The 8-dot grip icon is visual only; you can drag from the whole top handle.

## Installation

Install the zip through Blender Preferences > Add-ons > Install. If an older Witch Quickbar build is already enabled, disable it before enabling this version to avoid duplicate operator registration.
