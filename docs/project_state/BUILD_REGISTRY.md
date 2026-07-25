# Blender.Tools Build Registry

This registry records verified and candidate baselines. A build is not current merely because it was generated recently or discussed in chat.

## Witch Quickbar

### Public baseline — verified in repository

- Public version: `v1.0.2`
- Internal source correlation: `1.2.8`
- Branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Intended Blender target: `4.5.0`
- Status: unchanged public compatibility baseline

### Current local development delivery — Align Selection

- Version: `Dev_v1.5.0`
- Artifact: `witch_quickbar_dev_Dev_v1_5_0_Align_Selection_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- Target Blender version: `4.5.0`
- Source status: local-only; GitHub Quickbar source intentionally not updated
- Dependency: unchanged `mesh.wt_align_*` contract, compatible with Witch Tools Dev_v2.7.1
- User finding: Align Selection controls render; source-reference dropdown is absent and deferred to a separate local-only patch
- Blender runtime beyond presentation: pending

### Previous development builds

- `Dev_v1.4.0`: Selection Slots workflow user-reported passed
- `Dev_v1.3.18`: SHA-256 `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`

## Witch Tools

### Public baseline

- No verified public code baseline found on `Witch_Main_Tools`.
- Public compatibility surface remains unchanged.

### Current development build — Align Selection N-panel hotfix

- Version: `Dev_v2.7.1`
- Artifact: `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `f4783b620325e6c40c156d9aa05e2479ca0e0159b06f4177138b46bbfbc4c110`
- Build date: `2026-07-24`
- Supersedes: both Dev_v2.7.0 artifact identities
- Python files: 47
- PNG assets: 6
- Generated cache files: none
- Changes:
  - registers missing `show_edit_align_selection` persistent preference;
  - replaces invalid/unverified `ALIGN` header icon with `PIVOT_ACTIVE`;
  - retains all `mesh.wt_align_*` operators and alignment properties unchanged.
- Static syntax/compile: passed
- Duplicate operator IDs: passed, 96 identifiers
- UI-state and icon regression checks: passed
- ZIP/package verification: passed
- Blender 4.5 runtime: pending user validation
- Package identity/footer/public URLs: unchanged

### Verified Dev_v2.7.1 source patch

- Path: `addons/witch_tools/dev/patches/Dev_v2_7_1/`
- User-tested repair baseline: 127,760 bytes / SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`
- Build artifact: 132,763 bytes / SHA-256 `f4783b620325e6c40c156d9aa05e2479ca0e0159b06f4177138b46bbfbc4c110`
- Focused source patch and manifest: present
- Static/compile/operator-ID/ZIP/safe-path/package-hygiene verification: passed
- Full Dev_v2.7.1 source archive snapshot: deferred
- Scope: development-only source record

### Superseded/conflicting Dev_v2.7.0 records

- Earlier repository snapshot artifact: SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- User-tested replacement artifact: SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`
- Runtime finding on replacement artifact: empty Align Selection N-panel box
- Resolution: both superseded by Dev_v2.7.1; discrepancy preserved rather than silently reconciled

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
