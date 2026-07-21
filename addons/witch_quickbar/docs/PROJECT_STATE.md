# Witch Quickbar Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Quickbar
- Architecture: floating 3D View overlay companion
- Default target Blender version: 4.5
- Public compatibility branch: `Witch_Quick_Access`
- Development package identity: `witch_quickbar_dev`
- Development branch: `Blender_Dev`

## Current verified public baseline

- Public version represented at branch head: `v1.0.2`
- Internal/public source correlation: `1.2.8`
- Branch head: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Declared Blender metadata: `4.5.0`
- Update destination: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`

The public branch and update destination remain unchanged.

## Current development build

- Version: `Dev_v1.4.0`
- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Declared Blender target: `4.5.0`
- Python source files: 13
- PNG assets: 36
- Generated cache files: none
- Static syntax/package audit: passed
- Blender runtime in this implementation pass: not available

Dev_v1.4.0 was produced from the user-supplied Dev_v1.3.18 candidate without renaming the package, changing existing operator IDs, moving existing assets, or changing `UPDATE_URL`.

## Current implementation

Dev_v1.4.0 retains the floating overlay architecture and all Dev_v1.3.18 Main/Edit functionality. It adds:

- a populated `Select` tab;
- a compact Selection Slots section using the supplied LONGDISPLAY title icon;
- thin optional integration with Witch Tools Dev_v2.6.0 `mesh.wt_selection_slot_*` operators;
- slot name display and click-to-rename dialog;
- full-name tooltips and width-responsive name display;
- reselect, save/overwrite, clear, remove, add, and header Clear All actions;
- grip-based short-lived modal slot reorder;
- disabled explanatory state when the required Witch Tools backend is unavailable;
- five supplied SVG icons converted to transparent 64x64 PNG runtime assets:
  - `longdisplay.png`
  - `file_tick.png`
  - `trash.png`
  - `remove.png`
  - `add.png`

Quickbar does not store a duplicate slot collection or mesh markers. It invokes the canonical Witch Tools operators for actions, rename, and reorder.

## Last completed work

- Inspected Dev_v1.3.18 source, tab architecture, layout, drawing, gizmo input, persistence, and update URL.
- Added the Select tab and Selection Slots presentation.
- Added dedicated Quickbar operators for action dispatch and rename dialog.
- Added slot grip drag/drop using the existing short-lived modal interaction pattern.
- Increased gizmo capacity to cover dynamic slot rows and responsive name hit targets.
- Converted and bundled the five supplied icons.
- Added package README/changelog/notes/quick-start updates.
- Produced and statically audited the Dev_v1.4.0 ZIP.

## Current known-working state

Static validation:

- all 13 Python files parse and compile;
- no duplicate `bl_idname` values;
- all 36 icon references resolve to packaged PNG files;
- the five new icons are 64x64 transparent PNGs;
- synthetic layout construction with multiple slot rows completed;
- slot action hit targets, Add, Clear All, responsive name width, and Select tab were present in the generated layout;
- ZIP integrity, safe paths, and package hygiene passed;
- package/operator namespaces and public update URL remain unchanged.

No Blender overlay runtime claim is made for Dev_v1.4.0.

## Active problems

1. Blender 4.5 registration and overlay rendering require testing.
2. Witch Tools Dev_v2.6.0 dependency-present and dependency-absent behavior require runtime tests.
3. Slot name tooltip, rename dialog, Save/Reselect/Clear/Remove/Add/Clear All actions require interaction tests.
4. Grip reorder, canceled drag, overlap, and input pass-through require testing.
5. Width-responsive name layout and high slot counts require viewport-size testing.
6. Open/close, minimize/maximize, lock, resize, section/tab/mode reorder, file-load recovery, and unregister/re-register require regression testing.
7. Scene-data actions invoked through Quickbar require undo/redo testing without UI-state undo pollution.
8. The complete Dev_v1.4.0 source tree has not yet been imported into the final canonical repository location.
9. Public and dev side-by-side install/update behavior remains untested.

## Next exact implementation step

Install Witch Tools Dev_v2.6.0 first, then Quickbar Dev_v1.4.0 in Blender 4.5. Test the Select tab with short and long names, several slots, every action, drag reorder, resizing, pass-through, file reload, undo/redo, and Witch Tools disabled. Run the full Quickbar regression matrix. Patch only failures found by those tests.

## Public safety status

- public branch modified: no
- update URL modified: no
- external release links modified: no
- package identity modified: no
- existing public/dev operator IDs modified: no

## Test status

- archive integrity and safe paths: passed
- Python syntax/compile: passed for 13 files
- duplicate operator-ID scan: passed
- asset existence/dimensions: passed
- synthetic layout construction: passed
- Blender 4.5 runtime: not performed
- overlay input/pass-through: not tested
- save/reselect integration: not tested
- drag/resize/file-load recovery: not tested
- public update control: preserved statically, not launched
- clean/upgrade/side-by-side install: not tested

## Known remaining issues

Dev_v1.4.0 is a development build. Selection Slots requires Witch Tools Dev_v2.6.0 or later; Quickbar intentionally shows an unavailable state rather than maintaining a separate backend.
