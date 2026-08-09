## Witch Tools Dev_v2.10.1 — 2026-08-08

- Intended Blender target: 4.5.0
- Runtime baseline: Dev_v2.10.0 user-tested in Blender 4.5; merge/navigation/undo defects found
- Dev_v2.10.1 runtime verification: pending
- Additional Blender versions verified for Dev_v2.10.1: none
- Public releases / Quickbar: unchanged

# Blender Version Compatability

The filename retains the historical project spelling for continuity.

Last updated: 2026-08-05

## Policy

- Default development target: Blender 4.5 unless explicitly changed.
- A version is listed as tested only when the relevant build was actually run and verified.
- Static parsing and remembered reports are not substitutes for runtime records.

## Witch Quickbar / Witch Dock

### Public v1.0.2 / internal 1.2.8

- Target: Blender 4.5.0
- Branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Runtime verification in the current audit: not performed

### Guided Align integration

- Not implemented in Witch Quickbar/Witch Dock in this pass.
- A thin wrapper is deferred until Witch Tools Dev_v2.8.0 passes Blender 4.5 backend validation.

### Development Dev_v1.4.0 — Select tab

- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- Target: Blender 4.5.0
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Static audit: passed for 13 Python files and 36 PNG assets
- Blender 4.5 result: user reported the Selection Slots Select workflow worked perfectly
- Remaining limitations: full overlay/pass-through/drag/resize/lock/file-load/undo/backend-unavailable/side-by-side/update-launch regression remains pending

## Witch Tools

### Development Dev_v2.8.0 — Align Vertices / Edges / Faces candidate

- Artifact: `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- Target: Blender 4.5.0
- Size: 138,473 bytes
- SHA-256: `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`
- Source-tree SHA-256: `076912ce5d84115adb803ebfa793e04117053fe9af45d459cd4cbdb7be853504`
- Source baseline: verified Dev_v2.6.1 reconstruction; Dev_v2.7.0 snapshot parts were incomplete
- Static validation:
  - 48 Python files parsed and compiled;
  - duplicate scan passed for 99 operator/panel identifiers;
  - seven Guided Align operator IDs confirmed;
  - UI-state consistency passed;
  - seven pure constraint-math assertions passed;
  - patch reconstruction and source-tree equality passed;
  - ZIP integrity, safe paths, package root, and cache exclusion passed.
- Blender 4.5 runtime verification: not performed
- Required runtime tests: registration/UI, world-axis alignment, rail sliding, paired rails, custom guide, shape preservation, multi-object conversion, locks/errors, undo/redo, and save/reopen
- Known limitations: straight rails only; paired rails require one parent vertex per rail component; ambiguous multi-rail targets rejected; multiple shape keys unsupported; linked-mesh markers shared

### Development Dev_v2.7.1 — superseded documented hotfix

- Target: Blender 4.5.0
- Artifact SHA-256: `e68cf22a2db2ab426781bf8acfc2bfdbb8d6f1c8f62c42e1ccf166d30d6b467f`
- Static checks were recorded as passed.
- Blender runtime remained pending.
- Source limitation: the repository's Dev_v2.7.0 snapshot parts are truncated, so the complete Dev_v2.7.1 source cannot be reconstructed from the committed snapshot plus hotfix patch.

### Development Dev_v2.6.1 — Selection Slots N-panel hotfix

- Artifact: `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- Target: Blender 4.5.0
- SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Static audit: passed for 46 Python files; no generated cache files
- Simulated UI tests: expanded, collapsed, populated, empty scene, and initial Slot 1 creation passed
- Blender 4.5 runtime verification: pending user test
- Retained runtime evidence: Quickbar Select workflow user-reported passed; Dev_v2.5.2 Curvature Sync production workflow user-reported passed

### Development Dev_v2.6.0 — superseded initial Selection Slots build

- Artifact SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Blender 4.5 result: Quickbar integration worked, but the Witch Tools N-panel body failed to reveal its rows
- Status: superseded by Dev_v2.6.1

### Development Dev_v2.5.2 — superseded Curvature Sync column repair

- Artifact SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Automated runtime: Blender Python 5.2.0 LTS
- Blender 4.5 production workflow: user-reported passed
- Remaining limitations: undo/redo, formal normals/manifold, print-fit/slicer, and release/update testing

### Earlier preserved builds

- Dev_v2.5.1: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Dev_v2.5.0: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Dev_v2.4.0: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`

## Witch's Dev Modules

- Host: Dev_v0.0.9
- Artifact: `witch_dev_modules.zip`
- Target: Blender 4.5.0
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Static audit: passed
- Runtime verification: pending
- Packaging limitation: original archive contains generated `.pyc` files

## Witch Core

- Intended target: Blender 4.5
- Exact build/runtime verification: pending source import

## Required test record

Record component/version, artifact/source, Blender version, OS, date, features, result, changes required, limitations, and tester.
