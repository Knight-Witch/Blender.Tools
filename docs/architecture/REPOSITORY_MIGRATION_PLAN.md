# Repository Migration Plan

## Objective

Organize Blender.Tools as a maintainable monorepo without breaking existing public Witch Tools or Witch Quickbar installations, update checks, download links, package identities, or external release pages.

## Non-breaking rule

The migration is additive until all compatibility surfaces are audited. Existing public branches and files remain untouched during documentation and import phases.

## Phase 0 — Audit and documentation

Status: **active**

- Create `Blender_Dev` integration branch.
- Establish root and add-on documentation.
- Record existing public branches, versions, commits, URLs, update behavior, and package identifiers.
- Locate the latest local/chat-generated Witch Tools and Quickbar development files.
- Hash and compare those files against GitHub baselines.
- Do not move public code.

Exit criteria:

- public release inventory complete
- exact in-code update URLs located
- external release/download URLs recorded
- current dev baselines imported or explicitly declared missing
- no unresolved ambiguity about which files are public versus development

## Phase 1 — Import current development baselines

- Import the latest verified Witch Tools dev source into `Blender_Dev` without changing its internal package name.
- Import the latest verified Quickbar dev source separately from the public-release snapshot.
- Record original artifact names, versions, hashes, and ancestry.
- Create component state and changelog files.
- Do not publish these imports as public releases.

Exit criteria:

- both dev baselines install in target Blender version
- version metadata is internally consistent
- known public-release update paths remain unchanged

## Phase 2 — Additive monorepo directories

Introduce target directories without deleting compatibility locations:

```text
addons/witch_tools/
addons/witch_quickbar/
addons/witch_core/
shared/
prototypes/
tests/
build/
```

Where an old path is externally referenced, retain it or generate it during builds. Never replace an externally referenced path with a silent move.

## Phase 3 — Build and compatibility layer

- Create build manifests.
- Generate versioned ZIPs from canonical source.
- Vendor shared code into independent packages when needed.
- Add automated package-content checks.
- Add a compatibility output or mirror for legacy update/download paths.

## Phase 4 — Public migration testing

Test from actual installed public builds:

- Check for Updates button
- repository/project link
- release/download link
- version comparison behavior
- package upgrade without duplicate add-on registration
- preserved preferences and hotkeys
- Blender 4.5 behavior
- any additionally supported Blender version

No public path changes before these tests pass.

## Phase 5 — Public release transition

Only after approval:

- publish a release from canonical monorepo source
- update external sites once, only if necessary
- retain legacy URLs or redirect/compatibility files
- record migration in public changelogs and build registry

## Current known constraints

- `Witch_Quick_Access` contains a public Quickbar release lineage and must remain untouched during the initial migration.
- `Witch_Main_Tools` is the current default branch but does not presently provide a verified current Witch Tools development baseline.
- Recent Witch Tools and Quickbar dev work may exist only in generated/local artifacts and chat history. These must be imported and verified rather than reconstructed from memory.
- The exact source file and URL used by Quickbar's update button have not yet been independently mapped in the new documentation branch.

## Prohibited shortcuts

- changing the default branch as a cosmetic cleanup
- deleting or renaming public branches before URL audit
- moving package folders without testing installed updates
- creating duplicate canonical implementations
- declaring chat-generated ZIPs current without file comparison
- assuming external sites can all be edited later