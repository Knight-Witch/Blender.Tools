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
- Recorded the initial branch/release audit.
- Began Witch Tools, Quickbar, and Curvature Sync documentation scaffolding.

## Current known-working state

Public Quickbar source lineage is tracked on `Witch_Quick_Access`. Its branch head records public `v1.0.2`, internal source correlation `1.2.8`, and Blender 4.5 metadata.

No current Witch Tools development source has yet been verified on GitHub. The default branch contains placeholder documentation rather than a confirmed current implementation.

## Active problems

1. Latest locally developed Witch Tools files are not yet reconciled with GitHub.
2. Latest Quickbar development files after the tracked public baseline are not yet reconciled with GitHub.
3. Quickbar update-check URL and exact package path have not yet been mapped.
4. Public branch tree structure has not yet been fully inventoried.
5. No canonical automated build system exists yet.
6. No repository test fixtures have yet been imported.

## Next exact implementation step

Locate the latest candidate Witch Tools and Quickbar development artifacts, import them into an audit workspace, record hashes and metadata, and compare them against GitHub branch baselines before any code reorganization.

After baseline import, create the physical `addons/witch_tools` and `addons/witch_quickbar` source trees while retaining public compatibility paths.

## Outstanding decisions

- Exact vendoring/build method for shared modules.
- Whether legacy public branch files remain permanent mirrors or are generated from canonical source.
- Final package naming and source-tree location after compatibility testing.
- Whether public update checks should target releases, a manifest, or a stable compatibility file in a future release.

## Files changed in this documentation pass

- root README and rules
- architecture documents
- project-state and branch audit documents
- add-on documentation scaffolding
- Curvature Sync specification packet

## Test status

- Repository writes: completed on `Blender_Dev`.
- Blender runtime tests: not performed.
- Public update-button tests: not performed.
- Package installation tests: not performed.
- Public branches modified: no.

## Known remaining issues

The new documentation describes intended architecture, not a completed source migration. Current dev source and artifacts must still be imported and verified.