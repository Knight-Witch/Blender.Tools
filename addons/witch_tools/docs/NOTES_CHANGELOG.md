# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v2.6.1 — Selection Slots N-panel expansion hotfix

- User reported Quickbar Dev_v1.4.0 worked correctly, while Witch Tools Dev_v2.6.0 displayed only the Selection Slots header and Clear All control.
- Removed `ensure_selection_slots()` from `Panel.draw()` so the N-panel no longer attempts Scene mutation while drawing.
- Added a safe operator-driven `Create Slot 1` fallback for empty legacy/new scenes.
- Updated Add so empty initialization creates exactly Slot 1 rather than Slot 1 plus Slot 2.
- Made both the disclosure arrow and title text toggle the section.
- Added row-level UI failure containment.
- Produced `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`.

## Testing

- Static parsing/compile passed for all 46 Python files.
- Duplicate operator-ID scan passed for 92 identifiers.
- ZIP integrity, safe paths, and package hygiene passed.
- Simulated N-panel layout passed for expanded, collapsed, populated, and empty states.
- Simulated empty-scene Add behavior passed.
- Exact Blender 4.5 hotfix validation remains pending.

## Preserved state

- Selection Slots backend and Quickbar operator contract are unchanged.
- User-validated Curvature Sync remains included.
- No public branch, update URL, package identity, prior operator namespace, asset path, footer URL, or public release location changed.