# Development Source Snapshots

This area stores development-only source snapshots. It is isolated from the public `Witch_Main_Tools` and `Witch_Quick_Access` branches and is not a public release surface.

## Current status

- Witch Tools `Dev_v2.7.0` — current verified snapshot:
  - path: `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_7_0/`;
  - source ZIP SHA-256: `426b1a881b96d73922b18cba1a97f18fa944854d88dc1669d193b8b640093d45`;
  - reconstructed archive SHA-256: `2a73eaeb209602b30c4ee8e3378961038249ca3782cac23b7ad5923e3d994cab`;
  - verified source tree: 63 files, 412,416 bytes;
  - tree SHA-256: `c8ece8e4e0a750763e90ccabaa16cf6c0e1f0f8f01a06f67b2bbea1ae3d752b5`.
- Witch Tools `Dev_v2.6.1` — retained historical verified snapshot.
- Witch Quickbar `Dev_v1.5.0` — local-only delivery; no GitHub source snapshot/update was made per user instruction.
- Witch Quickbar `Dev_v1.4.0` repository snapshot/import remains pending.

Run:

```text
python tools/restore_dev_snapshot.py <snapshot-directory>
```

The restore script verifies the ordered parts, every part size/hash, reconstructed archive, safe extraction, package root, file count, byte count, and deterministic source-tree digest.

Snapshots remain separate from public source paths until an explicit audited integration/release pass is approved.
