# Curvature Sync MVP — Quick Start

Target build: Witch Tools Dev_v2.5.2 for Blender 4.5.

## Before running

- Save a backup copy of the `.blend` file.
- Keep every participating object aligned exactly as it fits together.
- Use multi-object Edit Mode when the upper and lower parts must share one column count.
- The current MVP expects planar circular arcs and explicit selections.

## Collar workflow

1. Select the upper and lower collar objects and enter multi-object Edit Mode.
2. Switch to Vertex Select.
3. Select exactly one **A/start** vertex on every horizontal curve to repair. These should be the curve-to-straight transition vertices on the same side.
4. Press **Capture A**. Witch Tools clears that selection.
5. Select exactly one **Middle** vertex on every curve, near the top center/symmetry line.
6. Press **Middle**. With **Normalize Middle to Curve Axis** enabled, these vertices identify the apex side and are moved to the exact fitted centerline.
7. Select exactly one **Z/end** vertex on every curve at the opposite curve-to-straight transition.
8. Press **Capture Z**.
9. Switch to Edge Select.
10. Select only the open A-to-Z curved edge chains. Alt-click each parallel chain as needed. Include matching chains on both objects in the same run when their loop positions must align.
11. Leave **Match Selected Maximum**, **Inject Missing Vertices**, **Build Missing Column Edges**, **Replace Misaligned Column Edges**, **Normalize Middle to Curve Axis**, and **Respect Vertex Locks** enabled for the collar repair.
12. Press **Analyze**.
13. If Analyze succeeds, press **Apply Curvature Sync**.
14. Inspect the result before saving over the working file. Review any reported unresolved column positions manually.

## Chaotic or diagonal cross-topology

Enable **Replace Misaligned Column Edges** when existing cross-edges connect different canonical column positions. The operator preflights these edges, dissolves only safe two-face interior edges, and rebuilds same-slot columns after the curve vertices are aligned. Boundary edges and edges carrying Seam, Sharp, Crease, bevel, custom data, mixed material, or mixed smoothing are rejected rather than guessed.

## Protected straight sections

Curvature Sync moves only vertices on the selected A-to-Z chains. Do not select edges beyond A or Z. Vertex Lock / Protected Edit Zone groups are respected:

- locked A/Z boundary vertices may remain fixed and may still receive connecting topology;
- locked interior vertices abort the operation instead of being moved;
- lock-group and edit-zone indices are remapped after vertex injection.

## Selection rules

Every selected curve component must be:

- one open chain;
- non-branching;
- contain exactly one captured A, Middle, and Z reference;
- use A and Z as its two endpoints.

Curvature Sync aborts before modifying the real mesh when these rules are not met.

## Current limitations

- Circular arcs only: XY, XZ, or YZ.
- No automatic dissolution of surplus chain vertices. Safe misaligned interior column edges can be replaced when the dedicated toggle is enabled.
- A captured Middle reference must already exist on each chain in this MVP.
- Column edges are only created where the corresponding vertices can be connected through a shared face.
- Unresolved positions are reported and left unchanged rather than forced.
- Interactive undo/redo must still be verified in Blender 4.5; save a backup first.
