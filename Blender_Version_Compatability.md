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
- Additional versions verified: none
- Known limitations: pending installed public-package and update-link tests

### Development Dev_v1.4.0 — Select tab

- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package folder: `witch_quickbar_dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Static Python/package/asset audit: passed for 13 Python files and 36 PNG assets
- Blender 4.5 runtime verification: not performed
- Additional versions verified: none
- Known compatibility limitations: registration, overlay drawing, Selection Slots dependency integration, slot drag/reorder, resize responsiveness, tooltip/input pass-through, file-load recovery, undo/redo, side-by-side install, and update-button launch remain untested

### Development Dev_v1.3.18 — superseded baseline

- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package folder: `witch_quickbar_dev`
- Archive SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Static audit: passed
- Status: superseded by Dev_v1.4.0; preserved source baseline

## Witch Tools

### Development Dev_v2.6.0 — Selection Slots

- Artifact: `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Static Python/package audit: passed for 46 Python files; no generated cache files shipped
- Blender 4.5 runtime verification for Selection Slots: not performed
- Additional versions verified for Selection Slots: none
- Retained runtime evidence: Dev_v2.5.2 Curvature Sync production workflow was user-reported successful in Blender 4.5 and is included in Dev_v2.6.0
- Known compatibility limitations: Dev_v2.6.0 registration, N-panel rendering/native icons, vertex/edge/face/mixed and multi-object restore, save/reopen persistence, custom-data propagation, and interactive undo/redo remain unverified

### Development Dev_v2.5.2 — superseded Curvature Sync column repair

- Artifact: `Witch_Tools_Dev_v2_5_2_Curvature_Sync_Column_Repair_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Archive SHA-256: `0b61992f09e745f011a13a45a29e5d8e342e0ab7c4e4405d828c76dfb85ef42a`
- Automated runtime actually tested: Blender Python `5.2.0 LTS` in a Linux container
- Blender 4.5 production workflow: user-reported passed on the supplied pre-curvature collar file
- User-tested behavior: add-on installed, Curvature Sync panel/workflow usable, saved anchors/selection available, Analyze/Apply completed, and corrected curvature/column result visually confirmed
- Automated result: 520 vertices injected, 1,324 moved, 96 misaligned edges replaced, 975 canonical column edges created, zero unresolved positions
- Remaining limitations: interactive undo/redo, formal normals/manifold checks, print-fit/slicer validation, update behavior, and public installation/upgrade testing
- Status: superseded by Dev_v2.6.0 but retained as the user-validated Curvature Sync baseline

### Development Dev_v2.5.1 — superseded Vertex Inject + Curvature Sync build

- Artifact: `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`
- Archive SHA-256: `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`
- Status: superseded by Dev_v2.5.2

### Development Dev_v2.5.0 — superseded Curvature Sync MVP

- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- Archive SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Static/runtime environment: passed selected tests under Blender Python `5.2.0 LTS`
- Status: superseded

### Development Dev_v2.4.0 — superseded candidate baseline

- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package folder: `Witch_Tools_Dev`
- Archive SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification in baseline audit: not performed
- Status: preserved source baseline used to produce Dev_v2.5.x and Dev_v2.6.0

## Witch's Dev Modules

### Host Dev_v0.0.9

- Artifact: `witch_dev_modules.zip`
- Package folder: `witch_dev_modules`
- Intended Blender target in source metadata: 4.5.0
- Archive SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Static Python syntax audit: passed
- Blender 4.5 runtime verification: not performed
- Additional versions verified: none
- Packaging limitation: supplied archive contains generated `.pyc` files for Python 3.11 and 3.13; canonical builds must exclude them
- Documentation limitation: package documentation is not consistently normalized to host Dev_v0.0.9

## Witch Core

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
