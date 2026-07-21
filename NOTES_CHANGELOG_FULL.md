# Blender.Tools Notes Changelog — Full History

## 2026-07-21 — Selection Slots development builds

- Implemented Witch Tools `Dev_v2.6.0` with persistent **Selection Slots** below Curvature Sync.
- Added vertex, edge, face, combined-domain, and multi-object Edit Mode save/reselect using scene records and per-mesh custom element markers.
- Added rename, save/overwrite, reselect, clear, Clear All, add, remove, and reorder controls plus a stable `mesh.wt_selection_slot_*` operator contract.
- Implemented Witch Quickbar `Dev_v1.4.0` with a populated **Select** tab using thin optional invocation of the canonical Witch Tools backend.
- Added responsive slot names, full-name tooltips, rename dialog, all slot actions, grip drag reorder, and a safe unavailable-backend state.
- Converted the five supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD SVGs into packaged transparent 64x64 PNG assets.
- Produced `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`, SHA-256 `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`.
- Produced `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`, SHA-256 `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`.
- Witch Tools static checks passed for 46 Python files; Quickbar static checks passed for 13 Python files and 36 PNG assets.
- Both archives passed ZIP integrity, safe paths, duplicate operator-ID, and package-hygiene checks; no cache or SVG source files were shipped.
- Quickbar synthetic multi-slot layout construction and asset-reference checks passed.
- Blender 4.5 Selection Slots persistence, multi-object, topology-change, undo/redo, and Quickbar overlay/input testing remain pending.
- Created the Selection Slots feature packet and updated Witch Tools/Quickbar state, roadmaps, notes, Quickbar architecture/input/assets/integration, build registry, compatibility, docs index, and umbrella state.
- Preserved all public branches, update URLs, package identities, existing operator namespaces, inherited asset paths, and public release locations.

## 2026-07-21 — Dev_v2.5.2 production collar validation in Blender 4.5

- The user installed Witch Tools `Dev_v2.5.2` in Blender 4.5 and reopened the supplied pre-curvature production collar file.
- The saved A/M/Z anchors and curvature-chain selection were available.
- Curvature Sync Analyze/Apply completed with **Replace Misaligned Column Edges** enabled.
- The user reported that the result worked beautifully, confirming the intended curvature and visible same-slot column topology in the actual Blender 4.5 workflow.
- This closes the primary installed Blender 4.5 production-workflow validation that remained pending after automated Blender Python 5.2.0 LTS testing.
- Interactive undo/redo, formal normals/manifold inspection, and final print-fit/slicer validation remain unreported and pending.
- Updated Curvature Sync state, Witch Tools state, umbrella project state, build registry, compatibility record, and latest/full notes.
- No public branch, Quickbar update destination, package identity, external release link, operator namespace, or asset path changed.

## 2026-07-21 — Witch Tools Dev_v2.5.2 Curvature Sync column repair

- Compared the user-supplied pre/post Curvature Sync collar files and confirmed that the intended curve coordinates and spacing were successful.
- Diagnosed 96 retained pre-existing cross-edges whose endpoints mapped to different canonical slots: 81 on `RIGHT EXTENSION` and 15 on `COLLAR - UPPER.002`.
- Added **Replace Misaligned Column Edges** to Curvature Sync.
- Added strict copied-BMesh preflight for safe two-face interior edges and rejection of boundary, non-two-face, Seam, Sharp, Crease, bevel/custom-data, mixed-material, and mixed-smoothing cases.
- Added native stale-edge dissolution followed by reconstruction of canonical same-slot column edges.
- Preserved the exact Dev_v2.5.1 curvature-coordinate result while correcting correspondence topology.
- Produced `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`, SHA-256 `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`.
- Static parsing passed for 45 Python files; no generated cache files were shipped.
- Registration/unregistration and actual collar processing passed under Blender Python 5.2.0 LTS.
- The actual test processed 26 chains, injected 520 vertices, moved 1,324, replaced 96 misaligned edges, created 975 canonical columns, and left zero unresolved positions.
- Exact vertex-coordinate multiset regression against the successful Dev_v2.5.1 post-curvature file passed.
- No zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced.
- A special-data edge test aborted during copied-BMesh preflight without changing real-mesh topology counts; save/reopen passed.
- Exact Blender 4.5 UI and interactive undo/redo testing remained pending until the production user validation recorded above.
- No public branch, Quickbar update destination, package identity, external release link, or asset path was changed.

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
- Exact Blender 4.5 UI, real collar selection behavior, and interactive undo/redo remained pending.
- No public branch, Quickbar update destination, package identity, external release link, or asset path was changed.

## 2026-07-21 — Witch Tools Dev_v2.5.0 Curvature Sync MVP

- Inspected the supplied Witch Tools Dev_v2.4.0 source and existing Vertex Lock / Protected Edit Zone implementation.
- Implemented Curvature Sync MVP directly in Witch Tools while preserving package identity, operator namespaces, assets, and footer URL behavior.
- Added A/M/Z capture with automatic selection clearing.
- Added circular XY/XZ/YZ fitting, exact middle-axis normalization, equal segment counts per side, multi-chain/multi-object synchronization, missing-vertex injection, and optional shared-face column construction.
- Added copied-BMesh dry-run validation, strict branched/ambiguous selection rejection, shape-key injection protection, unresolved-column reporting, and lock/edit-zone/anchor index remapping.
- Fixed a pre-existing Vertex Locks unregister failure caused by a missing safe RNA-property deletion helper.
- Produced `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`, SHA-256 `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`.
- Tested registration/unregistration, synthetic mismatch repair, protected anchors, invalid selection, actual collar processing, save/reopen, geometry validity, manifold state, and 3D edge-intersection comparison under Blender Python 5.2.0 LTS.
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
