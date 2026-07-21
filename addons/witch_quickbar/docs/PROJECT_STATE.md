# Witch Quickbar Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Quickbar
- Architecture: floating 3D View overlay companion
- Default target Blender version: 4.5
- Public compatibility branch: `Witch_Quick_Access`
- Development package identity: `witch_quickbar_dev`
- Development branch: `Blender_Dev`

## Public baseline

- Public version at branch head: `v1.0.2`
- Internal/public source correlation: `1.2.8`
- Branch head: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Update destination: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`
- Public branch and update destination: unchanged

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

## Current implementation

Dev_v1.4.0 retains the floating overlay architecture and Dev_v1.3.18 Main/Edit functionality. It adds:

- populated Select tab;
- thin optional integration with Witch Tools `mesh.wt_selection_slot_*` operators;
- responsive slot names, full-name tooltips, and rename dialog;
- reselect, save/overwrite, clear, remove, add, and Clear All;
- grip-based slot reorder;
- disabled explanatory state when the backend is unavailable;
- five supplied icons converted to transparent 64x64 PNG assets.

Quickbar does not store a duplicate slot backend.

## User validation

The user installed Dev_v1.4.0 in Blender 4.5 and reported that the Quickbar Selection Slots implementation worked perfectly in the tested workflow.

This confirms the primary Select-tab presentation and Witch Tools operator-invocation path in the user's environment. It does not yet constitute the complete Quickbar regression matrix.

## Current known-working state

- 13 Python files parse and compile;
- all 36 icon references resolve;
- ZIP integrity, safe paths, and package hygiene passed;
- synthetic multi-slot layout construction passed;
- Select-tab runtime workflow: user-reported passed in Blender 4.5;
- package/operator namespaces and public update URL remain unchanged.

## Active problems

1. Full overlay regression remains pending: pass-through, canceled drag, lock, resize, minimize/maximize, file-load recovery, unregister/re-register, and multiple viewport cases.
2. Witch Tools-disabled/unavailable state still requires runtime validation.
3. Undo/redo behavior for scene-data actions invoked through Quickbar remains unverified.
4. Public/dev side-by-side installation and update-button launch remain untested.
5. Complete Dev_v1.4.0 source import and source-derived registries remain pending.
6. Witch Tools Dev_v2.6.0 N-panel failed separately and is superseded by the Dev_v2.6.1 N-panel hotfix; Quickbar Dev_v1.4.0 does not require replacement.

## Next exact step

Keep Quickbar Dev_v1.4.0 installed. Install Witch Tools Dev_v2.6.1 and verify the repaired N-panel. Then complete the Quickbar regression matrix and backend-unavailable test.

## Public safety status

- public branch modified: no
- update URL modified: no
- external release links modified: no
- package identity modified: no
- existing public/dev operator IDs modified: no

## Test status

- archive/static/asset/layout checks: passed
- Blender 4.5 Select-tab workflow: user-reported passed
- full overlay input/pass-through regression: pending
- dependency-unavailable state: pending
- undo/redo: pending
- update control: preserved statically, not launched
- clean/upgrade/side-by-side install: pending

## Known remaining issues

Dev_v1.4.0 remains a development build. The primary Select workflow is user-validated, but full Quickbar runtime regression is still required.