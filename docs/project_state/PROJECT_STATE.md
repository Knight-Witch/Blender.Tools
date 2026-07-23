# Blender.Tools Project State

Last updated: 2026-07-23

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
- Isolated source snapshot: manifest and full reconstruction verification passed on `Blender_Dev`

### Witch Quickbar

- Current build: `Dev_v1.4.0`
- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Target: Blender `4.5.0`
- Select workflow: user-reported working perfectly in Blender 4.5
- Update destination: unchanged public `Witch_Quick_Access` branch
- Isolated source snapshot/import: pending

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
- Produced and statically/synthetically tested Witch Tools Dev_v2.6.1 as the N-panel hotfix.
- Created a development-only Witch Tools Dev_v2.6.1 snapshot under `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/`.
- Added a manifest recording the source ZIP, ordered Base64 parts, reconstructed archive, package root, and deterministic source-tree identity.
- Replaced the malformed first snapshot part with four smaller verified parts.
- Hardened `tools/restore_dev_snapshot.py` and completed final reconstruction verification:
  - reconstructed archive: 81,400 bytes, SHA-256 `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`;
  - extracted package root: `Witch_Tools_Dev`;
  - extracted source: 60 files, 383,270 bytes;
  - tree SHA-256: `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- Preserved public branches, official source paths, URLs, package identities, operator namespaces, inherited assets, and release locations.

## Current known-working state

Witch Tools Dev_v2.6.1:

- 46 Python files parse/compile;
- 92 operator IDs have no duplicates;
- ZIP integrity/safe paths/package hygiene passed;
- simulated expanded/collapsed/populated/empty N-panel layouts passed;
- simulated Slot 1 initialization passed;
- isolated source snapshot reconstruction and source-tree verification passed;
- package identity and footer URL preserved.

Quickbar Dev_v1.4.0:

- static/package/asset/layout checks passed;
- primary Blender 4.5 Select workflow user-reported passed;
- operator contract remains compatible with Witch Tools Dev_v2.6.1.

Previously verified runtime:

- Dev_v2.5.2 Curvature Sync production collar workflow user-reported passed in Blender 4.5.

## Active problems

1. Witch Tools Dev_v2.6.1 N-panel hotfix requires Blender 4.5 confirmation.
2. Selection Slots save/reselect, save/reopen, multi-object, topology propagation, and undo/redo require broader testing.
3. Quickbar full overlay regression remains pending despite the successful Select workflow.
4. Witch Quickbar Dev_v1.4.0 isolated source snapshot/import remains pending.
5. Public/dev side-by-side installation and update-button launch remain untested.
6. Selection markers are persistent custom data rather than immutable topology IDs.
7. Direct unpacked development source layouts and source-derived registries remain pending after snapshot preservation.
8. Final collar normals/manifold/print-fit inspection remains pending.
9. Witch Core source import remains pending.

## Next exact implementation step

1. Complete the isolated Quickbar Dev_v1.4.0 source snapshot and reconstruction verification.
2. Install Witch Tools Dev_v2.6.1 over Dev_v2.6.0 and confirm Selection Slots expands and displays Slot 1.
3. Test Save/Reselect, Add/Clear/Remove/Rename/Reorder, save/reopen, multi-object selection, and undo/redo.
4. Keep Quickbar Dev_v1.4.0 installed; no replacement is required for the Witch Tools N-panel patch.
5. Patch only failures found before official integration.

## Test status

- Dev_v2.5.2 Curvature Sync Blender 4.5: user-reported passed
- Quickbar Dev_v1.4.0 Select workflow Blender 4.5: user-reported passed
- Witch Tools Dev_v2.6.0 N-panel: failed to reveal slot rows
- Witch Tools Dev_v2.6.1 static/simulated tests: passed
- Witch Tools Dev_v2.6.1 source snapshot reconstruction: passed
- Witch Tools Dev_v2.6.1 Blender 4.5: pending
- Selection Slots persistence/multi-object/undo: pending
- Quickbar full overlay regression: pending
- Public branches/URLs modified: no

## Known remaining issues

Dev_v2.6.1 and Quickbar Dev_v1.4.0 remain development builds. Witch Tools source is reproducibly preserved on `Blender_Dev`; Quickbar source preservation remains pending. Neither development source is integrated into an official release path.
