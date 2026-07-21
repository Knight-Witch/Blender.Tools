# Curvature Sync Specification

## 1. Status and scope

Status: design specification. No implementation is implied.

Initial scope:

- Blender 4.5
- Edit Mode mesh topology
- planar circular open-arc spans
- multiple parallel edge chains
- separate mesh islands and separate aligned objects
- explicit A/Z span endpoints
- explicit or validated middle M column
- protected/ignored zones
- optional correspondence injection and face splitting
- print-critical geometry preservation

Later generic spline or non-planar support is outside the first implementation scope.

## 2. Terminology

### Chain

An ordered open sequence of connected vertices/edges following one curved horizontal/profile boundary.

### Parallel chain family

Several corresponding chains that describe different radii, heights, bevel boundaries, walls, or inset boundaries of the same curved structure.

### Column

A corresponding set of vertices/edges crossing from one chain to adjacent chains. In the collar reference, these are the visually vertical/radial edge chains.

### A and Z

The fixed start and end vertices of the curved repair span. Geometry beyond A and Z is outside curvature repair and normally remains straight/unchanged.

### M

The middle column/anchor on the declared symmetry axis. It divides the repair span into equal left and right sides.

### Canonical column lattice

The authoritative ordered set of angular positions shared by every participating chain and object.

### Master

The object/chain group providing the authoritative coordinate frame, anchors, or layout.

### Follower

Another chain/object synchronized to the master's canonical lattice while retaining its own radius and offsets.

### Protected zone

A stored set of mesh elements with explicit permissions controlling movement, deletion, fitting participation, and boundary topology operations.

## 3. User goals

The tool must let the user:

1. repair multiple malformed parallel curves together;
2. maintain the original overall circular curvature and fit-critical boundaries;
3. exclude straight extensions from curve repair;
4. create matching vertex/edge correspondence where it is missing;
5. produce an equal number of evenly spaced columns on both sides of M;
6. require a true middle column;
7. synchronize upper/lower or otherwise fitted objects so their columns align when assembled;
8. preserve topology attributes, winding, normals, and watertightness;
9. inspect/confirm planned repairs before destructive mutation.

## 4. Coordinate model

### Analysis frame

The operator must use one declared common analysis frame:

- object-local for single-object mode; or
- master-object local / explicit world frame for multi-object mode.

Every participant is transformed into the analysis frame for solving and transformed back into its own object-local space for mutation.

### Arc plane and axis

The first implementation solves a planar circle/arc with:

- plane origin/center `O`
- plane normal / curvature axis `N`
- angular span from A to Z
- middle direction/plane M

The center/symmetry reference may be specified by:

- object local X/Y/Z axis;
- world X/Y/Z axis;
- custom selected edge/vector;
- 3D Cursor and axis;
- fitted A/M/Z circle where permitted.

For the collar reference, the middle column lies on the local Y symmetry axis.

## 5. A/M/Z anchor contract

### A and Z

- A and Z define the movable curved span on every chain.
- A/Z positions are preserved by default.
- Vertices outside the ordered A-to-Z path are excluded from curvature movement.
- Protected straight extensions beyond A/Z are not curve-fit samples.

### M

- M is a real column position, not merely the midpoint between two columns.
- M must exist on every participating chain after correspondence repair.
- M positions are preserved by default and excluded from redistribution movement unless the user explicitly allows center correction.
- The number of intervals from A to M must equal the number from M to Z.

### Anchor validation

Preflight must detect:

- missing A, M, or Z sibling vertices;
- reversed chain ordering;
- A/M/Z not lying in a valid order;
- inconsistent center axis;
- mismatched spans between objects;
- anchors outside tolerance of the common frame.

The tool must offer a repair plan where valid, not silently invent anchors.

## 6. Canonical symmetrical column lattice

The user specifies either:

- segments per side; or
- total odd column count; or
- desired spacing from which a valid symmetrical count is derived.

Contract:

```text
Total columns = 2 * segments_per_side + 1
```

The lattice includes A, M, and Z and equal angular intervals on both sides of M.

Every participating chain uses the same ordered angular parameter values:

```text
θ0 ... θM ... θZ
```

The default distribution is even angular spacing, calculated separately over A-to-M and M-to-Z if the anchors are not perfectly symmetric within tolerance. In strict symmetry mode, the tool validates or derives a mirrored angular span and aborts when anchors contradict it beyond tolerance.

## 7. Multiple parallel chain solution

All chains in a repair group share:

- analysis plane
- circle center
- angular positions
- A/M/Z index mapping

Each chain preserves:

- its own radius;
- its own axial/height coordinate;
- intended offset from neighboring chains;
- protected anchors.

### Radius determination modes

1. **Anchor-derived per-chain radius** — use trusted A/M/Z positions for that chain.
2. **Preserve existing median radius** — robust median of eligible curved vertices after outlier exclusion.
3. **Master offset** — derive follower radius/offset from its relationship to a master chain.

Default for print-critical corresponding chains: preserve per-chain anchor-derived radius and shared center.

### Inter-chain spacing

Where adjacent chains form one face strip, corresponding columns must preserve a stable relationship. The operator must support:

- preserve each chain independently on concentric radii; and
- preserve measured master-to-follower offset at A/M/Z where geometry is not perfectly concentric.

The first circular collar implementation should use shared center plus per-chain radius/height.

## 8. Multi-object and multi-island synchronization

The repair group may contain chains from:

- one connected mesh;
- multiple islands in one mesh object;
- multiple separate objects already aligned in assembly position.

One master group defines the canonical lattice. Followers receive the same angular positions.

Follower objects retain their own:

- transforms;
- radii;
- height and bevel dimensions;
- materials and data layers;
- separate solid boundaries.

At the physical interface between upper/lower parts, corresponding column planes must align within tolerance so the parts would form visually continuous loops if joining faces were removed and boundary vertices merged.

## 9. Protected and ignored zones

Protected zones require explicit permissions.

### Default Curvature Sync protected behavior

Protected vertices:

- do not move;
- are excluded from curve fitting;
- are not dissolved;
- are not replaced.

Boundary topology may still be modified only when permitted:

- an injected vertex may connect to a protected adjacent vertex;
- a face touching a protected boundary may be split to maintain a closed surface;
- the protected vertex coordinate remains unchanged;
- the operation must not delete or reorder protected boundary elements.

### Required permission flags

A future shared protected-zone data model should support:

- `lock_position`
- `exclude_from_fit`
- `forbid_dissolve`
- `allow_boundary_connect`
- `allow_adjacent_face_split`

Curvature Sync must not treat protection as an undefined all-or-nothing flag.

## 10. Correspondence analysis

Before curvature movement, analyze every canonical column position on every chain.

Possible states:

- exact corresponding vertex exists;
- vertex exists within snap tolerance but is misplaced;
- required vertex is missing inside an edge;
- both vertices exist but connecting edge is missing;
- one endpoint exists and the sibling must be injected;
- multiple candidate vertices create ambiguity;
- topology branch/pole prevents safe chain continuation;
- surplus unmatched vertex exists.

The analysis produces a preview/report without mutation.

## 11. Auto-Aligned Vertex Inject prerequisite

### Selection model

Basic Mode 1 uses three selected vertices in ordered/active context:

- A: source upper/reference vertex
- B: source lower/reference vertex
- C: target lower/reference vertex, active/selected last
- D: new vertex to inject on the corresponding target edge

Flat/default relationship:

```text
D_ideal = C + (A - B)
```

Curvature-aware relationship:

- determine C's canonical angle;
- place D on A's chain/radius at the same angle;
- preserve A/B source chain relationship or shared curvature frame as configured.

### Target edge detection

The operator identifies the target edge/edge chain corresponding to A's row in the B-to-C direction. It must stop at forks or ambiguous paths.

### Injection

- split the containing edge at D;
- do not create a loose overlapping duplicate;
- preserve interpolated vertex/custom data;
- preserve inherited edge attributes on both resulting edge segments.

### Connect and split default

`Connect & Split Face` is on by default and toggleable.

When C and D lie on one face boundary:

- create edge C-D through a native BMesh face split/connect operation;
- replace the original face with two child faces;
- preserve original face winding, material index, smooth state, and custom data where possible;
- create C-D as a non-sharp internal subdivision edge by default;
- update local normals.

The implementation should not delete/refill manually when a native face split is valid.

### Failure rules

Abort before mutation if:

- selection is invalid;
- A-B relation is invalid;
- target edge cannot be resolved;
- projected D is beyond tolerance;
- D would overlap an existing vertex without a valid reuse plan;
- C and D cannot safely split a shared face;
- connection crosses unrelated topology;
- protected permissions forbid the required operation.

## 12. Bulk missing correspondence injection

Given a master lattice and multiple chains, bulk repair must:

1. order chains and vertices;
2. determine required canonical positions;
3. match existing vertices by angular/arc parameter and tolerance;
4. move eligible matched vertices when requested;
5. inject missing vertices into containing edges;
6. create missing column edges;
7. split affected faces;
8. preserve attributes and normals;
9. report unresolved/surplus topology.

### Surplus vertices

Default behavior: leave unmatched surplus vertices in place and select/report them.

Optional later behaviors:

- move to nearest canonical column;
- dissolve only when topologically safe and explicitly enabled.

Automatic dissolution is not first-version default.

## 13. Curvature fitting and flat-section exclusion

Malformed flat sections must not distort the intended arc.

Trusted fit sources may include:

- A/M/Z anchors;
- explicitly selected trusted reference vertices;
- stored curvature guide;
- locked vertices marked as trusted anchors;
- robust curved-region samples after flat-run/outlier rejection.

Initial deterministic mode: derive the circular frame primarily from A/M/Z and declared symmetry/center constraints.

Automatic flat-run detection may assist but must not override explicit anchors or silently accept an underdetermined fit.

## 14. Repair operation phases

### Analyze

- identify objects, islands, chains, A/M/Z, protected zones, and candidate columns;
- validate common frame;
- report missing and surplus correspondence;
- produce planned movement/topology counts.

### Repair correspondence

- inject missing A/M/Z and interior vertices;
- create missing column edges;
- split faces;
- preserve geometry attributes;
- stop and report unresolved ambiguity.

### Preview curvature

- calculate destination positions;
- optionally draw ghost positions/columns;
- do not mutate source mesh.

### Apply Curvature Sync

- move eligible vertices to canonical arc positions;
- preserve anchors and protected coordinates;
- ensure matching angular positions across chains/objects;
- update mesh normals;
- validate result;
- leave unresolved geometry selected;
- commit as one undoable operation.

## 15. Normals, winding, and attributes

Every created/split face must preserve original outward orientation.

Required preservation where applicable:

- face material index
- face smooth state
- UV/custom loop data
- edge Sharp
- edge Seam
- edge Crease
- bevel weight/custom edge attributes
- vertex groups and shape-key behavior must be explicitly evaluated before moving/injecting vertices

New interior column edges are non-sharp unless inherited geometry or an explicit option says otherwise.

After topology and movement:

- update affected face normals;
- compare/reverse any manually created face whose normal opposes its source face;
- validate no zero-area/degenerate faces were created.

## 16. UI proposal

### Curvature Sync group

- Create/Update Repair Group
- Analyze
- Set A Endpoints
- Set Z Endpoints
- Set/Verify Middle Column
- Set Master Object/Chains
- Use Protected Zones

### Column layout

- Symmetrical Layout — default on
- Require Middle Column — default on
- Segments per Side
- calculated Total Columns
- Even Angular Spacing — default on
- Same Layout Across Objects — default on

### Repair controls

- Inject Missing Correspondence
- Build Missing Column Edges
- Preview Curvature
- Apply Curvature Sync

### Preservation

- Preserve A/M/Z — default on
- Preserve Per-Chain Radius — default on
- Preserve Inter-Chain Spacing — default on
- Respect Protected Zones — default on
- Preserve Attributes — default on
- Correct Normals — default on
- Leave Unresolved Selected — default on

### Modes

- Validate Only
- Correspondence Repair Only
- Curvature Only
- Inject + Curvature

No repeated post-operation popup is required; persistent options and preview are preferred.

## 17. Reports

Analysis report should include:

- objects/islands/chains found
- A/M/Z validation
- current per-chain vertex counts
- requested canonical column count
- missing anchor siblings
- missing interior vertices
- missing connecting edges
- surplus/unmatched vertices
- protected conflicts
- ambiguous paths

Apply report should include:

- vertices injected
- vertices moved
- edges created
- faces split
- objects processed
- normals corrected
- unresolved items

## 18. Acceptance criteria

The first Curvature Sync implementation is accepted only when:

1. Multiple selected parallel chains share one canonical circular angular lattice.
2. A, M, and Z remain fixed by default.
3. Straight geometry outside A/Z remains unchanged.
4. Left/right column counts are symmetrical with a real middle column.
5. Missing vertices and column edges can be injected through safe face splits.
6. Corresponding columns align across separate fitted objects/islands.
7. Per-chain radii and intended spacing are preserved within configured tolerance.
8. Protected vertices do not move, while allowed boundary connects/splits still complete the surface.
9. Face winding, normals, material, smooth state, and supported edge attributes are preserved.
10. Undo restores the exact pre-operation mesh and redo reapplies it.
11. Ambiguous input aborts without partial destructive changes.
12. Tests include the split-collar reference pattern and synthetic fixtures.

## 19. Known limitations of initial version

- planar circular arcs only;
- explicit chain/anchor setup may be required;
- complex poles, branches, non-manifold regions, and feature interruptions may require manual exclusion;
- shape-key compatibility requires dedicated design/testing and may initially be blocked;
- arbitrary automatic cleanup of surplus vertices is not included;
- no claim of generic retopology.