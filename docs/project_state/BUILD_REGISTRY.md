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

### Current development build — Select tab

- Version: `Dev_v1.4.0`
- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Target Blender version: `4.5.0`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Build date: `2026-07-21`
- Supersedes: `Dev_v1.3.18`
- Python files: 13
- PNG assets: 36
- Static syntax/package/asset audit: passed
- Blender 4.5 result: user reported the Selection Slots Select workflow worked perfectly
- Remaining tests: full overlay pass-through, drag cancel, resize, lock, file-load recovery, unregister/re-register, undo/redo, backend unavailable, side-by-side install, update launch
- Dependency: Witch Tools Dev_v2.6.0+ operator contract; compatible with Dev_v2.6.1
- Update destination: unchanged
- Isolated source snapshot/import: pending
- Status: current development build; primary Select workflow user-validated, full regression pending

### Superseded development candidate

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`

## Witch Tools

### Public baseline

- Version: no verified public code baseline found on `Witch_Main_Tools`
- Default branch head: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Branch content state: placeholder documentation only

### Current development build — Selection Slots N-panel hotfix

- Version: `Dev_v2.6.1`
- Artifact: `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Target Blender version: `4.5.0`
- SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Build date: `2026-07-21`
- Supersedes: `Dev_v2.6.0`
- Python files: 46
- PNG assets: 6
- Generated cache files: none
- Static syntax/package audit: passed
- Simulated panel tests: expanded, collapsed, populated, empty scene, and Slot 1 initialization passed
- Runtime change: removes Scene mutation from N-panel draw, adds safe Slot 1 fallback, title click toggle, row failure containment
- Retained capabilities: Selection Slots backend/operator contract, Auto-Aligned Vertex Inject, user-validated Curvature Sync, Vertex Locks, Object Snap, existing Dev_v2.x workflows
- Blender 4.5 hotfix runtime: pending user validation
- Footer link: unchanged
- Status: current urgent development hotfix pending Blender 4.5 confirmation

### Verified isolated source snapshot

- Snapshot path: `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/`
- Manifest: `manifest.json`
- Restoration utility: `tools/restore_dev_snapshot.py`
- Source artifact size/SHA-256: 127,401 bytes / `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Reconstructed archive size/SHA-256: 81,400 bytes / `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`
- Extracted package root: `Witch_Tools_Dev`
- Extracted source tree: 60 files, 383,270 bytes
- Deterministic source-tree SHA-256: `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`
- Verification date: `2026-07-23`
- Verification result: ordered parts, individual part hashes/sizes, archive reconstruction/hash/size, safe extraction, package root, file count, byte count, and source-tree digest passed locally
- Scope: development-only preservation; no public or official source path changed

### Superseded development build — initial Selection Slots

- Version: `Dev_v2.6.0`
- Artifact: `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`
- SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Runtime result: Quickbar integration worked; Witch Tools N-panel showed header/Clear All but failed to reveal rows
- Status: superseded by Dev_v2.6.1

### Superseded development build — Curvature Sync column repair

- Version: `Dev_v2.5.2`
- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Blender 4.5 result: production collar workflow user-reported successful

### Earlier preserved builds

- `Dev_v2.5.1`: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- `Dev_v2.5.0`: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- `Dev_v2.4.0`: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`

## Witch's Dev Modules

- Host version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- Package folder: `witch_dev_modules`
- Target Blender version: `4.5.0`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Packaging defect: original archive contains 34 `.pyc` files
- Runtime test: pending

## Witch Core

- Current baseline: pending source import/audit
- Expected target: Blender 4.5

## Baseline and source manifests

Historical supplied-baseline manifests:

- `docs/project_state/baseline_manifests/WITCH_TOOLS_DEV_2_4_0.json`
- `docs/project_state/baseline_manifests/WITCH_QUICKBAR_DEV_1_3_18.json`
- `docs/project_state/baseline_manifests/WITCH_DEV_MODULES_0_0_9.json`

Current development preservation:

- Witch Tools Dev_v2.6.1 isolated snapshot manifest: complete and verified.
- Quickbar Dev_v1.4.0 isolated snapshot manifest: pending.
- Direct unpacked development source layouts and source-derived registries: pending.

## Rule

Do not replace a verified or candidate-current entry with a remembered version unless replacement files are hashed, compared, and explicitly recorded.
