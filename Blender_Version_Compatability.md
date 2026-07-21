# Blender Version Compatability

The filename retains the historical project spelling for continuity.

Last updated: 2026-07-21

## Policy

- Default development target: Blender 4.5 unless explicitly changed.
- A version is listed as tested only when the relevant build was actually run and verified.
- Public descriptions, source metadata, static parsing, and remembered reports are not substitutes for a runtime test record.

## Witch Quickbar

### Public v1.0.2 / internal 1.2.8

- Intended Blender target in tracked source metadata: 4.5.0
- Repository branch: `Witch_Quick_Access`
- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Blender 4.5 runtime verification in this audit: not performed
- Additional versions verified in this audit: none
- Known compatibility limitations: pending installed public-package and update-link tests

### Development Dev_v1.3.18

- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package folder: `witch_quickbar_dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification in this audit: not performed
- Additional versions verified in this audit: none
- Known compatibility limitations: registration, overlay behavior, side-by-side public/dev installation, and update-button launch remain untested

## Witch Tools

### Development Dev_v2.5.0 — Curvature Sync MVP

- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Static Python/package audit: passed
- Runtime environment actually tested: Blender Python `5.2.0 LTS`
- Blender 4.5 runtime verification: not performed; user test pending
- Operating environment: Linux container for automated checks
- Features tested: registration/unregistration, synthetic circular chain repair, vertex injection, shared-face splitting, exact middle normalization, locked-anchor behavior, locked-interior rejection, invalid-selection cancellation, actual two-object collar repair, save/reopen, geometry validity, manifold comparison, 3D edge-intersection comparison
- Result: tested operations passed in Blender Python 5.2.0 LTS; the collar test reported 41 unresolved column positions rather than forcing them
- Known compatibility limitations: normal Blender 4.5 UI interaction and interactive undo/redo remain unverified
- Tester: OpenAI container test harness using the user-supplied source and `.blend` file

### Development Dev_v2.4.0 — superseded candidate baseline

- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification in the baseline audit: not performed
- Status: preserved source baseline used to produce Dev_v2.5.0

## Witch's Dev Modules

### Host Dev_v0.0.9

- Artifact: `witch_dev_modules.zip`
- Package folder: `witch_dev_modules`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification in this audit: not performed
- Additional versions verified in this audit: none
- Packaging limitation: supplied archive contains generated `.pyc` files for Python 3.11 and 3.13; canonical source/builds must exclude them
- Documentation limitation: package documentation is not consistently normalized to host Dev_v0.0.9

## Witch Core

### Current development baseline

- Intended target: expected Blender 4.5 under project rules
- Exact build/version: unverified pending source import
- Runtime verification: not performed

## Test-record format

Each future entry must include:

- component and version
- source commit/artifact
- Blender version
- operating system
- date
- features tested
- result
- changes required
- known limitations
- tester