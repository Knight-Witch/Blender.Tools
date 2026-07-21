# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-20

## Update: supplied development baseline audit

- Audited and recorded Witch Tools `Dev_v2.4.0`, Witch Quickbar `Dev_v1.3.18`, and Witch's Dev Modules `Dev_v0.0.9` as the best available candidate current baselines.
- Added archive and per-file SHA-256 manifests for all three supplied ZIP files.
- Confirmed ZIP integrity, safe paths, package metadata, Blender 4.5 targets, and static Python syntax parsing.
- Located the Witch Tools footer GitHub destination and the exact Quickbar Check for Updates destination.
- Confirmed Quickbar's update control only opens the public `Witch_Quick_Access` branch and performs no version comparison.
- Added Witch Dev Modules local rules, project state, roadmap, and notes tracking.
- Recorded that the Dev Modules archive contains 34 prohibited `.pyc` files in `__pycache__` directories and has package-documentation version inconsistencies.
- Updated the documentation index, project state, branch/release audit, build registry, compatibility registry, and Witch Tools/Quickbar state and notes.

## Public compatibility

No public branch, update URL, package identity, operator namespace, external release link, asset path, or runtime source was changed.

## Testing

Static ZIP, hash, metadata, safe-path, and Python syntax audits were performed. Blender runtime, package installation, side-by-side installation, upgrade, UI, operator, undo/redo, and update-button browser-launch testing were not performed.
