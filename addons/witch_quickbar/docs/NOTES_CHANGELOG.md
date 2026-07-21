# Witch Quickbar Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v1.4.0 — Select tab and Selection Slots integration

- Added a populated `Select` tab to the floating overlay.
- Added compact Selection Slot rows with full-name tooltips, click-to-rename, reselect, save/overwrite, clear, remove, add, header Clear All, and grip drag reorder.
- Added optional thin invocation of Witch Tools Dev_v2.6.0+ `mesh.wt_selection_slot_*` operators rather than duplicating the canonical backend.
- Added a safe disabled requirement message when Witch Tools is unavailable.
- Converted the five supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD SVGs into transparent 64x64 PNG runtime assets.
- Increased dynamic gizmo capacity for slot rows and responsive name hit targets.
- Produced `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`, SHA-256 `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`.
- Updated overlay, input, asset, integration, roadmap, project-state, package, build, compatibility, and feature documentation.

## Testing

- ZIP integrity and safe-path checks passed.
- Static parsing/compile passed for all 13 Python files.
- All 36 icon references resolve to packaged PNGs.
- Duplicate operator-ID and package-hygiene checks passed.
- Synthetic multi-slot layout construction passed.
- Blender 4.5 overlay drawing, dependency integration, drag/reorder, resize, pass-through, file-load recovery, and undo/redo remain pending.

## Public compatibility

No public branch, `Witch_Quick_Access` update destination, package identity, existing operator namespace, inherited asset path, or public release location changed.
