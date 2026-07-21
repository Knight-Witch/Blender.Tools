# Witch Tools Local Agent Instructions

All root `PROJECT_RULES.md` and `AGENTS.md` requirements apply.

## Ownership

Witch Tools is the canonical owner of general-purpose Blender operators and N-panel workflows. General modeling, topology, BG3, and 3D-print tools belong here when their backend is reusable.

## UI preservation

- Preserve the established N-panel layout, category order, naming, and interaction patterns unless the requested feature requires a change.
- Update the Witch Tools UI map whenever controls move or are added.
- Do not copy Quickbar's overlay architecture into Witch Tools.

## Modularity

- Complex features must live in isolated modules.
- Backend geometry logic must be separable from panel drawing.
- Quickbar and Witch Core integrations must call the canonical backend rather than duplicate it.
- Experimental features should begin as Dev modules or feature-isolated packages.

## Mesh safety

Topology-changing operators must validate first, preserve attributes and normals, support one coherent undo step, and fail without partial destructive changes.

Protected zones must be consulted by any operator that moves, injects, dissolves, reconnects, or rebuilds protected geometry.

## Development baseline

Do not assume the latest Witch Tools development ZIP is in GitHub. Confirm and import the current source before implementing new features.

Default target: Blender 4.5 unless explicitly changed.

## Required documentation

Read and update:

- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- relevant feature packet
- `docs/NOTES_CHANGELOG.md`
- `docs/NOTES_CHANGELOG_FULL.md`
- user-visible `CHANGELOG.md` once the source tree is imported
- compatibility and build registry when applicable