# Witch Tools Precision Edit — Feature Specification

Status: development candidate  
Candidate: `Dev_v2.10.0`  
Target Blender: `4.5.0`  
Branch: `feature/witch-tools-magic-branch`

## Purpose

Provide fast, explicit mesh-edit precision workflows without relying on selection medians, repeated coordinate entry, or repetitive operator restarts.

Precision Edit contains:

1. Coordinate Copy
2. Planar Edit
3. Inject New
4. shared drag/magnetic infrastructure also used by Magic Branch

Witch Tools remains the canonical backend. Any later Witch Dock / Quickbar exposure must call Witch Tools operators rather than duplicate geometry logic.

## Coordinate Copy

Unchanged from the Dev_v2.9.0 candidate contract:

- Global or Local capture/application;
- any X/Y/Z mask;
- Location / Rotation / Scale geometry-frame operations;
- exactly one vertex/edge/face source capture;
- vertex targets independently; connected edge/face target components independently;
- no selection-wide target median;
- Global converts through world space per object; Local copies numeric object-local values;
- protected-target transaction preflight;
- default Apply shortcut `Ctrl+Shift+C`.

## Planar Edit

Unchanged from Dev_v2.9.0 candidate contract.

### Plane Lock

- stores object-local X/Y/Z lock values in BMesh custom layers;
- supports combined axes, partial unlock, clear-all and edge/face participation through vertices;
- lightweight Edit Mode guard restores locked coordinates;
- existing full Vertex Locks remain stronger protection.

### Level

- one vertex/edge/face source point captured in world space;
- every selected target vertex independently receives source X/Y/Z on enabled axes;
- supports multi-object Edit Mode with per-object world/local conversion;
- incompatible Vertex Lock / Plane Lock targets block before mutation.

## Inject New — Dev_v2.10.0

### Setup

- `Solo`: duplicate one selected vertex, edge, or face with no source connection.
- `Branch`: duplicate one selected vertex, edge, or face and create source-to-copy branch edges.
- `Slide`: insert one vertex into every selected source edge; all new vertices share the same relative position along their own edges.

Branch still creates branch edges, not automatic extrusion side faces.

### Movement

Solo/Branch now use independent global X/Y/Z toggles instead of one exclusive axis choice.

- one axis: motion constrained to that axis;
- two axes: motion constrained to the corresponding global plane;
- XYZ: free view-depth placement;
- optional captured straight Rail remains available and replaces free XYZ movement while enabled.

At least one XYZ axis must be enabled when Rail is off.

### Magnetic Snap

When enabled, the hovered mesh target is highlighted and participates in placement. Target priority is vertex, edge, face.

- vertex: nearest compatible new endpoint lands exactly on it while the rest of the injection remains rigid;
- edge: nearest compatible new endpoint lands on the closest edge point while the rest remains rigid;
- face: each new endpoint follows its own parallel travel line to the hovered face plane/boundary, allowing angled-wall placement without a face-median snap.

### Auto-Merge

Branch + Magnetic Snap may merge compatible contacts on commit.

- existing vertex -> weld;
- edge interior -> split target edge at exact contact then weld;
- compatible two-boundary face contacts may connect/split the face where Blender can do so safely.

Pure arbitrary face-interior retopology is intentionally not invented in this candidate.

Auto-Merge target geometry protected by Vertex Lock or Plane Lock blocks before intentional target mutation.

### Multi-edge Slide

Slide accepts one or more preselected source edges.

- one inserted vertex per selected edge;
- selected edge nearest the cursor acts as the current driver rail;
- every inserted vertex uses the same relative edge factor;
- factor clamps away from exact endpoints to avoid zero-length split edges;
- the selected driver rail is visually indicated.

Dev_v2.10.0 does not dynamically add completely unselected fan edges to the Slide set merely by hovering; that interaction remains deferred until its rollback/selection contract is validated.

### View navigation

During modal placement, holding MMB pauses geometry placement and passes navigation to Blender. The operator assigns the current live injection center as the orbit pivot candidate. Releasing MMB resumes placement.

### Scope / safety

- one active mesh object in Edit Mode;
- multiple shape-key meshes rejected;
- Vertex Lock references snapshotted/restored;
- Plane Lock and Vertex Lock guards suspended during modal topology changes and restored afterward;
- new vertices do not inherit Plane Lock masks;
- finish rejects zero-length edges and zero-area faces;
- cancel removes duplicates or dissolves inserted Slide vertices back out.

## Relationship to Magic Branch

Magic Branch is specified separately in `/docs/features/magic_branch/`. It uses the same `precision_edit_drag.py` and `precision_edit_topology.py` backend so hover, snap, merge, movement and topology primitives remain canonical.

## Edit Tools organization

Default top-level order in Dev_v2.10.0:

1. Coordinate Copy
2. Planar Edit
3. Vertex Snap
4. Object Snap
5. Inject New
6. Magic Branch
7. Edge Doctor
8. Vertex Lock
9. Selection Slots

The order is preference-backed and user-reorderable.

Edge Doctor contains:

- Missing Vertex / Edge Injector;
- Alignment Fixer;
- Curvature Sync.

## Acceptance criteria

Coordinate Copy / Planar Edit retain the Dev_v2.9 acceptance criteria.

Inject New additionally requires:

- all single/pair/triple X/Y/Z masks behave correctly;
- vertex/edge/face highlight matches the magnetic target actually solved;
- edge/vertex snaps preserve rigid geometry except the intended translated contact;
- face snap solves endpoints independently;
- Auto-Merge leaves no coincident duplicate endpoint at supported vertex/edge contacts;
- multiple selected Slide edges receive one inserted vertex each at the same relative factor;
- MMB pauses placement, pivots around current live geometry and resumes without a jump;
- commit/cancel/Undo/Redo do not leave partial destructive topology;
- normals/winding/material and relevant edge attributes are validated;
- manifold safety is required where the operation is expected to preserve manifoldness; loose Branch geometry is explicitly exempt from a global manifold requirement.

See `TEST_PLAN.md` and `/docs/features/magic_branch/TEST_PLAN.md`.

## Out of scope / deferred

- curved/polyline Inject New rails;
- multi-object simultaneous topology creation;
- Branch side-face/extrusion generation;
- arbitrary face-interior Auto-Merge retopology;
- hover-only dynamic addition of unselected fan edges to multi-edge Slide;
- Witch Dock / Quickbar wrappers before Witch Tools Blender 4.5 acceptance.
