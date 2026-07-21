# Selection Slots Specification

## 1. Scope

Initial scope:

- Blender 4.5
- mesh Edit Mode
- vertex, edge, face, and combined mesh-selection modes
- one or multiple mesh objects in multi-object Edit Mode
- persistent saved selections stored in the `.blend`
- multiple renameable, reorderable slots
- Witch Tools N-panel UI
- optional Witch Quickbar Select-tab access through canonical Witch Tools operators

Out of scope for the initial build:

- Object Mode object-selection sets
- armature bone selections
- UV-editor loop/UV selections independent of mesh element selection
- automatic reconstruction of deleted topology
- cross-file import/export of slots

## 2. Terminology

### Slot

A named scene record containing:

- stable slot UID;
- participating object references;
- saved mesh selection mode;
- vertex/edge/face element markers;
- stored element counts;
- display order.

### Save / overwrite

Replace the slot's prior element markers and metadata with the current Edit Mode selection.

### Reselect

Replace the current mesh selection with the elements still marked by the slot, entering multi-object Edit Mode for the saved objects when possible.

### Clear

Delete the stored selection data while preserving the slot row and user-entered name.

### Remove

Delete the slot row and its stored element data. At least one empty slot must always remain.

## 3. Persistence model

Selection identity must persist through save/reopen without relying on transient BMesh indices.

The initial implementation uses:

- a scene-level collection of slot records;
- a generated UID per slot;
- per-slot integer custom-data layers on mesh vertex, edge, and face domains;
- object pointers for the meshes that participated in the saved selection.

Layer names use an internal Witch Tools prefix and the generated UID. Slot display order and names are stored in scene data.

## 4. Save behavior

The Save action must:

1. require mesh Edit Mode;
2. inspect all unique mesh datablocks participating in multi-object Edit Mode;
3. store only the currently enabled mesh-selection domain or domains;
4. reject an empty selection without erasing valid prior slot data;
5. overwrite prior markers transactionally;
6. preserve the user's slot name;
7. report stored vertex, edge, and face counts.

## 5. Reselect behavior

The Reselect action must:

1. resolve every still-valid saved object in the current view layer;
2. reject the action when no saved mesh remains available and visible;
3. enter the required single- or multi-object Edit Mode context;
4. restore the saved mesh-selection mode;
5. deselect the current mesh elements on the participating meshes;
6. select every remaining marked element;
7. report the restored counts;
8. report a warning when markers exist but no matching element remains.

Elements deleted by later topology changes cannot be restored. Elements duplicated or split by operations that copy custom data may inherit slot markers; this must be documented rather than silently treated as immutable element identity.

## 6. Slot management

- A new scene begins with `Slot 1`.
- Users may add slots up to a conservative maximum of 20.
- New default names increment by visible list count.
- Names are editable and may be overwritten with arbitrary user text.
- An empty submitted name falls back to `Slot N`.
- Clear preserves the row and name.
- Remove deletes the row and data.
- Clear All clears data in every row but preserves rows and names.
- Removing the final row automatically recreates one empty `Slot 1`.
- Reordering changes presentation order without changing the slot UID or stored markers.

## 7. Witch Tools UI

Location: `Edit Tools`, immediately below Curvature Sync.

Header:

- native `LONGDISPLAY` tool icon;
- collapsible section title;
- top-right Clear All control using `TRASH`.

Each row provides:

- reorder controls;
- renameable name field;
- Reselect button;
- Save/overwrite button using `FILE_TICK`;
- Clear button using `TRASH`;
- Remove button using `REMOVE`;
- Add button using `ADD` on the final row only.

The name field must remain compact at normal N-panel width and naturally grow as the N-panel widens. Native N-panel implementation may use up/down reorder controls where Blender does not provide a reliable row-drag widget.

## 8. Witch Quickbar UI

Location: a populated tab named `Select`.

Requirements:

- thin invocation of Witch Tools operators;
- no duplicated saved-selection backend;
- custom supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD assets;
- click name to open rename dialog;
- full slot name shown in tooltip;
- name display grows as the floating Quickbar is widened;
- grip-based slot drag reorder;
- header Clear All icon;
- disabled explanatory state when Witch Tools Dev_v2.6.0 or the required operators are unavailable;
- no interference with overlay pass-through, resize, lock, section reorder, or file-load recovery.

## 9. Undo and failure rules

- Save, Clear, Clear All, and Remove modify persistent mesh/scene data and must be coherent actions.
- Reselect changes selection/context but not geometry.
- Slot ordering and presentation controls must not create partial geometry changes.
- Empty-save failure must leave the previous slot unchanged.
- Hidden, removed, or unavailable objects must not cause a crash.
- Quickbar must remain usable when Witch Tools is absent.

## 10. Acceptance criteria

The initial feature is accepted when:

- slots persist through save/reopen;
- vertex, edge, face, and combined-domain selections restore correctly;
- multi-object selections restore correctly;
- overwrite does not leave old markers;
- Clear, Clear All, Remove, Add, rename, and reorder behave distinctly;
- destructive topology changes fail gracefully or restore the surviving marked elements;
- Witch Tools unregister/register succeeds;
- Quickbar Select tab remains pass-through-safe and invokes the same canonical slots;
- public package identities and update URLs remain unchanged;
- Blender 4.5 runtime tests are recorded.
