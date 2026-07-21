# Blender.Tools Build Registry

This registry records verified and candidate baselines. A build is not current merely because it was generated recently or discussed in chat.

## Witch Quickbar

### Public baseline — verified in repository

- Public version: `v1.0.2`
- Internal source correlation: `1.2.8`
- Branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Intended Blender target: `4.5.0`
- Update destination: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`
- Status: public compatibility baseline; unchanged

### Current development build — Select tab

- Version: `Dev_v1.4.0`
- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Target Blender version: `4.5.0`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Build date: `2026-07-21`
- Supersedes development candidate: `Dev_v1.3.18`
- Python files: 13
- PNG assets: 36
- Generated cache/source SVG files: none
- Static syntax/package/asset audit: passed
- Runtime environment tested: none in this implementation pass
- Added capability: populated Select tab with optional Witch Tools Dev_v2.6.0 Selection Slots integration, responsive names, full tooltips, rename, save/reselect/clear/remove/add/Clear All, and drag reorder
- Dependency behavior: intended to remain usable without Witch Tools and show a disabled requirement state; runtime test pending
- Known limitations: Blender 4.5 overlay, pass-through, drag/resize, file-load recovery, undo/redo, and side-by-side installation unverified
- Update destination remains: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`
- Status: current development candidate pending Blender 4.5 runtime validation and canonical source import

### Superseded development candidate

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package folder: `witch_quickbar_dev`
- Target Blender version: `4.5.0`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Status: preserved baseline used to produce Dev_v1.4.0

## Witch Tools

### Public baseline

- Version: no verified public code baseline found on `Witch_Main_Tools`
- Default branch head: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Branch content state: placeholder documentation only

### Current development build — Selection Slots

- Version: `Dev_v2.6.0`
- Artifact: `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Build date: `2026-07-21`
- Supersedes: `Dev_v2.5.2`
- Python files: 46
- PNG assets: 6
- Generated cache files: none
- Static syntax/package audit: passed
- Runtime environment tested for Selection Slots: none in this implementation pass
- Added capability: persistent multi-slot vertex/edge/face/mixed selection save and restore, multi-object Edit Mode, add/remove/clear/Clear All/rename/reorder, and Quickbar operator contract
- Retained capabilities: Auto-Aligned Vertex Inject, user-validated Curvature Sync and misaligned-column repair, Vertex Locks, Object Snap, and existing Dev_v2.x workflows
- Known limitations: Selection Slots Blender 4.5 registration, save/reopen, topology propagation, multi-object restore, and undo/redo unverified
- Footer link remains: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools`
- Status: current development candidate pending Blender 4.5 Selection Slots validation and canonical source import

### Superseded development build — Curvature Sync column repair

- Version: `Dev_v2.5.2`
- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Automated runtime: Blender Python `5.2.0 LTS`
- Blender 4.5 result: user installed and reported production Curvature Sync result worked beautifully
- Status: preserved user-validated topology baseline included in Dev_v2.6.0

### Superseded development build — Vertex Inject + Curvature Sync

- Version: `Dev_v2.5.1`
- Artifact: `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`
- SHA-256: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Status: superseded by Dev_v2.5.2

### Superseded development build — Curvature Sync MVP

- Version: `Dev_v2.5.0`
- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Status: preserved first Curvature Sync MVP baseline

### Superseded development baseline

- Version: `Dev_v2.4.0`
- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Status: source baseline used for Dev_v2.5.x and Dev_v2.6.0

## Witch's Dev Modules

### Current development candidate

- Host version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- Package folder: `witch_dev_modules`
- Target Blender version: `4.5.0`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Included modules: Re-Namer `Dev_v0.0.1`, Loose Parts → Objects `Dev_v0.0.1`, Chain Generator `Dev_v0.0.8`
- Static audit: passed
- Packaging defect: 34 `.pyc` files in `__pycache__`
- Runtime test: pending

## Witch Core

- Current development baseline: not yet imported
- Expected target: Blender 4.5
- Status: pending audit

## Baseline manifests

Current immutable supplied-baseline manifests:

- `docs/project_state/baseline_manifests/WITCH_TOOLS_DEV_2_4_0.json`
- `docs/project_state/baseline_manifests/WITCH_QUICKBAR_DEV_1_3_18.json`
- `docs/project_state/baseline_manifests/WITCH_DEV_MODULES_0_0_9.json`

Dev_v2.6.0 and Quickbar Dev_v1.4.0 source manifests must be added when their complete source trees are imported canonically.

## Build-entry requirements

Every future entry must include component, version, source branch/commit, artifact, package identity, Blender target, tested versions, hash, build date, tests, limitations, and superseded baseline.

## Rule

Do not replace a verified or candidate-current entry with a remembered version unless the replacement files are hashed, compared, and explicitly recorded.
