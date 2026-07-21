# Witch Quickbar Project State

Last updated: 2026-07-20

## Identity

- Add-on: Witch Quickbar
- Architecture: floating 3D View overlay companion
- Default target Blender version: 4.5
- Public compatibility branch: `Witch_Quick_Access`
- Development package identity: `witch_quickbar_dev`

## Current verified public baseline

- Public version represented at branch head: `v1.0.2`
- Internal/public source correlation: `1.2.8`
- Branch head: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Declared Blender metadata: `4.5.0`

The public branch remains unchanged.

## Current development candidate

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Declared Blender target: `4.5.0`
- Python source files: 12
- PNG assets: 31
- Shipped cache artifacts: none
- Static Python syntax audit: passed
- Blender runtime test in this audit: not performed

This development package installs separately from the public package and is the best available candidate current dev baseline.

## Update/check behavior

The Check for Updates operator opens:

`https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`

It does not fetch a manifest or compare versions. The new `Blender_Dev` branch therefore does not alter the current update-button destination.

## Current recorded development features

Dev_v1.3.18 records:

- tab/module foundation with Main and Edit tabs
- Mirror Transform with Local/Global and X/Y/Z selection
- Mirror Objects with edit-mode handling
- Apply All Transforms from Object or mesh Edit Mode
- Vertex Snap in the Edit tab
- duplicate tools
- display-state, hotkey, overlay, drag, resize, lock, reorder, persistence, and file-load recovery systems

## Last completed work

- Hashed and statically audited the Dev_v1.3.18 archive.
- Recorded the complete source/asset manifest.
- Confirmed the separate dev package/operator namespace.
- Located the exact update/check URL and confirmed it is a URL-open action only.
- Preserved the public branch and all public URLs unchanged.

## Current known-working state

The public branch is tracked, but neither the public package nor Dev_v1.3.18 was runtime-tested during this audit. Static syntax and archive checks passed.

## Active problems

- canonical dev source tree has not yet been imported into `Blender_Dev`
- public branch package location still requires full tree mapping
- public and dev artifacts need clean-install and side-by-side-install testing
- update/check button browser launch must be tested from installed builds
- asset manifest documentation must be reconciled with the 31 files in the uploaded package
- current known bugs and regression status must be confirmed in Blender 4.5

## Next exact implementation step

Import Dev_v1.3.18 without renaming `witch_quickbar_dev`, changing operator IDs, moving assets, or changing `UPDATE_URL`. Then run the full Quickbar smoke-test matrix in Blender 4.5.

## Public safety status

- public branch modified: no
- update URL modified: no
- external release links modified: no
- package identity modified: no
- public operator IDs modified: no

## Test status

- archive integrity: passed
- archive safe-path checks: passed
- Python syntax parse: passed for 12 files
- Blender runtime: not tested
- public update control: inspected statically, not launched
- clean install: not tested
- upgrade: not tested
- side-by-side public/dev install: not tested

## Known remaining issues

Dev_v1.3.18 is now identified and hashed, but it is not yet a runtime-confirmed canonical repository baseline.
