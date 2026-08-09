## Dev_v2.10.1 — Runtime topology/navigation hotfix

- Inject New Edge Solo/Branch now accepts one or more selected edges as one rigid source set. Multi-edge Slide remains supported.
- Fixed Branch Auto-Merge so commit evaluates every created vertex, not only the single hovered magnetic endpoint. Coincident vertices weld; created vertices landing inside an existing edge subdivide that target edge first and weld into the inserted vertex.
- Prevented modifier navigation from resetting the temporary Inject/Magic Branch orbit pivot; only plain MMB during a live drag assigns the live geometry as the orbit pivot. Shift/Ctrl/Alt+MMB remain Blender navigation.
- Added explicit Magic Branch ON/OFF state and hotkeyable toggle; Persistent now controls stay-armed behavior rather than acting as the tool's only activation control.
- Magic Branch Vertex/Edge/Face buttons now switch Blender to the corresponding mesh selection mode through an undoable operator candidate.
- Paver can grow out of the source face plane when the enabled movement axes require it; e.g. Z-only can build a vertical wall from a horizontal face while retaining source tile depth.
- Paver/Organic/Vertex/Edge Auto-Merge now evaluates all supported overlapping created vertices at commit, including non-hovered contacts, and splits existing target edges at interior contacts rather than leaving an unsplit overlapping edge.
- Added an explicit Object Snap undo push because Blender 4.5 runtime testing showed Object Snap changes were not entering the undo history reliably.
- User runtime validation on Dev_v2.10.0 confirmed hover highlighting, magnetic snapping, Inject New Undo/Redo, Paver, Organic, and tested Organic magnetic vertex merge behavior.
- Dev_v2.10.1 remains a Blender 4.5 test candidate: the fixes above are source/static validated here but require user runtime retest.

## Dev_v2.10.0 — Magnetic Mesh Editing / Magic Branch

- Expanded Inject New with independent multi-axis X/Y/Z placement, Magnetic Snap vertex/edge/face highlighting, Branch Auto-Merge, multi-edge Slide, and MMB orbit around live injection geometry.
- Added shared drag/snap and topology backends used by both Inject New and Magic Branch.
- Added Magic Branch with Single/Persistent, Vertex/Edge/Face, Paver/Organic, magnetic placement, Auto-Merge, and a dedicated hotkeyable Persistent toggle.
- Reorganized repair tools under Edge Doctor: Missing Vertex / Edge Injector, Alignment Fixer, and Curvature Sync. Added two-edge L repair while preserving the existing A/B/C solver.
- Added persistent preference-backed Edit Tools reordering with drag grip, arrow fallback, and Reset Default.
- Added Dev_v2.10.0 packaging configuration for Blender 4.5.
- Static Python compilation passed for authored candidate modules. Blender 4.5 registration, GPU hover drawing, modal interaction, topology/attribute behavior, MMB pivot, Persistent Undo, reorder dragging, Undo/Redo, and save/reopen remain untested in the implementation environment.

## Dev_v2.9.0 — Precision Edit

- Added **Edit Tools > Coordinate Copy** above Vertex Snap with Global/Local coordinate type, X/Y/Z masks, Location/Rotation/Scale toggles, vertex/edge/face source capture, exact independent target application, and multi-object world-space conversion for meshes with different origins/transforms.
- Added default `Ctrl+Shift+C` Mesh keymap shortcut for **Apply Copied Coordinates** while retaining Blender-native keymap reassignment.
- Added **Edit Tools > Planar Edit** with persistent per-vertex Plane Lock axis constraints and exact per-target world-space Level behavior.
- Added **Edit Tools > Inject New** directly below Vertex Snap with Solo, Branch, and Slide setup modes; global X/Y/Z placement; arbitrary straight Rail endpoint capture; Vertex/Edge/Face source icons for Solo/Branch; and vertex-only subdivide-like Slide.
- Branch creates corresponding source-to-copy branch edges but does not auto-generate extrusion side faces.
- Preserved the existing **Edge / Vertex Inject** A/B/C auto-aligned repair workflow as a separate tool.
- Added integration with existing Vertex Locks and new Plane Locks so Coordinate Copy/Level preflight protected targets and Inject New suspends/restores guards around modal topology changes.
- Added hover help, step-numbered UI, status/error lines, quick-start documentation, feature specification/decisions/state/roadmap, and a Blender 4.5 topology-aware test plan.
- Development metadata is now `Dev_v2.9.0`, intended for Blender `4.5.0`.
- Source/static validation has been performed during implementation, but Blender 4.5 registration, panel rendering, modal interaction, real-mesh topology behavior, undo/redo, and save/reopen remain untested in the implementation environment.

## Dev_v2.8.0 — Guided Align

- Added the step-based **Align Vertices / Edges / Faces** Edit Tools section.
- Captures a parent vertex/edge/face anchor, supports subordinate vertex/edge/face selections, and matches only explicitly enabled world or custom-frame coordinates.
- Added arbitrary guide start/end editing and capture, guide-frame matching, and projection onto a custom line.
- Added straight captured slide rails, one-to-all and paired-by-rail parent mapping, rigid relative-shape preservation, whole-selection/per-island grouping, rail clamping, and Vertex Lock safety.
- Added non-mutating Analyze and transaction-first Apply planning.
- Source recovery note: implemented from the verified Dev_v2.6.1 source because the committed Dev_v2.7.0 snapshot parts do not match their manifest and cannot reconstruct the documented Dev_v2.7.1 build.
- Static and pure-math validation passed; Blender 4.5 runtime validation remains pending.

## Dev_v2.6.1 — Selection Slots N-panel Expansion Hotfix

- Fixed the Selection Slots N-panel body failing to render after expanding its header.
- Removed scene/slot initialization mutations from `Panel.draw()`.
- Added a safe `Create Slot 1` fallback for legacy or newly created scenes with no initialized slot rows.
- Made both the disclosure arrow and the Selection Slots title clickable.
- Added per-row UI failure containment so one bad row cannot blank the entire section.
- Preserved the Dev_v2.6.0 Selection Slots backend, Quickbar operator contract, and Dev_v2.5.2 Curvature Sync behavior.

## Dev_v2.6.0 — Selection Slots

- Added **Edit Tools > Selection Slots** directly below Curvature Sync.
- Added renameable, persistent save slots for mesh vertex, edge, face, and combined selection modes.
- Added multi-object Edit Mode save/reselect behavior.
- Added overwrite, reselect, clear, delete, add, reorder, and Clear All controls.
- Added responsive slot-name fields that widen with the N-panel.
- Stored selections through per-mesh custom element layers plus scene slot records so they persist in `.blend` files.
- Added the stable `mesh.wt_selection_slot_*` operator family for thin Quickbar integration.

## Dev_v2.5.2 — Misaligned Column Repair

- Added **Replace Misaligned Column Edges** under Edit Tools > Curvature Sync.
- Detects existing interior cross-edges whose endpoints map to different canonical column slots.
- Dissolves only unambiguous two-face interior edges and rebuilds correct same-slot columns.
- Rejects boundary, non-two-face, Seam, Sharp, Crease, bevel/custom-data, mixed-material, or mixed-smoothing edges before mutation.
- Analyze now reports the number of misaligned column edges planned for replacement.
- Applied the patch to the supplied pre-curvature collar file: 96 misaligned edges replaced, 975 canonical column edges created, and zero unresolved columns.
- Preserved the exact Dev_v2.5.1 vertex-coordinate result while removing the stale diagonal correspondence topology.

## Dev_v2.5.1 — Auto-Aligned Vertex Inject

- Added Edit Tools > Edge / Vertex Inject.
- Added ordered A/B/C selection using Blender selection history.
- Added D placement from the `C + (A - B)` relationship projected onto the inferred target edge chain.
- Added strict chain traversal, fork rejection, projection tolerance, and existing-vertex reuse.
- Added default Connect & Split Face behavior.
- Added copied-BMesh preflight before real mesh mutation.
- Preserved existing Vertex Lock, Protected Edit Zone, and Curvature Sync anchor references across injected topology.
- Added shape-key rejection and degenerate-face validation.
- Added `VERTEX_INJECT_QUICK_START.md`.


## Dev_v2.5.0 — Curvature Sync MVP

- Added Edit Tools > Curvature Sync for circular A-to-Middle-to-Z repair across multiple selected parallel edge chains.
- Added multi-object Edit Mode support so aligned upper/lower parts can receive the same symmetrical segment count.
- Added automatic missing-vertex injection by splitting selected curve edges and optional missing column-edge creation through shared faces.
- Added exact middle-axis normalization: the captured Middle vertex chooses the curve apex side and is moved to the fitted circle's mathematical centerline while A and Z remain fixed.
- Added Match Selected Maximum and Custom Per Side segment modes, with equal segment counts on both sides of Middle.
- Added dry-run validation before topology mutation, rejection of branched/closed/ambiguous selections, shape-key injection protection, and unresolved-column reporting.
- Added Vertex Lock / Protected Edit Zone integration: locked A/Z and already-correct Middle anchors may be used, locked interior vertices abort safely, and stored lock/edit-zone/anchor indices are remapped after topology changes.
- Fixed an existing Vertex Locks unregister error caused by a missing safe RNA-property deletion helper.
- Preserved the existing Witch Tools package identity and GitHub footer destination.

## Dev_v2.4.0
- Added Edit Tools > Object Snap with Vertex, Edge, and Face anchor modes.
- Added automatic target scope detection: whole active object for two-object snaps, or the disconnected target mesh island for same-object snaps.
- Added optional Edge/Face orientation matching with opposing-normal default and a same-direction toggle.
- Edge snaps use midpoint-to-midpoint translation; loose edges fall back to edge-direction alignment when no usable adjacent-face normal exists.
- Added the Blender `AREA_JOIN_DOWN` icon to the Object Snap section.

## Dev_v2.3.14
- Fixed Minimal View so workflow panels collapse to title bars instead of disappearing entirely.


## Dev_v2.3.12
- Fixed Minimal View so it now visibly collapses Witch Tools sections by hiding non-dashboard panels and forcing UI redraws.
## Dev_v2.3.8
- Fixed missing WindowManager workspace state properties for Mode Switcher workspace/UV behavior.
- Fixed blank Mode Switcher row caused by repeated AttributeError during draw.
- Synced addon metadata/version labels to Dev_v2.3.8.

## Dev_v2.3.7
- Fixed Mode Switcher row failing to draw by replacing the invalid UV icon enum and adding a safe button-draw fallback.

## Dev_v2.3.6
- Fixed Mode Switcher Cycle by restoring the missing runtime preferences imports.
- Fixed Last Used so it now swaps back to the previously used mode/workspace instead of only restoring non-switcher states.
- Added temporary workspace memory for mode switching so UV/other workspace transitions restore more predictably.

## Dev_v2.3.5
- Replaced the Patreon footer button with the provided Patreon custom icon asset.
- Increased the footer social button row size by roughly 20 percent.
- Enabled embossed footer icon buttons so Blender shows a clearer hover/clickable state.

## Dev_v2.3.4
- Replaced the website footer icon with the cropped Knight Witch emblem asset.
- Increased footer link icon row size to better match the mode switcher button scale.
- Centered the Mode Switcher Preferences button in the footer cycle settings section.
- Removed the non-functional Show floating mode dock preference and unregistered the unused floating dock gizmo system.
- Removed stale footer link state and stripped __pycache__ artifacts from the package.

## Dev_v2.3.2 — Phase 3 footer / quick settings / links
- Expanded the dev footer into a utility panel with Mode Cycle Settings, Hotkeys, and Links subsections.
- Added persistent cycle-mode toggles that now drive the Mode Switcher Cycle behavior.
- Added in-panel keymap editing access for important Witch Tools hotkeys and external link buttons for GitHub, Patreon, Ko-fi, Nexus, and PayPal.
- Removed an unused legacy footer helper and did a quick stale-reference/health check during the pass.


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

## Dev_v2.2.7
- Fixed the Head Tools top-level panel so it defaults closed like the other workflow sections.
- Improved the UV Editing mode switcher path so it tries to switch to a UV workspace and configure a UV editor instead of falling back to plain Edit behavior.

## Dev_v2.2.2
- Tightened Weight Tools label/field widths so source/target selectors and batch dropdowns stop covering their labels.
- Tightened Vertex Locks field rows for Protected Edit Zone name, Shape Mirror direction, and Max Match Distance.

## Dev_v2.2.1
- Finalized the pre-Phase-2 default panel structure: Mode Switcher open, dev footer open, all other top-level sections default-closed on first install.
- Split Export Tools and Troubleshooting Tools into separate top-level panels, updated Body/Hair icons, and moved Weight Tools to its intended default position.
- Reworked Weight Tools layout and icons for Single Transfer, Batch Transfer, Weight Mirror, and compact group-list behavior.
- Updated the UV mode button so it now enters the UV Editing workflow instead of acting like plain Edit Mode.
- Ran a health check pass: fixed the addon metadata/version mismatch, removed shipped cache artifacts, and syntax-checked the full package.

## Dev_v2.2.0
- Phase A UI architecture pass
- Added top-level workflow panels for Body, Armour, Hair, Armature, Shape Key, and Export & Troubleshooting
- Moved Cleanup / Armature out of Weight Tools into Armature Tools
- Reordered the default module layout for future expansion


## Dev_v2.1.0
- Switched the dev addon package to a stable folder/module name (`Witch_Tools_Dev`) so future dev updates can install over the prior dev build without requiring uninstall first.
- Removed shipped `__pycache__` artifacts from the package.
- Pruned stale/unused helper code and an unused tooltip topic.
- Cleaned addon metadata (`author`, version labels) and aligned Preferences labels/order with the current module structure.

## Dev_v2.0.12
- Reworked Vertex Locks into collapsible subsections with a clearer workflow order: core controls, protected edit zone, groups, sculpt protection, then shape mirror.
- Added auto-reveal for the Groups section after creating an edit zone, switched the zone-name default away from Breast Edit Zone, and added a visible group search/filter row with a compact scrolling list.
- Updated Vertex Locks buttons, icons, and toggles for Guard, Sculpt Mask, Create Edit Zone, Select Editable Interior, and Shape Mirror.

## Dev_v2.0.11
- Tightened over-aggressive label/field widths in Quick Modifiers, Head Tools, and Vertex Locks.
- Rebalanced Shrinkwrap rows so Target, Method, Snap, Offset, and Vertex Group stop crowding labels.

## Dev_v2.0.10
- Tightened aggressive label/field widths across Quick Modifiers, Head Tools, and Weight Transfer so fields stop covering their labels.
- Reworked Quick Modifiers shrinkwrap rows for cleaner spacing and replaced the old per-axis rotate rows with one shared X/Y/Z rotation strip plus a full-width Apply button.
- Rebuilt the Vertex Locks guard row into an even Guard / Guard Interval / value layout and simplified the lock action buttons into full-row controls.

## Dev_v2.0.9
- Ran a UI standardization pass to stop mixing incompatible button/layout patterns.
- Switched the most problematic full-width action buttons to cleaner text-first layouts so Blender no longer strands icons on the far left.
- Rebuilt Vertex Locks, Weight Mirror, and Quick Modifiers rows around tighter label/field groupings and cleaner split controls.


## Dev_v2.0.8
- Tightened inline label/field spacing helpers across the addon.
- Reworked Vertex Locks button layout to use full-width centered icon+text buttons where appropriate.
- Added a dedicated footer panel so the dev version row is always visible at the bottom of the addon.


## Dev_v2.0.6
- Fixed stale Mode Dock gizmo binding that still referenced the removed `wtm.switch_vertex_mode` operator.
- Remapped the floating dock button to `wtm.switch_vertex_paint_mode` so install no longer throws the unknown operator traceback.

## Dev_v2.0.4
- Reordered the default module stack to Mode Switcher, Auto Mirror, Edit Tools, Weight Tools, Quick Modifiers, then Head Tools.
- Renamed Modifier Tool to Quick Modifiers and moved the addon footer to the actual bottom of the full tool stack.
- Reworked Vertex Snap help so the title itself carries the tooltip guidance and removed the old how-to dropdown.
- Reworked Vertex Locks help and layout: added title/button tooltips, condensed the guard controls, clarified lock/unlock actions, relabeled the active-group side buttons, and cleaned up Shape Mirror wording.

# Changelog

## Dev_v2.0.3
- Ran a focused cleanup pass on the current dev baseline instead of widening the feature surface.
- Removed stale unused help-topic entries and deduplicated the shared Mode Switcher panel draw logic.
- Added active-mode highlighting to the Mode Switcher so the current mode button is visibly depressed in both the View3D and Image Editor panels.
- Removed shipped `__pycache__` artifacts from the package.

## Dev_v2.0.2
- Fixed the install-blocking import error by restoring `PANEL_CATEGORY` in `state.py` for the refactored section panel modules.
- Kept the Dev_v2.0.1 Mode Switcher changes intact while repairing the package manifest/constants layer.

## Dev_v2.0.1
- Removed the `RMB shortcuts` line from the Mode Switcher.
- Expanded the Mode Switcher to include Sculpt, Texture Paint, Vertex Paint, and UV mode buttons.
- Replaced the old Vertex button behavior with a real Vertex Paint mode button.
- Made the Mode Switcher icon row larger, centered, and width-responsive with a clamp so it stops growing after roughly 2x size.
- Added a tooltip description to the Pose in Weight Paint toggle instead of relying on surrounding helper text.

## v13.2.0
- Ran a strict refactor / cleanup / stabilization pass without changing the toolset surface area.
- Split the sidebar UI into section-specific panel modules so future tool updates can patch one panel without editing a giant shared draw file.
- Removed the parent category `?` icons from the top-level section headers.
- Reorganized shared property definitions by tool family and simplified registration into a cleaner manifest.
- Reorganized addon preferences into clearer sections and stripped `__pycache__` artifacts from the shipped package.

## v13.1.11
- Increased the Auto Mirror icon-to-button spacing again so the Edit and Weight icons no longer feel crowded against their control groups.
- Increased the divider breathing room so the separator sits farther away from the topology button while keeping the single-row layout intact.

## v13.1.10
- Added explicit spacing between the Edit/Weight icons and their button groups in Auto Mirror so the icons no longer sit jammed against the controls.
- Added extra breathing room around the compact divider so the topology segment does not crowd the separator.
- Kept the single-row Auto Mirror layout and compact split-style button groups intact.

## v13.1.9
- Collapsed Auto Mirror into a single left-justified row so Edit and Weight controls sit together instead of floating as separate rows.
- Tightened the spacing around the Edit and Weight icons and added a compact visual divider between the two mirror groups.
- Kept the compact X/icon segments and widened Auto just enough to show the full label cleanly.

- Dev_v2.0.0: Promoted the post-refactor build to the new dev versioning baseline, added per-tool collapsible sections inside multi-tool modules, and added a footer version row with a Witch Tools preferences link.


## Dev_v2.0.5
- Standardized left-justified icon + title rows across panel subsection headers.
- Tightened icon/text alignment for icon-bearing buttons in Edit Tools / Vertex Locks.
- Repacked without __pycache__ artifacts.


## Dev_v2.0.5
- Standardized left-justified icon + title rows across panel subsection headers.
- Tightened icon/text alignment for icon-bearing buttons in Edit Tools / Vertex Locks.
- Repacked without __pycache__ artifacts.

## Dev_v2.0.7
- Tightened global inline icon/text button sizing so icons no longer strand on the far left in wide buttons.
- Reduced label-to-field spacing for pointer, enum, and numeric rows across Edit, Weight, Quick Modifiers, and Head Tools.
- Rebuilt Weight Mirror controls into compact grouped rows with mirror, vertex-group, and prop icons.

## Dev_v2.2.3
- Tightened Vertex Locks Name and Max Match Distance rows so the field widths stop covering their labels.

## Dev_v2.2.5
- Rebuilt the Vertex Locks Name and Max Match Distance rows to use fixed-width field cells so the labels remain fully visible.

## Dev_v2.2.7
- Updated Head Tools button text/icons for Prep, Editing, and Finishing to match the requested visual standards.
- Moved Fix Armature & Ears and Fix Head Seam Normals into Head Tools > Editing so Finishing stays focused on LOD/export cleanup.


## Dev_v2.2.8 — Blender 4.5
- Fixed UV Editing switch so it now attempts a real UV workspace/editor switch instead of only falling back to Edit Mode.
- Added fallback logic to repurpose a non-3D editor area into a UV/Image Editor when no UV workspace is present.
- Fixed addon version metadata mismatch in `__init__.py`.

## Dev_v2.3.3
- Footer links now use the uploaded custom icon assets for GitHub, Ko-fi, PayPal, Nexus, and Website.
- Footer links were reordered to GitHub, Patreon, Ko-fi, PayPal, Nexus, Website.
- Footer link buttons now sit at the top of the footer and are no longer inside a collapsible Links section.
