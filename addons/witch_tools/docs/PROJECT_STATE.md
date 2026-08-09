# Witch Tools Project State

Last updated: 2026-08-08

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-magic-branch`
- Dev_v2.10.0 tested baseline: `f010eaa136dd8e68b78485858a369d38fc89a078`
- Current candidate: `Dev_v2.10.1`
- Target Blender: `4.5.0`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Last completed work

Dev_v2.10.0 was user-tested in Blender 4.5. Passing behavior: hover highlighting, Magnetic Snap, Inject New Undo/Redo, Paver, Organic, and tested Organic magnetic vertex merge. The test exposed multi-edge Edge-source, multi-contact merge, stale unsplit target-edge, Magic Branch camera/activation/selection-mode, Paver out-of-plane/return-path merge, and Object Snap Undo failures.

Dev_v2.10.1 source fixes are implemented: Edge Solo/Branch supports one or more selected edges; Auto-Merge scans every created vertex and splits existing target edges before welding interior contacts; MMB pivot changes occur only on plain MMB during a live drag; Magic Branch has explicit ON/OFF plus separate Persistent behavior; Branch Type switches Blender mesh selection mode; Paver can grow out of plane under explicit axis constraints; Object Snap pushes an explicit Undo boundary.

## Current known-working state

The Dev_v2.10.0 behaviors listed above are user-confirmed in Blender 4.5. Dev_v2.10.1 package Python syntax/version validation passed during source patch integration. Do not infer Dev_v2.10.1 runtime success from those static checks.

## Active problems / limitations

Dev_v2.10.1 requires Blender 4.5 retest for multi-edge source behavior, every Auto-Merge topology case, normals/winding/material/custom-edge-data preservation, cancel/Undo/Redo, Magic Branch modal lifecycle and camera navigation, selection-mode Undo restoration, Z-wall Paver dimensions, return-path Paver merge, and Object Snap Undo. Dynamic unselected-fan Slide and arbitrary face-interior retopology remain deferred. Persistent per-branch Undo and Edit Tools drag-grip reordering remain runtime-unverified.

## Next exact implementation step

Install Dev_v2.10.1 in Blender 4.5 and run the regression blocks in the Precision Edit and Magic Branch test plans. Fix only observed failures before starting new feature scope or Witch Dock/Quickbar exposure.

## Files changed

Source: `precision_edit_topology.py`, `precision_edit_drag.py`, `operators_inject_new.py`, `operators_magic_branch.py`, `precision_edit_props.py`, `panel_precision_edit.py`, `operators_object_snap.py`, `operators_ui.py`, `__init__.py`, `state.py`, plus source quick starts/changelog/readme/compatibility. Repository documentation: Precision Edit and Magic Branch packets, UI map, roadmap, project state, notes and compatibility metadata.

## Test status

- Dev_v2.10.0 Blender 4.5 user pass: performed and recorded above
- Dev_v2.10.1 Python AST/version validation: passed
- Dev_v2.10.1 Blender 4.5 runtime: not performed
- Additional Blender versions: not tested
- Public release / Quickbar changes: none
