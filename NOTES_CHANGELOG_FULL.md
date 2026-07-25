# Blender.Tools Notes Changelog — Full History

## 2026-07-24 — Align Selection development builds

- Implemented Witch Tools Dev_v2.7.0 with canonical **Edit Tools > Align Selection**.
- Added Source and Target Anchor capture for vertex, edge, face, and mixed mesh selections.
- Added world-space Match Coordinates and shape-preserving Move Shape on X/Y/Z combinations.
- Added Whole Selection and Per Selected Island grouping, including independent alignment of multiple disconnected cavities.
- Added multi-object world/local conversion and preflight for locks, stale captures, missing anchors, shape keys, and invalid transforms.
- Added a local-only Quickbar Dev_v1.5.0 Edit-tab integration through the canonical Witch Tools operator/property contract.
- Produced Witch Tools artifact SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`.
- Produced Quickbar artifact SHA-256 `d2ace3cd3310686664cebfce6242717af3afed3f5954a4bd3cd6bc2a26eded5c`.
- Static/core/synthetic/package tests passed; Blender runtime remains pending.
- Added the Align Selection feature packet and a verified Witch Tools Dev_v2.7.0 source snapshot.
- Quickbar source was intentionally not committed to GitHub.
- No public compatibility surface changed.

## 2026-07-23 — Witch Tools Dev_v2.6.1 isolated source snapshot verification

- Added a complete development-only manifest for the Witch Tools Dev_v2.6.1 source snapshot on `Blender_Dev`.
- Replaced the malformed original first Base64 part with four smaller verified parts and removed the superseded file.
- Hardened `tools/restore_dev_snapshot.py` to validate parts, archive identity, safe extraction, package root, file count, byte count, and source-tree digest.
- Final reconstruction passed for 60 files, 383,270 bytes, tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- No public compatibility surface changed.

## 2026-07-21 — Witch Tools Dev_v2.6.1 Selection Slots N-panel hotfix

- Removed slot initialization from `Panel.draw()`.
- Added safe operator-driven Slot 1 initialization, corrected initial Add behavior, made title/arrow clickable, and contained row draw failures.
- Produced Dev_v2.6.1 and passed static/synthetic checks; Blender 4.5 confirmation remained pending.
- Quickbar Dev_v1.4.0 remained the current integration build.

## 2026-07-21 — Selection Slots development builds

- Added persistent Selection Slots to Witch Tools Dev_v2.6.0.
- Added a thin Quickbar Dev_v1.4.0 Select tab.
- Quickbar workflow was user-reported successful; Witch Tools N-panel required Dev_v2.6.1.

## 2026-07-21 — Dev_v2.5.2 production collar validation

- User reported the corrected Curvature Sync collar result worked beautifully in Blender 4.5.

## 2026-07-21 — Dev_v2.5.2 Curvature Sync column repair

- Rebuilt misaligned same-slot columns while preserving successful curvature coordinates.

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added standalone A/B/C vertex injection and face splitting.

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Added circular multi-chain/multi-object topology repair and correspondence injection.

## 2026-07-20 — Supplied baseline audit and repository architecture

- Audited Witch Tools Dev_v2.4.0, Quickbar Dev_v1.3.18, and Dev Modules Dev_v0.0.9.
- Established repository rules, architecture boundaries, build tracking, and feature packets on `Blender_Dev`.
