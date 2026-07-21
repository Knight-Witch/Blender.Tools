# Blender.Tools Project State

Last updated: 2026-07-20

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Development integration branch: `Blender_Dev`
- Branch origin: `Witch_Quick_Access`
- Default repository branch: `Witch_Main_Tools`
- Default Witch Tools target Blender version: `4.5`

## Last completed work

- Created the `Blender_Dev` branch without modifying public branches.
- Established root repository rules and documentation hierarchy.
- Defined parent add-on architecture and ownership boundaries.
- Added a staged, non-breaking repository migration plan.
- Recorded the initial branch/release audit and build/compatibility registries.
- Created Witch Tools, Witch Quickbar, and Witch Core local documentation systems.
- Created Quickbar-specific overlay, input, asset, and integration contracts.
- Created the complete Curvature Sync feature packet and domain use-case notes.
- Added shared, prototype, test, and build-system scaffolding without moving runtime code.
- Verified that `Blender_Dev` was created directly from the tracked Quickbar public head and contained only additive documentation/scaffolding plus the development-branch README change at the time of comparison.

## Current known-working state

Public Quickbar source lineage is tracked on `Witch_Quick_Access`. Its branch head records public `v1.0.2`, internal source correlation `1.2.8`, and Blender 4.5 metadata.

No current Witch Tools development source has yet been verified on GitHub. The default branch contains placeholder documentation rather than a confirmed current implementation.

The new repository organization is documentation-first. It does not yet represent imported canonical runtime source trees.

## Active problems

1. Latest locally developed Witch Tools files are not yet reconciled with GitHub.
2. Latest Quickbar development files after the tracked public baseline are not yet reconciled with GitHub.
3. Quickbar update-check URL and exact package path have not yet been mapped.
4. Public branch tree structure has not yet been fully inventoried.
5. No canonical automated build system exists yet.
6. No repository test fixtures have yet been imported.
7. Witch Core source/project documents have not yet been imported.

## Next exact implementation step

Locate the latest candidate Witch Tools, Witch Quickbar, and Witch Core development artifacts. Import them into an audit workspace, record hashes and metadata, and compare them against GitHub branch baselines before any code reorganization.

For Quickbar, inventory the public branch package/source tree and locate the exact update/check URL before moving any file.

After verified baseline import, create the physical canonical source trees under `addons/` while retaining or generating every required public compatibility path.

## Outstanding decisions

- Exact vendoring/build method for shared modules.
- Whether legacy public branch files remain permanent mirrors or are generated from canonical source.
- Final package naming and source-tree location after compatibility testing.
- Whether future public update checks should target releases, a manifest, or a stable compatibility file.
- Exact feature-branch name and initial Dev module package for Curvature Sync after Witch Tools import.

## Files changed in this documentation pass

- root README, rules, contribution guide, changelogs, compatibility registry, and ignore rules
- architecture and migration documents
- project-state, branch audit, and build registry documents
- Witch Tools, Quickbar, and Witch Core documentation trees
- Curvature Sync specification packet and use-case notes
- shared, prototype, test, and build scaffolding

## Test status

- Repository writes: completed on `Blender_Dev`.
- Branch comparison against `Witch_Quick_Access`: performed during setup; branch originated at the exact public head and was not behind.
- Blender runtime tests: not performed.
- Public update-button tests: not performed.
- Package installation/upgrade tests: not performed.
- Public branches modified: no.
- Runtime source moved or refactored: no.

## Known remaining issues

The documentation describes intended architecture, requirements, and the migration process—not a completed source migration. Current development source and artifacts must still be imported and verified before new tool implementation begins.