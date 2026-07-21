# Blender.Tools Project State

Last updated: 2026-07-21

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Development integration branch: `Blender_Dev`
- Branch origin: `Witch_Quick_Access`
- Default repository branch: `Witch_Main_Tools`
- Default Witch Tools target Blender version: `4.5`

## Current development builds

### Witch Tools

- Current build: `Dev_v2.6.1`
- Artifact: `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Supersedes: `Dev_v2.6.0`
- Target: Blender `4.5.0`
- Hotfix runtime: pending Blender 4.5 user test
- Retained Curvature Sync workflow: user-reported passed in Blender 4.5

### Witch Quickbar

- Current build: `Dev_v1.4.0`
- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Target: Blender `4.5.0`
- Select workflow: user-reported working perfectly in Blender 4.5
- Update destination: unchanged public `Witch_Quick_Access` branch

### Witch's Dev Modules

- Version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Original packaging defect: 34 `.pyc` files

## Last completed work

- Implemented and user-validated the primary Curvature Sync production collar workflow through Dev_v2.5.2.
- Implemented Selection Slots in Witch Tools Dev_v2.6.0 and the Quickbar Select tab in Dev_v1.4.0.
- User reported the Quickbar implementation worked perfectly.
- User reported the Witch Tools Dev_v2.6.0 N-panel showed only the Selection Slots header/Clear All and would not reveal its controls.
- Inspected the current package and produced Dev_v2.6.1:
  - removed slot initialization from `Panel.draw()`;
  - added safe operator-driven Slot 1 initialization;
  - fixed empty Add behavior;
  - made the title/arrow clickable;
  - added row draw failure containment.
- Statically and synthetically audited Dev_v2.6.1.
- Updated feature, Witch Tools, Quickbar, build, compatibility, project-state, and notes documentation.
- Preserved public branches, URLs, package identities, operator namespaces, inherited assets, and release locations.

## Current known-working state

Witch Tools Dev_v2.6.1:

- 46 Python files parse/compile;
- 92 operator IDs have no duplicates;
- ZIP integrity/safe paths/package hygiene passed;
- simulated expanded/collapsed/populated/empty N-panel layouts passed;
- simulated Slot 1 initialization passed;
- package identity and footer URL preserved.

Quickbar Dev_v1.4.0:

- static/package/asset/layout checks passed;
- primary Blender 4.5 Select workflow user-reported passed;
- operator contract remains compatible with Witch Tools Dev_v2.6.1.

Previously verified runtime:

- Dev_v2.5.2 Curvature Sync production collar workflow user-reported passed in Blender 4.5.

## Active problems

1. Witch Tools Dev_v2.6.1 N-panel hotfix requires immediate Blender 4.5 confirmation.
2. Selection Slots save/reselect, save/reopen, multi-object, topology propagation, and undo/redo require broader testing.
3. Quickbar full overlay regression remains pending despite the successful Select workflow.
4. Public/dev side-by-side installation and update-button launch remain untested.
5. Selection markers are persistent custom data rather than immutable topology IDs.
6. Final collar normals/manifold/print-fit inspection remains pending.
7. Canonical source imports and source-derived registries/manifests remain pending.
8. Witch Core source import remains pending.

## Next exact implementation step

1. Install Witch Tools Dev_v2.6.1 over Dev_v2.6.0.
2. Confirm Selection Slots expands and displays Slot 1.
3. Test Save/Reselect on the current collar chain selection, then Add/Clear/Remove/Rename/Reorder.
4. Test save/reopen, multi-object selection, and undo/redo.
5. Keep Quickbar Dev_v1.4.0 installed; no Quickbar replacement is required.
6. Patch only failures found, then import successful sources canonically.

## Test status

- Dev_v2.5.2 Curvature Sync Blender 4.5: user-reported passed
- Quickbar Dev_v1.4.0 Select workflow Blender 4.5: user-reported passed
- Witch Tools Dev_v2.6.0 N-panel: failed to reveal slot rows
- Witch Tools Dev_v2.6.1 static/simulated tests: passed
- Witch Tools Dev_v2.6.1 Blender 4.5: pending
- Selection Slots persistence/multi-object/undo: pending
- Quickbar full overlay regression: pending
- Public branches/URLs modified: no

## Known remaining issues

Dev_v2.6.1 and Quickbar Dev_v1.4.0 remain development builds. The Quickbar Select workflow is user-validated; the Witch Tools N-panel hotfix is ready for immediate user validation.