# Witch Tools Notes Changelog — Latest Update

## 2026-08-05 — Dev_v2.8.0 Guided Align

- Added **Edit Tools > Align Vertices / Edges / Faces** as a four-step guided workflow.
- Added persistent parent-anchor and straight slide-rail captures for vertex, edge, face, and mixed selections.
- Added world XYZ matching with explicit coordinate toggles; disabled coordinates remain unchanged.
- Added arbitrary Custom Guide start/end coordinates, selection capture, anchor-to-start copy, custom-frame matching, and guide-line projection.
- Added free-coordinate movement, captured-rail sliding, one-anchor and paired-by-rail mapping, rigid shape preservation, whole-selection/per-island grouping, rail clamping, and Vertex Lock preflight.
- Added transactional Analyze planning and clear failures for stale captures, impossible rail intersections, ambiguous pairing, curved rails, locked targets, multiple shape keys, and non-invertible transforms.
- Re-established an auditable unpacked development source from the verified Dev_v2.6.1 snapshot because the repository's Dev_v2.7.0 source snapshot is incomplete and cannot be reconstructed from its committed parts.
- Target Blender: 4.5. Python parsing, pure constraint-math tests, operator-ID checks, and package validation passed. Blender 4.5 runtime/UI/undo testing remains pending.
