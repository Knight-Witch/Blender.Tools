# Witch's Dev Modules Local Agent Instructions

All root `PROJECT_RULES.md` and `AGENTS.md` requirements apply.

## Purpose

Witch's Dev Modules is an isolated host for experimental Blender operators that are not yet ready for integration into Witch Tools, Witch Quickbar, or Witch Core.

## Rules

- Preserve independent Dev module versions while tools are experimental.
- Do not represent a module as Witch Tools release scope merely because it exists here.
- Keep modules isolated from one another unless a shared utility is explicitly approved.
- Promote stable general-purpose tools into Witch Tools rather than maintaining duplicate canonical implementations.
- Do not import Quickbar overlay code.
- Remove `__pycache__` and `.pyc` files from every source import and distributable package.
- Preserve each module's behavior and UI during baseline import; documentation cleanup must not silently alter runtime code.

## Required reading

Before changing Dev Modules, read:

- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/NOTES_CHANGELOG.md`
- the relevant module source and package documentation
- root architecture and add-on-boundary documents

## Testing

Every package update must test registration/unregistration, module isolation, one-step undo where applicable, malformed selections, and absence of generated cache files in the artifact.

Default target: Blender 4.5 unless explicitly changed.
