# Witch Tools Project State

Last updated: 2026-07-23

## Current baseline

- Add-on: Witch Tools
- Development branch: `Blender_Dev`
- Package: `Witch_Tools_Dev`
- Current build: `Dev_v2.6.1`
- Artifact: `Witch_Tools_Dev_v2_6_1_Selection_Slots_NPanel_Hotfix_Blender_4_5.zip`
- Artifact SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Target Blender version: `4.5.0`
- Public branches and official source/release paths: unchanged

## Current implementation

Dev_v2.6.1 retains Selection Slots, Curvature Sync, Replace Misaligned Column Edges, Auto-Aligned Vertex Inject, Vertex Locks/Protected Edit Zones, and the existing Dev_v2.x workflows. It changes only the Selection Slots N-panel presentation and empty-slot initialization paths from Dev_v2.6.0.

## Isolated development source snapshot

The exact Dev_v2.6.1 source is preserved at `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/`.

- Manifest: `manifest.json`
- Restore/verification utility: `tools/restore_dev_snapshot.py`
- Source ZIP: 127,401 bytes; SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`
- Reconstructed archive: 81,400 bytes; SHA-256 `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`
- Package root: `Witch_Tools_Dev`
- Extracted source: 60 files; 383,270 bytes
- Deterministic source-tree SHA-256: `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`
- Final ordered-part/archive/source-tree reconstruction verification: passed locally on 2026-07-23

This snapshot is development-only and remains separated from official/public source paths.

## Last completed work

- Implemented and packaged the Dev_v2.6.1 Selection Slots N-panel hotfix.
- Added the isolated source snapshot manifest.
- Replaced the malformed first snapshot part with four smaller verified parts and removed the superseded file.
- Hardened the restore tool to verify part sizes/hashes, archive size/hash, safe extraction, package root, file count, byte count, and source-tree digest.
- Completed final reconstruction verification.
- Updated snapshot, roadmap, build/state, and notes documentation.

## Current known-working state

- Dev_v2.5.2 Curvature Sync production collar workflow: user-reported passed in Blender 4.5.
- Quickbar Dev_v1.4.0 Select workflow: user-reported passed in Blender 4.5.
- Dev_v2.6.1 Python parse/compile, operator-ID, ZIP safety, package hygiene, and simulated panel tests: passed.
- Dev_v2.6.1 source snapshot reconstruction: passed.

## Active problems

1. Dev_v2.6.1 N-panel expansion and row interaction require Blender 4.5 validation.
2. Selection Slots save/reopen, multi-object behavior, topology propagation, and undo/redo remain incompletely tested.
3. Quickbar full overlay regression remains pending.
4. Quickbar Dev_v1.4.0 isolated source snapshot/import remains pending.
5. Direct unpacked development source layouts and source-derived registries remain pending after snapshot preservation.
6. Final collar normals/manifold/print-fit inspection remains pending.

## Next exact implementation step

1. Complete the Quickbar Dev_v1.4.0 isolated snapshot and reconstruction verification.
2. Test Witch Tools Dev_v2.6.1 in Blender 4.5, beginning with N-panel expansion and Slot 1 rendering.
3. Test Selection Slots Save/Reselect, management actions, save/reopen, multi-object behavior, and undo/redo.
4. Patch only failures found before official integration.

## Files changed for snapshot preservation

- `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/manifest.json`
- `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/parts/*.b64`
- `addons/witch_tools/dev/SNAPSHOT_VERIFICATION.md`
- `tools/restore_dev_snapshot.py`
- `addons/DEV_SOURCE_SNAPSHOTS.md`
- Witch Tools and root project state, roadmap, build registry, and notes files

## Test status

- Snapshot part verification: passed
- Archive reconstruction and SHA-256: passed
- Safe extraction: passed
- Package root/file count/byte count/tree digest: passed
- Blender 4.5 Dev_v2.6.1 UI/runtime: pending
- Public branch/release behavior: unchanged and not retested
