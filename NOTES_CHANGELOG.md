# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-24

## Witch Tools Dev_v2.7.0 — Align Selection

- Added the canonical Align Selection backend and N-panel controls under Edit Tools.
- Added persistent Source and Target Anchor capture for vertex, edge, face, and mixed selections.
- Added Match Coordinates for direct world-space X/Y/Z assignment.
- Added Move Shape to align an anchor while preserving the complete selected shape.
- Added Whole Selection and Per Selected Island, including independent alignment of multiple cavities.
- Added multi-object world/local conversion and strict preflight for locks, stale captures, missing anchors, shape keys, and invalid transforms.
- Produced `Witch_Tools_Dev_v2_7_0_Align_Selection_Blender_4_5.zip`, SHA-256 `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`.
- Added a verified Dev_v2.7.0 source snapshot on `Blender_Dev`.

## Local Quickbar Dev_v1.5.0

- Added compact Align Selection controls to the Edit tab.
- The Quickbar calls Witch Tools operators/properties and contains no duplicate geometry backend.
- Produced `witch_quickbar_dev_Dev_v1_5_0_Align_Selection_Blender_4_5.zip`, SHA-256 `d2ace3cd3310686664cebfce6242717af3afed3f5954a4bd3cd6bc2a26eded5c`.
- Quickbar source was intentionally not updated on GitHub per user instruction.

## Testing

- Static syntax, duplicate operator IDs, pure core tests, synthetic operator planning, Quickbar layout/integration, ZIP integrity, package hygiene, and Witch Tools snapshot reconstruction passed.
- Blender 4.5 registration, real mesh execution, N-panel/overlay UI, undo/redo, save/reopen, multi-object/multi-island runtime, locks, and shape-key behavior remain pending.

## Compatibility

No public branch, package identity, update URL, inherited asset path, or public release location changed.
