# Align Selection Test Plan

Target runtime: Blender 4.5.

## Static and package tests

- Parse and compile every Python file.
- Scan operator IDs for duplicates.
- Verify ZIP integrity and safe relative paths.
- Confirm no cache, temporary, editor, or test files ship.
- Confirm package identities and update URLs remain unchanged.
- Confirm Quickbar contains no duplicate geometry backend.
- Confirm every Align Selection UI-state name referenced by `state.py` and `panel_edit_tools.py` is registered in `WitchToolsPreferences`.
- Confirm the N-panel section uses a valid Blender icon identifier already used successfully by the add-on.

## N-panel rendering regression

1. Install Dev_v2.7.1 over Dev_v2.7.0.
2. Open View3D sidebar > Witch Tools > Edit Tools.
3. Confirm **Align Selection** renders between Curvature Sync and Selection Slots rather than as an empty box.
4. Expand and collapse the section.
5. Confirm the following render:
   - Median / Active Element source-reference dropdown;
   - Capture Source;
   - X/Y/Z toggles;
   - Match Coordinates / Translate-Preserve Shape operation selector;
   - Capture Target Anchor(s) and grouping selector in Translate mode;
   - Apply and Clear.
6. Restart Blender and confirm disclosure state persists.

## Core math tests

- X/Y/Z and multi-axis masks.
- Match Coordinates preserves disabled axes.
- Move Shape applies one identical delta per component.
- Relative distances remain unchanged.
- Point averaging and selected-component partitioning.
- Empty and malformed inputs.

## Figure A runtime test

Capture one source vertex, select a wall, enable X, choose Match Coordinates, apply, verify world X equality and unchanged Y/Z, then undo/redo. Repeat with edge, face, mixed references, Median, Active Element, and other axis combinations.

## Figure B runtime test

Capture Source and the alignment wall as Target Anchor, select the complete cavity, choose Move Shape and X, apply, verify anchor alignment and unchanged cavity dimensions, then undo/redo.

## Multiple-cavity runtime test

- Select two disconnected cavity shapes.
- Capture anchor geometry in each.
- Use Per Selected Island.
- Verify each anchor independently reaches Source and each cavity retains dimensions.
- Verify an island without an anchor cancels all changes.

## Multi-object runtime test

- Use objects with different transforms.
- Capture Source on one object and move targets on another.
- Verify visible world alignment and correct local reconstruction.
- Test non-invertible transform cancellation where constructible.

## Capture tests

- Vertex, edge, face, and mixed captures.
- Median and Active Element references.
- Recapture overwrite and Clear.
- Save/reopen persistence.
- Deleted, subdivided, or duplicated captured topology and stale-count behavior.

## Safety tests

- Vertex Lock enabled cancellation without mutation.
- Explicit lock bypass where supported.
- Shape-key cancellation.
- Missing context, no axes, empty target, stale markers, and missing anchor.
- Source exclusion from movement.
- All failure paths leave coordinates unchanged.

## Quickbar regression — deferred until local Quickbar patch

- Add and test source-reference control.
- Verify backend unavailable state.
- Drag, resize, lock, minimize/maximize, launcher, section reorder, and pass-through.
- UI-only actions do not pollute undo.
- Apply produces one undo step.
- Existing Select and Edit tools remain functional.

## Acceptance record

Record exact Blender version, add-on version, geometry setup, screenshots, Figures A/B measurements, undo/redo, passes/failures, and compatibility limitations.
