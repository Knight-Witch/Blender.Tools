# Witch Tools Notes Changelog — Full History

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
- Blender 4.5 Selection Slots runtime, save/reopen, multi-object, topology-change, and undo/redo tests remain pending.
- Retained the user-validated Dev_v2.5.2 Curvature Sync workflow and preserved public branches, URLs, package identity, prior operator IDs, and asset paths.

## 2026-07-21 — Dev_v2.5.2 Blender 4.5 production collar validation

- The user installed Dev_v2.5.2 in Blender 4.5 and reopened the supplied pre-curvature production collar file.
- The saved A/M/Z anchors and curvature-chain selection were available.
- Curvature Sync Analyze/Apply completed with **Replace Misaligned Column Edges** enabled.
- The user reported that the result worked beautifully, confirming the intended curvature and visible same-slot column topology in the actual production workflow.
- This validates the primary installed Blender 4.5 workflow that remained pending after automated Blender Python 5.2.0 LTS tests.
- Interactive undo/redo, formal normals/manifold inspection, and final print-fit/slicer validation remain unreported and pending.
- No public branch, Quickbar URL, package identity, operator namespace, asset path, update destination, or public release location changed.

## 2026-07-21 — Dev_v2.5.2 Curvature Sync column repair

- Compared the user-supplied pre/post Curvature Sync collar files.
- Confirmed that the Dev_v2.5.1 circular fit and vertex redistribution were correct.
- Diagnosed 96 retained pre-existing cross-edges mapped to different canonical column slots: 81 on `RIGHT EXTENSION` and 15 on `COLLAR - UPPER.002`.
- Added **Replace Misaligned Column Edges** to Curvature Sync.
- Added copied-BMesh preflight that permits only safe two-face interior edges and rejects boundary, non-two-face, Seam, Sharp, Crease, bevel/custom-data, mixed-material, and mixed-smoothing cases.
- Added native stale-edge dissolution and canonical same-slot column reconstruction.
- Preserved the exact Dev_v2.5.1 successful curve-coordinate result while correcting topology correspondence.
- Produced `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`, SHA-256 `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`.
- Static parsing passed for all 45 Python files; no generated cache files were shipped.
- Blender Python 5.2.0 LTS registration/unregistration passed.
- The actual collar test processed 26 chains, injected 520 vertices, moved 1,324, replaced 96 misaligned edges, created 975 canonical columns, and reported zero unresolved positions.
- Exact vertex-coordinate multiset regression against the Dev_v2.5.1 post-curvature file passed.
- No zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced.
- A marked special-data edge caused copied-BMesh preflight cancellation without real-mesh topology changes; save/reopen passed.
- Exact Blender 4.5 UI and interactive undo/redo remained pending until the production user validation recorded above.
- No public branch, Quickbar URL, package identity, operator namespace, asset path, or update destination changed.

## 2026-07-21 — Collar embedded-edge / unsplit-face repair

- Inspected `Collar_DESIGN_v6 - Copy.blend` after manual vertex and edge insertion.
- Identified eight unambiguous stale-face cases represented by zero-face wire edges whose endpoints belonged to exactly one existing face: two on `COLLAR - UPPER.002` and six on `RIGHT EXTENSION`.
- Produced a Blender 4.5 exact-file repair script that uses the existing edge to split the stale face, preserving the inserted vertices and edge network.
- Added strict baseline object/count validation, transactional temporary-BMesh processing, material and smoothing preservation, normal update, safe output naming, and JSON reporting.
- Added validation preventing new zero-length edges, zero-area faces, duplicate faces, boundary changes, or overlinked-edge-count changes.
- Added optional Windows BAT execution and manual Blender Scripting instructions.
- Added `WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces` to the roadmap for later generalized Witch Tools integration.
- Script syntax and exact-file behavior passed under Blender Python 5.2.0 LTS; Blender 4.5 execution remains pending.
- No Witch Tools package, public branch, operator namespace, asset path, or update URL changed.

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
