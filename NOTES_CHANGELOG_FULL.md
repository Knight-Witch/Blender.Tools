# Blender.Tools Notes Changelog — Full History

## 2026-07-21 — Witch Tools Dev_v2.5.1 Auto-Aligned Vertex Inject

- Extended the Curvature Sync MVP build with a standalone Edge / Vertex Inject tool.
- Added click-ordered A/B/C selection and validation that A-B and B-C are real mesh edges.
- Added ideal D calculation from `C + (A - B)` and target-chain inference from A in the B-to-C direction.
- Added straightest-continuation traversal, ambiguous-fork rejection, projected target-edge splitting, projection tolerance, and existing-vertex reuse.
- Added default optional C-D shared-face connection and split.
- Added copied-BMesh preflight, shape-key rejection, zero-area-face validation, and lock/edit-zone/anchor remapping.
- Added Edit Tools UI, `VERTEX_INJECT_QUICK_START.md`, user-visible changelog, compatibility, state, roadmap, and build-registry updates.
- Produced `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`, SHA-256 `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`.
- Static parsing passed for 45 Python files; no generated cache files were shipped.
- Blender Python 5.2.0 LTS registration/unregistration passed.
- Synthetic injection placed D at the exact expected target-edge location and split one quad into two valid faces.
- Curvature Sync synthetic regression passed after the new operator was integrated.
- Exact Blender 4.5 UI, real collar selection behavior, and interactive undo/redo remain pending.
- No public branch, Quickbar update destination, package identity, external release link, or asset path was changed.

## 2026-07-21 — Witch Tools Dev_v2.5.0 Curvature Sync MVP

- Inspected the supplied Witch Tools Dev_v2.4.0 source and existing Vertex Lock / Protected Edit Zone implementation.
- Implemented Curvature Sync MVP directly in Witch Tools while preserving package identity, operator namespaces, assets, and footer URL behavior.
- Added A/M/Z capture with automatic selection clearing.
- Added circular XY/XZ/YZ fitting, exact middle-axis normalization, equal segment counts per side, multi-chain/multi-object synchronization, missing-vertex injection, and optional shared-face column construction.
- Added copied-BMesh dry-run validation, strict branched/ambiguous selection rejection, shape-key injection protection, unresolved-column reporting, and lock/edit-zone/anchor index remapping.
- Fixed a pre-existing Vertex Locks unregister failure caused by a missing safe RNA-property deletion helper.
- Produced `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`, SHA-256 `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`.
- Tested registration/unregistration, synthetic mismatch repair, protected anchors, invalid selection, actual collar processing, save/reopen, geometry validity, manifold state, and 3D intersection comparison under Blender Python 5.2.0 LTS.
- Exact Blender 4.5 UI and interactive undo/redo remained pending.

## 2026-07-20 — Supplied development baseline audit

- Audited user-supplied Witch Tools `Dev_v2.4.0`, Witch Quickbar `Dev_v1.3.18`, and Witch's Dev Modules `Dev_v0.0.9` archives.
- Recorded artifact names, package identities, Blender 4.5 metadata, archive SHA-256 hashes, and complete per-file manifests.
- Confirmed ZIP integrity, safe archive paths, and Python syntax parsing.
- Recorded Dev Modules cache-file and documentation-version defects.
- Located Witch Tools and Quickbar GitHub destinations and confirmed Quickbar only opens its public branch.
- Confirmed no runtime source, public branch, update URL, package identity, operator namespace, asset path, or external release location was changed.

## 2026-07-20 — Development architecture and non-breaking repository organization

- Created `Blender_Dev` from `Witch_Quick_Access` without modifying public branches.
- Established repository rules, source-of-truth hierarchy, documentation system, architecture boundaries, migration safeguards, build tracking, and session handoff requirements.
- Defined Witch Tools, Witch Quickbar, Witch Core, shared backend, Dev module, and use-case ownership.
- Added Curvature Sync specification, state, roadmap, decisions, test plan, and reference cases.
