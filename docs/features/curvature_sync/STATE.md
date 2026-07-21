# Curvature Sync State

Last updated: 2026-07-20

## Status

- Feature phase: specification
- Implementation: not started
- Owning add-on: Witch Tools
- Target Blender version: 4.5
- Feature version: unassigned
- Development branch: planned after Witch Tools baseline import

## Implemented

Nothing. The current repository contains design and documentation only.

## Specified

- Auto-Aligned Vertex Inject Mode 1
- default Connect & Split Face behavior
- local normal/winding and attribute preservation
- curvature-aware vertex placement
- bulk missing correspondence injection
- multiple parallel chain repair
- A/M/Z anchor model
- canonical symmetrical angular column lattice
- protected/ignored zone semantics
- multiple object/island synchronization
- upper/lower fitted print-part column alignment
- preflight, preview, and failure behavior

## Not implemented

- source modules
- operators
- UI
- persistent repair groups
- protected-zone extension
- preview drawing
- tests and fixtures
- build integration
- Quickbar integration

## Blocking dependencies

1. Locate and import the current Witch Tools development baseline.
2. Inspect the actual Vertex Lock implementation and data model.
3. Confirm current module registration and UI architecture.
4. Create synthetic test fixtures representing the collar topology failures.

## Current known-working state

None. No Blender runtime claim is made.

## Active risks

- ambiguous edge-chain traversal
- multi-object coordinate transforms
- protected-zone boundary permissions
- UV/custom-data interpolation on edge split
- non-manifold or branched topology
- shape keys
- transaction/undo integrity across bulk BMesh changes
- accidental movement of print-critical anchors

## Next exact implementation step

After Witch Tools baseline import, build a minimal isolated Dev module implementing only:

1. ordered A/B/C selection validation;
2. target-edge resolution for a single shared face;
3. D injection by edge split;
4. C-D face split;
5. face/edge attribute preservation;
6. normal/winding validation;
7. one-step undo.

Do not start multi-chain curvature solving until this primitive passes its test plan.

## Files changed in latest update

Documentation packet only.

## Test status

Not tested.