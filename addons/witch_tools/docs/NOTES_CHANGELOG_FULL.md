# Witch Tools Notes Changelog — Full History

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Inspected the supplied Dev_v2.4.0 source and existing Vertex Lock / Protected Edit Zone implementation.
- Implemented Curvature Sync under Edit Tools without changing the `Witch_Tools_Dev` package identity, existing operator namespaces, assets, or footer link.
- Added explicit A/M/Z capture, automatic selection clearing, circular XY/XZ/YZ fitting, exact middle-axis normalization, equal segment counts per side, multi-chain/multi-object synchronization, missing-vertex injection, and optional shared-face column construction.
- Added copied-BMesh preflight, strict ambiguous/branched selection rejection, shape-key injection protection, unresolved-column reporting, and stored lock/edit-zone/anchor index remapping.
- Fixed the existing Vertex Locks unregister cleanup failure caused by a missing safe RNA-property deletion helper.
- Produced `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`, SHA-256 `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`.
- Added the package changelog entry, README workflow, collar quick-start guide, latest/full notes, and compatibility update.
- Static parsing passed for all 44 Python files; no generated cache files were shipped.
- Blender Python 5.2.0 LTS registration/unregistration, synthetic repair, protected-anchor, invalid-selection, actual collar, save/reopen, geometry-validity, manifold, and 3D intersection comparison tests were performed.
- Exact Blender 4.5 UI and interactive undo/redo testing remain pending.

## 2026-07-20 — Development baseline audit

- Recorded user-supplied `Witch Tools Dev_v2.4.0` as the best available candidate current baseline.
- Recorded artifact `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`, package folder `Witch_Tools_Dev`, Blender target 4.5.0, and archive SHA-256 `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`.
- Added a complete per-file SHA-256 manifest.
- Confirmed archive safety, 43 parseable Python files, 6 PNG assets, and no generated cache files.
- Recorded Object Snap as the current Dev_v2.4.0 addition.
- Located the footer GitHub destination at `Witch_Main_Tools` and documented that it is a direct link rather than a version-comparison system.
- Updated Witch Tools state and repository build/branch/compatibility records.
- Confirmed no Witch Tools runtime source was changed and no Blender runtime test was performed.

## 2026-07-20 — Documentation architecture and baseline recovery

- Established Witch Tools as the canonical owner of general-purpose modeling and topology operators.
- Added local development and mesh-safety rules.
- Recorded that the current Dev_v2.x source baseline was not yet verified in GitHub.
- Added baseline-recovery tasks before new code implementation.
- Added roadmap entries for Auto-Aligned Vertex Inject, manual inject, bulk correspondence repair, protected zones, and Curvature Sync.
- Created the Curvature Sync feature packet.
- Confirmed no Witch Tools source code was modified or tested in this documentation pass.