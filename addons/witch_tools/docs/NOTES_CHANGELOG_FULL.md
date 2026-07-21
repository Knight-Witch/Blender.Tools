# Witch Tools Notes Changelog — Full History

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added ordered A/B/C standalone vertex injection under Edit Tools.
- Added A-B/B-C edge validation and ideal D relation from `C + (A - B)`.
- Added target-chain inference, straightest-continuation traversal, ambiguous-fork rejection, projection tolerance, and existing-vertex reuse.
- Added projected target-edge splitting and optional/default C-D shared-face splitting.
- Added copied-BMesh preflight, shape-key rejection, zero-area-face validation, and lock/edit-zone/anchor remapping.
- Added UI controls and `VERTEX_INJECT_QUICK_START.md`.
- Produced `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`, SHA-256 `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`.
- Static parsing passed for 45 Python files; no generated cache files were shipped.
- Blender Python 5.2.0 LTS registration/unregistration, synthetic vertex injection, C-D face split, and Curvature Sync regression tests passed.
- Exact Blender 4.5 UI, real collar injection, and interactive undo/redo remain pending.

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Inspected the supplied Dev_v2.4.0 source and existing Vertex Lock / Protected Edit Zone implementation.
- Implemented Curvature Sync without changing `Witch_Tools_Dev` identity, existing operator namespaces, assets, or footer link.
- Added A/M/Z capture, circular plane fitting, exact middle normalization, equal segment counts, multi-chain/multi-object synchronization, missing-vertex injection, and optional column construction.
- Added copied-BMesh preflight, strict ambiguous-selection rejection, shape-key protection, unresolved-column reporting, and lock/edit-zone/anchor remapping.
- Fixed the existing Vertex Locks unregister cleanup failure.
- Produced `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`.
- Synthetic and actual-collar harness tests passed under Blender Python 5.2.0 LTS, with unresolved positions reported rather than forced.

## 2026-07-20 — Development baseline audit

- Recorded user-supplied Witch Tools Dev_v2.4.0 as the baseline used for the Dev_v2.5.x line.
- Recorded artifact identity, Blender target, hash, per-file manifest, syntax result, assets, and GitHub footer destination.

## 2026-07-20 — Documentation architecture and baseline recovery

- Established Witch Tools ownership, local rules, mesh-safety requirements, roadmap, state, notes tracking, and the Curvature Sync feature packet.
