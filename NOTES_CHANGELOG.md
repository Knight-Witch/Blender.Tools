# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-24

## Witch Tools Dev_v2.7.1 — Align Selection N-panel hotfix

- User test showed the Quickbar Align Selection controls but an empty box in the Witch Tools Edit Tools N-panel.
- Diagnosed a missing `show_edit_align_selection` declaration in `WitchToolsPreferences`; the panel and UI-state registry referenced the property, causing the draw path to stop at the section header.
- Added the missing persistent preference and replaced the invalid/unverified `ALIGN` icon with valid `PIVOT_ACTIVE`.
- Preserved the Align Selection backend and Quickbar operator/property contract.
- Produced `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`, 132,053 bytes, SHA-256 `d912536da3d6bd7681ce58a85c3a3099bffc17403fc0233fcb9f93551d67c9e9`.

## Baseline reconciliation

- The exact user-tested replacement Dev_v2.7.0 ZIP had SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`, differing from the earlier repository snapshot identity.
- Dev_v2.7.1 explicitly supersedes both Dev_v2.7.0 identities and records the tested replacement as its patch baseline.

## Testing

- 47 Witch Tools Python files parsed and compiled.
- 96 operator IDs had no duplicates.
- UI-state declaration consistency, invalid icon regression, ZIP integrity, safe paths, package hygiene, and source-patch checks passed.
- Blender 4.5 N-panel confirmation and real Align Selection execution remain pending.

## Quickbar scope

- Quickbar Dev_v1.5.0 was not changed and remains local-only.
- Its missing source-reference dropdown will be handled after Witch Tools is confirmed.
- No public branch, package identity, update URL, inherited asset path, or public release location changed.
