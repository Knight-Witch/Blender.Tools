# Selection Slots State

Last updated: 2026-07-21

## Identity

- Canonical owner: Witch Tools
- Witch Tools build: `Dev_v2.6.0`
- Witch Tools artifact: `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`
- Witch Tools SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Quickbar integration build: `Dev_v1.4.0`
- Quickbar artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Quickbar SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Target Blender version: `4.5`
- Development branch: `Blender_Dev`

## Implemented in Witch Tools Dev_v2.6.0

- persistent scene slot collection;
- generated stable UID per slot;
- per-slot BMesh integer custom layers for vertex, edge, and face domains;
- exact save/overwrite of current enabled mesh-selection modes;
- multi-object Edit Mode save and reselect;
- automatic entry into the saved multi-object Edit Mode context when possible;
- rename, add, remove, clear, Clear All, and up/down reorder;
- at least one slot maintained automatically;
- maximum 20 slots;
- saved selection counts and object references;
- N-panel section immediately below Curvature Sync;
- native LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD UI icons;
- stable `mesh.wt_selection_slot_*` operator family for secondary access surfaces;
- `.blend` persistence through scene and mesh custom data.

## Implemented in Quickbar Dev_v1.4.0

- populated `Select` tab;
- optional availability detection for Witch Tools Dev_v2.6.0 operators;
- thin invocation of canonical Witch Tools save/reselect/clear/remove/add/move/rename actions;
- click-to-rename dialog;
- full-name tooltip and width-responsive name display;
- grip-based drag reorder;
- header Clear All;
- disabled requirement message when Witch Tools is unavailable;
- five supplied SVG icons converted into packaged transparent 64x64 PNG assets.

## Static validation completed

- Witch Tools package: 46 Python files and 6 PNG assets;
- Quickbar package: 13 Python files and 36 PNG assets;
- complete Python AST/compile checks passed;
- no duplicate `bl_idname` values found;
- ZIP integrity and safe-path checks passed;
- no `__pycache__`, `.pyc`, `.pyo`, or SVG source files shipped;
- Quickbar icon-reference inventory resolved to existing packaged PNGs;
- Quickbar synthetic layout construction with multiple slot rows passed;
- package roots remain `Witch_Tools_Dev` and `witch_quickbar_dev`;
- Witch Tools footer URL and Quickbar public update URL remain unchanged.

## Runtime status

Blender runtime testing was not available in the current implementation session. The following remain unverified in Blender 4.5:

- add-on registration/unregistration;
- actual BMesh custom-layer save and reselect behavior;
- save/reopen persistence;
- multi-object context restoration;
- interactive undo/redo;
- N-panel rendering and native icon availability;
- Quickbar overlay drawing, drag reorder, resize responsiveness, tooltips, pass-through, and file-load recovery;
- side-by-side Witch Tools/Quickbar installation and dependency-unavailable behavior.

## Known limitations

- Slot markers are persistent custom element data, not immutable topology UUIDs.
- Deleting an element removes its saved marker.
- Splitting or duplicating topology may copy a marker to newly created elements depending on Blender's custom-data propagation.
- Shared linked objects using one Mesh datablock share the underlying marker layers.
- Hidden or unavailable saved objects are not forcibly unhidden.
- N-panel uses up/down buttons rather than a custom drag interaction; Quickbar provides drag reorder.
- Object Mode, bone, and independent UV selections are not supported in this build.

## Next exact step

Install Witch Tools Dev_v2.6.0 in Blender 4.5 first, then Quickbar Dev_v1.4.0. Test vertex, edge, face, mixed-domain, multi-object, save/reopen, overwrite, clear/remove, reorder, undo/redo, Quickbar Select-tab drag, resize, pass-through, and missing-backend behavior. Patch only failures found in those tests before treating either build as release-ready.
