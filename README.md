# Blender.Tools

Blender.Tools is the central development repository for Knight Witch Blender add-ons and shared Blender infrastructure.

## Add-on family

- **Witch Tools** — primary general-purpose N-panel toolkit and canonical owner of shared modeling, topology, BG3, and 3D-print workflow operators.
- **Witch Quickbar** — separate floating-overlay companion interface with its own drawing, input-routing, persistence, assets, and display-state architecture.
- **Witch Core** — specialized 3D-printing and manufacturing workflow add-on.
- **Witch Dev Modules** — isolated development modules used before stable tools are integrated into their owning add-on.

## Development branch

`Blender_Dev` is the integration branch for current development and repository organization. Existing public release branches and their paths are intentionally preserved until their update URLs, download paths, and external release links have been fully audited.

Current public branches must not be reorganized merely to match this development tree. Migration into the monorepo structure will be staged and compatibility-preserving.

## Source of truth

Repository code and documentation are authoritative. Chat history, generated ZIP files, previous assistant statements, and remembered project context are supporting evidence only.

Before modifying code, read:

1. `AGENTS.md`
2. `PROJECT_RULES.md`
3. `docs/architecture/ARCHITECTURE.md`
4. the relevant add-on's local `AGENTS.md` and `PROJECT_STATE.md`
5. the relevant feature specification and state documents

Start with `docs/INDEX.md` for the documentation map.

## Current baseline warning

At the creation of `Blender_Dev`:

- the tracked Quickbar public branch contains a public release lineage;
- the default `Witch_Main_Tools` branch contains only minimal placeholder Witch Tools documentation;
- the latest locally developed Witch Tools and Quickbar development builds have not yet been conclusively reconciled against GitHub.

No development build should be declared current until its files, version metadata, target Blender version, and ancestry are imported and recorded in the build registry.