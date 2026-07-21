# Witch's Dev Modules Roadmap

## Current baseline work

- `WDM-AUD-001` Import Dev_v0.0.9 source without generated cache files.
- `WDM-DOC-001` Normalize README, changelog, notes changelogs, and compatibility records to the declared host/module versions.
- `WDM-TEST-001` Test add-on registration and unregistration in Blender 4.5.
- `WDM-TEST-002` Smoke-test Re-Namer, Loose Parts → Objects, and Chain Generator independently.
- `WDM-PKG-001` Create a clean package and verify no `__pycache__` or `.pyc` files are included.

## Module work

### Re-Namer

- Preserve existing Dev_v0.0.1 behavior during import.
- Create a feature state and test plan before expansion.

### Loose Parts → Objects

- Preserve existing Dev_v0.0.1 behavior during import.
- Test island ordering, naming, transforms, materials, and undo.

### Chain Generator

- Preserve existing Dev_v0.0.8 behavior during import.
- Reconcile host/module version documentation.
- Test generated-link ordering, direction controls, naming, reference spacing, rigid-link behavior, and cleanup.

## Planned experimental additions

- Vertex Inject prototype after Witch Tools protected-zone audit.
- Curvature Sync prototype after Mode 1 Vertex Inject acceptance tests.

These additions are experimental and are not committed Witch Tools release scope.

## Promotion rule

A module may move into Witch Tools only after:

- specification and acceptance criteria exist;
- Blender runtime tests pass;
- ownership and dependencies are documented;
- package/source hygiene passes;
- the integrated implementation replaces rather than duplicates the experimental canonical logic.
