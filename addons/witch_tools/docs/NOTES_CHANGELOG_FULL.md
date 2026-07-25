# Witch Tools Notes Changelog — Full History

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
- Produced `Witch_Tools_Dev_v2_7_0_Align_Selection_Blender_4_5.zip`, SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`.
- Added and locally verified a reproducible Dev_v2.7.0 source snapshot.
- Blender 4.5 interactive/runtime validation remains pending.
- No public branch, package identity, update URL, footer URL, official source path, or release location changed.

## 2026-07-23 — Dev_v2.6.1 isolated source snapshot verification

- Added the development-only snapshot manifest at `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/manifest.json`.
- Replaced the malformed original first Base64 part with four smaller verified parts and removed the superseded file.
- Recorded the exact source ZIP identity: 127,401 bytes, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`.
- Recorded the reconstructed `.tar.xz` identity: 81,400 bytes, SHA-256 `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`.
- Hardened `tools/restore_dev_snapshot.py` to verify the explicit ordered part list, every part size/hash, archive size/hash, safe extraction, package root, file count, byte count, and deterministic source-tree digest.
- Final local reconstruction verification passed for package root `Witch_Tools_Dev`: 60 files, 383,270 bytes, source-tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- This update preserved source only; no Witch Tools runtime behavior changed.
- No public compatibility surface changed.

## 2026-07-21 — Dev_v2.6.1 Selection Slots N-panel expansion hotfix

- User reported Quickbar Dev_v1.4.0 worked correctly in Blender 4.5, while Witch Tools Dev_v2.6.0 showed only the Selection Slots title bar and Clear All control.
- Removed slot initialization from the N-panel draw path.
- Added a safe operator-driven empty-scene Slot 1 fallback.
- Updated Add so empty initialization creates exactly Slot 1.
- Made the Selection Slots title and disclosure arrow both clickable.
- Added per-row draw failure containment so one row cannot blank the complete section.
- Preserved the canonical Selection Slots backend, Quickbar operator contract, package identity, prior tools, and user-validated Curvature Sync implementation.
- Produced `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`.
- All 46 Python files parsed/compiled; 92 operator IDs had no duplicates; ZIP safety/package hygiene passed.
- Simulated populated, empty, expanded, and collapsed N-panel layouts passed; simulated empty-scene initialization passed.
- Exact Blender 4.5 Dev_v2.6.1 validation remains pending.

## 2026-07-21 — Dev_v2.6.0 Selection Slots

- Added **Edit Tools > Selection Slots** immediately below Curvature Sync.
- Added persistent renameable slots for vertex, edge, face, and combined mesh selection modes.
- Added multi-object Edit Mode save/reselect behavior.
- Added save/overwrite, reselect, clear, Clear All, add, remove, rename, and reorder controls.
- Added one automatic Slot 1 and a maximum of 20 slots.
- Added scene slot records with generated UIDs, object references, stored modes/counts, and per-mesh vertex/edge/face integer custom-data markers.
- Added stable `mesh.wt_selection_slot_*` operators for optional Quickbar integration.
- Added responsive N-panel names and LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD native icons.
- Produced `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`, SHA-256 `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`.
- ZIP integrity, safe paths, 46-file Python syntax/compile, duplicate operator-ID, and package-hygiene checks passed.
- Runtime result: Quickbar integration worked in the user test, but the Witch Tools N-panel body failed to expand and was superseded by Dev_v2.6.1.
- Retained the user-validated Dev_v2.5.2 Curvature Sync workflow and preserved public compatibility surfaces.

## 2026-07-21 — Dev_v2.5.2 Blender 4.5 production collar validation

- The user installed Dev_v2.5.2 in Blender 4.5 and reopened the supplied pre-curvature production collar file.
- Curvature Sync Analyze/Apply completed with **Replace Misaligned Column Edges** enabled.
- The user reported that the result worked beautifully, confirming the intended curvature and visible same-slot column topology.
- Interactive undo/redo, formal normals/manifold inspection, and final print-fit/slicer validation remain pending.

## 2026-07-21 — Dev_v2.5.2 Curvature Sync column repair

- Diagnosed and replaced 96 retained pre-existing cross-edges mapped to different canonical column slots.
- Preserved the exact successful curvature coordinates while rebuilding canonical same-slot columns.
- Produced `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`, SHA-256 `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`.
- Automated collar processing, geometry regression, topology checks, special-data preflight cancellation, and save/reopen passed.

## 2026-07-21 — Collar embedded-edge / unsplit-face repair

- Identified eight unambiguous stale-face cases in `Collar_DESIGN_v6 - Copy.blend`.
- Produced a Blender 4.5 exact-file repair script preserving the inserted edge network.

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added ordered A/B/C standalone vertex injection, target-chain inference, projected split, optional C-D face split, preflight, and lock/edit-zone/anchor remapping.
- Produced `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`, SHA-256 `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`.

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Added circular A/M/Z multi-chain and multi-object Curvature Sync, missing-vertex injection, optional column construction, protected-zone integration, and strict preflight.

## 2026-07-20 — Development baseline audit

- Recorded supplied Witch Tools Dev_v2.4.0 as the baseline used for the Dev_v2.5.x/2.6.x line.

## 2026-07-20 — Documentation architecture and baseline recovery

- Established Witch Tools ownership, rules, roadmap, state, notes tracking, and feature packets.
