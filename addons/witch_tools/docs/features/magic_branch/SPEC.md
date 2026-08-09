# Magic Branch — Feature Specification

Candidate: `Witch Tools Dev_v2.10.0`  
Target Blender: `4.5.0`  
Status: source candidate; Blender runtime validation pending

## Purpose

Magic Branch turns common Edit Mode topology growth into a click-drag-drop workflow. The operator stays focused on fast local construction: choose the geometry type, click-drag a source element, optionally magnetize to existing topology, release to commit, and either exit or remain armed for another branch.

## Tool modes

### Single Branch

One completed click-drag commits the branch and exits the modal tool.

### Persistent

After a successful branch, the operator remains armed. The next click-drag immediately starts another branch without returning to the N-panel. Persistent is a saved toggle and also has a dedicated operator, `mesh.wt_magic_branch_toggle_persistent`, so the user can assign any Blender hotkey.

## Branch types

### Vertex

- Source: one clicked vertex.
- Live geometry: duplicated vertex plus one source-to-new edge.
- Commit on existing target vertex with Magnetic Snap + Auto-Merge: the duplicated endpoint is welded into the target, leaving a direct source-to-target branch edge.

### Edge

- Source: one clicked edge.
- Live geometry: copied edge plus source-to-copy connections for both endpoints.
- Vertex/edge magnetic contact aligns the nearest corresponding copied endpoint while preserving the copied edge as a rigid shape.
- Face magnetic contact solves each copied endpoint independently along its travel line.

### Face

The source face edge is chosen dynamically from drag direction: moving the cursor toward a face boundary makes that boundary the emitting edge.

#### Paver

- Repeats equal-size tiles outward from the chosen source edge.
- On quads, source depth is derived from the opposite edge; fallback geometry uses the center-to-edge direction.
- Number of tiles grows/shrinks with drag distance.
- Paver preserves equal tile dimensions. It does not stretch the final tile to hit an arbitrary off-grid target.
- Magnetic hover may guide destination/highlight and compatible coincident outer contacts may auto-merge.

#### Organic

- Creates one connected face sharing the chosen source edge.
- The opposite/new edge follows the mouse within enabled axes.
- Magnetic Snap may align the live outer vertices to vertex, edge, or face targets.

## Movement

X/Y/Z are independent global-axis toggles. At least one must be enabled.

- one enabled axis: screen drag projects along that global axis;
- two enabled axes: mouse ray intersects the corresponding global plane through the source anchor;
- X+Y+Z: free view-depth mouse placement.

Default is X+Y+Z enabled.

## Magnetic Snap

Magnetic Snap is shared with Inject New and uses the same hover contract.

Priority at the cursor:

1. vertex;
2. edge;
3. face.

The hovered target is visibly highlighted during the modal operation.

### Vertex target

The compatible live endpoint with the lowest constrained residual is aligned to the target vertex while the rest of the live branch remains rigid.

### Edge target

The compatible live endpoint is aligned to the closest point on the hovered edge while the rest of the branch remains rigid.

### Face target

Each live endpoint follows its own parallel travel line to the hovered face plane. Contacts outside the face polygon resolve to the nearest face boundary. This allows an edge approaching an angled wall to land its two endpoints at different boundary points instead of translating to one face median.

## Auto-Merge

Auto-Merge is meaningful only with Magnetic Snap.

- target vertex: weld live endpoint into the existing vertex;
- target edge: split the edge at the exact contact when necessary, then weld;
- face boundary: compatible boundary contacts use the same vertex/edge materialization rules;
- two boundary contacts on one target face may connect through that face where Blender can do so safely.

A face-interior magnetic point is a placement target but is not automatically turned into arbitrary interior retopology in this candidate. The tool refuses to invent a destructive face topology rule that has not been specified/tested.

Existing Vertex Locks and Plane Locks on merge targets block Auto-Merge before intentional target mutation.

## View navigation during drag

While live geometry is being dragged:

- hold MMB: placement pauses and the event is passed to Blender viewport navigation;
- orbit pivot is moved to the current live branch center;
- release MMB: placement resumes from the existing live geometry.

## Selection / scope

- one active mesh object in Edit Mode;
- source is picked directly in the 3D viewport according to the chosen Vertex/Edge/Face mode;
- multiple shape-key meshes are rejected;
- multi-object topology branching is deferred.

## Acceptance criteria

The candidate is acceptable only after Blender 4.5 tests prove:

1. registration/unregistration and Edit Tools panel rendering are clean;
2. Vertex/Edge/Face click-drag picking works from practical camera angles;
3. X/Y/Z single, paired, and XYZ-free movement obey enabled axes;
4. vertex/edge/face hover highlights the target actually used by the solve;
5. Vertex and Edge magnetic semantics match the rigid-endpoint behavior above;
6. Face magnetic placement resolves individual endpoint travel lines rather than one median;
7. Auto-Merge creates no coincident duplicate endpoint at a vertex/edge contact;
8. Paver preserves equal source tile dimensions and can create/reduce multiple tiles while dragging;
9. Organic creates one connected adaptable face;
10. MMB orbit pauses placement, pivots around the live branch, and resumes without a jump;
11. Single Branch exits after commit;
12. Persistent remains armed across multiple branches and has safe Undo behavior;
13. Esc/right-click/cancel never leaves partial destructive topology;
14. normals/winding, materials and relevant edge attributes are preserved where Blender/BMesh semantics permit;
15. zero-length edges and zero-area faces are rejected;
16. Vertex Lock / Plane Lock references remain valid through commit/cancel/undo/redo;
17. malformed or ambiguous source/target states fail safely.

See `TEST_PLAN.md` for the executable Blender validation matrix.

## Dev_v2.10.1 Blender 4.5 regression addendum

Dev_v2.10.0 user testing confirmed hover highlighting, Magnetic Snap, Inject New Undo/Redo, Paver, Organic, and the tested Organic vertex-merge path. Failures found were: Edge Solo/Branch restricted to one edge; only one magnetic contact merged; an old unsplit target edge remained through an inserted vertex; Magic Branch reset the view pivot while waiting; no explicit Magic Branch ON/OFF; no Z-wall Paver growth from a horizontal source; Paver return-path overlaps did not all merge; Branch Type did not synchronize Blender Vertex/Edge/Face selection mode; Object Snap did not enter Undo history.

Dev_v2.10.1 implements source fixes for those cases. Blender 4.5 runtime retest remains required.
