# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Update: Witch Tools Dev_v2.5.2 Curvature Sync column repair

- Compared the user-supplied `Collar_PRE-curvature_sync.blend` and `Collar_POST-curvature_sync.blend` files.
- Confirmed that Dev_v2.5.1 produced the intended circular curvature and vertex spacing.
- Diagnosed the remaining diagonal topology as 96 pre-existing cross-edges whose endpoints mapped to different canonical column slots: 81 on `RIGHT EXTENSION` and 15 on `COLLAR - UPPER.002`.
- Added **Replace Misaligned Column Edges** to Curvature Sync.
- Added copied-BMesh preflight that accepts only safe two-face interior edges and rejects boundary, non-two-face, Seam, Sharp, Crease, bevel/custom-data, mixed-material, and mixed-smoothing cases before real mutation.
- Added stale-edge dissolution followed by canonical same-slot column reconstruction.
- Packaged `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip` with SHA-256 `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`.
- Updated Curvature Sync state/roadmap, Witch Tools state/roadmap, build registry, compatibility records, package documentation, and latest/full notes.

## Testing

Using Blender Python `5.2.0 LTS`:

- complete package syntax and registration/unregistration passed;
- the actual pre-curvature collar processed 26 chains at 26 segments per side;
- 520 vertices were injected and 1,324 moved;
- 96 misaligned existing column edges were replaced;
- 975 canonical column edges were created;
- zero column positions remained unresolved;
- resulting vertex-coordinate multisets exactly matched the successful Dev_v2.5.1 curvature result;
- no zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced;
- special-data rejection occurred during copied-BMesh preflight without real-mesh topology-count changes;
- save and reopen passed.

## Public compatibility

No public branch, Quickbar update destination, package identity, existing operator namespace, external release link, or asset path was changed.

## Testing limitation

Exact Blender 4.5 installation, panel rendering, interactive selection, and undo/redo remain pending user validation. The uploaded pre/post collar files were not overwritten.