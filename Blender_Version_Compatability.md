# Blender Version Compatability

The filename retains the historical project spelling for continuity.

Last updated: 2026-07-20

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

### Development Dev_v2.4.0

- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification in this audit: not performed
- Additional versions verified in this audit: none
- Known compatibility limitations: install, registration, UI, operators, undo, and feature behavior remain untested in the current repository audit

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
