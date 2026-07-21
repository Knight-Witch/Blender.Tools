# Witch Tools Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit
- Default target Blender version: 4.5
- Development package identity: `Witch_Tools_Dev`
- Development branch: `Blender_Dev`

## Current development build

- Version: `Dev_v2.6.0`
- Artifact: `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`
- SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Package folder: `Witch_Tools_Dev`
- Declared Blender target: `4.5.0`
- Python source files: 46
- PNG assets: 6
- Generated cache files: none
- Static syntax/package audit: passed
- Blender runtime in this implementation pass: not available

Dev_v2.6.0 was produced from the successful Dev_v2.5.2 collar build without changing package identity, prior operator identifiers, assets, or the Witch Tools footer URL.

## Current implementation

Dev_v2.6.0 retains:

- Auto-Aligned Vertex Inject;
- Curvature Sync circular A/M/Z multi-chain and multi-object repair;
- Replace Misaligned Column Edges;
- Vertex Lock / Protected Edit Zone integration;
- all existing Dev_v2.x panels and workflows.

It adds **Edit Tools > Selection Slots** immediately below Curvature Sync:

- persistent renameable slots for vertex, edge, face, and combined mesh selection modes;
- one or multiple objects in multi-object Edit Mode;
- save/overwrite, reselect, clear, Clear All, remove, add, and reorder;
- automatic initial Slot 1 and a maximum of 20 slots;
- scene slot records with stable UIDs and object references;
- per-slot vertex/edge/face integer custom-data markers stored in mesh data;
- `.blend` persistence design without transient BMesh-index storage;
- stable `mesh.wt_selection_slot_*` operator family for Quickbar integration;
- responsive N-panel name fields and native LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD icons.

## Last completed work

- Recorded user validation that Dev_v2.5.2 corrected the production collar curvature/column topology in Blender 4.5.
- Implemented Selection Slots as the canonical Witch Tools backend and N-panel UI.
- Added Quickbar-safe operator contracts for save, reselect, clear, Clear All, add, remove, rename, and move.
- Added a Selection Slots quick-start and package README/changelog/notes/compatibility updates.
- Produced and statically audited the Dev_v2.6.0 ZIP.
- Created the repository Selection Slots specification, state, roadmap, test plan, decisions, and reference cases.

## Current known-working state

Previously verified Dev_v2.5.2 state:

- the user installed it in Blender 4.5 and confirmed the production Curvature Sync result worked beautifully;
- automated Blender Python 5.2 tests passed for the collar correspondence repair and save/reopen.

Dev_v2.6.0 static validation:

- all 46 Python files parse and compile;
- no duplicate `bl_idname` values;
- ZIP integrity and safe paths passed;
- no `__pycache__`, `.pyc`, `.pyo`, or unrelated source assets shipped;
- package root remains `Witch_Tools_Dev`;
- footer URL remains `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools`.

Selection Slots itself has not yet been runtime-tested in Blender.

## Active problems

1. Dev_v2.6.0 installation and registration require Blender 4.5 testing.
2. Vertex, edge, face, mixed-domain, and multi-object save/reselect behavior require runtime validation.
3. Save/reopen persistence and interactive undo/redo are unverified.
4. Blender topology operations may delete or propagate custom marker data; actual Blender 4.5 behavior must be recorded.
5. Hidden or unavailable saved objects are not forcibly unhidden.
6. Linked objects sharing one Mesh datablock share underlying selection-marker layers.
7. N-panel native tooltip behavior for clipped editable names requires visual validation.
8. The full Dev_v2.6.0 source tree has not yet been imported into the final canonical repository source location.
9. Source-derived UI and operator registries remain pending.
10. Final collar normals/manifold/print-fit inspection remains pending independently of Selection Slots.

## Next exact implementation step

Install Dev_v2.6.0 in Blender 4.5 on a backup `.blend`. Test:

1. vertex, edge, face, and combined-domain slots;
2. multi-object Edit Mode;
3. overwrite after adding a missed element;
4. save/reopen persistence;
5. clear versus remove and Clear All;
6. add, rename, and reorder;
7. deleted/subdivided/duplicated topology behavior;
8. undo/redo;
9. regression of Curvature Sync, Vertex Inject, Vertex Locks, Object Snap, panel collapse, and unregister/re-register.

Patch only runtime failures found by those tests. After validation, import the complete Dev_v2.6.0 source tree canonically and generate UI/operator registries.

## Test status

- Dev_v2.5.2 Blender 4.5 production Curvature Sync: user-reported passed
- Dev_v2.6.0 ZIP integrity and safe paths: passed
- Dev_v2.6.0 Python syntax/compile: passed for 46 files
- Duplicate operator-ID scan: passed
- Cache/package hygiene: passed
- Blender 4.5 Selection Slots runtime: not performed
- Save/reopen: not performed for Selection Slots
- Multi-object selection restore: not performed
- Interactive undo/redo: not verified
- Public release/update behavior: not modified or tested

## Known remaining issues

Dev_v2.6.0 is a development build, not a public release. Selection Slots uses persistent custom element markers rather than immutable topology UUIDs, so destructive topology changes can alter which elements survive or inherit a saved slot.
