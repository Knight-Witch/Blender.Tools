# Quickbar Integration with Witch Tools

## Principle

Witch Quickbar is a secondary access surface. Witch Tools owns canonical general-purpose implementations and persistent scene/mesh data.

## Integration modes

### Witch Tools installed

Quickbar may:

- call registered Witch Tools operators by stable `bl_idname`;
- expose compact buttons for approved Witch Tools actions;
- query capability availability;
- display a clear unavailable/disabled state when a required Witch Tools version or operator is missing.

### Witch Tools not installed

Quickbar must continue to load and run its native standalone features. Optional Witch Tools controls must not break registration, overlay drawing, or viewport input.

## Version compatibility

Each integration must declare:

- minimum Witch Tools version;
- required operator IDs;
- expected arguments/results;
- fallback when unavailable.

Avoid importing arbitrary Witch Tools UI modules. Prefer stable operators or backend contracts.

## Canonical ownership

Quickbar must not copy the implementation of:

- Curvature Sync;
- Vertex/Edge Inject;
- Selection Slots persistence and mesh markers;
- protected-zone logic;
- bulk topology repair;
- other complex Witch Tools operators.

A small wrapper may prepare context and invoke the canonical operator.

## Selection Slots contract — Dev_v1.4.0

Minimum backend: Witch Tools Dev_v2.6.0.

Required operators:

- `mesh.wt_selection_slot_add`
- `mesh.wt_selection_slot_remove`
- `mesh.wt_selection_slot_save`
- `mesh.wt_selection_slot_clear`
- `mesh.wt_selection_slot_clear_all`
- `mesh.wt_selection_slot_reselect`
- `mesh.wt_selection_slot_rename`
- `mesh.wt_selection_slot_move`

Read-only presentation data:

- `context.scene.witch_tools.selection_slots`
- each slot's `name`, `has_data`, and display order.

Quickbar behavior:

- save/reselect/clear/remove/add/Clear All invoke the corresponding operator;
- rename uses a Quickbar dialog and commits through the Witch Tools rename operator;
- grip drag calculates a target row and commits repeated one-step Witch Tools move operations;
- Quickbar stores no duplicate slot collection, UID, object references, counts, or mesh custom layers;
- when the collection/operators are unavailable, the Select tab displays `Witch Tools Dev_v2.6.0+ required` and remains non-blocking.

## Undo

When Quickbar invokes a Witch Tools scene/data operator, the operation must appear according to the canonical operator's undo contract. Quickbar UI state changes remain outside scene undo history.

## UI behavior

Quickbar controls remain compact. Detailed diagnostics, persistence semantics, topology propagation warnings, and test reporting belong in Witch Tools and the Selection Slots feature packet.

## Distribution

Runtime add-on dependency and build-time vendoring are separate decisions:

- Selection Slots currently uses optional runtime operator invocation.
- Quickbar remains installable without Witch Tools.
- Shared low-level modules may eventually be vendored by a tested build system.
- Vendored code must be generated from one canonical source and not manually forked.

## Curvature Sync position

Curvature Sync remains a Witch Tools feature. Quickbar integration is not included in Dev_v1.4.0; the Select tab exposes Selection Slots only.

## Required tests

- Witch Tools Dev_v2.6.0 enabled before Quickbar;
- Witch Tools disabled while Quickbar remains enabled;
- Witch Tools unregistered during a Quickbar session;
- operator cancellation and warnings;
- selection-slot action undo/redo;
- file change and scene slot refresh;
- no duplicate backend data;
- no Quickbar registration or input failure when the dependency is missing.
