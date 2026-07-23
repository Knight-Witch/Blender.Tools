# Development Source Snapshots

This area stores development-only source snapshots for Witch Tools and Witch Quickbar. It is isolated from the public `Witch_Main_Tools` and `Witch_Quick_Access` branches and is not a public release surface.

## Current status

- Witch Tools `Dev_v2.6.1` — manifest and reconstruction verification complete at `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/`.
  - source artifact SHA-256: `671290a99803c2b709c0595237756a46faecbac3400cc5cb3b03c50d0fa4ba3e`;
  - reconstructed archive SHA-256: `33ee629982fc453cc357b2a8ae08c53f03865791fe6c3c0e37822e0c176334aa`;
  - verified source tree: 60 files, 383,270 bytes, tree SHA-256 `8729d11c0f8d47125ce945204353bec7c11c398ae704b2b293fd64f3af5e51a3`.
- Witch Quickbar `Dev_v1.4.0` — isolated source snapshot/import remains pending final assembly and verification.

Run `python tools/restore_dev_snapshot.py <snapshot-directory>` from the repository root. The script reads the ordered part list from `manifest.json`, verifies every part, reconstructs and verifies the `.tar.xz`, performs safe-path extraction, and verifies the extracted package root, file count, byte count, and deterministic source-tree digest.

The snapshots intentionally remain separate from public source paths until an explicit integration/release pass is approved.
