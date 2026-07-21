# Witch Quickbar Asset Manifest

Status: **inventory pending source audit**

Quickbar uses visual assets that are part of its runtime presentation. Paths and filenames are compatibility-sensitive.

## Required inventory fields

For every asset, record:

- asset ID
- filename and repository path
- packaged runtime path
- type and dimensions
- source/author
- license/permission
- controls or states using it
- required versus optional
- fallback behavior
- first version used
- last verified version

## Known asset roles from tracked public lineage

The current public documentation/changelog indicates assets for roles including:

- Knight Witch emblem / closed launcher
- footer shortcut or quick-access icon
- settings/preferences icon
- mirror action icon
- Cursor pivot icon
- World pivot icon
- reorder grip and standard control symbols

Exact filenames and paths have not yet been extracted and must not be guessed.

## Asset rules

- Do not rename or move packaged assets until source references and public package paths are audited.
- Do not substitute unrelated assets during code refactoring.
- Missing optional assets must use a documented fallback.
- Missing required assets must fail visibly without breaking viewport input.
- Do not include source PSDs, temporary exports, or unrelated artwork in release ZIPs unless required.
- Do not distribute font files.

## Inventory table

| Asset ID | File/path | Role | Required | Fallback | Verified version |
|---|---|---|---|---|---|
| Pending | Pending source audit | Closed launcher emblem | Yes | Document after audit | Public v1.0.2 lineage |
| Pending | Pending source audit | Footer shortcut icon | Yes | Document after audit | Public v1.0.2 lineage |
| Pending | Pending source audit | Settings icon | Yes | Blender/native fallback may apply; verify | Public v1.0.2 lineage |
| Pending | Pending source audit | Mirror/pivot icons | Yes | Text/native fallback; verify | Public v1.0.2 lineage |

## Next action

Map the `Witch_Quick_Access` branch tree and imported dev artifact, then replace all pending entries with exact paths and hashes.