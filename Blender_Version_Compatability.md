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

### Development Dev_v2.5.2 — Curvature Sync column repair

- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Static Python/package audit: passed for 45 Python files; no generated cache files shipped
- Runtime environment actually tested: Blender Python `5.2.0 LTS`
- Blender 4.5 runtime verification: not performed; user test pending
- Operating environment: Linux container for automated checks
- Features tested: registration/unregistration, actual 26-chain collar Curvature Sync, missing-vertex injection, curvature movement, detection and replacement of 96 misaligned existing column edges, canonical column reconstruction, exact coordinate regression, topology-degeneracy and duplicate checks, boundary-count comparison, special-data preflight rejection, save/reopen
- Result: 520 vertices injected, 1,324 moved, 96 misaligned edges replaced, 975 canonical column edges created, and zero unresolved column positions in the tested collar file
- Regression result: resulting vertex-coordinate multisets exactly matched the successful Dev_v2.5.1 curvature result; the patch changed topology correspondence rather than the intended curve coordinates
- Known compatibility limitations: normal Blender 4.5 UI interaction, installed-package behavior, and interactive undo/redo remain unverified; only safe two-face interior misaligned edges are replaced
- Tester: OpenAI container test harness using the user-supplied Dev package and pre/post `.blend` files

### Development Dev_v2.5.1 — superseded Vertex Inject + Curvature Sync build

- Artifact: `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Archive SHA-256: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Runtime environment actually tested: Blender Python `5.2.0 LTS`
- Blender 4.5 runtime verification: not performed
- Status: superseded by Dev_v2.5.2 after the production collar exposed retained misaligned existing column edges

### Development Dev_v2.5.0 — superseded Curvature Sync MVP

- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Static Python/package audit: passed
- Runtime environment actually tested: Blender Python `5.2.0 LTS`
- Blender 4.5 runtime verification: not performed
- Result: first circular Curvature Sync MVP; superseded by Dev_v2.5.1 and Dev_v2.5.2

### Development Dev_v2.4.0 — superseded candidate baseline

- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification in the baseline audit: not performed
- Status: preserved source baseline used to produce Dev_v2.5.x

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