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

### Current development candidate

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Target Blender version: `4.5.0`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Static audit: passed
- Runtime test: pending

## Witch Tools

### Public baseline

- Version: no verified public code baseline found on `Witch_Main_Tools`
- Default branch head: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Branch content state: placeholder documentation only

### Current urgent development build — Vertex Inject + Curvature Sync

- Version: `Dev_v2.5.1`
- Artifact: `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Build date: `2026-07-21`
- Supersedes: `Dev_v2.5.0`
- Python files: 45
- PNG assets: 6
- Generated cache files: none
- Static syntax/package audit: passed
- Runtime environment tested: Blender Python `5.2.0 LTS`
- Blender 4.5 runtime: pending user validation
- Added capability: standalone ordered A/B/C Auto-Aligned Vertex Inject with projected target-edge split and optional C-D shared-face split
- Retained capability: Curvature Sync circular multi-chain/multi-object MVP
- Runtime tests: registration/unregistration, synthetic vertex injection, synthetic face split, Curvature Sync synthetic regression
- Known limitations: active-object single inject; explicit click-order selection; ambiguous forks abort; Blender 4.5 UI and interactive undo/redo unverified
- Footer link remains: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools`
- Status: current urgent candidate build pending Blender 4.5 user test and canonical source import

### Superseded urgent development build — Curvature Sync MVP

- Version: `Dev_v2.5.0`
- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Status: superseded by Dev_v2.5.1; preserved as the first Curvature Sync MVP baseline

### Superseded development baseline

- Version: `Dev_v2.4.0`
- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Status: source baseline used for Dev_v2.5.x

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

Current imported-baseline manifests:

- `docs/project_state/baseline_manifests/WITCH_TOOLS_DEV_2_4_0.json`
- `docs/project_state/baseline_manifests/WITCH_QUICKBAR_DEV_1_3_18.json`
- `docs/project_state/baseline_manifests/WITCH_DEV_MODULES_0_0_9.json`

A Dev_v2.5.1 source manifest must be added when its full source is imported into the canonical repository tree.

## Build-entry requirements

Every future entry must include component, version, source branch/commit, artifact, package identity, Blender target, tested versions, hash, build date, tests, limitations, and superseded baseline.

## Rule

Do not replace a verified or candidate-current entry with a remembered version unless the replacement files are hashed, compared, and explicitly recorded.
