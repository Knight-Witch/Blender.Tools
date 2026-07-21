# Witch Core Local Agent Instructions

All root `PROJECT_RULES.md` and `AGENTS.md` requirements apply.

## Ownership

Witch Core owns specialized 3D-printing and manufacturing workflows, initially including Knight Witch Cauldron Core SVG-to-TPU-housing generation.

Generic mesh/topology algorithms belong in Witch Tools or the shared utility layer. Witch Core may orchestrate them but must not maintain a second canonical implementation.

## Workflow safety

Print/manufacturing operators must preserve or explicitly validate:

- physical dimensions and units
- wall thickness and clearances
- manifold/watertight geometry
- normals and face winding
- connector/interface fit
- object transforms and scale
- non-destructive backup/preview where practical

## Development baseline

Do not assume a current Witch Core source baseline is present until it has been imported and verified. Confirm version, package identity, Blender target, and current Cauldron Core workflow state before coding.

Default target: Blender 4.5 unless explicitly changed.

## Documentation

Update:

- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- feature specifications and test plans
- latest/full notes changelogs
- user-facing changelog after source import
- build and Blender compatibility records