# Contributing to Blender.Tools

Blender.Tools is currently maintained under Knight Witch's project rules and proprietary license. Contributions require explicit authorization.

## Before work

Read:

1. `AGENTS.md`
2. `PROJECT_RULES.md`
3. `docs/architecture/ARCHITECTURE.md`
4. relevant add-on local rules/state
5. relevant feature packet

Confirm the source branch, baseline commit, add-on version, and Blender target.

## Branches

- `Blender_Dev` — development integration
- `feature/<name>` — temporary feature work
- `fix/<name>` — isolated fixes
- public release branches — compatibility surfaces; do not alter casually

Do not use long-lived branches as substitutes for permanent source directories.

## Changes

- Keep changes scoped.
- Avoid unrelated refactors.
- Preserve UI and behavior unless change is required.
- Add/update tests and documentation with code.
- Do not duplicate canonical implementations.
- Record any architecture decision affecting multiple components.

## Blender target

Default target: Blender 4.5.

Additional compatibility may be claimed only after testing.

## Documentation update checklist

Depending on the change, update:

- feature `SPEC.md`
- feature `STATE.md`
- feature/add-on `ROADMAP.md`
- feature `DECISIONS.md`
- feature `TEST_PLAN.md`
- add-on `PROJECT_STATE.md`
- add-on `CHANGELOG.md` for user-visible changes
- `NOTES_CHANGELOG.md`
- `NOTES_CHANGELOG_FULL.md`
- build registry and compatibility log

## Testing

Record exactly:

- Blender version
- operating system
- source commit/build
- tests performed
- tests not performed
- failures and limitations

Never mark an untested fix as working.

## Packaging

Use the repository build process once established. Do not manually edit generated vendored code. Inspect ZIP contents and exclude caches, temporary files, local assets, and unrelated documentation.

## Public-release safety

Before altering URLs, paths, package identities, or update behavior, complete the compatibility audit and test an installed public release.