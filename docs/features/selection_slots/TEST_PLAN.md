# Selection Slots Test Plan

Target: Blender 4.5

## 1. Installation and lifecycle

1. Install Witch Tools Dev_v2.6.1 over Dev_v2.6.0.
2. Enable, disable, and re-enable the add-on.
3. Expand Edit Tools > Selection Slots by clicking the arrow.
4. Collapse and expand it by clicking the title text.
5. Confirm Slot 1 renders below the header and Clear All.
6. Create a new scene and open a legacy `.blend`; confirm Slot 1 is initialized without a draw error.
7. Save and reopen; confirm the slot collection persists.
8. Keep Quickbar Dev_v1.4.0 installed and verify its Select tab still invokes the same Witch Tools slots.

Acceptance: no registration error, blank body, repeated Slot 1/Slot 2 initialization, draw-time RNA mutation error, stale handler, or package conflict.

## 2. Empty-scene fallback

1. Use a scene whose Selection Slots collection is empty.
2. Expand the N-panel section.
3. Confirm it displays `Create Slot 1` instead of failing to draw.
4. Click it once; confirm exactly one Slot 1 exists.
5. Click Add once; confirm Slot 2 is created.

Acceptance: initialization occurs through the operator, not `Panel.draw()`, and no duplicate initial row is created.

## 3. Vertex selection

1. Enter Edit Mode in Vertex Select mode.
2. Select a non-contiguous set.
3. Save to Slot 1.
4. Deselect all and reselect Slot 1.
5. Compare exact surviving elements/counts.
6. Save/reopen and repeat.

Acceptance: marked vertices and Vertex Select mode restore.

## 4. Edge selection

Repeat with:

- one contiguous loop;
- several fragmented chains;
- boundary and interior edges;
- a Curvature Sync chain selection.

Acceptance: the saved edge set restores without repeated Alt-click selection.

## 5. Face selection

Repeat with disconnected and adjacent face regions.

Acceptance: exact surviving marked faces restore and unrelated faces remain unselected.

## 6. Combined selection modes

Enable multiple mesh selection modes where Blender permits, save, and restore.

Acceptance: the stored mode tuple and surviving marked domains restore consistently with Blender selection flushing.

## 7. Multi-object Edit Mode

1. Select two or more mesh objects with different element selections.
2. Enter multi-object Edit Mode.
3. Save one slot.
4. Leave Edit Mode and select another object.
5. Reselect the slot.

Acceptance: saved objects are selected, multi-object Edit Mode opens, and each mesh receives its saved selection.

## 8. Slot management

Test:

- Add through Slot 5.
- Rename to short and long names.
- Widen and narrow the N-panel.
- Overwrite after adding a missed element.
- Clear and confirm row/name remain.
- Remove and confirm row/data are deleted.
- Remove the final row and confirm one empty Slot 1 returns.
- Reorder with up/down controls.
- Clear All and confirm rows/names remain.
- Attempt to exceed 20 slots.

Acceptance: each control has distinct behavior and slot UID/data do not swap during reorder.

## 9. Failure and topology-change behavior

1. Attempt Save with no active-domain elements selected.
2. Confirm prior valid data remains.
3. Delete some saved elements and reselect.
4. Split and duplicate marked geometry; inspect marker propagation.
5. Remove or hide a saved object.
6. Attempt reselect with every saved object unavailable.

Acceptance: no crash or partial corruption; surviving data is selected or a clear warning is reported.

## 10. Undo/redo

Test Ctrl+Z/Ctrl+Shift+Z after:

- Save/overwrite;
- Clear;
- Clear All;
- Remove;
- slot initialization;
- geometry edits after a saved selection;
- Quickbar invocation of scene-data actions.

Acceptance: no partial custom-layer state, add-on exception, or Quickbar input lockup.

## 11. Quickbar Select tab

The user reported the Dev_v1.4.0 Select workflow worked correctly. Complete the remaining regression matrix:

- rename and full-name tooltip;
- responsive width;
- all slot actions;
- drag upward/downward and cancel;
- viewport pass-through;
- locked/unlocked and resized dock;
- open/close, minimize/maximize, file-load recovery;
- Witch Tools disabled/unavailable state;
- unregister/re-register.

## 12. Regression

Witch Tools:

- Curvature Sync Analyze/Apply;
- Vertex Inject;
- Vertex Locks/Protected Edit Zones;
- Object Snap;
- panel collapse/minimal view;
- unregister/re-register.

Quickbar:

- Main and Edit tabs;
- Mode controls;
- Apply All Transforms;
- Mirror workflows;
- Vertex Snap and duplicate tools;
- section/tab/mode reorder;
- update URL;
- file-load recovery.

## 13. Required record

Record build/hash, Blender version/OS, file, selection domain/object count, result, undo/redo, save/reopen, failures, and tester.