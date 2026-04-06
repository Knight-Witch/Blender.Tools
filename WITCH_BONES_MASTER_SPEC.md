# Witch Bones — Master Development Roster

## Tool Identity

**Addon name:** `Witch Bones v0.1.0`  
**Repo umbrella:** `Knight-Witch/Blender.Tools`  
**Current tool path:** `Witch_Bones_Armature_Transfer`

### Immediate purpose
Automate the **OVA → BG3 cloak/jacket custom bone transfer workflow**, including:

- source rig cleanup
- source-bone filtering
- mesh-weight-based detection of actually used bones
- helper clone creation
- manual positioning stage
- commit of custom bones into the BG3 armature
- target mesh vertex-group preparation
- weight transfer
- delayed rename
- orphaned support-weight handling
- BG3 cloth flagging
- project backup/version safeguards
- restore/rollback tools

### v0.1 scope lock
The first release is specifically for:

- **OVA** source rigs
- **BG3** target rigs
- **cloak / jacket** custom bone workflows
- especially `B_Cloak_*` style chains

Later support such as BDO, skirts, hair, and broader body workflows should be architecturally anticipated, but **not** allowed to bloat the first release.

---

## Core Design Philosophy

### Safety first
This tool performs potentially destructive rigging and weight operations. It must include multiple safety layers:

- project-level backup save copies
- automatic version saves before destructive phases
- hidden source rig backup duplicates
- hidden orphan-weight backups
- restore buttons for addon-managed states
- hard gates that block finalization when unresolved issues remain

### User-guided, not opaque
The tool should automate tedious work but avoid silent destructive assumptions.

Preferred flow:

**detect → review → confirm → apply**

Not:

**detect → silently commit**

### Clean UI, dense functionality
The addon should stay visually clean:

- collapsible sections
- compact controls
- sensible icon use
- hover descriptions / lite tooltips
- concise status summaries
- no giant walls of UI text

Future: add a toggle between **lite tooltips** and **expansive tooltips**.

---

## High-Level Workflow

1. User selects source and target objects.
2. Tool runs preflight validation.
3. Tool recommends project backup save and can create one automatically.
4. Tool creates hidden internal working backups.
5. User selects source game or runs auto-detect.
6. Tool loads source profile rules.
7. Tool strips known junk bones from the source working copy.
8. Tool shows remaining bones with category filters and manual toggles.
9. Tool detects actual weighted source influences from the selected source mesh.
10. Tool merges category expectations with real detected usage.
11. Tool classifies source influences into custom / direct / alias / orphan states.
12. Tool allows review, pause, and continue.
13. Tool creates helper clone armature and optional helper mesh clone.
14. User repositions helper clone against the BG3 skeleton.
15. Tool commits selected custom bones into the BG3 armature.
16. Tool prepares target meshes and vertex groups.
17. Tool resolves direct and aliased support-group mappings.
18. Tool routes user into orphan-resolution if needed.
19. Tool transfers weights.
20. Tool renames custom bones and matching vertex groups.
21. Tool applies BG3 cloth settings where relevant.
22. Tool logs results and leaves restore/cleanup options available.

---

## UI Structure

## A. Project Safety
Purpose: protect the file before destructive operations.

Controls:

- current project file status
- backup status
- `Save Backup Copy`
- `Open Backup Folder`
- `Revert to Backup Save`

Behavior:

- first-use warning recommending backup save
- one-click save of `_BoneBackup_YYYY-MM-DD_TIMESTAMP.blend`
- if the file is unsaved, prompt to save first, then auto-generate the backup
- before destructive phases, auto-generate the next version automatically

## B. Setup
Purpose: define the session inputs.

Fields:

- Source Game
- `Auto Detect` source game button
- Source Armature
- Target Armature
- Source Mesh
- Primary Target Mesh
- Additional Target Mesh list
- Optional Source Mesh to Clone with Helper
- BG3 Parent Bone
- active source profile / mapping profile display

Status area:

- source validity
- target validity
- mesh-armature pairing validity
- current session stage

## C. Source Bone Filtering
Purpose: reduce source rig noise and define the working keep set.

Controls:

- bone search
- category dropdown
- eye icon to show/hide excluded bones
- toggle: auto-uncheck bones not in active category
- toggle: lock detected extras
- checkbox list of remaining bones
- select all / clear / invert
- compact summary

## D. Categories
Purpose: manage keep-list presets.

Features:

- built-in categories
- local project categories
- global saved categories
- indicator for project-local unsaved categories
- `+ Category`
- per-bone add/remove
- `Save Locally`
- `Save Globally`
- `Delete Category`

## E. Detection / Review
Purpose: show what the source mesh actually uses and what the tool plans to do.

Displays:

- detected weighted source bones
- detected extras outside the active category
- hierarchy parents auto-added for chain integrity
- classification table:
  - new custom bone
  - direct target match
  - aliased target match
  - unresolved orphan
- `Confirm`
- `Pause`
- `Continue Session`

## F. Helper Clone / Alignment
Purpose: create a temporary clone rig + optional object clone for positioning.

Controls:

- `Create Helper Clone`
- `Delete Helper Clone`
- `Rebuild Helper Clone`
- helper status
- selected helper objects count
- alignment confirmation

## G. Commit / Transfer Pipeline
Purpose: perform the main operations in order.

Operators:

- `Commit Custom Bones`
- `Prepare Target Groups`
- `Resolve Known Mappings`
- `Review Orphans`
- `Transfer Weights`
- `Preview Rename`
- `Apply Rename`
- `Apply BG3 Cloth Flags`
- `Run Full Finalization`

## H. Restore / Cleanup
Purpose: recover from mistakes and remove temporary clutter.

Controls:

- `Restore Orphan State`
- `Restore All Orphans`
- `Cleanup Temporary Assets`
- `Delete Session Working Copies`
- `Resume Last Session`

## I. Log / Report
Purpose: expose the session history clearly.

Display:

- session timeline
- last successful step
- warnings
- unresolved blockers
- created backups
- rename results
- orphan resolution history

---

## Preflight System

### Purpose
Catch invalid setups before the tool modifies anything.

### Required checks

- source armature exists
- target armature exists
- source mesh exists
- at least one target mesh exists
- object types are correct
- source mesh has vertex groups
- target mesh is bound or bindable to the target armature
- target armature contains the selected BG3 parent bone
- source armature has usable edit bones
- BG3 custom object property panel exists if cloth automation is expected
- naming collisions that would block cloning or renaming
- save path exists or file has been saved at least once

### Output
Compact report with:

- pass
- warning
- blocking error

Also add a **Dry Run** button that reuses the same analysis path without making scene changes.

---

## Project Backup and Versioning System

### Backup naming convention
Use the current file base name plus:

`_BoneBackup_YYYY-MM-DD_TIMESTAMP.blend`

Example:

`MyProject_BoneBackup_2026-04-05_160412.blend`

### Manual backup controls

- `Save Backup Copy`
- `Open Backup Folder`
- `Revert to Backup Save`

### Automatic version saves
Before destructive phases, silently generate the next backup version.

Destructive phases include:

- source cleanup commit
- helper commit to target armature
- orphan resolution apply
- rename apply
- final cleanup phase

### Revert to backup save
This should really mean:

- browse matching backup versions
- user selects one
- tool opens that `.blend` file as the active project

It should **not** pretend to do an in-place rewind.

---

## Source Profile System

### Purpose
The addon should know how to behave based on the source game / source rig type.

### v0.1 support
Only **OVA** must ship in v0.1.

### Source Game selector
The UI should include:

- `Source Game` dropdown
- `Auto Detect` button
- detection confidence status

### Auto-detect logic
Use rig fingerprinting, not guesses.

Possible signals:

- bone naming patterns
- known prefixes
- signature bones
- common chain structures
- known profile markers

### Profile storage architecture
Profiles should be structured data, ideally JSON-based.

Three layers:

- bundled profiles
- local custom profiles
- imported external profiles

### Profile contents
Each source profile should contain:

- game name
- optional body type
- detection fingerprints
- known junk-bone rules
- default categories
- clone rules
- alias mappings
- rename rules
- unresolved-bone notes
- comments

### Future expansion
Later support can include:

- BDO
- local custom community profiles
- import/export of profile JSON
- community-reviewed public profile library via GitHub

Direct auto-publishing from Blender into a public profile library should **not** be part of v0.1.

---

## Source Rig Cleanup System

### Hidden source backup
Before cleanup, create a hidden backup duplicate of the source armature, and optionally the source mesh if needed.

### Working copy
Cleanup should happen on a working copy, not the only live source rig.

### Known-junk rules
Support a list of known-nope bones or naming patterns that are safe to strip immediately.

Examples:

- `weapon`
- `sheath`
- irrelevant accessory bones

This should be editable in the profile or addon preferences.

### Manual cleanup layer
After automated stripping, the tool shows the remaining bones and lets the user manually refine the keep set.

---

## Category System

### Purpose
Categories act as fast keep-list presets.

### v0.1 required categories

- `Cloak / Sleeveless Jacket`
- `Jacket / Long Sleeve`

Future:

- `Skirt`
- `Hair`
- `Body`
- `Custom`

### Behavior
When a category is selected:

- the visible list collapses to that category
- excluded bones can be revealed with an eye icon
- optional auto-uncheck turns off everything outside the category
- weight-detected extras can re-add themselves and stay locked if desired

### Local vs global categories
Support:

- project-local categories
- global saved categories

The UI should visually differentiate local unsaved categories.

---

## Weight-Based Bone Detection

### Purpose
Prevent the tool from missing required influences just because a preset category was incomplete.

### Detection logic
When a source mesh is selected, the tool scans its vertex groups and compares them against the source armature.

It identifies:

- actual influencing source bones
- effective bone usage above threshold
- required hierarchy parents for chain integrity

### Threshold controls
Do **not** use “group exists = counts.”

Use configurable thresholds such as:

- minimum weight threshold
- minimum affected vertex count

### Detected extras behavior
If the mesh uses bones outside the active category, those should be listed as detected extras and auto-included by default.

### Confirm / Pause
The user should be able to:

- confirm and proceed
- pause and save session state
- continue later

---

## Source Bone Classification System

Each influencing source bone must be classified into one of four states.

### A. New Custom Bone
This is the cloak-bone case.

Example:

`B_Cloak_101`

These need to be cloned into BG3.

### B. Direct Target Match
The source support bone already has a correct target equivalent.

These do not need cloning; they need correct target-group mapping.

### C. Aliased Target Match
The source bone does not share the BG3 name, but a known mapping exists.

### D. Unresolved / Orphaned
The source bone is relevant, is not a new cloak bone, and does not yet have a known target mapping.

This state must block finalization until resolved.

---

## Mapping System

### Purpose
Handle non-identical but functionally equivalent support-bone naming between the source rig and BG3.

### v0.1 role
Needed even in the cloak-focused release because support weights may appear on non-cloak bones.

### Mapping table
Mappings should be stored as structured entries:

- source bone name
- target BG3 name
- mapping mode
- notes

### Mapping modes

- direct
- alias
- clone
- unresolved

### Future reuse
Once a source-to-BG3 alias is confirmed, it should be reusable in future projects.

---

## Session State / Pause / Resume

### Purpose
Users need to be able to stop mid-pipeline without losing context.

### Stored session data
Preserve:

- selected source game/profile
- selected objects
- active category
- keep-set result
- detected extras
- classification results
- helper clone status
- orphan resolution progress
- last completed stage
- created backups
- restore metadata

### Session stages

- setup
- preflight passed
- source prepared
- bone set resolved
- helper clone created
- helper aligned
- custom bones committed
- target groups prepared
- orphan review pending
- transfer complete
- rename complete
- finalize complete

### Resume behavior
If a session is paused or Blender is reopened, the addon should show a clear `Resume Last Session` option.

---

## Helper Clone Stage

### Purpose
Let the user preview and reposition the selected custom rig segment before committing it into the BG3 armature.

### What gets created

- helper armature with selected source bones
- optional helper mesh clone associated with those bones

### Selection behavior
The helper armature and helper mesh should remain selected together so the user can move, rotate, and scale them as a unit.

### Transform fidelity
Bone creation should preserve:

- head
- tail
- roll
- parent-child relationships
- local orientation / rest transform

Use correct edit-bone transform logic rather than a loose visual copy.

---

## Commit to BG3 Armature

### Purpose
Inject the new custom cloak bones into the target BG3 skeleton.

### What gets committed
Only bones classified as **new custom bone** should be cloned into the target armature.

Do **not** duplicate support bones that already belong to BG3.

### Parenting rules
The cloned custom chain should preserve its internal hierarchy.

Root bones should be parented to the selected `BG3 Parent Bone`.

### Collision handling
If a target bone already exists with the final intended name or temp name, the tool must stop or skip with a clear report.

No silent overwrite.

---

## Target Mesh Preparation

### Supported targets

- one primary target mesh
- optional additional target meshes

### Vertex group creation
On all selected target meshes, create empty vertex groups matching the temporary source custom-bone names before transfer.

### Armature sanity
Confirm that each target mesh is paired with the correct target BG3 armature before proceeding.

---

## Weight Transfer

### Main goal
Transfer source weights to target meshes while preserving temporary name compatibility.

### Transfer method
Use Blender data transfer / weight transfer with name-based group mapping where relevant.

### Geometry mapping
This should be configurable, with a sane default for typical armor transfers.

### Multi-target support
The tool should iterate across all selected target meshes and report success/failure per mesh.

---

## Orphan Resolution System

### Trigger
If the tool detects unresolved non-cloak source influences that do not have a known BG3 equivalent, it enters orphan review.

### Hard gate
The pipeline must **not** allow finalization to proceed while unresolved orphans remain.

If unresolved orphan mappings exist, the user should be rerouted into the orphan review stage.

Finalize buttons should be disabled or replaced with `Resolve Orphans`.

### Per-orphan choices

#### Merge Into Existing BG3 Group
Add the orphan group’s weights into a chosen BG3 group, then normalize.

#### Replace Destination Group
Use the orphan’s weight state to override the chosen BG3 group.

#### Park / Keep for Later
Preserve the orphaned group in a safe way and leave the session marked incomplete or flagged for manual review.

### Backup requirement
Before orphan resolution is applied, the tool must create hidden backups of:

- the orphan group
- the destination target group if one exists

### Restore behavior
The user should be able to:

- restore one orphan resolution
- restore all orphan resolutions from the session

The tool should restore saved backup states, not try to reverse the result by inference.

### Explicit warning
Restore should be described honestly: it reverts to the last addon-managed orphan backup state, not later manual painting done afterward.

---

## Rename System

### Delayed rename principle
Custom cloak bones and matching target groups must retain original source-compatible names during the transfer stage.

Only after weights are safely transferred should the rename happen.

### Rename preview
Before final rename, the tool should show:

- old name
- new name
- collisions if any

### Final rename
The rename step should update both:

- new custom bones in the target armature
- matching vertex groups on all affected target meshes

### Conflict blocking
If the rename would create duplicates or overwrite existing valid names, the tool must stop and report.

---

## BG3 Cloth Flag Automation

### Purpose
If the mesh is using cloak/skirt style custom physics-bone workflows, the tool should help set the correct BG3 object property flags.

### v0.1 behavior
For cloak/skirt use cases, automatically set `Cloth` on affected render meshes in the BG3 mesh-type panel if that property is available.

### Future expansion
Later, if needed, the tool could help with cloth-physics proxy workflows, but that is out of scope for the first release.

---

## Logging and Reporting

### Session log
Every major action should be recorded.

Recommended entries:

- project backup saved
- source working copy created
- junk bones removed
- category applied
- mesh-driven extras detected
- helper clone created
- custom bones committed
- target groups created
- known mappings resolved
- orphan backups created
- orphan actions applied
- rename preview passed
- rename applied
- cloth flag applied
- cleanup run

### User-facing reports
The UI should provide readable summaries, not just console spam.

---

## Cleanup System

### Purpose
Remove temporary clutter when the session is done.

### Temporary assets to manage
The addon will likely create:

- source working copies
- hidden source backups
- helper clone armatures
- helper mesh clones
- hidden orphan backups
- temporary collections
- temporary session metadata if needed

### Cleanup options

- cleanup helper assets only
- cleanup all temporary session assets
- preserve backups
- purge addon backups

This should be user-controlled, not fully automatic.

---

## Collections / File Hygiene

The tool should manage its internal assets in clean dedicated collections.

Suggested structure:

- `WITCH_BONES_BACKUPS`
- `WITCH_BONES_HELPERS`
- `WITCH_BONES_SESSION`
- `WITCH_BONES_ORPHAN_BACKUPS`

Hide them by default as appropriate.

---

## Tooltips / UX Notes

### Immediate requirement
Use **lite tooltips** in v0.1.

Buttons and toggles should have concise short descriptions.

### Future expansion
Later, include an addon preference for:

- lite tooltips
- expansive tooltips

Expansive mode should give fuller process descriptions and button explanations.

### Later onboarding
A later version can include a first-time-user tutorial / onboarding flow with optional links to:

- Patreon
- GitHub
- Ko-fi

That should **not** interfere with first-release scope.

---

## Community Profile / Library Plan

### Long-term model
Use a JSON-based source profile system that can eventually be:

- bundled in the addon
- saved locally
- exported/imported
- community-reviewed through GitHub

### Public repo use
A public GitHub repo is the correct eventual place for source profiles.

Do **not** build direct live auto-write to a spreadsheet or public data source from inside Blender.

### Why
The addon should use trusted structured profiles, not messy uncontrolled live data.

---

## Development Phases

## Phase 0 — Foundation

Build:

- addon scaffold
- naming/version structure
- UI shell
- persistent properties
- basic session state
- project backup system
- preflight

## Phase 1 — OVA Cloak Source Prep

Build:

- source game selector
- OVA source profile
- working copy logic
- junk-bone stripping
- bone list UI
- category system
- mesh-driven influence detection
- bone classification system

## Phase 2 — Helper Clone + Commit

Build:

- helper armature generation
- optional helper mesh clone
- selection/link behavior
- transformed placement support
- commit into BG3 target armature
- parent hierarchy handling
- collision reporting

## Phase 3 — Transfer + Rename

Build:

- multi-target mesh support
- target group prep
- known direct/alias mappings
- weight transfer pipeline
- rename preview
- final rename

## Phase 4 — Orphan Safety Layer

Build:

- orphan detection
- hard gate blocking
- merge/replace/park options
- orphan backup creation
- restore orphan state
- orphan report UI

## Phase 5 — BG3 Finalization + Cleanup

Build:

- cloth flag automation
- cleanup tools
- session logging
- dry run
- resume session
- result reporting

## Phase 6 — Later Expansion

Later, after the cloak workflow is proven:

- BDO source profile
- more category groups
- richer mapping library
- category/profile import/export
- expansive tooltip mode
- onboarding/tutorial
- community-reviewed profile sharing

---

## Non-Negotiable Safeguards

These should be treated as mandatory:

- preflight validation
- project backup prompt
- automatic version save before destructive steps
- hidden source working backup
- hidden orphan backup
- hard stop on unresolved orphans
- rename conflict blocking
- no silent overwrite of bones/groups
- session resume
- cleanup control

---

## Pending Placeholder

There is still one additional critical feature not yet remembered by the user.

Leave an explicit placeholder in planning until that is added:

`[PENDING CRITICAL FEATURE — user to add when remembered]`

---

## Definition of v0.1 Success

`Witch Bones v0.1.0` is a success if it can reliably do this:

Take an **OVA cloak/jacket source rig and source mesh**, detect the real required bone set, let the user review and position a helper clone, commit only the needed custom cloak bones into the **BG3 armature**, prepare one or more target meshes, transfer weights safely, force orphan resolution where needed, rename correctly into BG3 convention, apply BG3 cloth flags, and provide enough backup/restore/versioning protection that a user can recover from mistakes without losing their file.

---

## Immediate Data Needed for Implementation

For initial build work, the most useful source data is:

### OVA
- one representative real working armor example
- full armature bone list for that specific armature
- parent-child hierarchy if possible
- source mesh vertex group list
- notes on obvious cloak/support/junk bones

### BG3
- target armature bone list for the chosen body type
- likely good parent bone from a known-good jacket/cloak mod
- any trusted support-bone correspondence notes

Detection will do a lot of heavy lifting for identifying **which bones are used**, but it cannot replace a real alias/mapping table for non-custom support bones.
