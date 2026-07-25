# Witch Tools Development Source Verification

## Dev_v2.7.1 patch

- Status: passed locally on 2026-07-24.
- Path: `patches/Dev_v2_7_1/`.
- User-tested baseline: 127,760 bytes; SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`.
- Build artifact: 132,053 bytes; SHA-256 `d912536da3d6bd7681ce58a85c3a3099bffc17403fc0233fcb9f93551d67c9e9`.
- Focused source patch and manifest: present.
- Python parse/compile: passed for 47 files.
- Duplicate operator IDs: none across 96 identifiers.
- UI-state registration and icon-reference checks: passed.
- ZIP integrity, safe paths, single package root, and cache-file exclusion: passed.
- Blender 4.5 runtime: pending.

## Historical full snapshots

- Dev_v2.7.0: retained, but superseded after the conflicting user-tested replacement artifact was identified.
- Dev_v2.6.1: retained historical verified snapshot.

These development source records do not modify public Witch Tools source or release paths.
