# Witch Quickbar Overlay Architecture

## Status

This document records the required architectural boundaries. Exact class/module names must be reconciled with the imported current source.

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
- launcher movement

They must release control cleanly and never leave Blender selection/input blocked.

### Scene operator layer

Scene-changing actions must use dedicated undoable operators where practical:

- rotations
- origin/cursor operations
- selection/grid operations
- mirror workflows
- future Witch Tools invocations

UI state changes must not enter Blender's object/scene undo history.

## Display states

The tracked public lineage contains:

- Full
- Minimized
- Closed Launcher

State transitions, last-open-state restoration, launcher position, and hotkey behavior must remain consistent unless explicitly redesigned and tested.

## Persistence

Persist only intentional user configuration:

- display state and last open state
- location and size
- lock state
- section order and collapse state
- mode order and cycle inclusion
- assigned hotkeys

Migration code must preserve prior preference keys where possible.

## File-load recovery

Opening or resetting a Blender file must not leave stale draw handlers, gizmos, or modal state. The current source includes recovery intent and must be audited before changes.

## Multi-area behavior

The exact current behavior across multiple 3D View areas and windows must be documented after source audit. New code must not assume a single 3D View without tests.

## Failure and cleanup

On disable/unregister:

- stop overlay runtime
- remove handlers
- unregister gizmos/operators/keymaps
- remove dynamic WindowManager properties
- cancel timers
- tag affected areas for redraw

## Prohibited refactors

- replacing overlay with an N-panel for convenience
- merging drawing and scene mutation into one handler
- swallowing all viewport events
- adding permanent modal capture for ordinary clicks
- renaming persistent properties without migration
- moving required assets without compatibility handling