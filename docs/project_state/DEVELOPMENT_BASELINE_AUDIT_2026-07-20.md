# Development Baseline Audit — 2026-07-20

## Scope

This audit records the three user-supplied candidate development baselines for `Knight-Witch/Blender.Tools`.

No public branch, package identifier, runtime URL, or external release location was modified during the audit.

## Verified uploaded artifacts

### Witch Tools

- Uploaded artifact: `Witch_Tools_Dev_v2_4_0_Blender_4_5.zip`
- SHA-256: `e141774f307f2402f2d0151f1f69be9f8fb6257254d0a1db223b6c1f3d457e6e`
- Archive size: 97,702 bytes
- Package folder: `Witch_Tools_Dev`
- Declared add-on: `Witch Tools Dev_v2.4.0`
- Declared version tuple: `(2, 4, 0)`
- Declared Blender target: `(4, 5, 0)`
- Python files: 43
- Asset files: 6 PNG icons
- Package cache artifacts: none
- Python syntax parse: passed for all 43 Python files
- Runtime validation in Blender: not performed in this audit

Current recorded feature at this baseline: Edit Tools > Object Snap, including vertex, edge, and face anchoring, optional orientation matching, and disconnected-island scope detection.

The footer GitHub link is currently:

`https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Main_Tools`

This is a link button, not a verified automatic version-comparison system.

### Witch Quickbar

- Uploaded artifact: `witch_quickbar_dev_Dev_v1_3_18_package.zip`
- SHA-256: `01fc12ee366c6484e209d1ee71519bd1f1ca711d4fc3c2710fec5e20b2ba2a1b`
- Archive size: 116,502 bytes
- Package folder: `witch_quickbar_dev`
- Declared add-on: `Witch Quickbar Dev_v1.3.18`
- Declared version tuple: `(1, 3, 18)`
- Declared Blender target: `(4, 5, 0)`
- Python files: 12
- Asset files: 31 PNG icons
- Package cache artifacts: none
- Python syntax parse: passed for all 12 Python files
- Runtime validation in Blender: not performed in this audit

The development package uses the separate `witch_quickbar_dev` package/operator namespace, allowing it to install alongside the public Quickbar package.

The Check for Updates control invokes Blender's URL opener with:

`https://github.com/Knight-Witch/Blender.Tools/tree/Witch_Quick_Access`

It does not currently fetch or compare version metadata. It only opens the public Quickbar repository branch. Therefore the new `Blender_Dev` branch does not alter the current public/dev update-button destination.

### Witch's Dev Modules

- Uploaded artifact: `witch_dev_modules.zip`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Archive size: 174,514 bytes
- Package folder: `witch_dev_modules`
- Declared host add-on: `Witch's Dev Modules Dev_v0.0.9`
- Declared version tuple: `(0, 0, 9)`
- Declared Blender target: `(4, 5, 0)`
- Python source files: 17
- Python syntax parse: passed for all 17 source files
- Shipped cache artifacts: 34 `.pyc` files inside `__pycache__` directories
- Runtime validation in Blender: not performed in this audit

Declared module versions:

- Re-Namer: `Dev_v0.0.1`
- Loose Parts → Objects: `Dev_v0.0.1`
- Chain Generator: `Dev_v0.0.8`

The cache files must be removed from any canonical source import or future distribution package.

Documentation inside the archive is internally inconsistent:

- `bl_info` and `addon_info.py` identify host `Dev_v0.0.9`.
- `README.md` still begins with `Dev_v0.0.8`.
- `CHANGELOG.md`, `NOTES_CHANGELOG.md`, and the compatibility log contain later v0.0.9 information appended after older headings instead of being normalized to a clear latest-first state.

The source version metadata is coherent; the package documentation requires cleanup after the immutable baseline is recorded.

## Archive safety and structural checks

All three ZIP files passed the following static checks:

- no absolute archive paths
- no `..` path traversal entries
- readable ZIP central directories
- Python source parse without syntax errors
- declared Blender target present
- declared package folder present

These checks do not establish that the add-ons install, register, unregister, or function correctly in Blender.

## Baseline status

The uploaded files are now the best available candidate baselines:

- Witch Tools: `Dev_v2.4.0`
- Witch Quickbar: `Dev_v1.3.18`
- Witch's Dev Modules: `Dev_v0.0.9`

They should be treated as candidate current baselines until installed and smoke-tested in Blender 4.5.

The per-file SHA-256 manifest is stored in:

`docs/project_state/baseline_manifests/DEVELOPMENT_BASELINE_MANIFEST_2026-07-20.json`

## Required next steps

1. Preserve the uploaded archives as immutable external baseline artifacts.
2. Import source into canonical development trees without renaming package folders or operator namespaces.
3. Remove only prohibited generated files from the canonical Dev Modules source copy:
   - `__pycache__/`
   - `.pyc`
4. Install each original artifact in Blender 4.5 and run registration/unregistration smoke tests.
5. Test Quickbar's public update/check button and verify the destination remains `Witch_Quick_Access`.
6. Inventory every Quickbar asset against the package manifest.
7. Generate UI and operator registries from the imported source.
8. Begin Curvature Sync work against Witch Tools `Dev_v2.4.0`, after verifying the existing Vertex Lock implementation and protected-zone data model.

## Testing performed

- ZIP integrity and safe-path audit
- SHA-256 archive hashing
- per-file hashing
- metadata inspection
- static Python syntax parsing
- URL inspection for Witch Tools footer links and Quickbar update control

## Testing not performed

- Blender installation
- add-on registration or unregistration
- UI rendering
- scene operations
- undo/redo
- public release upgrade path
- update-button browser launch
- Blender 4.5 runtime behavior
