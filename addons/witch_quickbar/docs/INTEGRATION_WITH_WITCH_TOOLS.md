# Quickbar Integration with Witch Tools

## Principle

Witch Quickbar is a secondary access surface. Witch Tools owns canonical general-purpose implementations.

## Integration modes

### Witch Tools installed

Quickbar may:

- call registered Witch Tools operators by stable `bl_idname`
- expose compact buttons for approved Witch Tools actions
- query capability availability
- display a clear unavailable/disabled state when a required Witch Tools version is missing

### Witch Tools not installed

Quickbar must continue to load and run its native standalone features. Optional Witch Tools buttons must not break registration.

## Version compatibility

Each integration must declare:

- minimum Witch Tools version
- required operator IDs
- expected arguments/results
- fallback when unavailable

Avoid importing arbitrary Witch Tools UI modules. Prefer stable operator or backend contracts.

## Canonical ownership

Quickbar must not copy the implementation of:

- Curvature Sync
- Vertex/Edge Inject
- protected-zone logic
- bulk topology repair
- other complex Witch Tools operators

A small wrapper may prepare context and invoke the canonical operator.

## Undo

When Quickbar invokes a Witch Tools scene operator, the operation must appear as one normal undoable action. Quickbar UI state changes remain outside scene undo history.

## UI behavior

Quickbar controls should remain compact. Detailed setup, diagnostics, previews, and repair reports belong in Witch Tools. Quickbar may open/focus the relevant Witch Tools section when a compact invocation is insufficient.

## Distribution

Runtime add-on dependency and build-time vendoring are separate decisions:

- Operator invocation can be optional at runtime.
- Shared low-level modules may eventually be vendored into both packages by the build system.
- Vendored code must be generated from one canonical source and not manually forked.

## Initial Curvature Sync position

Curvature Sync is not a Quickbar feature during prototype development. After it is stable in Witch Tools, Quickbar may receive:

- a shortcut to open the Curvature Sync section
- a compact `Analyze` or `Apply Saved Group` action, only if safe and useful

No Quickbar integration is current scope until the Witch Tools operator contracts are stable.