# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-20

## Update: development architecture and non-breaking repository organization

- Created `Blender_Dev` from the tracked Quickbar public branch without modifying public branches.
- Replaced the development-branch root README with the Blender.Tools umbrella overview.
- Added root agent, project, contribution, compatibility, and packaging rules.
- Added documentation index, parent architecture, add-on boundaries, UI/operator/version contracts, and staged migration plan.
- Added branch/release audit, project state, build registry, and Blender compatibility registry.
- Added Witch Tools local rules, state, roadmap, and notes changelogs.
- Added Witch Quickbar local rules, state, roadmap, overlay/input/asset/integration contracts, and notes changelogs.
- Added Witch Core local rules, state, roadmap, and notes changelogs.
- Added the full Curvature Sync feature packet and BG3, general modeling, and 3D-printing use-case notes.
- Added ADRs for the monorepo/development branch and public compatibility preservation.
- Added shared, prototype, test, and build-system scaffolding without moving runtime code.
- Added repository ignore rules for caches, generated archives, Blender backups, and temporary files.

## Public compatibility

No public branch, update URL, package identity, external release link, asset path, or runtime source was changed.

## Testing

Documentation/repository writes and branch comparison only. Blender runtime, package installation, and installed-update testing were not performed.