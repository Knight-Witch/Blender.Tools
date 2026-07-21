# Witch Quickbar Asset Manifest

Last updated: 2026-07-21

Quickbar runtime assets are compatibility-sensitive. Existing filenames and paths remain unchanged unless explicitly listed as new additions.

## Asset rules

- Do not rename or move packaged assets until source references and package paths are audited.
- Do not substitute unrelated assets during refactoring.
- Missing optional assets require a documented fallback.
- Missing required assets must fail visibly without blocking viewport input.
- Do not include source PSDs, temporary exports, unrelated artwork, or font files.
- Supplied SVG source files are not shipped in Dev_v1.4.0; the current loader uses converted PNGs.

## Dev_v1.4.0 Selection Slots additions

The user supplied Blender-style SVG artwork. Each file was converted to a transparent 64x64 grayscale+alpha PNG and packaged under `witch_quickbar_dev/icons/`.

| Asset ID | Runtime path | Role | Dimensions | SHA-256 | Required | Fallback | First version |
|---|---|---|---:|---|---|---|---|
| `longdisplay` | `icons/longdisplay.png` | Selection Slots section icon | 64x64 | `4528b82e17fc0bfff5645634c07315e500a61bea3ae59cc58758cd039742f52d` | Yes | section text remains; missing icon must not block input | Dev_v1.4.0 |
| `file_tick` | `icons/file_tick.png` | Save/overwrite slot | 64x64 | `2d037e17d5d4bf31345158976dfd1afecdad033e32b93d4994f3827848bc7cb6` | Yes | disabled/missing icon action must remain identifiable by tooltip | Dev_v1.4.0 |
| `trash` | `icons/trash.png` | Clear slot / Clear All | 64x64 | `e6541284893ec5b3940f1f0b5c0c5bae088de84ba184fad18d9d0c8bd8687f92` | Yes | tooltip/textual unavailable state | Dev_v1.4.0 |
| `remove` | `icons/remove.png` | Remove slot row | 64x64 | `67dc32ba673cd893bc1cc8daf822f841ed0428c4d5cade67e50d510510a1b144` | Yes | tooltip/textual unavailable state | Dev_v1.4.0 |
| `add` | `icons/add.png` | Add slot | 64x64 | `e320917b2ef1dfc85120d548ee504b0eaa1ff297fca5fb00e3388798a3558cbc` | Yes | tooltip/textual unavailable state | Dev_v1.4.0 |

## Current packaged inventory status

Dev_v1.4.0 contains 36 PNG files. Static validation confirmed every `ICON_FILES` mapping resolves to an existing packaged PNG. The five additions above are fully inventoried. The 31 inherited Dev_v1.3.18 assets still require a complete historical source/license/path audit.

## Known inherited asset roles

Inherited packaged assets include:

- Knight Witch emblem / closed launcher
- footer shortcut and preferences icons
- mode icons
- mirror and pivot icons
- grid/cursor/selection icons
- reorder grip and chevron
- duplicate and Vertex Snap icons

## Next action

During canonical Dev_v1.4.0 source import, generate the complete 36-file asset table with exact hashes, roles, source/permission records, required/fallback status, and version history. Runtime-test missing-icon handling and texture-cache cleanup in Blender 4.5.
