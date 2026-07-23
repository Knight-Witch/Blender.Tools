# Development Source Snapshots

This area stores development-only source snapshots for Witch Tools and Witch Quickbar. It is isolated from the public `Witch_Main_Tools` and `Witch_Quick_Access` branches and is not a public release surface.

Current snapshots:

- Witch Tools `Dev_v2.6.1` — exact source package reconstructed from `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/parts/*.b64`.
- Witch Quickbar `Dev_v1.4.0` — exact source package reconstructed from `addons/witch_quickbar/dev/snapshots/witch_quickbar_dev_Dev_v1_4_0/parts/*.b64`.

Run `python tools/restore_dev_snapshot.py <snapshot-directory>` from the repository root. The script concatenates the numbered Base64 parts, decodes the `.tar.xz`, verifies its SHA-256, and extracts the complete installable source tree under the snapshot directory's `restored/` folder.

The snapshots intentionally remain separate from public source paths until an explicit integration/release pass is approved.
