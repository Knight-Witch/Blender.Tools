# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-23

## Update: Witch Tools Dev_v2.6.1 source snapshot verification

- Added a complete development-only manifest for the Witch Tools Dev_v2.6.1 source snapshot on `Blender_Dev`.
- Replaced the malformed original first Base64 part with four smaller verified parts and removed the superseded file.
- Hardened `tools/restore_dev_snapshot.py` to validate the ordered part list, each part size/hash, reconstructed archive size/hash, safe extraction, package root, file count, byte count, and deterministic source-tree digest.
- Final reconstruction passed:
  - source ZIP: 127,401 bytes, SHA-256 `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`;
  - reconstructed `.tar.xz`: 81,400 bytes, SHA-256 `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`;
  - extracted `Witch_Tools_Dev`: 60 files, 383,270 bytes, tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- Added a dedicated snapshot verification record and corrected the development snapshot index to show Witch Tools complete and Quickbar still pending.

## Scope

- This update preserves and verifies source; it does not change Witch Tools runtime behavior.
- Witch Tools Dev_v2.6.1 Blender 4.5 N-panel validation remains pending.
- Witch Quickbar Dev_v1.4.0 source snapshot/import remains pending.
- No public branch, official source path, update destination, package identity, operator namespace, inherited asset path, external release link, or public download location changed.
