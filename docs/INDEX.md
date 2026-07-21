# Blender.Tools Documentation Index

This file maps the authoritative documentation for the repository.

## Required reading order

1. `/AGENTS.md`
2. `/PROJECT_RULES.md`
3. `/docs/architecture/ARCHITECTURE.md`
4. `/docs/architecture/ADDON_BOUNDARIES.md`
5. the relevant add-on's local `AGENTS.md`
6. the relevant add-on's `docs/PROJECT_STATE.md`
7. the relevant feature packet
8. `/docs/project_state/BUILD_REGISTRY.md`
9. current code and version metadata

## Root architecture

- `architecture/ARCHITECTURE.md` — parent repository and add-on architecture
- `architecture/ADDON_BOUNDARIES.md` — canonical ownership and dependency boundaries
- `architecture/UI_CONVENTIONS.md` — shared UI semantics and presentation contracts
- `architecture/OPERATOR_CONTRACTS.md` — common Blender operator behavior
- `architecture/VERSIONING_AND_PACKAGING.md` — versions, builds, and release artifacts
- `architecture/REPOSITORY_MIGRATION_PLAN.md` — staged non-breaking migration plan

## Current repository state

- `project_state/PROJECT_STATE.md` — umbrella development handoff
- `project_state/BUILD_REGISTRY.md` — authoritative known build baselines
- `project_state/BRANCH_AND_RELEASE_AUDIT.md` — branch, release, URL, and migration audit

## Decisions

Repository-wide accepted decisions live in `decisions/` as ADR files. Feature-local decisions remain in the feature packet unless they alter multiple add-ons or shared infrastructure.

## Add-on documentation

### Witch Tools

- `/addons/witch_tools/AGENTS.md`
- `/addons/witch_tools/docs/PROJECT_STATE.md`
- `/addons/witch_tools/docs/ROADMAP.md`
- `/addons/witch_tools/docs/NOTES_CHANGELOG.md`
- `/addons/witch_tools/docs/NOTES_CHANGELOG_FULL.md`

### Witch Quickbar

- `/addons/witch_quickbar/AGENTS.md`
- `/addons/witch_quickbar/docs/PROJECT_STATE.md`
- `/addons/witch_quickbar/docs/OVERLAY_ARCHITECTURE.md`
- `/addons/witch_quickbar/docs/INPUT_EVENT_CONTRACT.md`
- `/addons/witch_quickbar/docs/ASSET_MANIFEST.md`
- `/addons/witch_quickbar/docs/INTEGRATION_WITH_WITCH_TOOLS.md`
- `/addons/witch_quickbar/docs/NOTES_CHANGELOG.md`
- `/addons/witch_quickbar/docs/NOTES_CHANGELOG_FULL.md`

### Witch Core

Witch Core documentation will be added when the current baseline is imported and audited.

## Feature packets

Each substantial feature uses a self-contained packet:

- `README.md` — overview and ownership
- `SPEC.md` — intended behavior
- `STATE.md` — actual implementation state
- `ROADMAP.md` — planned, deferred, experimental, and rejected work
- `TEST_PLAN.md` — acceptance and regression testing
- `DECISIONS.md` — feature-local decisions
- `REFERENCE_CASES.md` — real or synthetic problem cases

Current packets:

- `features/curvature_sync/`

## Document roles

- **Specification:** what the feature must do
- **State:** what currently exists
- **Roadmap:** what may be done later
- **Decision record:** why a choice was made
- **Changelog:** what changed historically
- **Latest notes changelog:** latest documentation update only
- **Full notes changelog:** cumulative documentation history

Do not use roadmap or chat text as evidence that a feature is already implemented.