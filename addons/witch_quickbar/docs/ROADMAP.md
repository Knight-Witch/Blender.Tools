# Witch Quickbar Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Baseline and compatibility work

### QB-BASE-001 — Inventory public branch source and assets

- Status: active
- Branch: `Witch_Quick_Access`
- Goal: exact file tree, package directory, asset paths, operator IDs, preference IDs, and version metadata

### QB-BASE-002 — Locate and verify update-check URL

- Status: active
- Priority: critical before migration
- Goal: record source file, constant/logic, destination, version comparison, and installed behavior

### QB-BASE-003 — Import latest development artifact

- Status: blocked pending artifact location
- Goal: compare post-public dev source against public v1.0.2/internal 1.2.8

### QB-BASE-004 — Build Quickbar registries and test matrix

- Status: planned
- Dependency: QB-BASE-001 and QB-BASE-003

## Known development issues to reconcile after import

The following issues were discussed after prior development and must be matched to actual source before fixes:

- Apply All Transforms control appears to report an action without applying transforms.
- Mirror Transform / Mirror Selected edit-mode availability and background mode handling require verification.
- Mirror Objects axis selection and optional join behavior were discussed for development scope.

These entries are context only until current source and project state are imported.

## Architecture work

### QB-ARCH-001 — Preserve floating-overlay architecture during monorepo migration

- Status: active documentation

### QB-ARCH-002 — Stable optional Witch Tools invocation contract

- Status: planned
- Dependency: Witch Tools operator registry

### QB-BUILD-001 — Generate independent Quickbar release package from canonical source

- Status: planned
- Requires package-identity and update compatibility tests

## Later features

- additional compact Witch Tools shortcuts after stable integration
- customizable tool tabs/sections where consistent with overlay architecture
- expanded preferences and optional user layout controls

No later feature is current release scope until explicitly assigned.