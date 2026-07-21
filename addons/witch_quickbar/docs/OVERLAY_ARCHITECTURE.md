# Witch Quickbar Overlay Architecture

## Status

This document records required architectural boundaries and the Dev_v1.4.0 Selection Slots extension. Exact current source remains pending canonical repository import.

## Core principle

Quickbar is a custom floating overlay drawn in Blender's 3D View. It must not be converted into an N-panel or ordinary popover as part of unrelated refactoring.

## Required layers

### Runtime lifecycle

Responsible for:

- starting and stopping the overlay
- per-window/area state where required
- redraw scheduling
- file-load recovery
- clean unregister

### Drawing layer

Responsible for:

- panel, section, button, icon, tooltip, and launcher drawing
- Blender theme-aware presentation
- geometry calculation for hit targets
- display-state-specific layout
- responsive Selection Slot name truncation and full-name tooltip display

Drawing must not directly perform scene mutations.

### Input/gizmo layer

Responsible for:

- button hit targets
- mouse and keyboard event routing
- pass-through outside active controls
- invoking dedicated operators
- avoiding an always-running modal operator for ordinary button clicks where the current repaired architecture uses gizmos

### Short-lived modal interactions

Allowed for interactions that inherently require modal movement:

- dragging the dock
- resizing
- section reorder
- tab and mode reorder
- Selection Slot row reorder from its grip
- launcher movement

They must release control cleanly and never leave Blender selection/input blocked.

### Scene/operator integration layer

Scene-changing actions must use dedicated undoable operators where practical. Dev_v1.4.0 Selection Slots does not mutate mesh selection-marker data directly; it invokes the canonical Witch Tools `mesh.wt_selection_slot_*` operator family.

UI state changes must not enter Blender's object/scene undo history.

## Display states

The tracked lineage contains:

- Full
- Minimized
- Closed Launcher

State transitions, last-open-state restoration, launcher position, and hotkey behavior must remain consistent unless explicitly redesigned and tested.

## Tabs and dynamic content

Dev_v1.4.0 adds a populated `Select` tab containing a dynamic Selection Slots section.

The layout layer must:

- calculate row count from the canonical Witch Tools slot collection;
- reserve sufficient panel height for visible slots;
- expand slot-name width as dock width grows;
- keep icon controls at stable hit-target sizes;
- show Add only on the final row;
- show a disabled explanatory row when the Witch Tools backend is unavailable;
- keep Main and Edit tab behavior unchanged.

The current gizmo pool was increased to cover dynamic rows and tiled responsive name hit targets. Runtime profiling is required before increasing the 20-slot backend limit.

## Selection Slot interaction boundaries

- Clicking a slot name opens a short native rename dialog through a dedicated Quickbar operator.
- Save, reselect, clear, remove, add, Clear All, rename, and reorder invoke Witch Tools operators.
- Grip drag uses a short-lived Quickbar modal solely to calculate the target order; the final move is committed through the canonical Witch Tools operator.
- The Select tab must remain available but disabled safely when Witch Tools Dev_v2.6.0+ is absent.
- Quickbar must not create its own scene collection or mesh custom-data layers.

## Persistence

Persist only intentional Quickbar configuration:

- display state and last open state
- location and size
- lock state
- section order and collapse state
- mode and tab order
- assigned hotkeys
- Selection Slots section open/collapsed preference

Selection Slot names, order, and element data belong to Witch Tools scene/mesh data and persist in the `.blend`, not in Quickbar preferences.

## File-load recovery

Opening or resetting a Blender file must not leave stale draw handlers, gizmos, or modal state. On restart, the Select tab re-queries the current scene's Witch Tools slot collection rather than retaining stale slot references.

## Multi-area behavior

The exact behavior across multiple 3D View areas and windows must be documented after runtime audit. Selection Slot dynamic rows must not assume one region or retain hit targets from another area.

## Failure and cleanup

On disable/unregister:

- stop overlay runtime
- remove handlers
- unregister gizmos/operators/keymaps
- remove dynamic WindowManager properties
- cancel timers and Selection Slot drag state
- clear image/texture caches including the five new assets
- tag affected areas for redraw

## Prohibited refactors

- replacing overlay with an N-panel for convenience
- merging drawing and scene mutation into one handler
- swallowing all viewport events
- adding permanent modal capture for ordinary clicks
- renaming persistent properties without migration
- moving required assets without compatibility handling
- copying the Selection Slots backend into Quickbar
- directly editing Witch Tools mesh marker layers from the overlay
