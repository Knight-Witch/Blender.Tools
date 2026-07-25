# Witch Tools Project State

Last updated: 2026-07-24

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable operator backend
- Development branch: `Blender_Dev`
- Development package: `Witch_Tools_Dev`
- Default target Blender version: `4.5`

## Current development build

- Version: `Dev_v2.7.1`
- Artifact: `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`
- Size: 132,189 bytes
- SHA-256: `e68cf22a2db2ab426781bf8acfc2bfdbb8d6f1c8f62c42e1ccf166d30d6b467f`
- Supersedes: both recorded Dev_v2.7.0 artifact identities
- Package folder: `Witch_Tools_Dev`
- Declared target: Blender `4.5.0`
- Python source files: 47
- PNG assets: 6
- Generated cache files: none
- Blender runtime: N-panel hotfix pending user confirmation

## Baseline conflict resolved

The Dev_v2.7.0 replacement ZIP actually installed and tested by the user had SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`. Earlier repository records also referenced a different Dev_v2.7.0 artifact, SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`.

Dev_v2.7.1 uses the exact user-tested failing replacement package as its repair baseline and explicitly supersedes both identities.

## Current implementation

Dev_v2.7.1 retains the Dev_v2.7.0 Align Selection backend, Selection Slots hotfix, user-validated Curvature Sync workflow, Replace Misaligned Column Edges, Auto-Aligned Vertex Inject, Object Snap, Vertex Locks/Protected Edit Zones, and existing Dev_v2.x tools.

The hotfix changes only N-panel presentation state:

- registers the missing `show_edit_align_selection` persistent preference;
- changes the section icon from invalid/unverified `ALIGN` to valid `PIVOT_ACTIVE`;
- leaves `mesh.wt_align_*` operators and alignment properties unchanged.

## Companion Quickbar build

Quickbar remains local-only and unchanged for this patch:

- Version: `Dev_v1.5.0`
- Role: compact Edit-tab controls invoking Witch Tools
- Known UI gap: source-reference dropdown is not exposed yet
- Repository Quickbar source: intentionally unchanged per user instruction

## Development source record

- Path: `addons/witch_tools/dev/patches/Dev_v2_7_1/`
- Contains the focused runtime/version patch, manifest, and delivered build identity.
- Static/compile, operator-ID, ZIP-integrity, safe-path, and package-hygiene verification: passed.
- A full Dev_v2.7.1 archive snapshot is deferred; the verified patch is the current repository source record for this hotfix.

## Last completed work

- Reproduced the user's empty Align Selection N-panel box from source inspection.
- Identified the missing preference property that stopped panel drawing.
- Identified the invalid/unverified section icon identifier.
- Implemented and rebuilt Dev_v2.7.1.
- Added a focused source patch and corrected manifest.
- Updated feature state, decisions, roadmap, test plan, UI map, project state, build registry, and latest/full notes.
- Did not modify Quickbar source or public branches.

## Current known-working state

Previously user-validated in Blender 4.5:

- Dev_v2.5.2 Curvature Sync production collar workflow.
- Quickbar Dev_v1.4.0 Selection Slots workflow.
- Quickbar Dev_v1.5.0 Align Selection controls render.

Dev_v2.7.1 validation outside Blender:

- 47 Python files parsed and compiled;
- 96 operator IDs have no duplicates;
- Align Selection disclosure property exists in preferences and the UI-state registry;
- invalid `ALIGN` icon reference removed;
- ZIP integrity, safe paths, package root, and package hygiene passed;
- source patch manifest verified.

## Active problems

1. Dev_v2.7.1 N-panel rendering requires Blender 4.5 confirmation.
2. Align Selection real-mesh execution, undo/redo, multi-object, multi-island, lock, stale-marker, shape-key, and save/reopen tests remain pending.
3. Quickbar Dev_v1.5.0 does not expose Median/Active Element and will be handled in a separate local-only patch.
4. Full Quickbar overlay regression remains pending.
5. Direct unpacked development source layout and source-derived registries remain pending.
6. Final collar normals/manifold/print-fit inspection remains pending independently.

## Next exact implementation step

1. Install Dev_v2.7.1 over Dev_v2.7.0.
2. Confirm the Align Selection N-panel header and controls render.
3. Confirm the reference dropdown contains Median and Active Element.
4. Test Match Coordinates on X and undo/redo.
5. Test Preserve Shape on one cavity, then two disconnected cavities.
6. After Witch Tools passes, patch the local-only Quickbar reference-mode UI.

## Test status

- Python parse/compile: passed
- Duplicate operator IDs: passed
- UI-state declaration consistency: passed
- Invalid Align icon regression: passed by source inspection
- ZIP integrity/safe paths/package hygiene: passed
- Source patch/manifest verification: passed
- Blender 4.5 N-panel rendering: pending
- Blender 4.5 Align Selection runtime: pending
- Quickbar source updated on GitHub: no
- Public branches/URLs modified: no
