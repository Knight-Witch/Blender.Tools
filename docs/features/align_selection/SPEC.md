# Align Vertices / Edges / Faces Specification

Feature ID: `WT-ALIGN-001`  
Candidate implementation: Witch Tools `Dev_v2.8.0`  
Target Blender: `4.5.0`

## 1. Scope

Current development scope:

- Mesh Edit Mode.
- Vertex, edge, face, and mixed-domain parent capture.
- Active Element or Median parent reference.
- Vertex, edge, face, and mixed subordinate selections.
- World X/Y/Z matching with independently enabled components.
- Arbitrary Custom Guide coordinate frame defined by editable start/end points.
- Custom-frame component matching.
- Projection to an arbitrary guide line.
- Free-coordinate movement.
- Movement constrained to explicitly captured straight mesh-edge rails.
- One-parent-to-all and explicit paired-by-rail relationships.
- Optional rigid relative-spacing/shape preservation.
- Whole-selection and per-selected-island target grouping.
- Multi-object Edit Mode world/local conversion.
- Witch Tools N-panel UI.
- Transaction-first failure behavior.

Out of current scope:

- Curved/polyline movement rails.
- Rotation or scale matching.
- Surface-normal, tangent, nearest-point, or arbitrary-surface projection.
- Automatic parent/child guessing by nearest distance or vertex index.
- Object Mode alignment.
- Armatures, curves, UV selections, or non-mesh domains.
- Duplicated geometry logic in Witch Dock/Quickbar.

## 2. Terminology

### Parent Anchor

A captured mesh selection defining the alignment reference. Vertex selections are used directly. Edges and faces resolve to their unique participating vertices.

- `Active Element`: uses the active captured vertex, edge endpoints, or face vertices.
- `Median`: arithmetic mean of all captured parent vertices.

### Subordinates

The vertices participating in the current selection when Analyze or Align is invoked, excluding captured parent vertices. Selected edges and faces participate through their vertices.

### Alignment Frame

The coordinate system in which components are matched.

- `World XYZ`: Blender world coordinates.
- `Custom Guide`: custom X follows Guide Start to Guide End; custom Y and Z are a stable perpendicular orthonormal basis.

### Match Coordinates

For every enabled component, change the subordinate coordinate to the reference coordinate. Disabled components remain unchanged.

### Project to Guide Line

In Custom Guide mode, set custom Y and Z to zero while leaving custom X unchanged. This moves a point to the guide line without changing its distance along the line.

### Slide Rail

An explicitly captured existing mesh-edge component defining the only permitted movement line. Rails are movement constraints, not topology locks and not Protected Edit Zones.

### One Anchor to All

Every subordinate group uses the same captured parent reference.

### Paired by Rail

Each subordinate island is paired to the one captured rail component it touches. Each paired rail component must contain exactly one captured parent vertex. No spatial guessing is permitted.

### Preserve Relative Spacing / Shape

Move every vertex in a target group by one identical world-space translation, preserving all intra-group offsets.

## 3. User workflow

The UI must expose exactly four conceptual steps:

1. **Capture Parent Anchor**
2. **Choose Alignment Target**
3. **Choose How Targets May Move**
4. **Select Subordinates and Apply**

Analyze must perform full planning without mutation. Align must use the same planning path and mutate only after all preflight passes.

## 4. World-axis example

For the user's horizontal collar row:

1. select the red parent vertex and Capture Anchor;
2. choose World XYZ;
3. enable only Z;
4. choose Free Coordinates;
5. select the yellow subordinate vertices;
6. Analyze, then Align.

Every subordinate receives the parent's world Z. World X and Y remain unchanged, so the vertices move vertically without shifting sideways or in depth.

## 5. Slide-along-edge example

For targets that must remain on existing vertical edges:

1. capture the parent anchor;
2. choose Captured Rails;
3. select the straight existing edges and Capture Rails;
4. enable the coordinate to equalize;
5. select the subordinate endpoints;
6. Analyze, then Align.

Each target must touch exactly one captured rail. The solution is computed as `p + t*d`. If enabled coordinate constraints imply different values of `t`, the operation cancels rather than moving off the rail.

## 6. Parent/child series example

For multiple red parent vertices and green subordinate endpoints:

1. capture all red parent vertices;
2. choose Paired by Rail;
3. capture the disconnected edge components linking each parent to its subordinate;
4. select subordinate endpoints or subordinate islands;
5. Analyze, then Align.

Each rail component must contain exactly one parent vertex and each subordinate island must touch exactly one rail component. These components define the mapping explicitly.

## 7. Custom guide example

For a 45-degree or arbitrary line:

1. capture the parent;
2. choose Custom Guide;
3. enter Guide Start/End or capture either point from selected geometry;
4. optionally copy the parent reference to Guide Start;
5. choose:
   - Match Anchor in Guide Frame, then enable custom X/Y/Z components; or
   - Project to Guide Line;
6. select subordinates, Analyze, and Align.

Guide Start and Guide End must not coincide. The frame construction must remain deterministic for guide directions near world axes.

## 8. Coordinate policy

- Analysis is performed in world space.
- Object-local coordinates are transformed through `matrix_world`.
- Planned results are converted back through the inverse matrix only after preflight succeeds.
- Non-invertible transforms cancel before mutation.
- Parent vertices are excluded from subordinate movement.
- Disabled components remain exactly at their original planned value apart from floating-point conversion.

## 9. Capture storage

Persistent custom-data markers:

- parent vertices: `wt_align_selection_source`
- rail edges: `wt_align_selection_rail`

Scene metadata stores expected parent and rail counts. Apply compares surviving markers with recorded counts. A mismatch caused by topology changes cancels and requires recapture.

Capture replaces the previous marker set for the same role and clears the current selection so the next workflow step starts cleanly.

## 10. Free-coordinate behavior

Without shape preservation:

- each subordinate vertex is solved independently;
- enabled frame components are matched;
- disabled components are preserved.

With shape preservation:

- each chosen target group receives one common translation;
- target-group reference is the arithmetic mean of group vertices;
- Whole Selection groups all subordinates on each object;
- Per Selected Island groups disconnected selected topology independently.

## 11. Rail behavior

- A rail is a disconnected component of captured mesh edges.
- The candidate accepts only a straight line within `align_rail_straight_tolerance`.
- Zero-length rails are rejected.
- Targets must touch exactly one rail component.
- A target touching no rails or multiple rails is rejected.
- `Stay Within Captured Rail` clamps permissible `t` to the captured rail point extent and rejects a requested point beyond that extent.
- Multiple enabled component constraints must solve to one consistent `t` within `align_solve_tolerance`.

With rigid shape preservation, one common rail-compatible translation must satisfy the entire group. The system must not deform a group to make an impossible constraint pass.

## 12. Paired-by-rail behavior

- Paired mode partitions subordinate selections into connected islands.
- Each subordinate island must touch exactly one rail component.
- Each paired rail component must contain exactly one captured parent vertex.
- That parent vertex is the reference for that subordinate island.
- Edge/face parent capture remains supported for One Anchor to All, but paired mode is deliberately vertex-parent oriented in the candidate.

## 13. Safety and transaction rules

The complete operation cancels before mutation when:

- no required Match component is enabled;
- parent capture is missing or stale;
- rail capture is missing or stale when required;
- no subordinate vertices remain;
- a target has no rail or multiple rails;
- paired mapping has zero or multiple parents on a rail;
- a rail is curved beyond tolerance or zero length;
- rail component constraints do not produce one parameter;
- a clamped solution lies beyond captured rail extent;
- an enabled Vertex Lock affects any target;
- an affected mesh has multiple shape keys;
- an object transform cannot be inverted;
- Edit Mode context is unavailable.

All planned local coordinates must be calculated before mutation. Unexpected Apply failure must attempt to restore original local coordinates. No preflight failure may leave partial movement.

## 14. Multi-object behavior

- Parent and subordinate geometry may span mesh objects participating in multi-object Edit Mode.
- World-space analysis provides a shared coordinate frame.
- Direct markers are stored on Mesh datablocks.
- Linked objects sharing a Mesh datablock therefore share markers and remain a documented limitation.
- Objects containing required markers must participate in the current Edit Mode operation; the candidate does not silently edit hidden/non-participating objects.

## 15. UI and operator contract

Witch Tools location: **Edit Tools > Align Vertices / Edges / Faces**.

Canonical operator IDs:

- `mesh.wt_guided_align_capture_anchor`
- `mesh.wt_guided_align_capture_rails`
- `mesh.wt_guided_align_capture_guide_point`
- `mesh.wt_guided_align_copy_anchor_to_guide_start`
- `mesh.wt_guided_align_clear`
- `mesh.wt_guided_align_analyze`
- `mesh.wt_guided_align_apply`

Witch Dock/Quickbar is deferred. A later wrapper must invoke this contract and must not contain a duplicate geometry backend.

## 16. Acceptance criteria

The candidate is accepted only after Blender 4.5 testing confirms:

- world Z matching aligns the screenshot's yellow vertices to the red parent without changing X/Y;
- captured rails slide those vertices along their existing straight edges;
- multiple red parents correctly map to green children through disconnected rails;
- arbitrary-angle custom-frame matching and line projection are correct;
- rigid shape preservation retains all intra-group distances;
- multiple selected islands receive correct independent movement;
- edge, face, and mixed parent/subordinate selections resolve correctly;
- multi-object transforms produce visible world alignment;
- locks, stale markers, malformed rails, impossible constraints, shape keys, and invalid transforms cancel without partial mutation;
- one undo restores all moved vertices and redo reapplies them;
- save/reopen preserves valid captures or fails with a clear recapture requirement;
- no topology, normals, face winding, materials, UVs, sharp/seam attributes, or unrelated data are changed.

## 17. Known limitations

- Straight rails only.
- Paired rails require one parent vertex per rail component.
- A target island touching multiple rails is ambiguous and rejected.
- Multiple shape keys are unsupported.
- Linked objects share marker data.
- Topology edits may require recapture.
- Runtime validation remains pending.
