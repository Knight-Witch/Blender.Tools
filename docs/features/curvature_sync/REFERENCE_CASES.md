# Curvature Sync Reference Cases

## CS-R01 — Flat chunks in an intended semicircular collar

Problem:

- a large curved span is represented by uneven polygonal sections;
- several local edge runs are visibly flat;
- ordinary Subdivide adds vertices along existing straight chords and does not restore intended curvature.

Required behavior:

- preserve A/M/Z and overall fit-critical arc;
- move eligible intermediate vertices to the circular solution;
- exclude straight extensions beyond A/Z.

## CS-R02 — Parallel chains with different vertex counts

Problem:

- outer, inner, bevel, wall, and inset chains were built independently;
- corresponding radial columns do not exist;
- LoopTools spacing/circle cannot create correspondence between chains with unequal counts.

Required behavior:

- create one canonical angular lattice;
- inject missing vertices where needed;
- align all chains to the same angles;
- preserve per-chain radius and height.

## CS-R03 — Inline vertices without cross-chain edges

Problem:

- vertices exist in the middle of valid face-boundary edges;
- they are not loose;
- some do not have the matching connecting edge to adjacent chains.

Required behavior:

- classify them as surplus, matched, or reusable;
- create missing siblings/connecting edges when valid;
- do not use Delete Loose;
- do not automatically dissolve by default.

## CS-R04 — Single missing vertex/column

Problem:

- source column A-B exists;
- target lower vertex C exists;
- corresponding upper vertex D is missing inside an edge;
- one broad face should become two faces.

Required behavior:

- calculate/inject D;
- connect C-D by splitting the original face;
- preserve winding, normals, material, smooth state, and edge attributes.

## CS-R05 — Bulk missing columns

Problem:

- many column positions exist on some chains but are absent on others;
- manual subdivide/slide/connect is slow and error-prone.

Required behavior:

- analyze all required canonical positions;
- inject and split in bulk;
- report unresolved/surplus topology;
- remain one undoable operation.

## CS-R06 — Protected straight collar arms

Problem:

- the curved rear span transitions into straight outward arms;
- smoothing/circle tools may move the straight geometry.

Required behavior:

- A/Z bound the movable span;
- protected straight zones remain coordinate-identical;
- protected boundary vertices may accept permitted connections/splits without moving.

## CS-R07 — Required center column and bilateral count

Problem:

- existing columns are not symmetric around the intended middle/Y axis;
- one side has a different count or spacing.

Required behavior:

- require/repair M;
- produce the same number of intervals on both sides;
- use an odd total column count;
- evenly distribute angular positions.

## CS-R08 — Upper and lower print halves fit but topology does not align

Problem:

- two separate solid mesh objects occupy the correct assembly geometry;
- their interface and curved surfaces use unrelated segmentation;
- corresponding columns do not line up visually or topologically.

Required behavior:

- one master lattice drives both objects;
- each retains its own solid geometry and Z/height structure;
- interface column planes align within tolerance;
- if joining faces were removed and boundaries merged, the columns would continue as coherent loops.

## CS-R09 — Mesh islands instead of separate objects

Problem:

- corresponding upper/lower or layered parts are separate islands in one object.

Required behavior:

- same as multi-object synchronization, without assuming connected topology.

## CS-R10 — Ambiguous feature interruption

Problem:

- details, poles, branches, notches, or non-manifold geometry interrupt a target path.

Required behavior:

- preflight reports ambiguity;
- protected/excluded zones may isolate the region;
- tool aborts rather than routing a column through unrelated geometry.

## CS-R11 — Print-critical preservation

Problem:

- topology must be cleaner/smoother without changing assembly fit, wall dimensions, straight arms, or small details.

Required behavior:

- preserve anchors and protected dimensions;
- maintain watertightness/manifold state where applicable;
- do not remesh or approximate protected features;
- verify normals and winding.

## Fixture policy

Create synthetic repository fixtures reproducing these topology patterns. Do not require proprietary or commercially sensitive production meshes for automated tests.