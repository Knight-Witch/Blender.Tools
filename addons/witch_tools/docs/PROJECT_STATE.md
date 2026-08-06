# Witch Tools Project State

Last updated: 2026-08-05

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh-operator backend
- Development branch: `feature/witch-tools-guided-align`
- Intended integration branch: `Blender_Dev`
- Development package: `Witch_Tools_Dev`
- Default target Blender version: `4.5.0`

## Current candidate build

- Version: `Dev_v2.8.0`
- Artifact: `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip`
- Size: 138,473 bytes
- SHA-256: `c24ae0b7b4ffc398a80b914a574f0d7118668a85a803b0b6d3bf18c3efb5217c`
- Package folder: `Witch_Tools_Dev`
- Declared target: Blender `4.5.0`
- Python source files: 48
- Total packaged files: 63
- Generated cache files: none
- Runtime status: static candidate; Blender 4.5 UI, geometry, undo/redo, and save/reopen validation pending

## Baseline and source recovery

The repository's Dev_v2.7.0 snapshot cannot be reconstructed from the committed files. Its manifest records 20,000-byte source parts, while the committed parts are truncated to 5,000 bytes. The documented Dev_v2.7.1 patch only contains the narrow N-panel hotfix and is not a complete source tree.

Dev_v2.8.0 therefore uses the last verified complete source baseline, Dev_v2.6.1, and re-establishes the newer alignment capability as an auditable direct source tree. This is an explicit recovery decision, not a claim that the incomplete Dev_v2.7.x snapshot was usable.

Current direct source:

- `addons/witch_tools/dev/Witch_Tools_Dev/`
- feature patch record: `addons/witch_tools/dev/patches/Dev_v2_8_0/`
- verified Dev_v2.6.1 snapshot: `addons/witch_tools/dev/snapshots/Witch_Tools_Dev_v2_6_1/`

## Current implementation

Dev_v2.8.0 adds **Edit Tools > Align Vertices / Edges / Faces** as a four-step workflow:

1. capture a parent anchor;
2. choose a world or custom alignment target;
3. choose free movement or captured straight slide rails;
4. select subordinate geometry, Analyze, and Align.

Implemented behavior:

- parent anchor capture from selected vertices, edges, faces, or mixed selections;
- Active Element or Median anchor reference;
- world-space X/Y/Z coordinate matching with disabled coordinates preserved;
- editable Custom Guide start/end points;
- guide point capture from selected geometry and anchor-to-guide-start copy;
- custom-frame coordinate matching;
- projection onto an arbitrary guide line while preserving distance along the line;
- free-coordinate movement;
- straight captured slide-rail movement;
- one-anchor-to-all and explicit paired-by-rail parent/child mapping;
- rigid relative-spacing/shape preservation;
- whole-selection and per-selected-island grouping;
- optional clamp to captured rail extent;
- Vertex Lock, stale marker, shape-key, ambiguous mapping, impossible constraint, and non-invertible transform preflight;
- world/local conversion for multi-object Edit Mode;
- transaction-first planning before coordinate mutation;
- one Blender Undo operator boundary for Apply.

The operator changes vertex coordinates only. It does not add, remove, weld, reconnect, or remesh topology.

## UI location and order

Current `Edit Tools` order:

1. Vertex Snap
2. Object Snap
3. Edge / Vertex Inject
4. Curvature Sync
5. Align Vertices / Edges / Faces
6. Selection Slots
7. Vertex Locks / remaining Edit Tools controls

## Witch Dock / Quickbar status

Not modified in this pass. Witch Tools must remain the canonical geometry backend. A compact Witch Dock/Quickbar wrapper is deferred until the Dev_v2.8.0 backend is tested in Blender 4.5 and the final operator/property contract is accepted.

## Last completed work

- Read repository, architecture, add-on, and feature rules before changing code.
- Confirmed the current branch, documented versions, Blender target, and source-baseline conflict.
- Reconstructed the verified Dev_v2.6.1 source.
- Added the Guided Align math, operators, properties, registration, panel UI, tooltips, quick-start instructions, and package documentation.
- Restored a direct unpacked development source tree on the feature branch.
- Recorded the compressed source patch and manifest.
- Ran static, pure-math, identifier, UI-state, and package validation.
- Did not modify public branches or Witch Dock/Quickbar source.

## Current known-working state

Previously user-validated in Blender 4.5:

- Dev_v2.5.2 Curvature Sync production collar workflow.
- Quickbar Dev_v1.4.0 Selection Slots workflow.

Dev_v2.8.0 validation completed outside Blender:

- all 48 Python files parsed and compiled;
- 99 operator/panel identifiers have no duplicates;
- seven Guided Align operators are registered in source;
- UI-state names referenced by the panel are declared in preferences;
- seven pure constraint-math assertions passed;
- patch dry-run and application against the verified baseline passed;
- patched source tree matched the packaged candidate source;
- ZIP integrity, safe paths, single package root, and cache exclusion passed.

## Active problems and limitations

1. Blender 4.5 registration, panel rendering, operator execution, undo/redo, and save/reopen are untested.
2. Captured slide rails must be straight within tolerance; curved/polyline rails are rejected.
3. Paired-by-rail mode requires exactly one captured parent vertex in each disconnected rail component.
4. A subordinate island touching multiple rail components is rejected as ambiguous.
5. Multiple shape keys are unsupported.
6. Linked objects sharing one Mesh datablock share marker data.
7. Objects containing captured markers must participate in the current multi-object Edit Mode context.
8. Topology edits can invalidate captured counts and require recapture.
9. Witch Dock/Quickbar exposure is deferred.

## Next exact implementation step

Install `Witch_Tools_Dev_v2_8_0_Guided_Align_Blender_4_5.zip` in Blender 4.5 and test, in order:

1. panel registration, disclosure persistence, and all four UI steps;
2. one red anchor plus yellow targets, world Z matching, free movement;
3. the same geometry using captured vertical rails so targets slide only along existing edges;
4. multiple red parents and green subordinates using disconnected paired rails;
5. a 45-degree Custom Guide, both guide-frame matching and line projection;
6. rigid shape preservation for a connected target region and multiple selected islands;
7. Vertex Locks, stale captures, impossible constraints, shape keys, and ambiguous rails;
8. multi-object Edit Mode with different transforms;
9. undo, redo, save, reopen, and recapture behavior.

Only after this passes should the Witch Dock/Quickbar wrapper be implemented.

## Test status

- Python parse/compile: passed
- Duplicate operator/panel IDs: passed
- UI-state declaration consistency: passed
- Pure constraint math: passed
- Source patch reconstruction: passed
- ZIP integrity/safe paths/package hygiene: passed
- Blender 4.5 registration and panel rendering: not performed
- Blender 4.5 real-mesh execution: not performed
- Undo/redo: not performed
- Save/reopen: not performed
- Witch Dock/Quickbar updated: no
- Public branches or release URLs modified: no
