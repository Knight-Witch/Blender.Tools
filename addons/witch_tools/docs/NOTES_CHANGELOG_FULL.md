# Witch Tools Notes Changelog — Full History

## 2026-07-24 — Dev_v2.7.1 Align Selection N-panel rendering hotfix

- User test showed an empty box at the Align Selection position in Witch Tools while the local Quickbar controls rendered.
- Diagnosed a missing `show_edit_align_selection` Boolean declaration in `WitchToolsPreferences`; the property existed in the UI-state registry and panel, causing the draw path to stop at the disclosure header.
- Registered the missing persistent preference and changed the section icon from invalid/unverified `ALIGN` to valid `PIVOT_ACTIVE`.
- Preserved all Align Selection backend behavior, operator IDs, scene-property contracts, and Quickbar integration.
- Recorded that the user-tested replacement Dev_v2.7.0 ZIP, SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`, differed from the earlier repository snapshot identity; Dev_v2.7.1 supersedes both.
- Produced `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`, SHA-256 `f4783b620325e6c40c156d9aa05e2479ca0e0159b06f4177138b46bbfbc4c110`.
- Static parse/compile, operator-ID, UI-state consistency, icon-reference, ZIP integrity, safe-path, package-hygiene, and source-patch checks passed.
- Exact Blender 4.5 N-panel and runtime validation remains pending.
- Quickbar source was not updated on GitHub.

## 2026-07-24 — Dev_v2.7.0 Align Selection

- Added a canonical Witch Tools Align Selection backend and N-panel section.
- Added persistent Source and Target Anchor capture for vertices, edges, faces, and mixed selections.
- Added Match Coordinates on any X/Y/Z combination in world space.
- Added Move Shape with Whole Selection and Per Selected Island grouping to preserve cavity dimensions and independently align multiple disconnected selections.
- Added multi-object Edit Mode conversion between a shared world-space analysis frame and object-local coordinates.
- Added strict preflight for unavailable or stale captures, island-anchor omissions, enabled Vertex Locks, multiple shape keys, and invalid transforms.
- Added pure helper and synthetic planning tests for coordinate matching, component translation, distance preservation, and lock cancellation.
- Added local-only Quickbar Dev_v1.5.0 exposure through thin Witch Tools operator/property calls.
- Added the Align Selection feature packet and `ALIGN_SELECTION_QUICK_START.md`.
- Blender 4.5 interactive/runtime validation remained pending.
- No public compatibility surface changed.

## 2026-07-23 — Dev_v2.6.1 isolated source snapshot verification

- Added the development-only snapshot manifest and hardened reconstruction verification.
- Final local reconstruction passed for 60 files, 383,270 bytes, source-tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- No public compatibility surface changed.

## 2026-07-21 — Dev_v2.6.1 Selection Slots N-panel expansion hotfix

- Removed slot initialization from the N-panel draw path.
- Added safe empty-scene Slot 1 initialization, title/arrow interaction, and row draw containment.
- Exact Blender 4.5 validation remained pending.

## 2026-07-21 — Dev_v2.6.0 Selection Slots

- Added persistent renameable saved mesh selections and thin Quickbar integration.
- Quickbar worked in user testing; Witch Tools N-panel required Dev_v2.6.1.

## 2026-07-21 — Dev_v2.5.2 Blender 4.5 production collar validation

- User reported the corrected Curvature Sync result worked beautifully.

## 2026-07-21 — Dev_v2.5.2 Curvature Sync column repair

- Replaced 96 misaligned existing cross-edges and rebuilt canonical columns while preserving successful curvature coordinates.

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added standalone A/B/C vertex injection and face-splitting support.

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Added circular multi-chain and multi-object topology repair and correspondence injection.

## 2026-07-20 — Development baseline audit and architecture

- Recorded supplied baselines and established Witch Tools ownership, rules, roadmap, state, notes, and feature packets.
