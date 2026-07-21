# Curvature Sync Test Plan

## General rules

- Target Blender version: 4.5
- Record exact build/version and fixture used.
- Test both success and failure paths.
- Verify geometry numerically where possible, not only visually.
- Every destructive test must verify undo and redo.
- An aborted operation must leave no partial mutation.

## Fixture set

Create sanitized synthetic `.blend` fixtures:

1. clean semicircular quad collar
2. flattened arc sections
3. mismatched parallel-chain vertex counts
4. missing top-chain vertex with valid lower source pair
5. missing connecting column edge
6. multiple missing correspondences across one face strip
7. surplus inline vertices
8. protected straight extensions
9. upper/lower separate fitted solids with mismatched segmentation
10. multiple islands in one object
11. branched/ambiguous topology failure fixture
12. non-manifold failure fixture
13. material/UV/Sharp/Seam/Crease attribute fixture
14. transformed multi-object fixture
15. malformed A/M/Z fixture

The commercial/production collar is a manual validation case, not the only regression fixture.

## Auto-Aligned Vertex Inject tests

### Valid single inject

- select A, B, C in documented order
- D is inserted into the target edge rather than created loose
- D position satisfies configured relationship/tolerance
- C-D edge is created when default toggle is on
- original face becomes exactly two valid faces
- no hole or overlapping face

### Toggle off

- D is injected
- C-D is not created
- face is not split
- mesh remains valid

### Selection failures

- fewer/more than three vertices
- no active C
- A-B not a valid source relation
- target edge missing
- target path fork
- D outside edge/chain
- D overlaps existing vertex
- C/D not on a valid shared face

Expected: clear error, no mutation.

### Attribute preservation

Verify:

- material index
- smooth/flat state
- UV interpolation/continuity
- Sharp, Seam, Crease, and bevel attributes on split inherited edges
- new C-D edge defaults
- vertex groups/custom data where supported

### Normals and winding

- both child faces face the original direction
- no inverted normals
- no zero-area faces
- local normal update succeeds

## Repair-group and chain tests

- ordered open chains detected from explicit selection
- reversed chains normalized or rejected clearly
- disconnected selections rejected
- multiple chains classified correctly
- A/M/Z order validated
- missing sibling anchors reported
- straight geometry outside A/Z excluded

## Circular solve tests

### Exact semicircle

- A/M/Z unchanged
- all intermediate vertices lie on expected circle within tolerance
- even angular spacing
- equal interval count on both sides
- real middle column preserved

### Flattened sections

- flat vertices move to the intended arc
- trusted anchors/guide determine curve
- malformed flat sections do not bias the fit

### Parallel chains

- all chains share identical angular parameters
- each retains intended radius and height
- connecting columns remain coherent
- inter-chain spacing is within tolerance

## Bulk correspondence tests

- inject one missing vertex
- inject multiple vertices across several chains
- create missing edges where vertices already exist
- split all affected faces correctly
- report counts accurately
- leave surplus vertices selected by default
- no automatic unsafe dissolve

## Protected-zone tests

- protected positions do not move
- protected vertices are excluded from fit
- protected elements are not dissolved
- permitted boundary connection succeeds
- permitted adjacent face split succeeds
- forbidden connection aborts without mutation
- straight protected arms remain unchanged byte-for-byte/numerically

## Multi-object and multi-island tests

- common analysis frame handles object transforms
- upper/lower fitted objects receive identical angular column positions
- interface columns align within tolerance
- objects remain separate and retain transforms
- multi-island behavior matches separate-object behavior
- selection and active-object state are restored/documented

## Print-safety tests

- object remains watertight where input was watertight
- no new non-manifold edges
- no self-intersection introduced in supported cases
- wall thickness and A/M/Z dimensions remain within tolerance
- upper/lower assembly alignment is preserved
- face winding is outward

## Undo/redo tests

For each successful operation:

1. capture pre-state counts/coordinates/attributes
2. apply
3. undo
4. verify exact restoration
5. redo
6. verify result matches first apply

Test repeated cycles and operation after mode changes.

## Failure atomicity

Inject faults or use ambiguous fixtures so failures occur during:

- analysis
- edge split planning
- face split planning
- protected-zone validation
- multi-object transform validation

Expected: no partial changes.

## Performance tests

Measure:

- 10, 100, 1,000, and 10,000 planned column correspondences where practical
- analysis time
- apply time
- memory behavior
- UI responsiveness

The implementation should batch BMesh operations rather than call context operators per element.

## Compatibility tests

Required: Blender 4.5.

Any additional version must be recorded as tested only after the same core suite passes or documented exceptions are identified.

## Acceptance record

Every test run must record:

- feature/dev version
- source commit
- Blender version
- operating system
- fixture version
- pass/fail
- screenshots or numeric output where useful
- known deviations
- tester/date