# Blender.Tools Build Registry

This registry records verified and candidate baselines. A build is not current merely because it was generated recently or discussed in chat.

## Witch Quickbar

### Public baseline — verified in repository

- Public version: `v1.0.2`
- Internal source correlation: `1.2.8`
- Branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Intended Blender target in metadata: `4.5.0`
- Additional versions tested: not independently verified in this repository audit
- Artifact filename: not yet recorded
- Public package folder: not yet mapped from the branch tree
- Update destination: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`
- Status: public tracked baseline; compatibility branch must remain intact

### Current development candidate — user supplied and statically audited

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Target Blender version: `4.5.0`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Build date represented by archive timestamps: `2026-07-15`
- Static audit: ZIP safety and Python syntax passed
- Runtime test: not performed in this audit
- Update behavior: opens the public `Witch_Quick_Access` branch; no version comparison is performed
- Status: best available candidate development baseline pending Blender 4.5 smoke test and source import

## Witch Tools

### Public baseline

- Version: no verified public code baseline found on `Witch_Main_Tools`
- Default branch head: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Branch content state: placeholder documentation only

### Current urgent development build — Curvature Sync MVP

- Version: `Dev_v2.5.0`
- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Build date: `2026-07-21`
- Supersedes development baseline: `Dev_v2.4.0`
- Python files: 44
- PNG assets: 6
- Generated cache files: none
- Static syntax/package audit: passed
- Runtime environment tested: Blender Python `5.2.0 LTS`
- Blender 4.5 runtime: pending user validation
- Runtime tests: registration/unregistration, synthetic repair, protected locks, invalid-selection rollback, actual two-object collar repair, save/reopen, topology validation
- Known limitations: circular planar MVP; explicit A/M/Z and chain selection; unresolved columns may remain; interactive undo/redo and Blender 4.5 UI not verified
- GitHub footer link remains: `https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools`
- Status: current urgent candidate build pending Blender 4.5 user test and canonical source import

### Superseded development baseline — user supplied and statically audited

- Version: `Dev_v2.4.0`
- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Build date represented by archive timestamps: `2026-07-20`
- Static audit: ZIP safety and Python syntax passed
- Current recorded feature: Edit Tools > Object Snap
- Status: preserved baseline used to produce Dev_v2.5.0

## Witch's Dev Modules

### Current development candidate — user supplied and statically audited

- Host version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- Package folder: `witch_dev_modules`
- Target Blender version: `4.5.0`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Build date represented by archive timestamps: `2026-05-10`
- Included modules:
  - Re-Namer `Dev_v0.0.1`
  - Loose Parts → Objects `Dev_v0.0.1`
  - Chain Generator `Dev_v0.0.8`
- Static audit: ZIP safety and Python syntax passed
- Packaging defect: 34 `.pyc` files shipped inside `__pycache__` directories
- Documentation defect: package documents are not normalized to the declared host `Dev_v0.0.9`
- Runtime test: not performed in this audit
- Status: candidate baseline; canonical import must strip generated cache files and preserve the original archive hash in the audit record

## Witch Core

- Current development baseline: not yet imported into this branch
- Target Blender version: expected `4.5`, must be confirmed
- Status: pending audit

## Baseline manifests

Per-file SHA-256 manifests are stored under:

- `docs/project_state/baseline_manifests/WITCH_TOOLS_DEV_2_4_0.json`
- `docs/project_state/baseline_manifests/WITCH_QUICKBAR_DEV_1_3_18.json`
- `docs/project_state/baseline_manifests/WITCH_DEV_MODULES_0_0_9.json`

A Dev_v2.5.0 source/build manifest must be added when the full source is imported into the canonical repository tree.

## Build-entry requirements

Every future entry must include:

- component
- public or development version
- source branch and commit
- artifact filename
- package folder/add-on identifier
- target Blender version
- additional versions actually tested
- source hash or archive hash
- build date
- test status
- known limitations
- superseded baseline

## Rule

Do not replace an entry marked verified or candidate-current with a remembered or chat-generated version unless the replacement files are hashed, compared, and explicitly recorded.