# Witch Quickbar Notes Changelog — Full History

## 2026-07-21 — Dev_v1.4.0 Blender 4.5 Select-tab validation

- The user installed Quickbar Dev_v1.4.0 and reported that the Selection Slots implementation worked perfectly in the tested workflow.
- This confirms the primary Select-tab rendering and canonical Witch Tools operator-invocation path in the user's Blender 4.5 environment.
- Quickbar Dev_v1.4.0 remains valid with Witch Tools Dev_v2.6.1 because the N-panel hotfix does not change the Selection Slots operator contract.
- No Quickbar runtime source, package, icons, branch, operator ID, or update URL changed for the Witch Tools hotfix.
- Full overlay pass-through, drag cancellation, resize, lock, file-load recovery, unregister/re-register, undo/redo, and backend-unavailable validation remain pending.

## 2026-07-21 — Dev_v1.4.0 Select tab and Selection Slots integration

- Added a populated `Select` tab to the floating overlay.
- Added compact Selection Slot rows with full-name tooltips, click-to-rename, reselect, save/overwrite, clear, remove, add, header Clear All, and grip drag reorder.
- Added optional thin invocation of Witch Tools Dev_v2.6.0+ `mesh.wt_selection_slot_*` operators instead of duplicating slot scene/mesh data.
- Added a disabled explanatory state when Witch Tools is unavailable.
- Converted and packaged the five supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD SVG icons as transparent 64x64 PNG files.
- Increased gizmo capacity for dynamic rows and tiled responsive name hit targets.
- Produced `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`, SHA-256 `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`.
- Static parsing/compile passed for 13 Python files; all 36 icon mappings resolve; no cache or SVG source files were shipped.
- Synthetic layout construction passed.
- Preserved the public branch, update URL, package identity, operator IDs, asset paths, and public release location.

## 2026-07-20 — Development baseline audit

- Recorded user-supplied Quickbar Dev_v1.3.18, package identity, Blender 4.5 target, archive hash, source/assets, and update URL.

## 2026-07-20 — Documentation architecture and public compatibility protection

- Established Quickbar overlay, input, asset, integration, state, roadmap, and compatibility documentation.