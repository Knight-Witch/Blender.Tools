## 2026-08-08 — Witch Tools Dev_v2.10.1 runtime fix candidate

- Recorded Blender 4.5 user-test results for Witch Tools Dev_v2.10.0.
- Patched canonical Witch Tools topology integration, Magic Branch interaction behavior, Paver axis growth, and Object Snap Undo.
- Updated Witch Tools project/feature/test documentation and Dev_v2.10.1 packaging metadata.
- Public release branches and Witch Quickbar are unchanged. Runtime retest is pending.

# Blender.Tools Notes Changelog — Full History

## 2026-07-24 — Witch Tools Dev_v2.7.1 Align Selection N-panel hotfix

- User test showed Quickbar Align Selection controls but an empty Witch Tools N-panel box.
- Diagnosed the missing `show_edit_align_selection` preference registration and the invalid/unverified `ALIGN` section icon.
- Added the missing persistent preference and changed the icon to `PIVOT_ACTIVE` without changing geometry logic or the Quickbar contract.
- Recorded the discrepancy between the earlier Dev_v2.7.0 snapshot identity and the exact user-tested replacement artifact; Dev_v2.7.1 supersedes both.
- Delivered `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`, 132,189 bytes, SHA-256 `e68cf22a2db2ab426781bf8acfc2bfdbb8d6f1c8f62c42e1ccf166d30d6b467f`.
- Static/compile, operator-ID, UI-state, icon, ZIP, package-hygiene, and source-patch checks passed.
- Blender 4.5 N-panel and runtime validation remains pending.
- Quickbar source remained local-only and unchanged.
- No public compatibility surface changed.

## 2026-07-24 — Align Selection development builds

- Implemented Witch Tools Dev_v2.7.0 with canonical **Edit Tools > Align Selection**.
- Added Source and Target Anchor capture for vertex, edge, face, and mixed mesh selections.
- Added world-space Match Coordinates and shape-preserving Move Shape on X/Y/Z combinations.
- Added Whole Selection and Per Selected Island grouping, including independent alignment of multiple disconnected cavities.
- Added multi-object world/local conversion and preflight for locks, stale captures, missing anchors, shape keys, and invalid transforms.
- Added a local-only Quickbar Dev_v1.5.0 Edit-tab integration through the canonical Witch Tools operator/property contract.
- Static/core/synthetic/package tests passed; Blender runtime remained pending.
- Quickbar source was intentionally not committed to GitHub.
- No public compatibility surface changed.

## 2026-07-23 — Witch Tools Dev_v2.6.1 isolated source snapshot verification

- Added a complete development-only manifest and hardened reconstruction verification.
- Final reconstruction passed for 60 files, 383,270 bytes, tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- No public compatibility surface changed.

## 2026-07-21 — Witch Tools Dev_v2.6.1 Selection Slots N-panel hotfix

- Removed slot initialization from `Panel.draw()` and added safe initialization/title/row safeguards.
