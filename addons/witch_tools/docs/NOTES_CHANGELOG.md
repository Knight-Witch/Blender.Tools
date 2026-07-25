# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-24

## Dev_v2.7.1 — Align Selection N-panel Rendering Hotfix

- User test showed an empty box at the Align Selection position in Witch Tools while the local Quickbar controls rendered.
- Diagnosed the missing `show_edit_align_selection` Boolean property in `WitchToolsPreferences`; the panel and UI-state registry referenced it, so drawing stopped at the section header.
- Registered the missing persistent preference with a default expanded state.
- Replaced the invalid/unverified `ALIGN` section icon with valid `PIVOT_ACTIVE`.
- Preserved all Align Selection geometry logic, operator IDs, property contracts, and Quickbar integration.
- Delivered `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`, 132,189 bytes, SHA-256 `e68cf22a2db2ab426781bf8acfc2bfdbb8d6f1c8f62c42e1ccf166d30d6b467f`.

## Baseline record

- The exact user-tested replacement Dev_v2.7.0 ZIP had SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`, differing from the earlier Dev_v2.7.0 snapshot identity.
- Dev_v2.7.1 explicitly supersedes both Dev_v2.7.0 identities.

## Testing

- 47 Python files parsed and compiled.
- 96 operator IDs had no duplicates.
- UI-state preference/registry consistency passed.
- Invalid Align icon regression check passed.
- ZIP integrity, safe paths, package hygiene, and source patch manifest checks passed.
- Exact Blender 4.5 N-panel rendering and Align Selection runtime remain pending.

## Preserved state

- Quickbar Dev_v1.5.0 is unchanged and remains local-only.
- Public branches, package identity, update URLs, inherited assets, and official release locations remain unchanged.
