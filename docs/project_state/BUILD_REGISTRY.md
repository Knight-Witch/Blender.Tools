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
- Status: unchanged public compatibility baseline

### Current local development delivery — Align Selection

- Version: `Dev_v1.5.0`
- Artifact: `witch_quickbar_dev_Dev_v1_5_0_Align_Selection_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Target Blender version: `4.5.0`
- SHA-256: `d2ace3cd3310686664cebfce6242717af3afed3f5954a4bd3cd6bc2a26eded5c`
- Build date: `2026-07-24`
- Supersedes locally: `Dev_v1.4.0`
- Python files: 14
- PNG assets: 36
- Static syntax/package/layout/integration tests: passed
- Dependency: Witch Tools Dev_v2.7.0 `mesh.wt_align_*` contract
- Source status: local-only; GitHub Quickbar source intentionally not updated
- Blender 4.5 runtime: pending
- Update destination and package identity: unchanged

### Previous development build — Select tab

- Version: `Dev_v1.4.0`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Blender 4.5 Selection Slots workflow: user-reported passed
- Repository source snapshot/import: pending

### Earlier candidate

- `Dev_v1.3.18`: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`

## Witch Tools

### Public baseline

- No verified public code baseline found on `Witch_Main_Tools`.
- Default branch historical head: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`.
- Public compatibility surface remains unchanged.

### Current development build — Align Selection

- Version: `Dev_v2.7.0`
- Artifact: `Witch_Tools_Dev_v2_7_0_Align_Selection_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- Build date: `2026-07-24`
- Supersedes: `Dev_v2.6.1`
- Python files: 48
- PNG assets: 6
- Generated cache files: none
- Added:
  - persistent Source and Target Anchor capture;
  - Match Coordinates;
  - shape-preserving Move Shape;
  - X/Y/Z combinations;
  - Whole Selection and Per Selected Island;
  - multiple-cavity and multi-object planning;
  - lock, stale-marker, shape-key, missing-anchor, and transform preflight;
  - stable Quickbar operator/property contract.
- Static syntax/package audit: passed
- Pure core and synthetic operator-planning tests: passed
- Blender 4.5 runtime: pending
- Package identity/footer/public URLs: unchanged

### Verified isolated Dev_v2.7.0 source snapshot

- Path: `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_7_0/`
- Source ZIP: 136,327 bytes / `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- Reconstructed archive: 85,712 bytes / `2a73eaeb209602b30c4ee8e3378961038249ca3782cac23b7ad5923e3d994cab`
- Extracted package: `Witch_Tools_Dev`
- Source tree: 63 files / 412,416 bytes
- Tree SHA-256: `c8ece8e4e0a750763e90ccabaa16cf6c0e1f0f8f01a06f67b2bbea1ae3d752b5`
- Verification: passed locally on 2026-07-24
- Scope: development-only preservation

### Historical builds

- `Dev_v2.6.1`: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- `Dev_v2.6.0`: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- `Dev_v2.5.2`: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- `Dev_v2.5.1`: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- `Dev_v2.5.0`: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- `Dev_v2.4.0`: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`

## Witch's Dev Modules

- Version: `Dev_v0.0.9`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Packaging defect: original archive contains 34 `.pyc` files
- Runtime: pending

## Witch Core

- Current baseline: pending source import/audit
- Expected target: Blender 4.5

## Rule

Do not replace a verified or candidate-current entry with a remembered version unless replacement files are hashed, compared, and explicitly recorded.
