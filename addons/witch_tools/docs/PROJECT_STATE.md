# Witch Tools Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit
- Default target Blender version: 4.5
- Development package identity: `Witch_Tools_Dev`
- Development branch: `Blender_Dev`

## Current development build

- Version: `Dev_v2.6.1`
- Artifact: `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`
- SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Supersedes: `Dev_v2.6.0`
- Package folder: `Witch_Tools_Dev`
- Declared Blender target: `4.5.0`
- Python source files: 46
- PNG assets: 6
- Generated cache files: none
- Static syntax/package audit: passed
- Exact Blender 4.5 hotfix runtime: pending user test

Dev_v2.6.1 was produced from Dev_v2.6.0 without changing package identity, existing operator identifiers, assets, Selection Slots storage format/operator contract, or the Witch Tools footer URL.

## Current implementation

Dev_v2.6.1 retains:

- persistent Selection Slots backend for vertex/edge/face/mixed and multi-object Edit Mode selections;
- `mesh.wt_selection_slot_*` operator integration used by Quickbar Dev_v1.4.0;
- Auto-Aligned Vertex Inject;
- user-validated Curvature Sync and Replace Misaligned Column Edges;
- Vertex Lock / Protected Edit Zone integration;
- all existing Dev_v2.x panels and workflows.

Dev_v2.6.1 fixes the Selection Slots N-panel:

- removes slot initialization/mutation from `Panel.draw()`;
- adds an operator-driven empty-scene Slot 1 fallback;
- prevents the fallback Add action from creating Slot 1 and Slot 2 together;
- makes the title and disclosure arrow both clickable;
- contains per-row draw errors so one row cannot blank the section.

## Last completed work

- User reported Quickbar Dev_v1.4.0 worked correctly in Blender 4.5.
- User reported Witch Tools Dev_v2.6.0 showed the Selection Slots title/Clear All but no expandable body.
- Inspected the Dev_v2.6.0 package and isolated unsafe draw-path initialization as a failure risk.
- Implemented and packaged Dev_v2.6.1.
- Updated package changelog, quick start, README, notes, compatibility, feature state/roadmap/test plan, build registry, and project state.

## Current known-working state

Previously verified:

- Dev_v2.5.2 Curvature Sync production collar workflow passed in the user's Blender 4.5 environment.
- Quickbar Dev_v1.4.0 Select workflow was user-reported working.

Dev_v2.6.1 validation completed outside Blender:

- all 46 Python files parse and compile;
- 92 operator IDs scanned with no duplicates;
- ZIP integrity and safe paths passed;
- no generated cache files shipped;
- simulated N-panel layout passed for expanded, collapsed, populated, and empty states;
- simulated Add behavior creates exactly Slot 1 from an empty scene and Slot 2 on the next Add;
- package root and footer URL remain unchanged.

## Active problems

1. Dev_v2.6.1 N-panel expansion and row interaction require immediate Blender 4.5 validation.
2. Selection Slots save/reselect, save/reopen, multi-object, topology propagation, and undo/redo remain incompletely tested.
3. Full Quickbar overlay regression remains pending despite the user-reported successful Select workflow.
4. Hidden/unavailable saved objects are not forcibly unhidden.
5. Linked objects sharing one Mesh datablock share marker layers.
6. Full canonical source import and source-derived registries remain pending.
7. Final collar normals/manifold/print-fit inspection remains pending independently of Selection Slots.

## Next exact implementation step

Install Dev_v2.6.1 over Dev_v2.6.0 in Blender 4.5. Expand Selection Slots and verify Slot 1 appears. Test Save and Reselect on the current collar edge selection, then test Add, Clear, Remove, rename, reorder, save/reopen, multi-object selection, and undo/redo. Quickbar Dev_v1.4.0 does not need to be replaced for this patch.

## Files changed in Dev_v2.6.1

Runtime:

- `panel_edit_tools.py`
- `operators_selection_slots.py`
- `state.py`
- `__init__.py`

Package documentation:

- `CHANGELOG.md`
- `NOTES_CHANGELOG.md`
- `NOTES_CHANGELOG_FULL.md`
- `README.md`
- `SELECTION_SLOTS_QUICK_START.md`
- `Blender_Version_Compatability.md`

## Test status

- ZIP integrity/safe paths: passed
- Python syntax/compile: passed for 46 files
- Duplicate operator IDs: passed
- Simulated populated/empty/collapsed N-panel layout: passed
- Simulated empty-scene initialization: passed
- Blender 4.5 Dev_v2.6.1 runtime: not performed
- Save/reopen and multi-object behavior: pending
- Interactive undo/redo: pending
- Public release/update behavior: unchanged and not retested

## Known remaining issues

Dev_v2.6.1 is a development hotfix. The N-panel failure mechanism has been removed and the package is statically/synthetically validated, but the corrected UI must be confirmed in Blender 4.5.