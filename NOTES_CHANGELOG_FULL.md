# Blender.Tools Notes Changelog — Full History

## 2026-07-21 — Witch Tools Dev_v2.6.1 Selection Slots N-panel hotfix

- User reported Quickbar Dev_v1.4.0 worked perfectly in the tested Selection Slots workflow.
- User reported Witch Tools Dev_v2.6.0 displayed only the Selection Slots header and Clear All control and would not reveal its rows.
- Inspected the Dev_v2.6.0 package and removed slot initialization from `Panel.draw()` so UI drawing no longer mutates Scene data.
- Added safe operator-driven Slot 1 initialization for empty scenes and corrected Add so it does not create Slot 2 during initial setup.
- Made the section title and disclosure arrow both clickable.
- Added row-level draw failure containment.
- Produced `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`.
- Static parsing/compile passed for 46 files; 92 operator IDs had no duplicates; ZIP safety/package hygiene passed.
- Simulated populated, empty, expanded, and collapsed N-panel layouts and empty-scene Slot 1 initialization passed.
- Exact Blender 4.5 Dev_v2.6.1 confirmation remains pending.
- Quickbar Dev_v1.4.0 remains the current integration build and does not require replacement.
- Updated Selection Slots feature state/roadmap/test plan, Witch Tools/Quickbar state and notes, build registry, compatibility, umbrella project state, and latest/full notes.
- No public branch, update URL, package identity, operator namespace, inherited asset path, or public release location changed.

## 2026-07-21 — Selection Slots development builds

- Implemented Witch Tools `Dev_v2.6.0` with persistent **Selection Slots** below Curvature Sync.
- Added vertex, edge, face, combined-domain, and multi-object Edit Mode save/reselect using scene records and per-mesh custom element markers.
- Added rename, save/overwrite, reselect, clear, Clear All, add, remove, and reorder controls plus a stable `mesh.wt_selection_slot_*` operator contract.
- Implemented Witch Quickbar `Dev_v1.4.0` with a populated **Select** tab using thin optional invocation of the canonical Witch Tools backend.
- Added responsive slot names, full-name tooltips, rename dialog, all slot actions, grip drag reorder, and a safe unavailable-backend state.
- Converted the supplied SVGs into packaged transparent PNG assets.
- Produced Dev_v2.6.0 and Quickbar Dev_v1.4.0 artifacts and passed static/package/layout checks.
- Runtime result: Quickbar Select workflow user-reported passed; Witch Tools N-panel required the Dev_v2.6.1 hotfix above.

## 2026-07-21 — Dev_v2.5.2 production collar validation in Blender 4.5

- The user installed Witch Tools Dev_v2.5.2, ran Curvature Sync with misaligned-column replacement, and reported that the corrected production collar result worked beautifully.

## 2026-07-21 — Witch Tools Dev_v2.5.2 Curvature Sync column repair

- Diagnosed retained misaligned cross-edges and rebuilt canonical same-slot columns while preserving the successful curvature coordinates.

## 2026-07-21 — Witch Tools Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added standalone A/B/C vertex injection and face-splitting support.

## 2026-07-21 — Witch Tools Dev_v2.5.0 Curvature Sync MVP

- Added circular multi-chain/multi-object topology repair and correspondence injection.

## 2026-07-20 — Supplied development baseline audit

- Audited Witch Tools Dev_v2.4.0, Quickbar Dev_v1.3.18, and Dev Modules Dev_v0.0.9 artifacts.

## 2026-07-20 — Development architecture and non-breaking repository organization

- Established repository rules, documentation, architecture boundaries, migration safeguards, build tracking, and feature packets on `Blender_Dev`.