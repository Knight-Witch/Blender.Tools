# Selection Slots State

Last updated: 2026-07-21

## Identity

- Canonical owner: Witch Tools
- Current Witch Tools build: `Dev_v2.6.1`
- Witch Tools artifact: `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`
- Witch Tools SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Superseded Witch Tools build: `Dev_v2.6.0`
- Quickbar integration build: `Dev_v1.4.0`
- Quickbar artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Quickbar SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Target Blender version: `4.5`
- Development branch: `Blender_Dev`

## Implemented backend

The canonical Witch Tools Selection Slots backend remains the Dev_v2.6.0 implementation:

- persistent scene slot collection;
- generated stable UID per slot;
- per-slot BMesh integer custom layers for vertex, edge, and face domains;
- exact save/overwrite of current enabled mesh-selection modes;
- multi-object Edit Mode save and reselect;
- rename, add, remove, clear, Clear All, and up/down reorder;
- at least one slot maintained automatically;
- maximum 20 slots;
- saved selection counts and object references;
- stable `mesh.wt_selection_slot_*` operator family;
- `.blend` persistence through scene and mesh custom data.

## Dev_v2.6.0 runtime result

User validation in Blender 4.5 found:

- Witch Quickbar Dev_v1.4.0 Select tab worked correctly in the tested workflow;
- the Witch Tools N-panel displayed the Selection Slots header and Clear All control;
- expanding the N-panel section did not reveal its slot rows.

The N-panel failure was isolated to the presentation/draw path rather than the Quickbar integration surface.

## Dev_v2.6.1 hotfix

Dev_v2.6.1 changes only the required Witch Tools N-panel and empty-slot initialization paths:

- removes `ensure_selection_slots()` from `Panel.draw()` so panel drawing never mutates Scene data;
- reads existing scene slot rows without modifying them;
- adds a safe operator-driven `Create Slot 1` fallback for an empty legacy/new scene;
- updates Add so an empty scene initializes Slot 1 without also creating Slot 2;
- makes both the disclosure arrow and title text toggle the section;
- contains an individual row draw failure so one row cannot blank the complete section;
- preserves the Selection Slots backend/operator contract and all Dev_v2.5.2 Curvature Sync code.

## Validation completed for Dev_v2.6.1

- complete AST/compile checks passed for 46 Python files;
- no duplicate `bl_idname` values were found across 92 operator identifiers;
- package root remains `Witch_Tools_Dev`;
- ZIP integrity and safe-path checks passed;
- no `__pycache__`, `.pyc`, or `.pyo` files were shipped;
- simulated N-panel layout passed for expanded, collapsed, populated, and empty-slot states;
- simulated Add behavior produced Slot 1 from an empty scene and Slot 2 on the next Add.

## Runtime status

Blender 4.5 user validation of Dev_v2.6.1 is pending. The following remain unverified:

- N-panel rows rendering and interaction after this hotfix;
- vertex, edge, face, mixed-domain, and multi-object save/reselect;
- save/reopen persistence;
- interactive undo/redo;
- marker behavior after topology deletion, subdivision, or duplication;
- complete Quickbar regression outside the user-tested Select workflow.

## Known limitations

- Slot markers are persistent custom element data, not immutable topology UUIDs.
- Deleting an element removes its saved marker.
- Splitting or duplicating topology may propagate a marker.
- Shared linked objects using one Mesh datablock share underlying marker layers.
- Hidden or unavailable saved objects are not forcibly unhidden.
- N-panel uses up/down controls; Quickbar uses grip drag reorder.
- Object Mode, bone, and independent UV selections are not supported.

## Next exact step

Install Witch Tools Dev_v2.6.1 over Dev_v2.6.0 in Blender 4.5. Confirm the Selection Slots section expands and displays Slot 1, then test save/reselect, add, clear, remove, rename, reorder, save/reopen, multi-object behavior, and undo/redo. Quickbar Dev_v1.4.0 does not require replacement for this N-panel-only patch.