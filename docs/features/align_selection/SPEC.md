# Align Selection Specification

## 1. Scope

Initial development scope:

- Blender 4.5;
- mesh Edit Mode;
- vertex, edge, face, and mixed-domain source/anchor capture;
- X, Y, and Z world-coordinate matching;
- destructive coordinate matching for selected targets;
- shape-preserving translation using a captured target anchor;
- one or multiple selected connected islands;
- one or multiple mesh objects in multi-object Edit Mode;
- Witch Tools N-panel UI;
- optional compact Witch Quickbar access through canonical Witch Tools operators.

Out of scope for Dev_v2.7.0:

- rotation or orientation matching;
- scale matching;
- nearest-point projection;
- normal, tangent, or custom-axis alignment;
- proportional falloff;
- automatic discovery of the intended anchor wall;
- Object Mode object alignment;
- armature or UV-editor selections;
- a duplicated Quickbar geometry backend.

## 2. Terminology

### Source

A captured mesh selection whose world-space vertex positions define the reference coordinate. A vertex is used directly. Edge, face, and mixed selections are converted to their unique participating vertices.

The Dev_v2.7.0 source coordinate is the arithmetic mean of all captured source vertices.

### Target Anchor

A captured mesh selection inside geometry that will be translated in **Move Shape** mode. Its arithmetic-mean world coordinate is compared with the source coordinate to calculate the translation.

### Current Selection

The geometry selected when **Apply Align Selection** is invoked.

- In **Match Coordinates**, it is the set of target vertices to modify.
- In **Move Shape**, it is the complete shape or shapes that must move while retaining their internal offsets.

### Match Coordinates

Write the captured source coordinate directly onto every current target vertex on enabled axes. This intentionally flattens the targets on those axes.

### Move Shape

Translate the current selection by the difference between the captured source and target-anchor coordinates. Relative distances among moved vertices remain unchanged.

### Per Selected Island

Partition the selected move vertices by connectivity through selected mesh edges. Each selected component uses the captured target-anchor vertices contained in that component and receives an independent translation.

## 3. User workflows

### Figure A: align one wall to a source coordinate

1. Select the source vertex, edge, face, or set.
2. Press **Capture Source**.
3. Select the wall vertices/faces to align.
4. Choose **Match Coordinates**.
5. Enable X, Y, and/or Z.
6. Press **Apply Align Selection**.

Every selected target vertex receives the source coordinate on enabled axes. Disabled axes remain unchanged.

### Figure B: move a complete cavity without collapsing it

1. Select the source and press **Capture Source**.
2. Select the cavity wall that must meet the source coordinate and press **Capture Target Anchor**.
3. Select the complete cavity, including the opposite wall and connecting geometry.
4. Choose **Move Shape**.
5. Enable the required axes.
6. Use **Whole Selection** for one common translation or **Per Selected Island** for multiple disconnected cavities.
7. Press **Apply Align Selection**.

The anchor wall reaches the source coordinate while subordinate geometry retains its relative distance from the anchor.

## 4. Coordinate policy

- Analysis is performed in world space.
- Every participating object's local vertex position is converted through its object matrix.
- Planned world-space results are converted back through the inverse object matrix before mutation.
- The source and target-anchor reference positions are arithmetic means of unique participating vertices.
- Source vertices are excluded from movement if they are also selected as targets.
- Only enabled world axes are modified.

## 5. Capture storage

Dev_v2.7.0 stores source and anchor membership using persistent integer vertex-domain custom-data markers:

- `wt_align_selection_source`
- `wt_align_selection_anchor`

Scene metadata stores the expected captured counts and capture state. Capture replaces the prior marker set for that role.

Because topology operations may delete or propagate custom data, Apply verifies that the surviving marker count equals the recorded count. A mismatch cancels the operation and requires recapture rather than guessing.

## 6. Match Coordinates behavior

The operator must:

1. require mesh Edit Mode;
2. require at least one enabled axis;
3. resolve a valid captured source;
4. require at least one currently selected target vertex after excluding source vertices;
5. calculate all result coordinates before mutation;
6. set enabled world coordinates to the source coordinate;
7. preserve disabled world coordinates;
8. convert results back to each object's local space;
9. update Edit Mode meshes in one undoable action.

## 7. Move Shape behavior

The operator must:

1. require a valid source and target anchor;
2. require the complete move geometry to be currently selected;
3. require every captured anchor vertex used for an island to be inside that island's move selection;
4. calculate translation deltas before mutation;
5. apply one common delta in Whole Selection mode;
6. apply one independent delta per connected selected component in Per Selected Island mode;
7. move all vertices in each planned component by the same enabled-axis delta;
8. preserve all intra-component vertex offsets exactly apart from floating-point conversion;
9. reject an island with no captured anchor instead of moving it by a guessed amount.

## 8. Vertex Lock and shape-key rules

When **Respect Vertex Locks** is enabled:

- any selected vertex marked by the current Witch Tools Vertex Lock system cancels the complete operation;
- no partial island is moved.

The operator rejects meshes with more than one shape key in Dev_v2.7.0. Shape-key-relative coordinate handling is deferred.

Protected Edit Zone behavior follows the existing Witch Tools protection contract where exposed by the current baseline. Any unresolved protection ambiguity must cancel before mutation.

## 9. Multi-object and multi-island behavior

- Source, anchor, and move selections may span multiple mesh objects participating in multi-object Edit Mode.
- World-space analysis provides one coordinate frame across objects with different transforms.
- Whole Selection may translate all selected vertices together.
- Per Selected Island computes connectivity per selected mesh topology; disconnected cavities may receive independent translations.
- Linked objects sharing one Mesh datablock share marker layers and remain a documented limitation.

## 10. UI

### Witch Tools

Location: **Edit Tools > Align Selection**, after Object Snap and before Vertex Inject.

Controls:

- Capture Source;
- Capture Target Anchor;
- Clear;
- Match Coordinates / Move Shape;
- X / Y / Z toggles;
- Whole Selection / Per Selected Island;
- Respect Vertex Locks;
- Apply Align Selection.

### Witch Quickbar

Location: **Edit** tab.

Quickbar provides a compact presentation of the same properties and invokes:

- `mesh.wt_align_capture`;
- `mesh.wt_align_clear`;
- `mesh.wt_align_apply`.

Quickbar must show a safe unavailable state when Witch Tools Dev_v2.7.0 or the required operator contract is absent. It must not contain a second geometry implementation.

## 11. Failure and transaction rules

The complete operation cancels before geometry mutation when:

- no axis is enabled;
- source or anchor capture is missing;
- source or anchor marker counts no longer match their capture metadata;
- no valid current target/move vertices remain;
- an island lacks an anchor;
- enabled locked vertices are present while lock protection is enabled;
- an affected mesh has unsupported shape keys;
- an object transform cannot be inverted;
- required Edit Mode context is unavailable.

No validation failure may leave a partial coordinate change.

## 12. Acceptance criteria

Dev_v2.7.0 is ready for user validation when:

- a source vertex can align a wall selection on X without changing target Y/Z;
- a complete cavity can translate from an anchor wall without changing its width or shape;
- two disconnected cavities can independently align their anchors to one source coordinate;
- X/Y/Z combinations behave correctly in world space;
- vertex, edge, face, and mixed source/anchor captures resolve to unique vertices;
- multi-object results convert correctly between world and local space;
- locked, stale, malformed, and unsupported selections cancel without partial mutation;
- one undo restores all moved vertices;
- Quickbar calls the Witch Tools operator contract and preserves overlay behavior;
- package identities and public update URLs remain unchanged;
- Blender 4.5 runtime results are recorded.

## 13. Known limitations

- Reference positions use arithmetic means; Active Element reference mode is not included.
- Marker identity is persistent custom data, not immutable topology identity.
- Topology-changing operations may require source/anchor recapture.
- Linked objects sharing a mesh datablock share marker layers.
- No rotation, scale, normal, custom-axis, nearest-point, or projection alignment.
- Blender runtime validation remains pending at delivery.
