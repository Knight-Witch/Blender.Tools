# Selection Slots

Selection Slots is a persistent mesh-selection workflow owned by Witch Tools and optionally exposed through Witch Quickbar.

## Purpose

The feature lets a user save an exact Edit Mode vertex, edge, face, or mixed-domain selection, continue working, and restore that selection later without rebuilding it manually.

The production reference case is the collar Curvature Sync workflow, where dozens of fragmented parallel chains had to remain reusable across repeated Analyze/Apply tests.

## Ownership

- Canonical backend and N-panel UI: Witch Tools
- Optional compact access surface: Witch Quickbar
- Target Blender version: 4.5
- Development branch: `Blender_Dev`

Quickbar invokes the registered `mesh.wt_selection_slot_*` operators. It does not keep a second copy of saved-selection data.

## Packet

- `SPEC.md` — behavior contract and UI requirements
- `STATE.md` — actual implemented build state
- `ROADMAP.md` — current, deferred, and research scope
- `TEST_PLAN.md` — acceptance and regression tests
- `DECISIONS.md` — accepted design decisions
- `REFERENCE_CASES.md` — production and synthetic examples
