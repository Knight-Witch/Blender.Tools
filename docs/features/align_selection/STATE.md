# Align Selection State

Last updated: 2026-07-24

## Status

- Feature ID: `WT-ALIGN-001`
- Current implementation: Witch Tools `Dev_v2.7.1`
- Canonical owner: Witch Tools
- Quickbar role: local-only compact integration in `Dev_v1.5.0`; unchanged by this hotfix
- Target Blender version: `4.5.0`
- Runtime status: N-panel rendering defect diagnosed and patched; Blender 4.5 confirmation pending

## Dev_v2.7.1 hotfix

User testing of the replacement Dev_v2.7.0 ZIP showed an empty N-panel box at the Align Selection position while the local Quickbar controls rendered.

Root cause:

- `state.UI_STATE_PROPS` and `panel_edit_tools.py` referenced `show_edit_align_selection`;
- `WitchToolsPreferences` did not register that property;
- the N-panel draw path stopped while constructing the Align Selection disclosure header;
- the section also referenced an unverified `ALIGN` icon identifier.

Correction:

- registered `show_edit_align_selection` as a persistent Boolean preference, defaulting to expanded;
- changed the section icon to the existing valid `PIVOT_ACTIVE` icon;
- retained all Dev_v2.7.0 alignment operators and property contracts unchanged.

## Implemented

- Persistent source and target-anchor capture from vertex, edge, face, or mixed selections.
- Median and Active Element source-reference modes in Witch Tools.
- World-space X/Y/Z coordinate matching.
- Match Coordinates mode for direct target flattening.
- Move Shape mode for shape-preserving translation.
- Whole Selection and Per Selected Island translation.
- Multiple disconnected cavity/island planning.
- Multi-object Edit Mode coordinate conversion.
- Vertex Lock preflight.
- Shape-key rejection.
- Stale capture-count detection.
- Preflight planning before mutation.
- Witch Tools N-panel controls.
- Thin local Quickbar Edit-tab integration.

## Build identity

- Artifact: `Witch_Tools_Dev_v2_7_1_Align_Selection_NPanel_Hotfix_Blender_4_5.zip`
- SHA-256: `f4783b620325e6c40c156d9aa05e2479ca0e0159b06f4177138b46bbfbc4c110`
- Package: `Witch_Tools_Dev`
- Baseline: exact user-tested replacement Dev_v2.7.0 ZIP, SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`

The replacement Dev_v2.7.0 ZIP differed from the earlier Dev_v2.7.0 snapshot identity recorded on GitHub. Dev_v2.7.1 explicitly supersedes both Dev_v2.7.0 identities and records the tested replacement artifact as its patch baseline.

## Testing completed

- All 47 Python files parsed and compiled.
- Duplicate operator-ID scan passed for 96 identifiers.
- UI-state consistency check confirmed `show_edit_align_selection` exists in both the preference declarations and registry.
- Panel source no longer references `section_icon='ALIGN'`.
- ZIP integrity, safe paths, single package root, and cache-file exclusion passed.
- Dev_v2.7.1 patch manifest and source patch were recorded on `Blender_Dev`.

## Testing pending

- Blender 4.5 registration and unregistration.
- Actual Align Selection N-panel header/body rendering.
- Disclosure persistence across restart/update.
- Actual source-reference dropdown behavior.
- Real BMesh capture and application.
- Multi-object and multiple-cavity runtime.
- Vertex Lock and shape-key behavior inside Blender.
- Undo/redo and save/reopen.
- Quickbar dropdown/layout work, which is intentionally deferred to the next local-only Quickbar pass.

## Known remaining issues

- The local Quickbar Dev_v1.5.0 does not yet expose the Witch Tools source-reference dropdown.
- Topology changes can invalidate or propagate marker layers; count mismatches require recapture.
- Linked objects sharing a Mesh datablock share source/anchor markers.
- Protected Edit Zone integration requires Blender runtime confirmation.
