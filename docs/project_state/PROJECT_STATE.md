# Blender.Tools Project State

Last updated: 2026-07-20

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Development integration branch: `Blender_Dev`
- Branch origin: `Witch_Quick_Access`
- Default repository branch: `Witch_Main_Tools`
- Default Witch Tools target Blender version: `4.5`

## Candidate development baselines

### Witch Tools

- Version: `Dev_v2.4.0`
- Artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Static audit: passed
- Blender runtime: not yet tested in this audit

### Witch Quickbar

- Version: `Dev_v1.3.18`
- Artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- Package: `witch_quickbar_dev`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Update destination: `Witch_Quick_Access` public branch
- Static audit: passed
- Blender runtime: not yet tested in this audit

### Witch's Dev Modules

- Version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- Package: `witch_dev_modules`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Static audit: passed
- Packaging hygiene: failed because the archive contains 34 `.pyc` files in `__pycache__`
- Blender runtime: not yet tested in this audit

## Last completed work

- Created the `Blender_Dev` branch without modifying public branches.
- Established root repository rules and documentation hierarchy.
- Defined parent add-on architecture and ownership boundaries.
- Added a staged, non-breaking repository migration plan.
- Created Witch Tools, Witch Quickbar, Witch Core, and Witch Dev Modules documentation systems.
- Created Quickbar-specific overlay, input, asset, and integration contracts.
- Created the complete Curvature Sync feature packet and domain use-case notes.
- Audited the three user-supplied development archives.
- Recorded archive and per-file SHA-256 manifests.
- Confirmed Witch Tools and Quickbar packages contain no generated cache files.
- Confirmed Quickbar Dev_v1.3.18 uses the separate dev package/operator namespace and opens the public `Witch_Quick_Access` branch for update checks.
- Recorded Dev Modules cache-file and documentation defects.

## Current known-working state

The source archives are now identified and statically validated, but they have not yet been installed or runtime-tested in Blender 4.5 during this audit.

Public Quickbar source lineage remains tracked on `Witch_Quick_Access`. No public branch or compatibility surface has been modified.

## Active problems

1. Candidate source trees have not yet been imported into canonical repository locations.
2. Blender 4.5 install/register/unregister smoke tests are pending for all three packages.
3. Public Quickbar package path and installed-update behavior still require runtime verification.
4. Dev Modules must be imported without generated cache files and its documents normalized to host Dev_v0.0.9.
5. No automated build system exists yet.
6. UI and operator registries have not yet been generated from the imported source.
7. Witch Core source/project baseline has not yet been supplied or audited.
8. Curvature Sync implementation must wait until the Witch Tools Vertex Lock/protected-zone architecture is inspected in the imported Dev_v2.4.0 source.

## Next exact implementation step

Import the candidate source archives into canonical development trees while preserving existing package folder names, operator IDs, asset paths, and update URLs. Strip only generated `__pycache__` and `.pyc` files from the Dev Modules canonical copy.

Then perform Blender 4.5 smoke tests and generate source-derived UI/operator inventories before beginning Vertex Inject or Curvature Sync implementation.

## Outstanding decisions

- Exact vendoring/build method for shared modules.
- Whether legacy public branch files remain permanent mirrors or are generated from canonical source.
- Final canonical source-tree package placement after installation testing.
- Whether future public update checks should target releases, a manifest, or a stable compatibility file.
- Whether the experimental Vertex Inject/Curvature Sync prototype starts in Witch Dev Modules or a feature-isolated Witch Tools dev package.

## Files changed in this documentation pass

- development baseline audit
- per-file source/archive manifests
- build registry
- Witch Tools project state
- Quickbar project state
- Witch Dev Modules rules, state, roadmap, and notes
- root and add-on changelog/state documentation

## Test status

- ZIP integrity and safe-path checks: passed for all three artifacts.
- Static Python syntax parse: passed for all source files.
- Blender runtime tests: not performed.
- Public update-button launch test: not performed.
- Package installation/upgrade tests: not performed.
- Public branches modified: no.
- Runtime source moved or refactored: no.

## Known remaining issues

The uploaded archives are the best available candidate baselines, but they are not yet canonical runtime-verified repository source. The next session must begin from this file and the baseline audit rather than chat memory.
