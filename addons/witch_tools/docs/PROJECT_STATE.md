# Witch Tools Project State

Last updated: 2026-07-24

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable operator backend
- Development branch: `Blender_Dev`
- Development package: `Witch_Tools_Dev`
- Default target Blender version: `4.5`

## Current development build

- Version: `Dev_v2.7.0`
- Artifact: `Witch_Tools_Dev_v2_7_0_Align_Selection_Blender_4_5.zip`
- SHA-256: `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- Supersedes: `Dev_v2.6.1`
- Package folder: `Witch_Tools_Dev`
- Declared target: Blender `4.5.0`
- Python source files: 48
- PNG assets: 6
- Generated cache files: none
- Blender runtime: not performed; exact Blender 4.5 validation pending

## Current implementation

Dev_v2.7.0 retains the Dev_v2.6.1 Selection Slots hotfix, user-validated Curvature Sync workflow, Replace Misaligned Column Edges, Auto-Aligned Vertex Inject, Object Snap, Vertex Locks/Protected Edit Zones, and all existing Dev_v2.x tools.

Dev_v2.7.0 adds **Edit Tools > Align Selection**:

- persistent Source and Target Anchor capture from vertex, edge, face, and mixed selections;
- Match Coordinates for direct world-space X/Y/Z coordinate assignment;
- Move Shape for translating complete selected geometry while preserving internal dimensions;
- Whole Selection and Per Selected Island grouping;
- independent alignment of multiple disconnected cavities;
- multi-object Edit Mode world/local coordinate conversion;
- Vertex Lock, stale-capture, missing-anchor, shape-key, and transform preflight;
- transactional planning before coordinate mutation;
- stable `mesh.wt_align_*` operator integration for Quickbar.

Feature packet: `docs/features/align_selection/`.

## Companion Quickbar build

A local-only Quickbar integration was produced without updating Quickbar source on GitHub, per user instruction:

- Version: `Dev_v1.5.0`
- Artifact: `witch_quickbar_dev_Dev_v1_5_0_Align_Selection_Blender_4_5.zip`
- SHA-256: `d2ace3cd3310686664cebfce6242717af3afed3f5954a4bd3cd6bc2a26eded5c`
- Role: compact Edit-tab controls invoking the canonical Witch Tools backend
- Repository Quickbar source/import: intentionally unchanged

## Isolated development source snapshot

The exact Dev_v2.7.0 Witch Tools source is preserved at:

`addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_7_0/`

Verification identity:

- Source ZIP: 136,327 bytes; SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- Reconstructed `.tar.xz`: 85,712 bytes; SHA-256 `2a73eaeb209602b30c4ee8e3378961038249ca3782cac23b7ad5923e3d994cab`
- Package root: `Witch_Tools_Dev`
- Extracted source: 63 files; 412,416 bytes
- Deterministic source-tree SHA-256: `c8ece8e4e0a750763e90ccabaa16cf6c0e1f0f8f01a06f67b2bbea1ae3d752b5`
- Ordered part, archive, safe extraction, package-root, file-count, byte-count, and source-tree verification: passed locally

## Last completed work

- Implemented and packaged Witch Tools Dev_v2.7.0 Align Selection.
- Implemented local Quickbar Dev_v1.5.0 thin integration.
- Added the Align Selection specification, state, roadmap, decisions, and test plan.
- Added a reproducible Dev_v2.7.0 source snapshot and manifest.
- Updated Witch Tools package documentation, compatibility notes, changelogs, root state, build registry, and latest/full notes.
- Preserved public branches, package identities, update URLs, and official release paths.

## Current known-working state

Previously user-validated in Blender 4.5:

- Dev_v2.5.2 Curvature Sync production collar workflow.
- Quickbar Dev_v1.4.0 Selection Slots workflow.

Dev_v2.7.0 validation completed outside Blender:

- all 48 Witch Tools Python files parse;
- 95 Witch Tools operator IDs have no duplicates;
- ZIP integrity, safe paths, and package hygiene passed;
- pure alignment-core tests passed;
- synthetic two-cavity Per Selected Island planning preserved cavity widths;
- Whole Selection, Match Coordinates, and locked-vertex cancellation tests passed;
- source snapshot reconstruction and tree verification passed.

Local Quickbar Dev_v1.5.0 validation completed outside Blender:

- all 14 Python files parse;
- 33 operator IDs have no duplicates;
- synthetic layout produced all expected controls;
- unavailable-backend and thin operator-invocation tests passed;
- ZIP integrity and package hygiene passed.

## Active problems

1. Witch Tools Dev_v2.7.0 registration, N-panel rendering, real mesh execution, and undo/redo require Blender 4.5 validation.
2. Quickbar Dev_v1.5.0 overlay layout, hit targets, pass-through, drag, resize, lock, and file-load behavior require Blender 4.5 validation.
3. Selection Slots Dev_v2.6.1 N-panel hotfix still lacks recorded Blender 4.5 confirmation.
4. Align Selection capture markers can be invalidated or propagated by topology changes; stale count mismatches require recapture.
5. Linked objects sharing one Mesh datablock share Align Selection and Selection Slot markers.
6. Shape-key-relative alignment, Active Element references, rotation, scale, custom frames, and projection are not implemented.
7. Final collar normals/manifold/print-fit inspection remains pending independently.

## Next exact implementation step

1. Install Witch Tools Dev_v2.7.0 and local Quickbar Dev_v1.5.0 in Blender 4.5.
2. Test Figure A: capture Source, select wall, Match Coordinates, X, Apply, undo/redo.
3. Test Figure B: capture Source and Target Anchor, select complete cavity, Move Shape, X, Apply, undo/redo.
4. Test two disconnected cavities with Per Selected Island.
5. Test vertex/edge/face captures, multi-object Edit Mode, locks, stale captures, save/reopen, and shape-key cancellation.
6. Patch only failures found before official integration.

## Files changed

Witch Tools runtime/package snapshot includes:

- `align_selection_core.py`
- `operators_align_selection.py`
- `ALIGN_SELECTION_QUICK_START.md`
- registration, properties, state, preferences, panel, UI operator, version, README, changelog, notes, and compatibility updates

Repository documentation:

- `docs/features/align_selection/*`
- `addons/witch_tools/docs/PROJECT_STATE.md`
- `addons/witch_tools/docs/ROADMAP.md`
- `addons/witch_tools/docs/UI_MAP.md`
- Witch Tools latest/full notes
- root project state, build registry, and latest/full notes
- Dev_v2.7.0 source snapshot and verification records

## Test status

- Static syntax: passed
- Duplicate operator IDs: passed
- Pure core tests: passed
- Synthetic operator planning: passed
- Synthetic Quickbar integration/layout: passed
- ZIP integrity/safe paths/package hygiene: passed
- Source snapshot reconstruction: passed
- Blender 4.5 runtime: not performed
- Undo/redo: not performed
- Save/reopen: not performed
- Public release/update behavior: unchanged and not retested
