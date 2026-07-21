# UI Conventions

## Scope

This document defines shared semantic and interaction conventions. It does not force Witch Tools and Witch Quickbar to use the same physical UI architecture.

## Shared terminology

- Use stable user-facing tool names across add-ons.
- A compact Quickbar control may abbreviate a label, but its tooltip must use the canonical Witch Tools name.
- Operator names, reports, and documentation must use the same core terminology.
- Avoid renaming established controls without a migration reason.

## Witch Tools N-panel

Witch Tools should use:

- clear category and subsection hierarchy
- preserved category ordering unless explicitly changed
- collapsible groups where density requires them
- concise button labels and specific tooltips
- visible state, warnings, and validation results near relevant controls
- disabled controls with an explanation rather than silent inactivity
- explicit preview/apply separation for risky operations

General topology tools should live under an Edit/Topology Repair area unless a later approved UI map specifies otherwise.

## Witch Quickbar

Quickbar presentation remains governed by its own style and overlay contracts. Shared semantic consistency does not imply N-panel widgets or layout.

Quickbar must preserve:

- compact dimensions
- custom drawing and hit areas
- lock, resize, reorder, minimize, maximize, close, and launcher affordances
- pass-through outside active hit targets
- icon consistency and fallback behavior
- direct, action-specific tooltips

## Destructive operations

Risky tools must provide one or more of:

- preview
- preflight report
- confirmation
- clear undo contract
- explicit failure before mutation

Do not use vague labels such as `Fix` when the operation changes topology. Prefer specific labels such as `Inject Missing Columns`, `Split Faces`, or `Apply Curvature Sync`.

## Reports

Success reports should state measurable work where useful:

- vertices injected
- edges created
- faces split
- objects processed
- unresolved items

Failure reports should state:

- the exact invalid condition
- which selection/object caused it where possible
- whether any mutation occurred
- what the user should correct

## Defaults

Defaults should represent the safest common workflow, not the most permissive behavior.

For topology repair:

- preserve attributes: on
- correct normals: on
- respect protected zones: on
- preview/validate: on where practical
- automatic destructive cleanup of unmatched vertices: off

## Accessibility and theme

- Use Blender theme colors where practical.
- Do not rely on color alone to communicate state.
- Icons must have tooltips.
- Compact controls must retain adequate hit targets.
- Avoid excessive persistent text in Quickbar; use tooltips and expandable sections.

## UI map requirement

Each add-on must maintain a current UI map. Moving a user-visible feature requires updating the UI map, changelog, state, and relevant screenshots/documentation.