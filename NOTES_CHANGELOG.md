# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Update: Witch Tools Dev_v2.6.1 Selection Slots N-panel hotfix

- User reported Quickbar Dev_v1.4.0 worked perfectly in the tested Blender 4.5 Selection Slots workflow.
- User reported Witch Tools Dev_v2.6.0 displayed the Selection Slots header/Clear All but would not reveal its slot rows.
- Inspected the current Dev_v2.6.0 package and removed slot initialization from `Panel.draw()`.
- Added safe operator-driven Slot 1 initialization for empty scenes.
- Updated Add so initial creation produces exactly Slot 1.
- Made both the section title and disclosure arrow clickable.
- Added per-row draw failure containment.
- Produced `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`.

## Testing

- 46 Python files parsed/compiled.
- 92 operator IDs scanned with no duplicates.
- ZIP integrity, safe paths, and package hygiene passed.
- Simulated expanded, collapsed, populated, and empty N-panel states passed.
- Simulated Slot 1 initialization passed.
- Exact Blender 4.5 Dev_v2.6.1 validation remains pending.

## Quickbar status

- Quickbar Dev_v1.4.0 does not require replacement; the Witch Tools operator contract is unchanged.
- Full Quickbar overlay regression remains pending despite the user-reported successful Select workflow.

## Public compatibility

No public branch, update destination, package identity, existing operator namespace, inherited asset path, external release link, or public download location changed.