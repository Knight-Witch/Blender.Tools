# ADR-0001 — Monorepo and Development Integration Branch

Status: accepted

Date: 2026-07-20

## Context

Witch Tools, Witch Quickbar, Witch Core, shared utilities, BG3 workflows, general modeling tools, and 3D-printing tools share architecture and development history. Splitting them into multiple repositories now would duplicate infrastructure and obscure ownership of cross-domain tools.

The existing repository uses separate public branches and has no verified central branch containing all current development baselines.

## Decision

- Keep one `Blender.Tools` monorepo.
- Organize permanent source by add-on/capability and documentation/tests by feature/use case.
- Use `Blender_Dev` as the current non-public development integration branch.
- Create feature branches from the integration branch after verified baseline import.
- Preserve existing public branches until migration compatibility is proven.

## Consequences

Positive:

- one canonical source for reusable capabilities
- centralized architecture and documentation
- easier cross-add-on testing
- no premature repository proliferation

Costs:

- requires staged import/migration
- build tooling must eventually package independent add-ons
- public branch compatibility must be maintained during transition

## Alternatives considered

### Separate repositories immediately

Rejected for now because the add-ons share code and the current baselines are not fully reconciled.

### Continue branch-per-add-on without an integration branch

Rejected because cross-domain features and shared docs would remain fragmented.

## Revisit conditions

A separate repository may be justified later if a component gains an independent release lifecycle, contributor/access model, licensing model, CI burden, or negligible shared code.