# Blender.Tools Parent Architecture

## Purpose

Blender.Tools is a monorepo for a family of Blender add-ons and shared development infrastructure. Permanent organization is based primarily on **capability ownership and distributable add-ons**, while use-case documentation and tests cover BG3 modding, general modeling, and 3D printing.

## Parent components

### Witch Tools

Witch Tools is the primary general-purpose add-on and canonical owner of reusable Blender operators. Its principal UI is a Blender N-panel.

Witch Tools owns stable implementations of:

- general mesh and topology tools
- transform, origin, cursor, selection, and cleanup tools
- weight, armature, naming, and refit tools
- BG3-specific workflow modules when they are not reusable outside BG3
- 3D-print-oriented geometry tools when they are not full manufacturing workflows
- protected edit-zone and geometry-selection infrastructure
- shared operator backends used by Quickbar or Witch Core

### Witch Quickbar

Witch Quickbar is a separately distributed floating-overlay companion. It is not an N-panel implementation and must retain a separate architecture for:

- overlay drawing
- gizmo and event routing
- dragging and resizing
- lock, minimize, maximize, close, and launcher states
- preferences and persistence
- icon and asset loading
- pass-through behavior
- file-load recovery
- separation of UI-only actions from undoable scene changes

Quickbar may invoke Witch Tools operators when available. It must not contain a second canonical implementation of a complex Witch Tools feature.

### Witch Core

Witch Core is a specialized workflow add-on for 3D-printing and manufacturing processes, initially including Cauldron Core housing generation. It may compose reusable Witch Tools/shared geometry functions into larger process-driven workflows.

### Witch Dev Modules

Dev modules isolate unstable operators and UI experiments. They may use independent `Dev_v###` versions until integration. A dev module is not automatically release scope.

## Shared layers

The intended long-term tree is:

```text
Blender.Tools/
├── addons/
│   ├── witch_tools/
│   ├── witch_quickbar/
│   └── witch_core/
├── shared/
│   ├── geometry/
│   ├── topology/
│   ├── protection/
│   ├── selection/
│   ├── logging/
│   └── compatibility/
├── prototypes/
├── docs/
├── tests/
├── build/
└── dist/
```

This is a target structure. Existing public branches are not moved into it until compatibility and URL audits are complete.

## Canonical backend rule

Each capability has one canonical implementation. UI surfaces call that implementation rather than copying it.

Example:

```text
Shared/Witch Tools topology backend
├── Curvature Sync
├── Vertex Inject
├── face split and attribute preservation
└── protected-zone queries

Witch Tools N-panel
└── full controls and diagnostics

Witch Quickbar
└── optional shortcut or compact invocation

Witch Core
└── process workflow invokes backend when needed
```

## Distribution dependency model

Preferred long-term model: one canonical shared source in the repository, vendored into independently installable release packages during the build process. This avoids runtime add-on dependency conflicts while preventing source duplication.

No vendoring system is considered implemented until build scripts and manifests exist and are tested.

## Use-case organization

BG3, general modeling, and 3D printing are application domains, not separate copies of the same code.

- Code belongs to its canonical capability/add-on owner.
- Use-case documents describe domain-specific workflows and limitations.
- Tests may be grouped by domain where different geometry or export constraints apply.

## Coordinate and transform policy

Geometry algorithms must explicitly document whether they operate in:

- object-local space
- world space
- view space
- a fitted/custom coordinate frame

Multi-object tools must convert all participating data into one declared analysis frame and restore results correctly to each object's local space.

## Data preservation policy

Topology-changing operators must explicitly handle or document:

- face winding and normals
- material indices
- smooth/flat face state
- UV layers
- color/custom data layers
- edge Sharp, Seam, Crease, and bevel attributes
- vertex groups and shape keys where relevant
- manifold and watertight requirements

## Failure policy

Operators must validate before mutation where possible. Ambiguous topology must produce a clear failure or preview report rather than a destructive guess. Multi-step operations must be transactional or provide reliable rollback through Blender undo.

## Public compatibility policy

Public branches, package folder names, operator IDs, preferences identifiers, update URLs, and release locations are API/compatibility surfaces. They remain stable until an audited migration provides an equivalent path.