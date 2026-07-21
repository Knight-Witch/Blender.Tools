# Blender.Tools Tests

## Purpose

Tests are organized by capability and use case. Test fixtures must be sanitized and distributable within repository permissions.

## Target structure

```text
tests/
├── automated/
├── manual/
├── fixtures/
│   ├── topology/
│   ├── bg3/
│   └── printing/
├── expected_results/
└── output/              # ignored
```

## Test record requirements

Every run records:

- add-on/feature version
- source commit
- Blender version
- operating system
- fixture version
- steps performed
- pass/fail
- known deviations

## Topology tests

At minimum verify:

- undo/redo
- mesh mode/context
- normals and winding
- attribute preservation
- protected zones
- manifold safety where applicable
- multiple objects/islands where supported
- malformed selection handling
- no partial destructive failure

## Production references

Commercial or copyrighted production meshes may be used for private manual validation but must not be the only regression cases. Reproduce failures in synthetic fixtures.

## Current state

No automated test runner or fixture suite has been imported yet. Curvature Sync fixture requirements are defined in its `TEST_PLAN.md`.