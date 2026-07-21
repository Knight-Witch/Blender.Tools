# Witch Quickbar Notes Changelog — Full History

## 2026-07-21 — Dev_v1.4.0 Select tab and Selection Slots integration

- Added a populated `Select` tab to the floating overlay.
- Added compact Selection Slot rows with full-name tooltips, click-to-rename, reselect, save/overwrite, clear, remove, add, header Clear All, and grip drag reorder.
- Added optional thin invocation of Witch Tools Dev_v2.6.0+ `mesh.wt_selection_slot_*` operators instead of duplicating slot scene/mesh data.
- Added a disabled explanatory state when Witch Tools is unavailable.
- Converted and packaged the five supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD SVG icons as transparent 64x64 PNG files.
- Increased gizmo capacity for dynamic rows and tiled responsive name hit targets.
- Produced `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`, SHA-256 `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`.
- Static parsing/compile passed for 13 Python files; all 36 icon mappings resolve; no cache or SVG source files were shipped.
- Synthetic layout construction with multiple slots, Add, Clear All, action hit targets, responsive names, and Select tab passed.
- Blender 4.5 overlay rendering, interaction, dependency integration, drag/reorder, resize, pass-through, file-load recovery, and undo/redo remain pending.
- Preserved the public branch, `Witch_Quick_Access` update URL, package identity, inherited operator IDs, asset paths, and public release location.

## 2026-07-20 — Development baseline audit

- Recorded user-supplied `Witch Quickbar Dev_v1.3.18` as the best available candidate current dev baseline.
- Recorded artifact `witch_quickbar_dev_Dev_v1_3_18_package.zip`, package folder `witch_quickbar_dev`, Blender target 4.5.0, and archive SHA-256 `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`.
- Added a complete source and 31-asset SHA-256 manifest.
- Confirmed archive safety, 12 parseable Python files, and no generated cache files.
- Confirmed the separate dev package/operator namespace intended for side-by-side installation with the public Quickbar.
- Located `UPDATE_URL` at `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`.
- Confirmed the Check for Updates operator only calls Blender's URL opener and performs no version comparison.
- Confirmed no public branch, URL, package identity, operator ID, or asset path was changed.
- Confirmed no Blender runtime test was performed.

## 2026-07-20 — Documentation architecture and public compatibility protection

- Recorded `Witch_Quick_Access` public branch baseline at commit `13242bf0141c7f539af97b39a4aca6e640c0901c`.
- Recorded public v1.0.2 / internal 1.2.8 correlation and Blender 4.5 metadata.
- Established local overlay and input-preservation rules.
- Added project state and a baseline-recovery/compatibility roadmap.
- Added overlay architecture, input/event, asset, and Witch Tools integration documents.
- Recorded root/package documentation-version mismatch for later audit.
- Recorded known development issues as unverified context pending source import.
- Confirmed no Quickbar source, public branch, URL, package identity, external link, or asset was changed or runtime-tested.
