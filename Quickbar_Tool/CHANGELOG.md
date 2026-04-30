# Changelog

## v1.0.0

Release correlation: public v1.0.0 was produced from internal build v1.3.10.

### Added

- Floating 3D View quickbar with a draggable title bar labeled `Witch's Quickbar`.
- Lock/unlock title-bar control.
- Left, right, and bottom border resizing.
- Persistent dock position, width, extra height, scale, lock state, section order, and mode order preferences.
- Always-visible Mode section with drag/drop mode-button reordering.
- Cycle Modes and Last Mode operators for shortcut assignment.
- Cycle Modes inclusion filtering in add-on preferences.
- Collapsible More Tools container.
- Reorderable More Tools subsections.
- Rotate subsection with 90° / 180° toggle and X/Y/Z rotation buttons.
- Origins & Cursor subsection with origin, cursor, selection, and grid helpers.
- Mirror Objects subsection with Cursor / World pivot toggle and one-click X-axis mirrored duplication for selected mesh objects.
- Footer controls for add-on preferences and update checking.
- Footer version display.

### Changed

- Public release metadata now uses `Witch Quickbar v1.0.0`.
- Footer version now displays `Version: v1.0.0`.
- Sidebar controls include toggles for Rotate, Origins & Cursor, and Mirror Objects.

### Cleaned

- Removed unused import from `draw.py`.
- Simplified mirror pivot assignment in `actions.py`.
- Kept the internal package folder name as `Witch_Quickbar_v1` so user preferences can persist across updates.
