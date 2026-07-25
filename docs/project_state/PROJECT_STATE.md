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

- Current build: `Dev_v2.7.1`
- Artifact: `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- Size: 132,189 bytes
- SHA-256: `e68cf22a2db2ab426781bf8acfc2bfdbb8d6f1c8f62c42e1ccf166d30d6b467f`
- Target: Blender `4.5.0`
- Source record: verified patch and manifest on `Blender_Dev`
- Runtime: N-panel hotfix pending user validation

### Witch Quickbar

- Current delivered companion build: `Dev_v1.5.0`
- Package: `witch_quickbar_dev`
- Target: Blender `4.5.0`
- Source handling: local-only; GitHub Quickbar source intentionally not updated
- Runtime finding: Align Selection controls render, but source-reference dropdown is not exposed
- This Witch Tools hotfix does not replace or modify Quickbar

## Baseline discrepancy

The exact replacement Dev_v2.7.0 ZIP used in the user's test had SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`. Earlier repository records referenced a different Dev_v2.7.0 artifact, SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`.

Dev_v2.7.1 uses the exact failing replacement package as its patch baseline, records the conflict explicitly, and supersedes both Dev_v2.7.0 identities.

## Last completed work

- Diagnosed the empty Witch Tools Align Selection N-panel box.
- Added the missing `show_edit_align_selection` persistent preference.
- Replaced the invalid/unverified `ALIGN` section icon with `PIVOT_ACTIVE`.
- Built Witch Tools Dev_v2.7.1 without changing alignment operators or Quickbar contracts.
- Added a focused patch, manifest, and corrected build identity to the Witch Tools development source area.
- Updated Align Selection feature docs, Witch Tools state/roadmap/UI map/notes, root state/build registry/notes, and source-record index.
- Quickbar source and public branches remained unchanged.

## Current known-working state

Previously user-validated:

- Witch Tools Dev_v2.5.2 Curvature Sync production collar workflow.
- Quickbar Dev_v1.4.0 Selection Slots workflow.
- Quickbar Dev_v1.5.0 Align Selection section rendering.

Dev_v2.7.1 validation outside Blender:

- 47 Python files parsed and compiled;
- 96 operator IDs have no duplicates;
- Align Selection UI-state declaration consistency passed;
- invalid icon reference removed;
- ZIP integrity, safe paths, and package hygiene passed;
- source patch/manifest verification passed.

## Active problems

1. Blender 4.5 confirmation of the Dev_v2.7.1 Align Selection N-panel is pending.
2. Real BMesh capture/application, multi-object, multi-island, undo/redo, locks, shape keys, and save/reopen remain pending.
3. Quickbar Dev_v1.5.0 source-reference UI will be patched separately and locally only.
4. Full Quickbar overlay regression remains pending.
5. Direct unpacked development source layout and source-derived registries remain pending.
6. Final collar normals/manifold/print-fit inspection remains pending.
7. Witch Core source import remains pending.

## Next exact implementation step

Install Witch Tools Dev_v2.7.1 and confirm the N-panel section renders fully. Test the Median/Active Element dropdown, Figure A, Figure B, and undo/redo. After Witch Tools passes, patch the local-only Quickbar reference-mode controls.

## Test status

- Curvature Sync Blender 4.5: user-reported passed
- Quickbar Align section rendering: user-reported passed
- Witch Tools Dev_v2.7.0 Align N-panel: failed, empty box
- Witch Tools Dev_v2.7.1 static/package/source-record checks: passed
- Witch Tools Dev_v2.7.1 Blender 4.5: pending
- Quickbar source updated on GitHub: no
- Public branches/URLs modified: no
