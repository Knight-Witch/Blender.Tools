# Align Selection State

Last updated: 2026-07-24

## Status

- Feature ID: `WT-ALIGN-001`
- Current implementation: Witch Tools `Dev_v2.7.0`
- Canonical owner: Witch Tools
- Quickbar role: local-only compact integration in `Dev_v1.5.0`
- Target Blender version: `4.5.0`
- Runtime status: implemented and statically/synthetically tested; Blender runtime pending

## Implemented

- Persistent source and target-anchor capture from vertex, edge, face, or mixed selections.
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

## Build identities

### Witch Tools

- Artifact: `Witch_Tools_Dev_v2_7_0_Align_Selection_Blender_4_5.zip`
- SHA-256: `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`
- Package: `Witch_Tools_Dev`

### Local Quickbar companion

- Artifact: `witch_quickbar_dev_Dev_v1_5_0_Align_Selection_Blender_4_5.zip`
- SHA-256: `d2ace3cd3310686664cebfce6242717af3afed3f5954a4bd3cd6bc2a26eded5c`
- Package: `witch_quickbar_dev`
- Repository source update: intentionally not performed per user instruction

## Testing completed

- Witch Tools: all 48 Python files parsed successfully.
- Quickbar: all 14 Python files parsed successfully.
- Duplicate operator-ID scans passed: 95 Witch Tools IDs and 33 Quickbar IDs.
- Pure alignment-core tests passed for axis masks, matching, translation deltas, averaging, connectivity, distance preservation, and edge cases.
- Synthetic operator-planning tests passed for independent translation of two disconnected cavities, preserved cavity widths, Whole Selection translation, Match Coordinates flattening, and locked-vertex cancellation.
- Synthetic Quickbar layout produced all 12 controls over four content rows.
- Quickbar unavailable-backend and thin operator-invocation tests passed.
- ZIP integrity, safe paths, and package hygiene passed.
- Witch Tools Dev_v2.7.0 source snapshot reconstruction and source-tree verification passed locally.

## Testing pending

- Blender 4.5 registration and unregistration.
- Actual N-panel rendering.
- Actual Quickbar overlay rendering, hit targets, pass-through, drag, resize, and lock regression.
- Real BMesh capture and application.
- Multi-object Edit Mode runtime.
- Per-island runtime with multiple cavities.
- Vertex Lock and shape-key behavior inside Blender.
- Undo/redo.
- Save/reopen capture persistence.
- Public update behavior, which was not changed.

## Known remaining issues

- Arithmetic-mean source/anchor reference only.
- Topology changes can invalidate or propagate marker layers; count mismatches require recapture.
- Linked objects sharing a Mesh datablock share source/anchor markers.
- Protected Edit Zone integration requires Blender runtime confirmation.
- Source vertices are always excluded from movement.
