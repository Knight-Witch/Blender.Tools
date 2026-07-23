# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-23

## Dev_v2.6.1 — Isolated source snapshot manifest and reconstruction verification

- Added the development-only snapshot manifest at `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/manifest.json`.
- Replaced the malformed original first Base64 part with four smaller verified parts and removed the superseded file.
- Recorded the exact source ZIP identity: 127,401 bytes, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`.
- Recorded the reconstructed `.tar.xz` identity: 81,400 bytes, SHA-256 `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`.
- Hardened `tools/restore_dev_snapshot.py` to verify ordered parts, every part size/hash, archive size/hash, safe extraction, package root, file count, byte count, and deterministic source-tree digest.
- Final reconstruction verification passed for package root `Witch_Tools_Dev`: 60 files, 383,270 bytes, tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.

## Scope and compatibility

- This is source preservation and verification only; no Witch Tools runtime code changed.
- Dev_v2.6.1 Blender 4.5 N-panel validation remains pending.
- Quickbar Dev_v1.4.0 source snapshot/import remains pending.
- No public branch, official source path, update URL, package identity, operator namespace, asset path, or release location changed.
