# Curvature Sync — General Modeling Use Case

Use Curvature Sync when a hard-surface curved region has:

- multiple parallel edge chains with different counts
- flat or uneven arc segments
- missing corresponding vertices or cross-chain edges
- separate objects/islands that should share segmentation

General modeling priorities:

- explicit A/M/Z anchors
- canonical angular column lattice
- preserved profile radii and offsets
- predictable topology and undo
- no generic remesh requirement

The authoritative behavior is defined in `/docs/features/curvature_sync/SPEC.md`.