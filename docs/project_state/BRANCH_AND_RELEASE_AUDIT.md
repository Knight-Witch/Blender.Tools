# Branch and Release Audit

Audit date: 2026-07-20

This document records verified repository baselines and unresolved compatibility questions. It must be updated before public paths or branches are changed.

## Repository

- Repository: `Knight-Witch/Blender.Tools`
- Visibility: public
- Default branch: `Witch_Main_Tools`
- Development integration branch: `Blender_Dev`

## `Witch_Main_Tools`

Verified head at initial audit:

- Commit: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Commit message: `Update and rename WITCH_BONES_MASTER_SPEC.md to WITCH_TOOLS_MASTER_SPEC.md`

Verified root state:

- `README.md`: `(Info coming soon)`
- `Changelog.md`: empty
- `WITCH_TOOLS_MASTER_SPEC.md`: `(placeholder)`

Conclusion:

The default branch does not currently provide a verified current Witch Tools implementation.

The user-supplied candidate current development artifact is now:

- `Witch Tools Dev_v2.4.0`
- package folder `Witch_Tools_Dev`
- archive SHA-256 `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Blender target `4.5.0`

The Dev_v2.4.0 footer GitHub button currently links to:

`https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools`

This is a direct URL-open link and does not establish that the default branch contains a downloadable current package.

## `Witch_Quick_Access`

Verified public head at initial audit:

- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Public version represented in uploaded add-on source: `v1.0.2`
- Internal/public correlation recorded in branch changelog: public `v1.0.2` produced from internal build `1.2.8`
- Declared Blender target in add-on metadata: Blender `4.5.0`

The root `README.md` on this branch identifies `v1.0.1`, while the head commit contains a newer `v1.0.2` package/documentation set. This remains a documentation/package-level mismatch to map before migration.

### Current Quickbar development candidate

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package folder: `witch_quickbar_dev`
- Operator namespace: `witch_quickbar_dev.*`
- Archive SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Blender target: `4.5.0`

The development package's Check for Updates operator opens:

`https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`

The operator uses `bpy.ops.wm.url_open`. It does not fetch a version manifest or perform version comparison.

Conclusion:

`Witch_Quick_Access` remains an active public compatibility branch. Do not rename, delete, reorganize, or rewrite it during monorepo setup. `Blender_Dev` and the separate `witch_quickbar_dev` package do not currently alter the public update destination.

## Witch's Dev Modules

User-supplied current candidate:

- Host: `Witch's Dev Modules Dev_v0.0.9`
- Package folder: `witch_dev_modules`
- Artifact: `witch_dev_modules.zip`
- Archive SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Blender target: `4.5.0`

The archive contains 34 prohibited `.pyc` files in `__pycache__` directories. These remain recorded in the immutable manifest but must not be copied into canonical source or future packages.

## Development branch search

The following likely historical branch names were checked and were not found:

- `Witch_Tools_Dev`
- `Witch_Dev`
- `Witch_Quickbar_Dev`
- `Witch_Quick_Access_Dev`

This does not prove no other development branch exists. The connector branch-search endpoint did not provide a definitive full inventory.

## `Blender_Dev`

Created from `Witch_Quick_Access` to preserve the richest verified tracked source baseline while leaving the public branch unchanged.

Purpose:

- central development integration
- documentation and architecture
- audit of supplied development artifacts
- staged monorepo organization
- feature branches such as Curvature Sync

`Blender_Dev` is not a public release branch.

## Outstanding audit items

- `AUD-PKG-001`: Map the exact public Quickbar package path and identity from the branch tree.
- `AUD-QB-001`: Import and compare the full public source/asset tree against Dev_v1.3.18.
- `AUD-WT-001`: Import Witch Tools Dev_v2.4.0 canonical source.
- `AUD-QB-002`: Import Quickbar Dev_v1.3.18 canonical source without changing package identity or URL.
- `AUD-WDM-001`: Import Dev Modules Dev_v0.0.9 without generated cache files.
- `AUD-BUILD-001`: Run Blender 4.5 clean-install, registration, unregistration, and upgrade tests.
- `AUD-EXT-001`: Verify current Nexus and other published download/version references.
- `AUD-URL-001`: Test update/link controls from installed builds.

## Safety conclusion

No public branch, package path, update URL, operator identity, or external release location has been changed. Organization and baseline records remain confined to `Blender_Dev`.
