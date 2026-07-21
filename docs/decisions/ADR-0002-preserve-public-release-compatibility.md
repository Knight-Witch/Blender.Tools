# ADR-0002 — Preserve Existing Public Release Compatibility

Status: accepted

Date: 2026-07-20

## Context

Witch Quickbar has a public release branch and installed update/check behavior. External pages may link to existing repository paths. Witch Tools and Quickbar development work has also occurred through generated/local artifacts that are not yet fully reconciled with GitHub.

A cosmetic repository restructure could break update buttons, download links, package upgrades, assets, or external references.

## Decision

- Do not modify or reorganize public release branches during the documentation/import phase.
- Treat branch names, file paths, package names, operator IDs, preference IDs, update URLs, and external release links as compatibility surfaces.
- Audit and test all compatibility surfaces before migration.
- Use additive source directories and compatibility outputs rather than destructive moves.
- Require installed-public-build update and upgrade tests before any public transition.

## Consequences

- The repository may temporarily contain legacy and canonical paths.
- Migration takes longer but does not require editing several external sites immediately.
- Build tooling may need to generate legacy-compatible outputs.

## Alternatives considered

### Immediate tree cleanup and path replacement

Rejected because it risks breaking public users and external links.

### Abandon existing public update behavior

Rejected because installed releases must remain functional.

## Verification requirements

Before altering public paths:

- locate exact update URL constants
- inventory external links
- record package/add-on identifiers
- test Check for Updates from installed public build
- test download destination
- test upgrade without duplicate registration or preference loss
- document rollback plan