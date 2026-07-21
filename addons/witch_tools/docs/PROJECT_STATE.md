# Witch Tools Project State

Last updated: 2026-07-20

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit
- Default target Blender version: 4.5
- Development package identity: `Witch_Tools_Dev`

## Current candidate baseline

- Version: `Dev_v2.4.0`
- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Declared Blender target: `4.5.0`
- Python source files: 43
- PNG assets: 6
- Shipped cache artifacts: none
- Static Python syntax audit: passed
- Blender runtime test in this audit: not performed

This user-supplied artifact is now the best available candidate current baseline. It is not yet a runtime-verified repository source baseline.

## Current recorded implementation

The package contains the modular Dev_v2.x N-panel architecture and includes:

- Mode Switcher
- Auto Mirror
- Edit Tools
- Vertex Snap
- Vertex Locks / protected edit-zone systems
- Object Snap added in Dev_v2.4.0
- Quick Modifiers
- Head, Body, Armour, Hair, Weight, Armature, Shape Key, Export, and Troubleshooting panels
- development footer and external links

The exact implementation must be inspected from the imported source before modifying any operator.

## Last completed work

- Hashed and statically audited the user-supplied Dev_v2.4.0 archive.
- Recorded a per-file manifest.
- Confirmed package identity, version metadata, target Blender version, and current footer GitHub destination.
- Confirmed no `__pycache__` or `.pyc` files are shipped.
- Preserved Curvature Sync as a Witch Tools topology-repair feature.

## Current known-working state

Unknown until Dev_v2.4.0 is installed and smoke-tested in Blender 4.5. Static syntax and archive checks passed, but this is not runtime verification.

## Active problems

- canonical source tree has not yet been imported into `Blender_Dev`
- Blender 4.5 install/register/unregister test pending
- current UI map and operator registry not yet generated from source
- Vertex Lock/protected-zone behavior must be audited before Curvature Sync implementation
- footer GitHub link still targets `Witch_Main_Tools`, whose verified branch content is placeholder documentation
- public-release/update strategy for Witch Tools remains unresolved

## Next exact implementation step

Import the Dev_v2.4.0 source without changing the `Witch_Tools_Dev` package folder or operator identifiers. Then:

1. install and smoke-test it in Blender 4.5;
2. generate the current UI and operator registries;
3. audit `operators_vertex_locks.py`, protection storage, and topology-safety helpers;
4. create an isolated Vertex Inject / Curvature Sync development module against this baseline.

## Planned feature sequence

1. Verify existing Vertex Lock/protection architecture.
2. Specify reusable protected-zone permissions.
3. Implement and test Mode 1 Vertex Inject as an isolated dev module.
4. Implement bulk correspondence repair.
5. Implement Curvature Sync circular multi-chain prototype.
6. Integrate into Witch Tools only after acceptance tests pass.

## Files changed in current pass

Documentation and manifests only. Runtime source was not modified.

## Test status

- archive integrity: passed
- archive safe-path checks: passed
- Python syntax parse: passed for 43 files
- Blender runtime: not tested
- source import: not completed
- Curvature Sync implementation: not started

## Known remaining issues

Dev_v2.4.0 is the best available candidate baseline, not yet a runtime-confirmed canonical repository baseline.
