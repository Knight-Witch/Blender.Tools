# Blender.Tools Agent Instructions

These instructions apply to all repository work.

Before modifying code or making claims about current implementation:

1. Read `PROJECT_RULES.md`.
2. Read `docs/architecture/ARCHITECTURE.md` and `docs/architecture/ADDON_BOUNDARIES.md`.
3. Read the relevant add-on's local `AGENTS.md` and `docs/PROJECT_STATE.md`.
4. Read the relevant feature's `SPEC.md`, `STATE.md`, `ROADMAP.md`, `DECISIONS.md`, and latest notes changelog.
5. Inspect the current code, version metadata, branch, build registry, and target Blender version.

Repository documentation and current code are authoritative over chat history, prior generated ZIP files, saved memories, and earlier assistant statements.

Do not modify public release branches, published download paths, update-check URLs, package identifiers, or externally referenced files unless the compatibility impact has been audited and the change is explicitly approved.

Do not refactor unrelated systems. Bug fixes must touch only required files unless a broader architectural correction has been approved.

Every meaningful implementation change must update the documentation required by `PROJECT_RULES.md`. Every session must leave an accurate project-state handoff.

Never claim a build, fix, feature, or Blender version works unless it was actually tested. Record untested work explicitly.