# Branch and Release Audit

Audit date: 2026-07-20

This document records verified repository baselines and unresolved compatibility questions. It must be updated before public paths or branches are changed.

## Repository

- Repository: `Knight-Witch/Blender.Tools`
- Visibility: public
- Default branch: `Witch_Main_Tools`
- New development integration branch: `Blender_Dev`

## `Witch_Main_Tools`

Verified head at initial audit:

- Commit: `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
- Commit message: `Update and rename WITCH_BONES_MASTER_SPEC.md to WITCH_TOOLS_MASTER_SPEC.md`

Verified root state:

- `README.md`: `(Info coming soon)`
- `Changelog.md`: empty
- `WITCH_TOOLS_MASTER_SPEC.md`: `(placeholder)`

Conclusion:

The default branch does **not** currently provide a verified current Witch Tools implementation or dev baseline. Recent Witch Tools dev files must not be assumed to exist here.

## `Witch_Quick_Access`

Verified head at initial audit:

- Commit: `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Public version represented in uploaded add-on source: `v1.0.2`
- Internal/public correlation recorded in branch changelog: public `v1.0.2` produced from internal build `1.2.8`
- Declared Blender target in add-on metadata: Blender `4.5.0`

The root `README.md` on this branch still identifies `v1.0.1`, while the head commit contains a newer `v1.0.2` package/documentation set. This indicates multiple documentation/package levels exist on the branch and must be mapped before migration.

Verified public compatibility surface:

- Quickbar includes a Check for Updates control described as linking to the project repository.
- Exact source file, URL constant, version-comparison behavior, and destination path remain to be mapped.

Conclusion:

`Witch_Quick_Access` is an active public-release compatibility branch. Do not rename, delete, reorganize, or rewrite it during initial monorepo setup.

## Development branch search

The following likely branch names were checked and were not found:

- `Witch_Tools_Dev`
- `Witch_Dev`
- `Witch_Quickbar_Dev`
- `Witch_Quick_Access_Dev`

This does not prove no other development branch exists. A full branch inventory remains required because the current connector branch-search endpoint did not return a complete listing.

## `Blender_Dev`

Created from `Witch_Quick_Access` to preserve the richest verified tracked source baseline while leaving the public branch unchanged.

Purpose:

- central development integration
- documentation and architecture
- import of verified local/chat dev baselines
- staged monorepo organization
- feature branches such as Curvature Sync

`Blender_Dev` is not a public release branch.

## Outstanding audit items

- `AUD-URL-001`: Locate every update/check URL in Quickbar source.
- `AUD-URL-002`: Identify external pages linking to repository branches, files, or releases.
- `AUD-PKG-001`: Record exact package folder names and Blender add-on identifiers for public and dev builds.
- `AUD-QB-001`: Map all files and asset paths on `Witch_Quick_Access`.
- `AUD-WT-001`: Locate and import the latest Witch Tools dev baseline.
- `AUD-QB-002`: Locate and import the latest Quickbar dev baseline after public `v1.0.2`/internal `1.2.8`.
- `AUD-BUILD-001`: Hash all candidate ZIPs and compare source contents.
- `AUD-EXT-001`: Verify current Nexus and other published download/version references.

## Safety conclusion

No public branch, package path, update URL, or external release location has been changed. Initial organization is confined to `Blender_Dev`.