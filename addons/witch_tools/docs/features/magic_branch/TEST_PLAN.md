# Magic Branch / Magnetic Precision — Blender 4.5 Test Plan

Candidate: `Witch Tools Dev_v2.10.0`  
Target: Blender `4.5.0`

No runtime item is passed until executed and recorded in Blender.

## A — Registration / UI / persistence

1. Install/enable in Blender 4.5; no traceback.
2. Confirm version displays Dev_v2.10.0 and target 4.5.
3. Edit Tools default order: Coordinate Copy, Planar Edit, Vertex Snap, Object Snap, Inject New, Magic Branch, Edge Doctor, Vertex Lock, Selection Slots.
4. Edge Doctor contains Missing Vertex / Edge Injector, Alignment Fixer, Curvature Sync.
5. Expand/collapse all sections and hover their help controls.
6. Toggle Reorder Tools; drag at least three sections to new positions and verify the visible order updates.
7. Verify up/down fallback works for every row.
8. Restart Blender and confirm custom order persists.
9. Reset default order.
10. Disable/re-enable add-on; no registration/unregistration errors.

## B — Inject New movement / Magnetic Snap

For Solo and Branch; repeat with Vertex, Edge, Face sources:

1. Test X only, Y only, Z only, XY, XZ, YZ, XYZ.
2. Confirm disabled world axes do not change.
3. Hover a vertex: vertex highlight appears and the nearest compatible new endpoint lands exactly on it.
4. Hover an edge: edge highlight appears; one compatible endpoint lands on the closest edge point while the remaining copied geometry preserves rigid alignment.
5. Hover a face: face highlight appears; each copied endpoint follows its own travel line to the face/boundary.
6. Use an angled parallel target wall and confirm two edge endpoints may resolve to two different boundary locations.
7. Move cursor between vertex/edge/face overlap and verify priority Vertex > Edge > Face.
8. Turn Magnetic Snap off; no target highlight and no magnetic solve.
9. Cancel from every target type and compare topology/coordinates/counts with the pre-operation state.
10. Undo/redo each committed case.

## C — Inject New Auto-Merge

Branch only, Magnetic Snap on:

1. Branch Vertex to existing vertex; commit. Confirm no duplicate endpoint remains and source connects directly to target.
2. Branch Vertex to target edge interior; confirm target edge is split exactly at contact and branch welds to that vertex.
3. Branch Edge to two compatible target boundaries; confirm both contacts become shared topology where supported.
4. Branch toward a face and exercise two boundary contacts that should split/connect the target face.
5. Confirm a pure face-interior magnetic placement does not silently invent arbitrary retopology.
6. Repeat with Auto-Merge off; new topology must remain separate even though placement is magnetically aligned.
7. Target protected by Vertex Lock: merge must fail safely without partial target mutation.
8. Target protected by Plane Lock: merge must fail safely without partial target mutation.
9. Check zero-length edges, zero-area faces, duplicate edges/verts, normals and winding after every merge.
10. Undo/redo and cancel checks.

## D — Multi-edge Slide

1. Select two parallel edges, invoke Slide, confirm one new vertex appears in each.
2. Move cursor near edge A; A becomes driver and both new vertices use the same relative factor.
3. Move cursor near edge B; B becomes driver without changing the shared factor relationship.
4. Repeat with 3–10 parallel selected edges.
5. Test differently sized but parallel edges; factor must remain relative, not absolute distance.
6. Test boundary, loose, and manifold selected edges.
7. Test Seam/Sharp/Crease/bevel/custom edge data and record Blender/BMesh preservation behavior.
8. Commit near each endpoint; clamp prevents zero-length splits.
9. Cancel after moving across several drivers; topology exactly restores.
10. Undo/redo committed multi-edge splits.
11. Verify unselected nearby fan edges are not silently added in Dev_v2.10.0.

## E — MMB orbit during Inject New

1. Begin dragging a live Vertex, Edge, and Face injection.
2. Hold MMB; live placement must pause.
3. Orbit in several directions; viewport should pivot around the live injection position.
4. Release MMB; placement resumes without a sudden geometry jump.
5. Repeat while magnetically snapped and while unsnapped.
6. Commit/cancel after orbit and verify topology.

## F — Magic Branch Vertex

1. Single Branch, XYZ free: click-drag source vertex into empty space; release creates one source-to-new edge and exits.
2. Persistent: create five branches consecutively without restarting the operator.
3. Test every axis combination.
4. Magnetic vertex and edge targets with Auto-Merge off/on.
5. Vertex-to-vertex Auto-Merge must reduce to direct source-target edge.
6. Face magnetic placement.
7. MMB orbit mid-drag.
8. Esc while waiting and Esc/right-click while live; no partial topology.
9. Undo/redo Single Branch.
10. In Persistent, verify one Undo step per committed branch if that is the intended runtime result; record any Blender modal limitation exactly.

## G — Magic Branch Edge

1. Single and Persistent.
2. Verify copied edge dimension/orientation stays rigid for vertex/edge magnetic snap.
3. Angled face target: endpoints solve independently.
4. Auto-Merge each endpoint to target vertices/edges.
5. Check source-to-copy side edges, no unintended faces.
6. MMB, cancel, undo/redo.
7. Verify materials/custom edge attributes on copied source edge; branch edges must not receive unsupported accidental source attributes.

## H — Magic Branch Face / Organic

1. Use a quad source face; drag toward each of its four edges and confirm emitted face switches to the edge nearest drag direction.
2. XYZ and constrained-axis movement.
3. Magnetic vertex/edge/face target tests.
4. Auto-Merge compatible outer contacts.
5. Confirm exactly one new face is created per branch.
6. Verify source face remains intact/shared at emission edge.
7. Normals/winding and material behavior.
8. Cancel from multiple positions; exact rollback.
9. MMB orbit and resume.
10. Undo/redo.

## I — Magic Branch Face / Paver

1. Quad source with known dimensions.
2. Drag one tile away; confirm new face dimensions match source tile depth/edge width as defined by emitting edge.
3. Drag farther; 2, 3, 5+ equal tiles appear.
4. Drag back; tile count decreases cleanly with no stale topology.
5. Switch drag direction around source face; emitting edge changes cleanly.
6. Magnetic hover over an on-grid endpoint and commit.
7. Hover an off-grid endpoint; verify Paver preserves equal tile size rather than stretching final tile.
8. Auto-Merge only where final outer contacts actually coincide compatibly.
9. Cancel after multiple rebuilds; exact source topology restored.
10. Normals/winding/material/edge-data tests.
11. Undo/redo.

## J — Edge Doctor

### A/B/C

1. Re-run existing known A/B/C repair cases and compare Dev_v2.9 behavior.
2. Verify projection tolerance, existing-vertex reuse, target split and optional Connect & Split.
3. No regression in lock/protected-zone handling.

### Two-edge L

1. Select exactly two edges sharing one corner B.
2. Confirm inferred D = A + C - B in local mesh coordinates.
3. If a vertex already exists within merge tolerance at D, reuse it.
4. Otherwise create D and connect A-D and C-D.
5. Test rotated/non-uniform object transform; local parallelogram relationship must remain consistent.
6. Test malformed: disjoint two edges, same endpoints, zero-length leg, extra selected edges.
7. Cancel/failure must not partially mutate.
8. Undo/redo.

## K — Topology/protection regression

For every topology-changing mode above:

- Vertex Locks remain fixed and references survive topology changes;
- Plane Locks remain valid and new verts do not inherit stale lock masks;
- Protected Edit Zone behavior remains correct;
- multiple shape-key meshes fail before mutation;
- normals and face winding are checked;
- material indices are checked;
- Seam/Sharp/Crease/bevel/custom edge data are checked where applicable;
- manifold count before/after is recorded where manifoldness is expected;
- branch-only loose geometry is not falsely required to be manifold;
- zero-length edges and zero-area faces are absent;
- malformed or ambiguous inputs fail without partial destructive changes.

## L — Stress

- 25 consecutive Inject New start/cancel cycles.
- 25 Persistent Magic Branch commits interspersed with cancellations and MMB orbit.
- large face Paver drag and shrink-back cycle.
- negative-scale, rotated and non-uniformly scaled active objects.
- save/reopen after committed topology and custom Edit Tools ordering.

## Result record

Record exact Blender build, OS, object transforms, selection mode, tool toggles, before/after counts, warnings/tracebacks, Undo behavior, and any attribute/normals/manifold differences.

## Dev_v2.10.1 regression block

1. Edge Solo/Branch: test multiple connected and disconnected selected source edges; the set must duplicate/move rigidly.
2. Move one branched edge so its two new endpoints land on two different target rails while only one rail is hovered. Both contacts must integrate.
3. Interior target-edge contacts must replace the old spanning edge with two segments sharing the inserted/welded vertex; no stale full edge may remain.
4. Test coincident vertex contacts, multiple contacts on one edge, and contacts on different edges. Check zero/duplicate geometry, normals/winding, material/edge attributes, Undo/Redo and cancel rollback.
5. Magic Branch waiting state: Shift+MMB pan and ordinary orbit must not snap the view back to the current selection.
6. During a live branch/injection, plain MMB must orbit around live geometry; modifier MMB must retain normal Blender navigation.
7. Magic Branch ON/OFF must actually enter/exit the modal tool. Persistent OFF exits after one branch; Persistent ON stays armed.
8. Branch Type Vertex/Edge/Face must switch Blender mesh selection mode; test Undo restoration.
9. Horizontal face + Z-only Paver must create vertical source-depth tiles with correct winding and no zero-area faces.
10. Pave +X, +Y, then -X back onto existing topology with Auto-Merge ON. Every supported overlap must integrate and interior edge contacts must subdivide the existing edge.
11. Object Snap Vertex/Edge/Face in object/island scopes must Undo and Redo in one coherent step.
