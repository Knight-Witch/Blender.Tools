# Blender.Tools Project State

Last updated: 2026-07-24

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Development branch: `Blender_Dev`
- Default branch: `Witch_Main_Tools`
- Public Quickbar branch: `Witch_Quick_Access`
- Default Witch Tools target: Blender `4.5`
- Public branches, package identities, update URLs, and release paths: unchanged

## Current development builds

### Witch Tools

- Current build: `Dev_v2.7.0`
- Artifact: `Witch_Tools_Dev_v2_7_0_Align_Selection_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- Target: Blender `4.5.0`
- Source snapshot: complete and verified on `Blender_Dev`
- Runtime: Blender validation pending

### Witch Quickbar

- Current delivered companion build: `Dev_v1.5.0`
- Artifact: `witch_quickbar_dev_Dev_v1_5_0_Align_Selection_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- SHA-256: `d2ace3cd3310686664cebfce6242717af3afed3f5954a4bd3cd6bc2a26eded5c`
- Target: Blender `4.5.0`
- Source handling: local-only; GitHub Quickbar source intentionally not updated
- Supersedes local Dev_v1.4.0 package for this workflow
- Existing Dev_v1.4.0 Selection Slots workflow: user-reported passed in Blender 4.5
- Dev_v1.5.0 runtime: pending

### Witch's Dev Modules

- Version: `Dev_v0.0.9`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Original packaging defect: 34 `.pyc` files

## Last completed work

- Added the canonical Align Selection backend and N-panel to Witch Tools Dev_v2.7.0.
- Added Match Coordinates and shape-preserving Move Shape modes.
- Added independent Per Selected Island alignment for multiple cavities.
- Added world-space multi-object conversion, persistent source/anchor captures, and strict preflight.
- Added local Quickbar Dev_v1.5.0 Edit-tab controls that invoke Witch Tools without duplicating geometry logic.
- Added complete Align Selection feature documentation and test plan.
- Built, hashed, and verified both distributable ZIPs.
- Added and verified the Witch Tools Dev_v2.7.0 isolated source snapshot.
- Did not update Quickbar source on GitHub, per user instruction.

## Current known-working state

Previously user-validated:

- Witch Tools Dev_v2.5.2 Curvature Sync production collar workflow in Blender 4.5.
- Quickbar Dev_v1.4.0 Selection Slots workflow in Blender 4.5.

Dev_v2.7.0 / Dev_v1.5.0 validation outside Blender:

- 48 Witch Tools and 14 Quickbar Python files parsed;
- duplicate operator-ID scans passed;
- pure alignment math and component tests passed;
- synthetic Figure-B-style cavity translation preserved relative distances;
- two disconnected cavities aligned independently in synthetic planning;
- lock cancellation and malformed-case tests passed;
- Quickbar layout and unavailable-backend tests passed;
- ZIP integrity and package hygiene passed;
- Witch Tools source snapshot reconstruction passed.

## Active problems

1. Blender 4.5 runtime testing for Align Selection is pending.
2. N-panel and Quickbar visual/interaction regression is pending.
3. Real BMesh capture, multi-object, multi-island, undo/redo, lock, shape-key, and save/reopen tests are pending.
4. Selection Slots Dev_v2.6.1 N-panel hotfix still lacks recorded Blender 4.5 confirmation.
5. Quickbar Dev_v1.5.0 is local-only and has no GitHub source snapshot.
6. Direct unpacked development source layouts and source-derived registries remain pending.
7. Final collar normals/manifold/print-fit inspection remains pending.
8. Witch Core source import remains pending.

## Next exact implementation step

Install Witch Tools Dev_v2.7.0 first, then local Quickbar Dev_v1.5.0. Test Figure A, Figure B, and two disconnected cavities in Blender 4.5, including undo/redo. Then test multi-object transforms, reference capture domains, locks, stale markers, shape-key cancellation, save/reopen, and Quickbar overlay regression.

## Test status

- Curvature Sync Blender 4.5: user-reported passed
- Quickbar Dev_v1.4.0 Select workflow: user-reported passed
- Align Selection static/core/synthetic tests: passed
- Dev_v2.7.0 source snapshot reconstruction: passed
- Align Selection Blender 4.5: pending
- Quickbar Dev_v1.5.0 overlay/runtime: pending
- Public branches/URLs modified: no
