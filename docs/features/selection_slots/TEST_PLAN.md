# Selection Slots Test Plan

Target: Blender 4.5

## 1. Installation and lifecycle

1. Install Witch Tools Dev_v2.6.0 over Dev_v2.5.2.
2. Enable, disable, and re-enable the add-on.
3. Confirm one empty `Slot 1` appears in Edit Tools below Curvature Sync.
4. Save and reopen a new `.blend`; confirm the slot collection persists.
5. Install Quickbar Dev_v1.4.0 after Witch Tools.
6. Verify Quickbar open/close, minimize/maximize, lock, resize, file-load recovery, and unregister/re-register.

Acceptance: no registration errors, stale handlers, broken panels, or package-identity conflicts.

## 2. Vertex selection

1. Enter Edit Mode on one mesh in Vertex Select mode.
2. Select a non-contiguous set of vertices.
3. Save to Slot 1.
4. Deselect all and reselect Slot 1.
5. Compare exact vertex indices/counts before and after.
6. Save/reopen and repeat reselect.

Acceptance: exact surviving marked vertices and Vertex Select mode restore.

## 3. Edge selection

Repeat the vertex test in Edge Select mode with:

- one contiguous loop;
- several fragmented chains;
- boundary and interior edges;
- a selection used by Curvature Sync.

Acceptance: the saved edge set restores without requiring repeated Alt-click selection.

## 4. Face selection

Repeat in Face Select mode using disconnected faces and adjacent regions.

Acceptance: exact faces restore and no unrelated faces become selected.

## 5. Combined selection modes

Enable multiple mesh selection modes where Blender permits it, save a mixed selection, and restore it.

Acceptance: the stored mode tuple and surviving marked domains restore consistently with Blender's normal selection flushing rules.

## 6. Multi-object Edit Mode

1. Select two or more mesh objects with different selections.
2. Enter multi-object Edit Mode.
3. Save one slot.
4. Leave Edit Mode and select another object.
5. Reselect the slot.

Acceptance: the saved objects are selected, multi-object Edit Mode opens, and each mesh receives its saved selection.

## 7. Slot management

Test:

- Add through at least Slot 5.
- Rename to short and long names.
- Widen and narrow the N-panel.
- Hover and edit long names.
- Overwrite a slot after adding a missed element.
- Clear a slot and confirm its row/name remain.
- Remove a slot and confirm its data layers are removed.
- Remove the final slot and confirm one empty Slot 1 is recreated.
- Reorder using N-panel up/down controls.
- Clear All and confirm rows/names remain.
- Attempt to exceed 20 slots.

Acceptance: each control has distinct documented behavior and no slot UID/data is accidentally exchanged during reorder.

## 8. Failure and topology-change behavior

1. Attempt Save with no active-domain elements selected.
2. Confirm prior valid slot data remains intact.
3. Delete some saved elements and reselect.
4. Split an edge carrying a slot marker and inspect whether Blender propagates the marker.
5. Duplicate marked elements and inspect propagation.
6. Remove or hide one saved object.
7. Attempt reselect with all saved objects unavailable.

Acceptance: no crash or partial corruption; surviving data is selected or a clear warning is reported. Propagation behavior is documented rather than silently rewritten.

## 9. Undo/redo

Test Ctrl+Z/Ctrl+Shift+Z after:

- Save/overwrite;
- Clear;
- Clear All;
- Remove;
- geometry edits made after a saved selection;
- Quickbar invocation of scene-data-changing actions.

Acceptance: no partial custom-layer state, add-on errors, or Quickbar input lockup. Record actual Blender undo behavior for selection-only actions separately.

## 10. Quickbar Select tab

With Witch Tools installed:

- verify Select tab appears;
- verify LONGDISPLAY title icon;
- verify each supplied icon;
- click slot name and rename;
- hover clipped long name and confirm full tooltip;
- widen Quickbar and confirm name area grows;
- save, reselect, clear, remove, add, and Clear All;
- drag slots upward and downward;
- confirm unrelated viewport input passes through;
- test rapid clicks and canceled drag;
- test locked/unlocked and resized dock states.

Without Witch Tools:

- disable Witch Tools;
- confirm Quickbar still registers and runs;
- confirm Select tab shows a clear unavailable-backend message;
- confirm no exceptions or dead hitboxes block the viewport.

## 11. Regression

Witch Tools:

- Curvature Sync Analyze/Apply;
- Vertex Inject;
- Vertex Locks and Protected Edit Zones;
- Object Snap;
- panel collapse/minimal view;
- unregister/re-register.

Quickbar:

- Main and Edit tabs;
- Mode buttons;
- Apply All Transforms;
- Mirror workflows;
- Vertex Snap;
- duplicate tools;
- section/tab/mode reorder;
- update URL button;
- file-load recovery.

## 12. Required test record

Record:

- build and hash;
- Blender version and OS;
- file used;
- selection domain and object count;
- result;
- undo/redo result;
- save/reopen result;
- known failures;
- tester.
