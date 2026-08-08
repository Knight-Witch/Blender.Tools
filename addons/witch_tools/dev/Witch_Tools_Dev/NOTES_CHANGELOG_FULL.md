## 2026-08-08 — Dev_v2.10.0 Magnetic Mesh Editing

- Added Inject New Magnetic Snap, Auto-Merge, multi-axis movement, multi-edge Slide and MMB navigation.
- Added Magic Branch Single/Persistent Vertex/Edge/Face drag-and-drop building with Paver/Organic face modes.
- Added Edge Doctor regrouping/two-edge L repair and preference-backed Edit Tools reordering.
- Added shared drag/snap/topology modules and Dev_v2.10 Blender 4.5 packaging.
- Added/updated feature specs, decisions, state, roadmaps, UI map, quick starts, acceptance criteria and Blender test plans.
- Runtime Blender 4.5 validation remains pending; static Python syntax compilation passed for the authored candidate modules.

## 2026-08-07 — Dev_v2.9.0 Precision Edit

- Added Coordinate Copy with Global/Local space, XYZ masks, Location/Rotation/Scale geometry-frame behavior, exact source capture, independent target application, multi-object world conversion, protection preflight, and `Ctrl+Shift+C` Apply.
- Added Planar Edit with persistent object-local Plane Lock axes and exact per-target world-space Level.
- Added Inject New with Solo/Branch/Slide, global XYZ movement, captured straight Rail endpoints, Vertex/Edge/Face Solo/Branch sources, and vertex-only edge-splitting Slide.
- Preserved the existing A/B/C Edge / Vertex Inject repair workflow as a separate tool.
- Added protection-system coordination, step-based compact UI, hover help, Precision Edit quick start, repository feature packet, acceptance criteria, roadmap/state, and Blender 4.5 test plan.
- Bumped development metadata to Dev_v2.9.0 targeting Blender 4.5.
- Runtime Blender 4.5 UI/mesh/modal/undo/save-reopen validation remains pending; no Blender executable was available in the implementation environment.

## Dev_v2.8.0 — Guided Align

- Added the step-based **Align Vertices / Edges / Faces** Edit Tools section.
- Captures a parent vertex/edge/face anchor, supports subordinate vertex/edge/face selections, and matches only explicitly enabled world or custom-frame coordinates.
- Added arbitrary guide start/end editing and capture, guide-frame matching, and projection onto a custom line.
- Added straight captured slide rails, one-to-all and paired-by-rail parent mapping, rigid relative-shape preservation, whole-selection/per-island grouping, rail clamping, and Vertex Lock safety.
- Added non-mutating Analyze and transaction-first Apply planning.
- Source recovery note: implemented from the verified Dev_v2.6.1 source because the committed Dev_v2.7.0 snapshot parts do not match their manifest and cannot reconstruct the documented Dev_v2.7.1 build.
- Static and pure-math validation passed; Blender 4.5 runtime validation remains pending.

## 2026-07-21 — Dev_v2.6.1 Selection Slots N-panel hotfix

- User reported that Quickbar Selection Slots worked, while the Witch Tools N-panel showed only the section header and Clear All and would not reveal its rows.
- Removed draw-time slot initialization from `panel_edit_tools.py`; Blender panel draw code now reads existing rows only.
- Added a safe operator-driven `Create Slot 1` fallback when a scene has no initialized rows.
- Made the title text and disclosure arrow both clickable.
- Added row-level error containment so one row cannot blank the full section.
- Updated the Add operator so an empty scene initializes Slot 1 without accidentally creating Slot 2.
- Produced Dev_v2.6.1 for Blender 4.5; static and simulated layout tests passed, exact Blender 4.5 runtime validation pending.

## 2026-07-21 — Dev_v2.5.2 Misaligned Column Repair

## 2026-07-21 — Dev_v2.6.0 Selection Slots

- Added Selection Slots under Edit Tools directly below Curvature Sync.
- Added persistent scene slots backed by mesh vertex/edge/face custom layers.
- Added renameable names, overwrite, reselect, clear, remove, add, Clear All, and reorder controls.
- Added multi-object Edit Mode selection capture and restoration of the stored mesh-selection mode.
- Added canonical operators for optional Quickbar integration without duplicating the selection backend.
- Added quick-start documentation.
- Static syntax/package validation passed; Blender 4.5 runtime and interactive undo behavior remain untested.


- Diagnosed the actual collar result: Curvature Sync placed every vertex correctly, but retained 96 pre-existing cross-edges whose endpoints mapped to different canonical slots. Those stale edges became diagonal after redistribution while the tool added new correct columns.
- Added **Replace Misaligned Column Edges** to Curvature Sync.
- Added safe preflight classification for two-face interior cross-edges and strict rejection of unsafe boundaries or special edge/face data.
- Added native BMesh dissolve-and-reconnect repair so stale diagonal columns are replaced by canonical same-slot columns.
- Added Analyze and Apply report counts for misaligned/replaced columns.
- Tested against `Collar_PRE-curvature_sync.blend`: 26 chains, 26 segments per side, 520 injected vertices, 1,324 moved vertices, 96 replaced misaligned edges, 975 created column edges, and zero unresolved positions.
- Confirmed the repaired result uses the exact same vertex coordinates as the user-approved Dev_v2.5.1 curvature result.
- Confirmed no zero-length edges, zero-area faces, duplicate edges, duplicate faces, or boundary-count changes were introduced.
- Confirmed failure on a special-data edge occurs during copied-BMesh preflight with no real-mesh topology-count change.
- Exact Blender 4.5 UI and interactive undo/redo remain pending.

## Dev_v2.5.0 — Curvature Sync MVP

## 2026-07-21 — Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added ordered A/B/C single-vertex injection.
- Added target-chain inference from A using B-to-C row direction and straightest continuation.
- Added projected target-edge split with tolerance and existing-vertex reuse.
- Added optional/default C-D face connection and split.
- Added copied-BMesh preflight, shape-key rejection, degenerate-face validation, and lock/anchor index remapping.
- Added Edit Tools UI and quick-start documentation.
- Synthetic runtime validation passed under Blender Python 5.2.0 LTS; Blender 4.5 interactive undo/redo remains untested.


- Implemented multi-chain, multi-object circular curvature repair.
- Added A/M/Z capture with automatic selection clearing.
- Added exact middle-axis normalization while preserving A/Z transition anchors.
- Added equal per-side segment counts, missing-vertex injection, and shared-face column connection.
- Added dry-run validation and safe cancellation for branched or ambiguous topology.
- Added Vertex Lock, Protected Edit Zone, and anchor-index remapping support.
- Fixed Vertex Locks unregister cleanup.
- Static parsing passed for the complete add-on package.
- Blender 5.2.0 LTS runtime tests passed for registration/unregistration and the tested Curvature Sync operations.
- A real collar test processed 21 selected chains across two objects, injected 480 vertices, moved 1,113 vertices, created 747 column edges, and preserved the lower object's manifold state; 41 non-connectable column positions were reported rather than forced.
- Exact Blender 4.5 runtime and interactive undo/redo testing remain outstanding.

Dev_v2.4.0
- Added a dedicated Object Snap subsection under Edit Tools using the AREA_JOIN_DOWN icon.
- Vertex mode translates the full target object or disconnected island from target vertex to source vertex.
- Edge mode translates midpoint-to-midpoint and can optionally align edge direction plus adjacent-face normals.
- Face mode translates center-to-center and can optionally align target/source face normals.
- Orientation matching defaults to opposing normals; the compact direction control can switch to same-direction normals.
- Separate-object snaps move the active edit-mode mesh object. Same-object snaps move only the disconnected target island.

Dev_v2.3.8
- Fixed missing WindowManager workspace state props used by Mode Switcher runtime.
- Synced version labels to Dev_v2.3.8.

Dev_v2.3.6
- Fixed Mode Switcher Cycle runtime import error.
- Fixed Last Used toggle behavior for switcher modes/workspaces.

Dev_v2.3.2
- Expanded the footer into Cycle Settings / Hotkeys / Links.
- Added persistent footer subsection state and persistent mode-cycle toggles.
- Hooked Mode Switcher Cycle to the saved cycle-mode settings.
- Added in-panel keymap editing access for important hotkeys.
- Added external link buttons for GitHub, Patreon, Ko-fi, Nexus, and PayPal.
- Removed an unused legacy footer helper and ran a small stale-reference/health check pass.

## Dev_v2.3.1
- Moved the minimal/restore layout toggle out of the footer and into the Mode Switcher header as an icon-only control.
- Swapped the expand/collapse icons so collapsed state shows expand and expanded state shows collapse.
- Changed the minimal-view hotkey registration to the global Window keymap so Ctrl+Alt+Tab works more reliably.
- Removed the duplicate footer minimal/restore button.


## Dev_v2.3.0 — Phase B persistence and minimal view
- Moved collapsible subsection UI state into addon preferences so it persists across Blender restarts and addon updates.
- Added Weight Transfer subsection collapses for Single Transfer and Batch Transfer.
- Added a hotkeyable Minimal View toggle that collapses Witch Tools into a compact state and restores the previous expanded layout.
- Added a footer button for Minimal View / Restore Layout.
- Added default keymaps for Minimal View toggle in 3D View and Image Editor: Ctrl+Alt+Tab.
- Added minimal-view support across workflow panels and kept Mode Switcher/Footer available while compacted.
- Cleaned UI-state dead code out of Scene properties and centralized it in addon preferences.

Dev_v2.2.1
- Finalized the intended default top-level module order and first-install collapse behavior.
- Split Export Tools and Troubleshooting Tools into separate workflow sections.
- Updated Body Tools to RNA and Hair Tools to the strands/curves object icon.
- Reworked Weight Tools iconography and layout clustering for transfer and mirror controls.
- Updated the UV mode button to switch into the UV Editing workflow.
- Health check pass: fixed addon metadata/version mismatch, removed cache artifacts, and syntax-checked the package.

Dev_v2.1.0
- Stable dev package/update stream setup (`Witch_Tools_Dev`) so future dev installs can overwrite the existing dev addon without uninstalling first.
- Removed shipped `__pycache__` artifacts.
- Removed unused UI helper functions and an unused tooltip topic.
- Updated Preferences labels/order to match the current module layout and cleaned addon metadata.

Dev_v2.0.11
- Reduced aggressive field widths in Quick Modifiers and related rows.
- Tightened head-tool and vertex-lock label/field balance.

Dev_v2.0.10
- Tightened field widths and spacing in Quick Modifiers, Head Tools, and Weight Transfer.
- Added Y rotation plus X/Y/Z axis toggles and a shared Apply Rotation action in Batch Object Tools.
- Reworked Vertex Locks guard row and simplified lock action button layout.

Dev_v2.0.9
- UI standardization pass for Vertex Locks, Weight Mirror, and Quick Modifiers.
- Stopped relying on the problematic full-width icon+text button pattern for the worst offenders.
- Rebuilt grouped rows around tighter labels, fields, and split controls.

- Dev_v2.0.3: Cleanup/stabilization pass. Removed shipped __pycache__ artifacts, pruned stale unused help-topic entries, deduplicated the shared Mode Switcher panel draw path, and added active-mode highlighting to the Mode Switcher in both View3D and Image Editor.
- v13.1.10: Tightened Auto Mirror spacing by adding explicit gaps between the Edit/Weight icons and their button groups and widening the space around the divider.
- v13.1.7: Rebuilt Auto Mirror into compact split-style 2-button and 3-button rows with tighter icon spacing and a full-width Auto label.
v13.1.6
- Fixed Auto Mirror draw break caused by invalid topology icon id.
- Restored topology toggle and full Weight row rendering by switching back to the valid grid icon.

v13.1.5
- Fixed the Auto Mirror panel regression where the topology toggle and full Weight row were not rendering.
- Rebuilt the row layout from the last known good structure and kept ORTHO for topology, GROUP_VERTEX for groups, compact X buttons, and tighter Auto spacing.

# NOTES CHANGELOG FULL

## v12.0.0
- Rebuilt Witch Tools as a new segmented package instead of continuing the old patch chain.
- Preserved the visible UI layout while replacing the internal plumbing.
- Kept the major tool sections: Mode Switcher, Auto Mirror, Vertex Snap, Weight Transfer, Modifiers, Batch Tools, Armature Tools, and Weight Mirror.
- Kept Blender-native right-click shortcut assignment instead of a custom popup system.
- Reduced runtime coupling by isolating Weight Paint session handling into dedicated runtime and handler modules.

## v13.0.0
- Reorganized the addon into stable top-level categories instead of individual tool panels.
- Added Vertex Mode to the Mode Switcher.
- Folded Batch Tools into Modifier Tool.
- Folded Vertex Locks into Edit Tools.
- Added Head Tools split into Prep / Editing / Finishing.
- Added Remove Unused Vertex Groups to Weight Tools.
- Removed `__pycache__` artifacts from the shipped package.

## v13.1.1.1
- Added Blender_Version_Compatability.md with target-version and confirmed-version tracking.
- Tightened top-level section headers with per-section icons and trailing help buttons.
- Condensed Auto Mirror rows and moved Auto onto the weight row.
- Expanded Shrinkwrap controls and added multi-object add/apply support.

## v13.1.2
- Auto Mirror rows spaced out and button widths controlled.
- Topology uses an icon button.
- Vertex-group mirror uses the GROUP_VERTEX icon button.

## v13.1.3
- Tightened Auto Mirror icon-to-button spacing to match the addon's normal row spacing.
- Replaced the incorrect topology icon with the ORTHO grid icon.
- Reduced the X button widths and tightened the Auto button so the row stays compact and left-justified.

v13.1.4
- Rebuilt the Auto Mirror row layout so both Edit and Weight rows render again in Blender 4.5.
- Kept the controls left-justified with tighter icon spacing, compact X buttons, ORTHO for topology, and a tighter Auto button.

- v13.1.8: rebuilt Auto Mirror row spacing so the mirror rows stay left-justified with tighter segment widths and a wider Auto button.- v13.1.9: Reworked Auto Mirror into a single left-justified row with tighter icon spacing, a compact divider, and a cleaner grouped Edit/Weight layout.

## v13.1.11
- Increased Auto Mirror spacing again between the Edit/Weight icons and their button groups.
- Increased divider padding so the separator sits farther from topology while keeping the one-row grouped layout.

## v13.2.0
- Strict refactor / cleanup / stabilization pass.
- Split panel UI into section-specific modules instead of keeping every major section in one shared panel file.
- Removed parent category `?` icons from the top-level section headers.
- Reorganized shared property definitions by tool family for cleaner targeted updates.
- Simplified registration so panels are pulled from a dedicated panel manifest.
- Reorganized addon preferences into clearer sections.
- Removed `__pycache__` artifacts from the shipped package.

- Dev_v2.0.0: Added nested collapsible tool sections for Modifier Tool, Edit Tools, and Weight Tools, plus a footer version row with a preferences link. Switched the addon to the new dev versioning baseline.

## Dev_v2.0.1
- Reworked the Mode Switcher for the next module-work phase.
- Removed the `RMB shortcuts` line from the panel.
- Expanded the mode strip to include Sculpt, Texture Paint, Vertex Paint, and UV mode buttons.
- Replaced the old Vertex button behavior with real Vertex Paint.
- Made the mode icons larger, centered, and responsive to N-panel width with a capped growth range.
- Added a proper tooltip description to Pose in Weight Paint.

- Dev_v2.0.2: Hotfix for the install-blocking `PANEL_CATEGORY` import error introduced in Dev_v2.0.1. Restored the missing constant in `state.py` so the refactored section panel modules can import cleanly in Blender 4.5.

Dev_v2.0.4
- Reordered modules, renamed Modifier Tool to Quick Modifiers, moved the footer to the bottom, and updated Edit Tools help/tooltip behavior for Vertex Snap and Vertex Locks.


## Dev_v2.0.5
- Standardized left-justified icon + title rows across panel subsection headers.
- Tightened icon/text alignment for icon-bearing buttons in Edit Tools / Vertex Locks.
- Repacked without __pycache__ artifacts.


## Dev_v2.0.5
- Standardized left-justified icon + title rows across panel subsection headers.
- Tightened icon/text alignment for icon-bearing buttons in Edit Tools / Vertex Locks.
- Repacked without __pycache__ artifacts.

Dev_v2.0.6
- Fixed stale Mode Dock gizmo binding from removed `wtm.switch_vertex_mode` to `wtm.switch_vertex_paint_mode`.

Dev_v2.0.7
- Global UI spacing cleanup for compact icon/text buttons and tighter field alignment.
- Weight Mirror control row rebuilt with grouped -X/+X, Tolerance, and Center Epsilon controls.

Dev_v2.0.8
- Tightened inline label/field spacing helpers.
- Reworked Vertex Locks button layout.
- Added dedicated footer panel.

Dev_v2.0.12
- Vertex Locks cleanup pass: reordered the tool into collapsible subsections for core controls, Protected Edit Zone, Groups, Sculpt Protection, and Shape Mirror.
- Groups now auto-reveal after Create Edit Zone, the search/filter row stays visible at the top, and the list stays compact and scrollable.
- Updated Guard, Sculpt Mask, Create Edit Zone, Select Editable Interior, and Shape Mirror buttons/icons, and removed the Breast Edit Zone default.

Dev_v2.2.0
- Added new workflow panel modules: Body Tools, Armour Tools, Hair Tools, Armature Tools, Shape Key Tools, and Export & Troubleshooting Tools.
- Reordered the default module layout to match the planned long-term workflow structure.
- Moved Cleanup / Armature out of Weight Tools into the new Armature Tools section.
- Expanded preferences scaffolding to mirror the new top-level architecture.

Dev_v2.2.2
- Tightened Weight Tools label/field widths so source/target selectors and batch dropdown rows stop covering their labels.
- Tightened the Vertex Locks Protected Edit Zone name row and Shape Mirror direction/max-distance rows to match the cleaner Head Tools-style field balance.
Dev_v2.2.3: tightened Vertex Locks inline field widths for Name and Max Match Distance.

Dev_v2.2.5
- Rebuilt Vertex Locks Name and Max Match Distance rows to use fixed-width field cells so the labels remain fully visible.

Dev_v2.2.7
- Updated Head Tools button text/icons for Prep, Editing, and Finishing.
- Moved Fix Armature & Ears and Fix Head Seam Normals into the Editing subsection so Finishing stays isolated to LOD/export cleanup.


- Dev_v2.2.7: Fixed Head Tools opening expanded by default by giving the top-level panel the same default-closed behavior as the other workflow modules. Improved the UV Editing mode switcher path to look for UV workspaces more flexibly and configure a UV editor when switching.

Dev_v2.2.8
- Fixed UV Editing switch to use a real workspace/editor path.
- Added fallback UV editor creation from an existing non-3D area.
- Corrected version metadata mismatch in __init__.py.

## Dev_v2.3.3
- Footer links now use the uploaded custom icon assets for GitHub, Ko-fi, PayPal, Nexus, and Website.
- Footer links were reordered to GitHub, Patreon, Ko-fi, PayPal, Nexus, Website.
- Footer link buttons now sit at the top of the footer and are no longer inside a collapsible Links section.

Dev_v2.3.4
- Footer icon row enlarged, website icon swapped to cropped emblem, mode switcher preferences button centered, floating mode dock preference/gizmo removed.

Dev_v2.3.5
- Footer social buttons enlarged, Patreon custom icon added, and embossed hover/click state enabled.

Dev_v2.3.7
- Fixed the Mode Switcher row rendering failure caused by the UV button icon enum.
- Added a safe fallback in mode-switcher button drawing so a bad icon cannot blank the whole row.

Dev_v2.3.12
- Minimal View now hides non-dashboard panels and redraws the UI immediately.

Dev_v2.3.14
- Minimal View now leaves workflow section title bars visible instead of hiding the panels completely.
