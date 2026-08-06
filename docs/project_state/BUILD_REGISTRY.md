# Blender.Tools Build Registry

This registry records verified and candidate baselines. A build is not current merely because it was generated recently or discussed in chat.

## Witch Quickbar / Witch Dock

### Public baseline — verified in repository

- Public version: `v1.0.2`
- Internal source correlation: `1.2.8`
- Branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Intended Blender target: `4.5.0`
- Status: unchanged public compatibility baseline

### Development status for Guided Align

- No Guided Align source change in this pass.
- The prior local development Quickbar artifacts are not treated as the Dev_v2.8.0 integration baseline.
- Next scope: build a thin wrapper only after Witch Tools Dev_v2.8.0 passes Blender 4.5 validation.

## Witch Tools

### Public baseline

- No verified public code baseline found on `Witch_Main_Tools`.
- Public compatibility surface remains unchanged.

### Current development candidate — Guided Align

- Version: `Dev_v2.8.0`
- Artifact: `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- Size: 138,473 bytes
- SHA-256: `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`
- Source-tree SHA-256: `076912ce5d84115adb803ebfa793e04117053fe9af45d459cd4cbdb7be853504`
- Build date: `2026-08-05`
- Python files: 48
- Total files: 63
- Generated cache files: none
- Feature branch: `feature/witch-tools-guided-align`
- Changes:
  - four-step Align Vertices / Edges / Faces workflow;
  - parent capture from vertex/edge/face/mixed selections;
  - Active Element and Median references;
  - world and custom-guide coordinate matching;
  - projection to arbitrary guide line;
  - free movement and straight captured rails;
  - one-to-all and paired-by-rail mapping;
  - rigid shape preservation and per-island grouping;
  - rail clamping and safety preflight;
  - non-mutating Analyze and transaction-first Apply.
- Static syntax/compile: passed
- Duplicate operator/panel identifiers: passed, 99 identifiers
- Guided Align operator count: passed, 7
- UI-state consistency: passed
- Pure constraint math: passed, 7 assertions
- Patch reconstruction/source-tree comparison: passed
- ZIP/package verification: passed
- Blender 4.5 runtime: pending
- Witch Dock/Quickbar updated: no
- Public branches/update URLs: unchanged

### Dev_v2.8.0 source record

- Direct source: `addons/witch_tools/dev/Witch_Tools_Dev/`
- Patch path: `addons/witch_tools/dev/patches/Dev_v2_8_0/`
- Patch encoding: `base64(xz(unified diff))`
- Decoded patch SHA-256: `8cc8f07360d06658668640f41d59c7bac1ecca1139d969e8f1c5140471af3a9d`
- Implementation baseline: verified Dev_v2.6.1 source snapshot
- Reason: the committed Dev_v2.7.0 source parts are truncated and do not match their manifest.

### Superseded/conflicting Dev_v2.7.x records

- Earlier repository Dev_v2.7.0 artifact identity: SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- User-tested replacement Dev_v2.7.0 identity: SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`
- Dev_v2.7.1 delivered hotfix identity: SHA-256 `e68cf22a2db2ab426781bf8acfc2bfdbb8d6f1c8f62c42e1ccf166d30d6b467f`
- Source status: documented artifacts existed, but the committed Dev_v2.7.0 snapshot parts are incomplete and cannot reconstruct the full source.
- Resolution: Dev_v2.8.0 explicitly rebuilds from the verified complete Dev_v2.6.1 source rather than silently trusting the broken snapshot.

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
