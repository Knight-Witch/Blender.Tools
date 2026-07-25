# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-24

## Dev_v2.7.0 — Align Selection

- Added the canonical Align Selection backend and N-panel controls under Edit Tools.
- Added Source and Target Anchor capture through persistent per-vertex marker layers.
- Added Match Coordinates for direct X/Y/Z coordinate assignment to the current target selection.
- Added Move Shape for translating the full current selection while preserving its internal geometry relative to the captured Target Anchor.
- Added Whole Selection and Per Selected Island grouping so multiple disconnected cavities can align independently to one Source.
- Declared world space as the common analysis frame and convert results back into each object's local space.
- Added multi-object Edit Mode support, Vertex Lock preflight, multi-shape-key rejection, and failure-before-mutation behavior.
- Added thin Quickbar Dev_v1.5.0 integration locally; Quickbar source was not uploaded to GitHub.
- Added `ALIGN_SELECTION_QUICK_START.md`.

## Testing

- Python parse/compile passed for the complete Witch Tools package.
- Pure transform-planning tests passed for axis masking, coordinate matching, translation deltas, connected components, and Figure-B-style relative-distance preservation.
- Operator IDs were checked for duplicates.
- Blender 4.5 registration, interactive UI, real mesh execution, undo/redo, multi-object, multi-island, lock, and shape-key behavior remain pending.

## Preserved state

- Curvature Sync, Vertex Inject, Selection Slots, package identity, public branches, official source paths, footer URL, and prior operator IDs remain unchanged.
