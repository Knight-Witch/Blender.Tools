## Dev_v2.10.1
- Target authoring version: Blender 4.5
- Additional Blender versions tested for this candidate: none
- User runtime baseline: Dev_v2.10.0 was tested in Blender 4.5 and exposed merge/navigation/undo issues addressed in this hotfix; the hotfix itself is not runtime-retested yet
- Static/source validation: full package Python syntax parse passed after the fix pass
- Runtime retest required: multi-edge Edge Solo/Branch, all-contact Auto-Merge/target-edge subdivision, Paver overlap merge, Paver Z wall growth, Magic Branch ON/OFF and selection-mode switching, modifier MMB navigation, Object Snap Undo
- Notes: Bugfix candidate only; no public release/Quickbar changes.

## Dev_v2.10.0
- Target authoring version: Blender 4.5
- Additional Blender versions tested for this candidate: none
- Static/source validation: authored candidate modules passed Python syntax compilation
- Runtime verification: not performed; no Blender executable is available in the implementation environment
- Known limitations: GPU hover target drawing, Magnetic Snap/Auto-Merge topology, multi-edge Slide rollback/data preservation, MMB orbit pivot/resume, Persistent Magic Branch Undo, N-panel drag reorder, Undo/Redo and save/reopen require Blender 4.5 validation
- Notes: Expanded Inject New, added Magic Branch, Edge Doctor regrouping/L repair, and preference-backed Edit Tools reordering.

## Dev_v2.9.0
- Target authoring version: Blender 4.5
- Additional Blender versions tested for this candidate: none
- Static/source validation: performed during implementation
- Runtime verification: not performed; no Blender executable is available in the implementation environment
- Known limitations: Coordinate Copy edge/face Rotation/Scale, Plane Lock transform enforcement/persistence, Inject New modal placement/cancel rollback/topology attributes/manifold behavior, undo/redo, and save/reopen require Blender 4.5 validation
- Notes: Added Coordinate Copy, Planar Edit, and Inject New while retaining the Dev_v2.8.0 Guided Align candidate and existing Edit Tools.

## Dev_v2.6.1
- Target authoring version: Blender 4.5
- Static package validation: passed
- Runtime verification: exact Blender 4.5 hotfix validation pending
- Known limitations: selection persistence, multi-object mode switching, and interactive undo remain pending broader user validation
- Notes: Fixed the Selection Slots N-panel expansion/rendering failure while preserving the Dev_v2.6.0 backend and Quickbar integration.

## Dev_v2.5.2
- Target authoring version: Blender 4.5
- Runtime environment tested in this development pass: Blender Python 5.2.0 LTS
- Exact Blender 4.5 runtime: user validation pending
- Static package validation: passed
- Runtime checks performed: registration/unregistration, actual collar correspondence repair, geometry-coordinate regression, topology-degeneracy checks, special-data preflight cancellation
- Known limitation: interactive undo/redo and installed UI behavior were not testable in the background runtime
- Notes: Added safe replacement of misaligned interior column edges while preserving the successful Curvature Sync geometry.

## Dev_v2.5.1
- Target authoring version: Blender 4.5
- Runtime environment tested: Blender Python 5.2.0 LTS
- Exact Blender 4.5 runtime: user validation pending
- Notes: Added Auto-Aligned Vertex Inject and retained Curvature Sync MVP.

## Dev_v2.5.0
- Target authoring version: Blender 4.5
- Runtime environment tested in this development pass: Blender Python 5.2.0 LTS
- Exact Blender 4.5 runtime: not available in the test container; user validation required
- Static package validation: passed for all Python modules
- Runtime checks performed: add-on register/unregister, synthetic Curvature Sync repair, locked-anchor handling, failure without mutation, actual two-object collar repair, save/reopen, topology-degeneracy checks
- Known limitation: background Python could not validate normal interactive Blender undo/redo behavior
- Notes: Added Curvature Sync MVP and fixed Vertex Locks unregister cleanup.

## Dev_v2.4.0
- Target authoring version: Blender 4.5
- Confirmed working versions: Not runtime-confirmed in this packaging pass
- Notes: Added Object Snap for whole-object/disconnected-island Vertex, Edge, and Face alignment with optional orientation matching.

## Dev_v2.3.14
- Target authoring version: Blender 4.5
- Notes: Minimal View now leaves workflow section title bars visible instead of hiding panels entirely.

## Dev_v2.3.8
- Target Blender version: 4.5
- Fixed missing WindowManager workspace properties required by the Mode Switcher runtime.

## Dev_v2.3.6
- Target authoring version: Blender 4.5
- Status: syntax-checked; runtime fix for Mode Switcher Cycle and Last Used behavior

## Dev_v2.3.4
- Target authoring version: Blender 4.5
- Confirmed working versions: not runtime-confirmed in this packaging pass
- Notes: Footer links now use the cropped Knight Witch emblem for website, larger footer icons, centered Mode Switcher Preferences button, floating mode dock preference removed.

## Dev_v2.3.2
- Target authoring version: Blender 4.5
- Confirmed runtime status: not runtime-tested in-container; syntax-checked package
- Notes: Phase 3 footer utilities pass. Added persistent cycle toggles, in-panel keymap editing access, and external link buttons.

## Dev_v2.3.0
- Target authoring version: Blender 4.5
- Confirmed in-container checks: Python syntax check passed for all addon modules.
- Notes: Phase B persistence pass; subsection collapse state now stored in addon preferences, plus Minimal View toggle and restore support.

# Blender Version Compatability

## Current release

- Release: **Dev_v2.10.1**
- Target authoring version: **Blender 4.5**
- Confirmed working versions for this candidate: **No Blender runtime confirmation in this implementation environment**
- Additional Blender versions tested: **None**
- Notes: Dev_v2.10.1 is a runtime bugfix candidate for multi-edge Inject New, all-contact Auto-Merge/edge subdivision, Magic Branch activation/navigation/Paver axis growth, and Object Snap Undo. Blender 4.5 retest is pending.

## Release history

| Release | Target authoring version | Confirmed working versions | Notes |
|---|---|---|---|
| Dev_v2.10.1 | Blender 4.5 | Source/static checks passed; runtime retest pending | Runtime-fix candidate for merge topology, navigation, Magic Branch activation/Paver axis growth, multi-edge Edge sources, and Object Snap Undo. |
| Dev_v2.10.0 | Blender 4.5 | Static Python/source checks only; Blender runtime pending | Magnetic Inject New, Magic Branch, Edge Doctor regrouping/L repair, and reorderable Edit Tools. |
| Dev_v2.9.0 | Blender 4.5 | Static/source checks only; Blender runtime pending | Added Coordinate Copy, Plane Lock/Level, and Inject New Solo/Branch/Slide; retained Guided Align and earlier tools. |
| Dev_v2.8.0 | Blender 4.5 | Static and pure-math checks only; Blender runtime pending | Added Guided Align with world/custom frames, straight slide rails, paired parent mapping, and rigid shape preservation. |
| Dev_v2.6.0 | Blender 4.5 | Quickbar user-reported working; Witch Tools N-panel body failed to expand | Initial Selection Slots build; superseded by Dev_v2.6.1 N-panel hotfix. |
| Dev_v2.5.2 | Blender 4.5 | Blender Python 5.2.0 LTS test runtime; exact 4.5 pending | Added safe replacement of misaligned interior column edges and canonical same-slot reconstruction; actual collar regression passed. |
| Dev_v2.5.1 | Blender 4.5 | Blender Python 5.2.0 LTS test runtime; exact 4.5 pending | Added Auto-Aligned Vertex Inject while retaining Curvature Sync. |
| Dev_v2.5.0 | Blender 4.5 | Blender Python 5.2.0 LTS test runtime; exact 4.5 pending | Added Curvature Sync MVP with multi-object parallel-chain synchronization, vertex injection, optional column construction, protected-zone integration, and strict preflight. |
| Dev_v2.4.0 | Blender 4.5 | Not runtime-confirmed in this packaging pass | Added Object Snap for full objects and disconnected islands with Vertex, Edge, and Face anchors plus optional orientation matching. |
| Dev_v2.2.2 | Blender 4.5 | Not yet runtime-confirmed by user | Tightened Weight Tools source/target selector widths and Vertex Locks field rows so dropdowns stop covering their labels. |
| Dev_v2.2.1 | Blender 4.5 | Not yet runtime-confirmed by user | Finalized default panel structure, split Export/Troubleshooting, updated Weight Tools layout/icons, fixed UV Editing behavior, and ran a cleanup/health check pass. |
| Dev_v2.2.0 | Blender 4.5 | Not runtime-tested in this session | Phase A UI architecture pass. Added Body, Armour, Hair, Armature, Shape Key, and Export & Troubleshooting workflow panels. Moved Cleanup / Armature out of Weight Tools into Armature Tools. |
| Dev_v2.1.0 | Blender 4.5 | Not yet runtime-confirmed by user | Stable dev package/update stream cleanup build. |
| Dev_v2.0.10 | Blender 4.5 | Not yet runtime-confirmed by user | Tightened aggressive label/field widths across the addon, rebuilt Quick Modifiers shrinkwrap and batch rotation layout, and reworked the Vertex Locks guard/action rows. |
| Dev_v2.0.9 | Blender 4.5 | Not yet runtime-confirmed by user | UI standardization pass focused on replacing the worst full-width icon+text button cases with cleaner text-first layouts, tighter grouped fields, and cleaner split controls. |
| Dev_v2.0.3 | Blender 4.5 | Not yet runtime-confirmed by user | Cleanup/stabilization pass. Removed package cache artifacts, pruned stale unused help-topic entries, deduplicated the Mode Switcher panel draw path, and added active-mode highlighting to the Mode Switcher. |
| Dev_v2.0.2 | Blender 4.5 | User reported it installed and ran | Hotfix for the install-blocking `PANEL_CATEGORY` import error introduced in Dev_v2.0.1 after the section-panel refactor. |
| Dev_v2.0.1 | Blender 4.5 | No | Install-blocking import error: missing `PANEL_CATEGORY` constant in `state.py` after the refactor panel split. |
| v13.2.0 | Blender 4.5 | Not yet runtime-confirmed by user | Strict refactor / cleanup / stabilization pass. Split panel drawing into section-specific modules, removed parent title `?` icons, reorganized shared props and preferences, simplified registration, and stripped package cache artifacts. |
| v13.1.11 | Blender 4.5 | Not yet runtime-confirmed by user | Increased Auto Mirror icon spacing again and widened divider padding after v13.1.10 still felt too cramped in Blender. |
| v13.1.10 | Blender 4.5 | Not yet runtime-confirmed by user | Added explicit icon/button spacing and more breathing room around the Auto Mirror divider while keeping the single-row grouped layout. |
| v13.1.9 | Blender 4.5 | Not yet runtime-confirmed by user | Reworked Auto Mirror into one compact row with tighter icon spacing and a divider between Edit and Weight controls. |
| v13.1.8 | Blender 4.5 | Not yet runtime-confirmed by user | Tightened Auto Mirror split-row alignment again after v13.1.7 still showed odd spacing and centering in Blender. |
| v13.1.7 | Blender 4.5 | Not yet runtime-confirmed by user | Rebuilt Auto Mirror rows as compact split-style button groups with tightened spacing and full Auto label width. |
| v13.1.6 | Blender 4.5 | Not yet runtime-confirmed by user | Fixed Auto Mirror panel draw break caused by invalid topology icon id (`ORTHO`). Switched topology back to the valid grid icon so the missing controls render again. |
| v13.1.5 | Blender 4.5 | Not yet runtime-confirmed by user | Fixed the Auto Mirror panel regression where only the Edit X row rendered; restored topology and the full Weight row with compact left-justified controls. |
| v13.1.4 | Blender 4.5 | Not yet runtime-confirmed by user | Rebuilt Auto Mirror row layout after v13.1.3 dropped the Weight row in Blender; restored both rows with tighter icon spacing and compact left-justified controls. |
| v13.1.3 | Blender 4.5 | Not yet runtime-confirmed by user | Auto Mirror row spacing tightened further, topology icon corrected to ORTHO, and compact button widths refined. |
| v13.1.3 | Blender 4.5 | No | Auto Mirror regression: Weight row disappeared in Blender after the spacing rewrite. |
| v13.1.2 | Blender 4.5 | Not yet runtime-confirmed by user | Auto Mirror layout cleanup: spacing, icon toggles, and controlled button widths. |
| v13.1.1 | Blender 4.5 | Not yet runtime-confirmed by user | Hotfix for missing weight-transfer pool helpers that blocked installation in 4.5. |
| v13.1.0 | Blender 4.5 | No | Import error on install: missing `build_source_pool` / `build_target_pool`. |
| v13.0.0 | Blender 4.5 | User reported it installed correctly | Baseline before v13.1 UI/shrinkwrap cleanup pass. |
| Dev_v2.0.0 | Blender 4.5 | Not yet runtime-confirmed by user | Refactor baseline promoted to dev versioning. Added per-tool collapsible sections inside multi-tool modules and a footer version row with a preferences link. |

- Dev_v2.2.3 — Target: Blender 4.5 — Adjusted Vertex Locks Name and Max Match Distance field sizing.
- Dev_v2.2.5 — Target: Blender 4.5 — Rebuilt Vertex Locks Name and Max Match Distance rows to use fixed-width field cells so the labels remain fully visible.
- Dev_v2.2.7 — Target: Blender 4.5 — Updated Head Tools button icons/text and moved Fix Armature & Ears plus Fix Head Seam Normals into Editing.

## Dev_v2.2.8
- Target authoring version: Blender 4.5
- Confirmed working versions: Not yet runtime-confirmed after this patch
- Notes: Fixes UV Editing mode button so it attempts a real UV workspace/editor switch and corrects addon metadata version mismatch.

## Dev_v2.3.1
- Target authoring version: Blender 4.5
- Confirmed runtime status: not runtime-tested in-container; syntax-checked package
- Notes: moved the minimal-view toggle to the Mode Switcher header, swapped collapse/expand icons, and moved the hotkey to the global Window keymap for more reliable activation.

## Dev_v2.3.3
- Target authoring version: Blender 4.5
- Notes: Footer link row reordered and updated to use uploaded custom icon assets where available. Patreon remains on a built-in icon because no Patreon asset was present in the provided files.

## Dev_v2.3.5
- Target authoring version: Blender 4.5
- Confirmed working versions: Blender 4.5 (not runtime-tested in container; packaged for user testing)
- Notes: Footer social buttons enlarged, Patreon custom icon added, embossed hover state enabled.

## Dev_v2.3.7
- Target authoring version: Blender 4.5
- Fix: repaired the Mode Switcher row not drawing by replacing the UV icon enum and adding a safe icon fallback.

| Dev_v2.3.12 | Blender 4.5 | Untested beyond package validation | Fixed Minimal View button so collapse visibly hides non-dashboard panels and forces redraw. |

## Witch Tools Dev_v2.5.1 — Vertex Inject + Curvature Sync

- Intended Blender target: 4.5.0
- Static syntax validation: passed
- Blender Python 5.2.0 LTS registration/unregistration: passed
- Synthetic Auto-Aligned Vertex Inject topology test: passed
- Blender 4.5 interactive UI and undo/redo: not yet tested
- Known limitation: runtime test environment differs from intended Blender 4.5 target
