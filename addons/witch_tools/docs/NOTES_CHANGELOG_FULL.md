# Witch Tools Notes Changelog — Full History

## 2026-08-07 — Dev_v2.9.0 Precision Edit

- Added Coordinate Copy, Planar Edit, and Inject New source candidate documentation.
- Added a full `precision_edit` feature packet with specification, decisions, state, roadmap, acceptance criteria, and Blender 4.5 topology-aware test plan.
- Documented Coordinate Copy Global/Local conversion, XYZ masks, independent target behavior, geometry-frame Location/Rotation/Scale semantics, multi-object support, protection preflight, and default `Ctrl+Shift+C` Apply shortcut.
- Documented Plane Lock persistent object-local axis constraints and Level exact per-target world coordinate assignment.
- Documented Inject New Solo/Branch/Slide behavior, global XYZ movement, straight captured Rail endpoints, vertex-only Slide edge insertion, Branch edge-only connections, modal commit/cancel, and protection-system coordination.
- Preserved the existing A/B/C Auto-Aligned Edge / Vertex Inject as a separate repair workflow.
- Updated the Edit Tools runtime order and the top-level Witch Tools roadmap/project state.
- Recorded that Witch Dock/Quickbar remains deferred until the canonical Witch Tools backend passes Blender 4.5 validation.
- Recorded an inherited documentation gap: the Dev_v2.8.0 roadmap references `/docs/features/align_selection/`, but that directory is absent on the source branch. No historical files were fabricated.
- Target Blender remains 4.5. Blender runtime/UI/modal/undo/save-reopen validation is pending because no Blender executable is available in the implementation environment.

## 2026-08-05 — Dev_v2.8.0 Align Vertices / Edges / Faces

- Added a four-step Guided Align workflow under Edit Tools.
- Added persistent parent-anchor capture from vertex, edge, face, and mixed selections with Active Element and Median references.
- Added world X/Y/Z matching with disabled coordinates preserved.
- Added editable arbitrary-angle Custom Guide points, selection capture, parent-to-start copy, custom-frame matching, and line projection.
- Added free movement, straight captured rails, one-to-all and paired-by-rail mapping, rigid shape preservation, whole/per-island grouping, rail clamping, and Vertex Lock safety.
- Added non-mutating Analyze and transaction-first Apply.
- Added strict cancellation for stale captures, curved/zero rails, impossible constraints, ambiguous rail pairing, multiple shape keys, locked targets, and invalid transforms.
- Re-established direct unpacked development source from the verified Dev_v2.6.1 snapshot because the committed Dev_v2.7.0 parts are truncated and cannot reconstruct the documented Dev_v2.7.1 source.
- Recorded artifact `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip`, 138,473 bytes, SHA-256 `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`.
- Python parse/compile, identifier uniqueness, UI-state consistency, pure constraint math, patch reconstruction, and ZIP/package validation passed.
- Blender 4.5 UI, real-mesh execution, undo/redo, and persistence remain pending.
- Witch Dock/Quickbar source was not modified.

## 2026-07-24 — Dev_v2.7.1 Align Selection N-panel rendering hotfix

- User test showed an empty box at the Align Selection position in Witch Tools while the local Quickbar controls rendered.
- Diagnosed a missing `show_edit_align_selection` Boolean declaration in `WitchToolsPreferences`; the property existed in the UI-state registry and panel, causing the draw path to stop at the disclosure header.
- Registered the missing persistent preference and changed the section icon from invalid/unverified `ALIGN` to valid `PIVOT_ACTIVE`.
- Preserved all Align Selection backend behavior, operator IDs, scene-property contracts, and Quickbar integration.
- Recorded that the user-tested replacement Dev_v2.7.0 ZIP differed from the earlier repository snapshot identity; Dev_v2.7.1 superseded both documented artifact identities.
- Static parse/compile, operator-ID, UI-state consistency, icon-reference, ZIP integrity, safe-path, package-hygiene, and source-patch checks passed.
- Exact Blender 4.5 N-panel and runtime validation remained pending.
- Quickbar source was not updated on GitHub.

## 2026-07-24 — Dev_v2.7.0 Align Selection

- Added a canonical Witch Tools Align Selection backend and N-panel section in the delivered development artifact.
- Added persistent Source and Target Anchor capture, world-axis coordinate matching, and shape-preserving translation.
- Added whole-selection/per-island and multi-object planning.
- Blender 4.5 runtime validation remained pending.
- Later source audit found the committed snapshot parts were truncated and could not reconstruct this source tree.

## 2026-07-23 — Dev_v2.6.1 isolated source snapshot verification

- Added the development-only snapshot manifest and hardened reconstruction verification.
- Final local reconstruction passed for the verified complete source tree.
- This became the recovery baseline for Dev_v2.8.0.

## 2026-07-21 — Dev_v2.6.1 Selection Slots N-panel expansion hotfix

- Removed slot initialization from the N-panel draw path.
- Added safe empty-scene Slot 1 initialization, title/arrow interaction, and row draw containment.
- Exact Blender 4.5 validation remained pending.

## 2026-07-21 — Dev_v2.6.0 Selection Slots

- Added persistent renameable saved mesh selections and thin Quickbar integration.
- Quickbar worked in user testing; Witch Tools N-panel required Dev_v2.6.1.

## 2026-07-21 — Dev_v2.5.2 Blender 4.5 production collar validation

- User reported the corrected Curvature Sync result worked beautifully.

## 2026-07-21 — Dev_v2.5.2 Curvature Sync column repair

- Replaced misaligned existing cross-edges and rebuilt canonical columns while preserving successful curvature coordinates.

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added standalone A/B/C vertex injection and face-splitting support.

## 2026-07-21 — Dev_v2.5.0 Curvature Sync MVP

- Added circular multi-chain and multi-object topology repair and correspondence injection.

## 2026-07-20 — Development baseline audit and architecture

- Recorded supplied baselines and established Witch Tools ownership, rules, roadmap, state, notes, and feature packets.
