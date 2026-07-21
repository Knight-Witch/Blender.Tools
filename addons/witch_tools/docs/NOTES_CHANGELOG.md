# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v2.5.2 — Curvature Sync column repair

- Compared `Collar_PRE-curvature_sync.blend` and `Collar_POST-curvature_sync.blend`.
- Confirmed that Dev_v2.5.1 produced the intended curve positions and spacing.
- Identified 96 retained pre-existing cross-edges mapped to different canonical slots: 81 on `RIGHT EXTENSION` and 15 on `COLLAR - UPPER.002`.
- Added **Replace Misaligned Column Edges** to the Curvature Sync UI.
- Added strict copied-BMesh preflight that accepts only safe two-face interior edges and rejects boundary, non-two-face, Seam, Sharp, Crease, bevel/custom-data, mixed-material, and mixed-smoothing cases.
- Added stale-edge dissolution followed by canonical same-slot column reconstruction.
- Preserved all existing Vertex Inject and Curvature Sync behavior and the exact successful Dev_v2.5.1 curve-coordinate result.
- Packaged `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`, SHA-256 `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`.
- Updated package README, quick start, user-visible changelog, compatibility record, project state, roadmap, feature documentation, build registry, and root/add-on notes.

## Testing

Using Blender Python `5.2.0 LTS`:

- complete package syntax and registration/unregistration passed;
- actual collar processing completed across 26 chains at 26 segments per side;
- 520 vertices were injected and 1,324 moved;
- 96 misaligned edges were replaced;
- 975 canonical column edges were created;
- zero positions remained unresolved;
- exact vertex-coordinate regression against the successful Dev_v2.5.1 post-curvature file passed;
- no zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced;
- special-data cancellation occurred during preflight without changing the real mesh;
- save/reopen passed.

## Remaining validation

Blender 4.5 installed-package behavior, panel rendering, interactive selection, normal undo/redo, and final production inspection remain pending. No public branch, Quickbar URL, package identity, operator namespace, asset path, or public release location changed.