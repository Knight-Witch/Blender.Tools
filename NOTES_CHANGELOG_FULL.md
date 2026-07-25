# Blender.Tools Notes Changelog — Full History

## 2026-07-24 — Witch Tools Dev_v2.7.1 Align Selection N-panel hotfix

- User test showed Quickbar Align Selection controls but an empty Witch Tools N-panel box.
- Diagnosed the missing `show_edit_align_selection` preference registration and the invalid/unverified `ALIGN` section icon.
- Added the missing persistent preference and changed the icon to `PIVOT_ACTIVE` without changing geometry logic or the Quickbar contract.
- Recorded the discrepancy between the earlier Dev_v2.7.0 snapshot identity and the exact user-tested replacement artifact; Dev_v2.7.1 supersedes both.
- Produced Dev_v2.7.1, SHA-256 `f4783b620325e6c40c156d9aa05e2479ca0e0159b06f4177138b46bbfbc4c110`.
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
- Quickbar Dev_v1.4.0 remained the integration build.

## 2026-07-21 — Selection Slots development builds

- Added persistent Selection Slots to Witch Tools and a thin Quickbar Select tab.
- Quickbar workflow passed user testing; Witch Tools N-panel required the hotfix.

## 2026-07-21 — Dev_v2.5.2 production collar validation

- User reported the corrected Curvature Sync collar result worked beautifully in Blender 4.5.

## 2026-07-21 — Dev_v2.5.2 Curvature Sync column repair

- Rebuilt misaligned same-slot columns while preserving successful curvature coordinates.

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added standalone A/B/C vertex injection and face splitting.

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Added circular multi-chain/multi-object topology repair and correspondence injection.

## 2026-07-20 — Supplied baseline audit and repository architecture

- Audited supplied development baselines and established repository rules, architecture boundaries, build tracking, and feature packets on `Blender_Dev`.
