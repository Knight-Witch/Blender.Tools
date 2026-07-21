# Blender.Tools Project Rules

## 1. Repository purpose

Blender.Tools is the authoritative development repository for:

- Witch Tools
- Witch Quickbar
- Witch Core
- Witch Dev Modules
- shared Blender infrastructure
- general modeling tools
- BG3-specific tools
- 3D-printing and manufacturing tools

The repository is the durable source of truth. Chat history, project memory, saved memories, generated downloads, and earlier assistant statements are supporting context only.

## 2. Source-of-truth hierarchy

When sources disagree, use this hierarchy and report the conflict:

1. Current code and verified tests describe actual behavior.
2. Feature specifications describe intended behavior.
3. Architecture documents and accepted decisions define structural constraints.
4. Project-state files describe current progress and known problems.
5. Roadmaps describe planned, deferred, experimental, or rejected work.
6. Changelogs describe historical changes.
7. Chat history and remembered context are non-authoritative.

Do not silently choose between conflicting code and documentation. Determine which is intended, then update the stale source.

## 3. Required reading before changes

Before modifying code or making current-implementation claims:

1. Read root `AGENTS.md` and this file.
2. Read parent architecture documents.
3. Read the relevant add-on's local rules and project state.
4. Read the relevant feature specification, state, roadmap, decisions, test plan, and latest notes changelog.
5. Inspect actual code and metadata.
6. Confirm active branch, baseline commit, add-on version, and intended Blender version.

Never assume an earlier ZIP, pasted file, or remembered version is current.

## 4. Scope management

Distinguish explicitly between:

- current release scope
- next release
- long-term roadmap
- research or experimental work
- deferred work
- rejected ideas

Do not collapse every discussed feature into the next release. Preserve long-term ideas without representing them as committed scope.

## 5. Add-on ownership and dependencies

- Witch Tools owns canonical general-purpose backend and N-panel implementations.
- Witch Quickbar is a separate floating-overlay architecture. It may expose or invoke Witch Tools functionality but must not duplicate canonical implementations.
- Witch Core owns specialized 3D-printing and manufacturing workflows. Generic geometry logic belongs in Witch Tools or the shared utility layer.
- Dev modules may remain independently versioned while experimental. Once integrated, the owning add-on version is authoritative.

Shared code must have one canonical source. Distribution builds may vendor shared modules when independent installation is required.

## 6. Public-release preservation

Published releases, external links, update buttons, package identifiers, branch names, URLs, and download paths are compatibility surfaces.

Before moving, renaming, or replacing any public file or branch:

1. Locate every in-code URL and external reference.
2. Record the current behavior in the branch/release audit.
3. Preserve redirects or compatibility paths where possible.
4. Test update checks from an installed public build.
5. Verify download and release links from each external site.
6. Obtain explicit approval for any breaking migration.

Repository cleanup must never break an installed public release merely to make the tree look cleaner.

## 7. Code-change discipline

- Do not rewrite or refactor unrelated systems unless technically necessary and approved.
- Bug fixes must modify only required files plus required documentation.
- Preserve established UI layout, category ordering, names, behavior, and workflow unless the requested change requires alteration.
- New tools must be modular and avoid unnecessary dependencies.
- Destructive mesh operators must validate before mutation and fail without partial destructive changes.
- Do not duplicate canonical backend logic in UI layers.

## 8. Witch Quickbar isolation

Witch Quickbar is not an N-panel implementation. Preserve its:

- overlay drawing architecture
- input routing and pass-through behavior
- gizmo and modal boundaries
- dragging and resizing
- lock, minimize, maximize, and launcher states
- persistence and file-load recovery
- assets and icon loading
- undo separation between UI-only and scene-changing operations

Changes to Quickbar require reading its overlay, input, persistence, asset, and integration contracts.

## 9. Blender compatibility

Default Witch Tools development target: **Blender 4.5**, unless explicitly changed.

Every release or development build must record:

- intended Blender target
- add-on version
- additional Blender versions actually tested
- known compatibility limitations

Do not claim compatibility with an untested version.

## 10. Versioning and artifacts

- Use explicit versioned filenames for downloads and builds.
- Record development-to-public release correlations.
- Do not overwrite historical artifacts without an explicit reason.
- Exclude `__pycache__`, `.pyc`, temporary files, editor files, local test data, and unrelated assets from distributable ZIP files.
- Every build must have a manifest or build-registry entry.

## 11. Documentation requirements

Every meaningful update must document newly discussed or implemented:

- features
- discoveries
- decisions
- changed behavior
- revised solutions
- known limitations
- compatibility results
- roadmap status
- unresolved problems

Maintain at the relevant add-on or project level:

- `NOTES_CHANGELOG.md` — latest documentation update only
- `NOTES_CHANGELOG_FULL.md` — complete cumulative documentation history
- `PROJECT_STATE.md` — current baseline and handoff
- `ROADMAP.md` — scoped future work
- `CHANGELOG.md` — user-visible implementation history

User-visible changes require the owning add-on's changelog update.

## 12. Specifications and acceptance criteria

Every substantial feature must have:

- terminology and scope
- user workflow
- behavior contract
- validation and failure rules
- protected and excluded behavior
- acceptance criteria
- test plan
- known limitations
- current state
- roadmap and decisions

A specification describes intended behavior. It must not falsely claim implementation is complete.

## 13. Testing

Do not state that a fix works unless it was tested or clearly label it untested.

For topology-changing operators, test at minimum:

- undo and redo
- correct Object/Edit Mode handling
- selection validation
- normals and face winding
- material, smoothing, UV, Sharp, Seam, Crease, and bevel-attribute preservation where applicable
- manifold safety where applicable
- protected-zone behavior
- multi-object and multi-island behavior where supported
- malformed and ambiguous selections
- cancellation without partial destructive changes
- failure reporting

For public-release compatibility, test update buttons and published URLs from installed release builds.

## 14. Delivery requirements

Every delivery must identify:

- add-on name
- version
- target Blender version
- active baseline and branch
- files changed
- testing performed
- testing not performed
- known remaining issues

When only changed files are requested, deliver only required patch files plus necessarily updated documentation.

## 15. Session continuity

At the end of meaningful development work, update the relevant project-state file with:

- current baseline
- last completed work
- current known-working state
- active problems
- next exact implementation step
- outstanding decisions
- files changed
- test status

The next session must begin from repository state files rather than relying on chat memory.

## 16. Migration rule

The initial monorepo organization is additive and documentation-first. Existing public branches remain untouched until their source trees, URLs, releases, and external dependencies have been audited. Code migration occurs in staged branches and must preserve install/update compatibility.