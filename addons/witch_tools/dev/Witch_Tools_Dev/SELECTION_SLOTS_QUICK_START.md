# Selection Slots Quick Start

Build note: Dev_v2.6.1 fixes the Witch Tools N-panel section expansion/rendering failure found in Dev_v2.6.0.

Target: Blender 4.5  
Build: Witch Tools Dev_v2.6.1

Selection Slots is under **Edit Tools**, directly below Curvature Sync.

## Save a selection

1. Enter mesh Edit Mode. Multi-object Edit Mode is supported.
2. Use Vertex, Edge, Face, or a combined mesh selection mode.
3. Select the mesh elements you need.
4. Click the **FILE_TICK** button on the desired slot.

Saving again overwrites that slot. The slot records the active mesh-selection domain and all participating mesh objects.

## Reselect

Click the selection button on the slot. Witch Tools replaces the current mesh selection, restores the saved vertex/edge/face selection mode, and enters multi-object Edit Mode on the saved meshes when needed.

## Slot controls

- Name field: type directly to rename the slot. It expands when the N-panel is widened.
- Select: restore the saved selection.
- FILE_TICK: save or overwrite the slot.
- TRASH: clear the stored selection but keep the slot and name.
- REMOVE: delete the slot row.
- ADD: add another slot; it appears only on the last row.
- Up/Down: reorder slots in the N-panel.
- Clear All: clear every stored selection while preserving the slot rows and names.

At least one empty slot is always retained. The current limit is 20 slots per scene.

## Storage behavior

Selection data is stored in the `.blend` through per-mesh custom element layers and scene slot records. It survives save/reopen and object renaming. Existing selected elements generally retain the marker through normal topology edits, but a slot can become incomplete if its saved elements are deleted, replaced, or changed by an operation that discards custom mesh data.

Linked objects that share one mesh datablock also share the underlying custom element layers; the slot still records which object was used for reselection.
