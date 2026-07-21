# Blender Operator Contracts

## Registration

Every operator must have:

- stable `bl_idname`
- clear label and description
- appropriate `bl_options`, including `UNDO` for scene-changing operations where Blender can support it safely
- deterministic registration/unregistration
- no orphaned handlers, keymaps, gizmos, or properties after unregister

## Context and mode handling

Operators must document supported modes and active-object requirements.

- Do not force Object Mode when an operation can safely preserve Edit Mode.
- If a mode transition is required, restore the prior mode and selection state when practical.
- Multi-object Edit Mode support must be explicit and tested.
- Context overrides must be narrow and validated.

## Selection validation

Validate all required objects and mesh elements before mutation.

Errors must distinguish between:

- wrong count
- wrong element type
- missing active element
- disconnected topology
- ambiguous traversal
- unsupported multi-object state
- protected-zone conflict

## Transactional behavior

Multi-step destructive operators must avoid partial results.

Preferred order:

1. analyze
2. validate
3. build an operation plan
4. snapshot required attributes/state
5. mutate
6. validate result
7. update mesh and reports

On failure before commit, leave the mesh unchanged. On unexpected failure during commit, rely on one coherent Blender undo step or restore from the operation snapshot.

## Topology and attribute preservation

Topology-changing operators must intentionally preserve or document changes to:

- face winding and normals
- material index
- smooth/flat face state
- UV and color/custom data
- Sharp, Seam, Crease, bevel weight, and other edge attributes
- vertex groups and shape keys where applicable

A new interior subdivision edge should default to non-sharp unless geometry or explicit settings require otherwise.

## Normals

- Store reference face normals before splitting/rebuilding.
- Preserve winding whenever using native BMesh split/connect operations.
- Compare resulting face orientation against the original where manual reconstruction occurs.
- Recalculate/update only affected geometry where practical.
- Never leave mixed or inverted winding after a successful operation.

## Coordinate frames

Operators must declare whether calculations use object-local, world, view, or custom fitted coordinates.

Multi-object operations must convert participants into a common analysis frame. Object transforms must not silently corrupt spacing or curvature.

## Protected zones

Protected zones may define separate permissions:

- movement prohibited
- topology deletion prohibited
- topology connection/split allowed at boundaries
- participation in curve fitting prohibited

An operator must not treat `protected` as an undefined all-or-nothing state.

## Reports and unresolved data

Successful bulk operators should report counts. Ambiguous or surplus elements should remain selected when useful and be listed in the report.

## Undo and redo

Test:

- immediate undo
- redo
- repeated operator use
- undo after mode restoration
- Quickbar invocation of the same backend

UI-only Quickbar actions must not pollute scene undo history.

## Performance

Bulk topology operators should analyze once and use BMesh or other appropriate batch operations rather than repeatedly invoking context-sensitive `bpy.ops` per element.

## Compatibility

Blender 4.5 is the default target. API use outside that target requires explicit compatibility guards and tests.