# Blender.Tools Notes Changelog — Full History

## 2026-07-20 — Supplied development baseline audit

- Audited user-supplied Witch Tools `Dev_v2.4.0`, Witch Quickbar `Dev_v1.3.18`, and Witch's Dev Modules `Dev_v0.0.9` archives.
- Recorded artifact names, package identities, Blender 4.5 metadata, archive SHA-256 hashes, and complete per-file manifests.
- Confirmed ZIP integrity, safe archive paths, and Python syntax parsing for 43 Witch Tools files, 12 Quickbar files, and 17 Dev Modules source files.
- Confirmed Witch Tools and Quickbar contain no generated cache files.
- Recorded that the Dev Modules archive contains 34 `.pyc` files inside `__pycache__` directories and therefore requires a cleaned canonical source/package import.
- Recorded Dev Modules documentation/version inconsistencies while preserving the original archive hash as the supplied baseline record.
- Located Witch Tools' footer link to `Witch_Main_Tools`.
- Located Quickbar's update destination at `Witch_Quick_Access` and confirmed its operator only opens the URL rather than fetching or comparing versions.
- Added Witch Dev Modules local rules, project state, roadmap, and notes changelogs.
- Updated the documentation index, umbrella and add-on project states, build registry, branch/release audit, compatibility registry, and latest/full notes changelogs.
- Confirmed no runtime source, public branch, update URL, package identity, operator namespace, asset path, or external release location was changed.
- Confirmed Blender runtime, installation, upgrade, UI, operator, and update-button launch tests were not performed.

## 2026-07-20 — Development architecture and non-breaking repository organization

- Created `Blender_Dev` from `Witch_Quick_Access` without modifying public branches.
- Established repository source-of-truth, scope, testing, documentation, versioning, delivery, and session-handoff rules.
- Added root contribution, compatibility, ignore, packaging, build, prototype, test, and shared-module scaffolding.
- Added the documentation index and parent architecture.
- Defined Witch Tools, Witch Quickbar, Witch Core, shared backend, and Dev module ownership boundaries.
- Recorded Quickbar's separate floating-overlay requirements.
- Added staged repository migration rules designed to preserve public update buttons, URLs, package identity, asset paths, and external links.
- Audited known branch baselines:
  - `Witch_Main_Tools` placeholder state at `ed92ded9fde9c1ee812faf227b31383b3eaa674d`
  - `Witch_Quick_Access` public lineage at `13242bf0141c7f539af97b39a4aca6e640c0901c`
- Recorded public Quickbar v1.0.2 / internal 1.2.8 correlation and Blender 4.5 metadata.
- Added build registry, Blender compatibility registry, umbrella project state, and branch/release audit.
- Added Witch Tools local rules, state, roadmap, and notes changelogs.
- Added Quickbar local rules, state, roadmap, overlay architecture, input contract, asset manifest scaffold, integration contract, and notes changelogs.
- Added Witch Core local rules, state, roadmap, and notes changelogs.
- Added Curvature Sync overview, full specification, state, roadmap, test plan, decisions, and reference cases.
- Added Curvature Sync use-case notes for BG3, general modeling, and 3D printing.
- Added ADRs for the monorepo/development branch and public compatibility preservation.
- Confirmed no Blender runtime code, public branch, update URL, package identity, external release link, or asset path was changed or tested in this pass.
