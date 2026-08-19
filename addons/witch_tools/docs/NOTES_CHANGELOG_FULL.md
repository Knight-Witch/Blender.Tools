Date: 2026-08-18

## Dev_v2.11.4 — exact 3D Print Toolbox Analyze bridge

- User retesting in Blender 5.0.1 confirmed the Dev_v2.11.3 STL export hotfix now creates the STL successfully.
- The same `_CAP 3` retest proved the locally reimplemented Analyze backend still disagreed with the installed original 3D Print Toolbox: Toolbox Non-flat 98 / Overhang 79 versus Witch Tools Non-flat 73 / Overhang 80; the remaining displayed fields matched on that fixture.
- Removed Witch Tools' parallel Analyze detector instead of attempting another local algorithm rewrite.
- Witch Tools `Check All` now invokes the installed 3D Print Toolbox `mesh.print3d_check_all` operator directly and mirrors that extension's live report.
- In Edit Mode, non-empty selectable Witch Tools result buttons invoke the original Toolbox `mesh.print3d_select_report` with the original live report index, restoring the exact Toolbox selection pipeline.
- Analyze no longer substitutes Witch Tools thresholds, BMesh/BVH checks, normal calculations, thickness rays, or an alternate detector fallback. If the Toolbox backend/report is unavailable, Analyze fails explicitly.
- Analyze therefore deliberately depends on the 3D Print Toolbox extension being installed/enabled. Transform, STL Export, Clean & Repair, and other Witch Tools functionality remain independent.
- Added Dev_v2.11.4 version metadata, compatibility/build contracts, project/feature state, roadmaps, UI map, spec, decisions, test plan, and changelogs.
- Primary runtime target remains Blender 5.0.1; Blender 4.5 remains secondary compatibility.
- Runtime gate: original Toolbox and Witch Tools must display identical counts on `_CAP 3`, then their Edit Mode result buttons must select the exact same elements.

Date: 2026-08-18

## Dev_v2.11.3 — STL export reliability hotfix

- Blender 5.0.1 runtime testing exposed that the integrated Export STL button could produce no expected file/result after a folder was selected.
- Source inspection found the exporter did not validate Blender's operator return status or verify an output file before reporting success; the exact Blender-side reason for cancellation/failure remains runtime-unknown.
- Added folder/selection validation, current native STL operator result/file validation, legacy operator compatibility attempt, and a self-contained binary STL fallback.
- The fallback exports selected evaluated meshes with modifiers, world transforms, triangulation, and negative-transform winding correction and uses a temporary file before replacing the destination.
- Export failures now report explicit details rather than silently appearing successful.
- The simple folder + Export STL UI and fixed STL format remain unchanged.
- Dev_v2.11.2 Analyze parity correction remains included and pending runtime parity retest.
- Updated source versioning, user changelog, project/feature state, test/compatibility/build documentation, and packaging validation for Dev_v2.11.3.
- Primary target remains Blender 5.0.1; Blender 4.5 remains secondary compatibility target. Runtime export/re-import validation is pending.

Date: 2026-08-18

## Dev_v2.11.2 — 3D Print Toolbox Analyze parity correction

- Blender 5.0.1 runtime comparison on the same `_CAP 3` mesh proved Dev_v2.11.1 Analyze Mesh was not equivalent to Blender's original 3D Print Toolbox.
- Matching fields on the fixture: Non-manifold 0, Bad Contiguous 0, Intersect Faces 0, Shells 1, Zero Faces 0, Zero Edges 0.
- Mismatched fields: original Toolbox Non-flat 98 / Thin 0 / Sharp 0 / Overhang 79 versus Dev_v2.11.1 Witch Tools 73 / 1 / 1 / 80.
- Replaced simplified Analyze approximations with Toolbox-equivalent behavior: original BVH overlap handling, 0.1 mm degenerate threshold, world-transformed 5° distorted-face check, six-sample backwards-ray 1 mm thickness check, signed 160° sharp-edge check, and world-transformed 45° downward-normal overhang check.
- Kept the Analyze threshold/settings UI hidden as requested; standard Toolbox defaults are now backend constants.
- Blender 5.0.1 became the primary Witch Tools development/runtime target. Blender 4.5 remains the secondary compatibility target for BG3 and workflows that still require it; `bl_info` minimum remains 4.5.0 for one-package compatibility testing.
- Updated project/feature state, roadmaps, spec, test plan, decisions, latest/full notes, compatibility documentation, build workflow, and user-visible changelog.
- Dev_v2.11.2 runtime retest is required on the same `_CAP 3` fixture before Analyze click-to-select implementation begins.

Date: 2026-08-18

## Dev_v2.11.1 — Advanced Clean Instant Clean-style restoration

- User review identified that Dev_v2.11.0 had over-condensed the Instant Clean-derived Advanced Clean UI instead of preserving its original interaction model.
- Restored Repair / Manifold / Topology / Normals / Dissolve as individual collapsible child sections with section-header enable toggles and per-section play actions.
- Main Clean runs the enabled sections; each section play action runs only that section, even when that section's global-enable toggle is off. Shift selection-only behavior applies to both paths.
- Restored original-style checkbox/boxed layouts where no redesign had been requested.
- Retained the explicit customizations: Object Data and Make Planar removed, Dissolve last, compact Manifold Remove Non-Manifold toggles, responsive Topology angle/Compare controls, compact Normals Clear Data toggles.
- Added `print3d_transform/DECISIONS.md` and expanded the feature spec/state/roadmap/test plan, global roadmap/UI map/project state, compatibility record, and user-visible changelog.
- Built full installable artifact `Witch_Tools_Dev_v2_11_1_3D_Print_Transform_Blender_4_5.zip`.
- GitHub Actions static/package validation passed; independent ZIP integrity and SHA-256 verification passed.
- Artifact SHA-256: `d6ecf1b893c1d619fc5974ec0ca1836fe7333abd4b9c5724ff497b63859c2441`.
- Candidate advanced to `Dev_v2.11.1`, target Blender remains `4.5.0`; runtime validation pending. User reference screenshots show Blender 5.0.1 but no Witch Tools 5.0.1 compatibility claim is made yet.

Date: 2026-08-18

## Dev_v2.11.0 — 3D Print Tools + Transform integration

- Corrected the feature baseline from the stale Dev_v2.9.0 precision-edit branch to the current Dev_v2.10.1 Magic Branch source.
- Added top-level Transform below Mode Switcher with object Location/Rotation/Scale and selected-mesh local Location editing.
- Added top-level 3D Print Tools above Edit Tools with simplified STL Export, consolidated Analyze Mesh counts, Make Manifold, Auto Fix, and Advanced Clean.
- Preserved Dev_v2.10.1 Magic Branch, Inject New, Edge Doctor, Object Snap, Edit Tools ordering, and current registration contracts.
- Added/updated `print3d_transform` specification, state, roadmap, acceptance criteria, and Blender 4.5 topology-aware test plan.
- Recorded click-to-select Analyze results as a required follow-up after detector/count parity is validated against Blender's original 3D Print Toolbox.
- Target Blender remains 4.5.0; Dev_v2.11.0 runtime validation is pending.

Date: 2026-08-08

## Dev_v2.10.1 — Blender 4.5 runtime-fix documentation

- Recorded Dev_v2.10.0 user runtime results and the exact failing merge/navigation/undo cases.
- Patched canonical Witch Tools Inject New/Magic Branch topology integration, navigation/activation, Paver axis growth, and Object Snap Undo.
- Updated Precision Edit and Magic Branch specs, decisions, states, roadmaps and regression tests.
- Candidate: `Dev_v2.10.1`, target Blender `4.5.0`; runtime retest pending.

## 2026-08-08 — Dev_v2.10.0 Magnetic Mesh Editing

- Added Inject New Magnetic Snap, Auto-Merge, multi-axis movement, multi-edge Slide and MMB navigation.
- Added Magic Branch Single/Persistent Vertex/Edge/Face drag-and-drop building with Paver/Organic face modes.
- Added Edge Doctor regrouping/two-edge L repair and preference-backed Edit Tools reordering.
- Added shared drag/snap/topology modules and Dev_v2.10 Blender 4.5 packaging.
- Added/updated feature specs, decisions, state, roadmaps, UI map, quick starts, acceptance criteria and Blender test plans.
- Runtime Blender 4.5 validation remains pending; static Python syntax compilation passed for the authored candidate modules.

# Witch Tools Notes Changelog — Full History

## 2026-08-07 — Dev_v2.9.0 Precision Edit

- Added Coordinate Copy, Planar Edit, and Inject New source candidate documentation.
- Added a full `precision_edit` feature packet with specification, decisions, state, roadmap, acceptance criteria, and Blender 4.5 topology-aware test plan.
- Documented Coordinate Copy Global/Local conversion, XYZ masks, independent target behavior, geometry-frame Location/Rotation/Scale semantics, multi-object support, protection preflight, and default `Ctrl+Shift+C` Apply shortcut.
- Documented Plane Lock persistent object-local axis constraints and Level exact per-target world coordinate assignment.
- Documented Inject New Solo/Branch/Slide behavior, global X/Y/Z movement, straight captured Rail endpoints, vertex-only Slide edge insertion, Branch edge-only connections, modal commit/cancel, and protection-system coordination.
- Preserved the existing A/B/C Auto-Aligned Edge / Vertex Inject as a separate repair workflow.
- Updated the Edit Tools runtime order and the top-level Witch Tools roadmap/project state.
- Completed the final source-contract audit for registration/property/operator/UI/keymap identifier wiring and feature-branch ancestry/diff scope; no reviewed identifier mismatch was found.
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
