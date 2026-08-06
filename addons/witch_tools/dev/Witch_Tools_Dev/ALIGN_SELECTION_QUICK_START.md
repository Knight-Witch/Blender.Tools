# Align Vertices / Edges / Faces — Quick Start

Build: **Witch Tools Dev_v2.8.0**  
Target Blender: **4.5**

The tool is under **Witch Tools > Edit Tools > Align Vertices / Edges / Faces**.

It treats edges and faces as groups of vertices. It never adds, deletes, welds, or reconnects topology.

## Basic axis alignment

Use this when several vertices need the same world X, Y, or Z coordinate.

1. Enter Edit Mode.
2. Select the parent vertex, edge, or face.
3. Press **Capture Selected Anchor**.
4. Leave **Frame** on **World XYZ**.
5. Turn on only the coordinates that must become equal.
   - Example: enable **Z** to level vertices vertically.
   - Coordinates left off remain unchanged.
6. Select the subordinate vertices, edges, or faces that should move.
7. Press **Analyze**.
8. Press **Align**.

For the horizontal collar example, capture the red vertex, enable only **Z**, leave X and Y off, select the yellow vertices, then Align. Their X and Y values are retained.

## Slide along existing edges

Use this when target vertices must move only along specific existing edges rather than moving freely.

1. Capture the parent anchor.
2. Under **Move Along**, choose **Captured Rails**.
3. Select the straight edges that targets are permitted to slide along.
4. Press **Capture Selected Slide Rails**.
5. Enable the coordinate that must become equal, such as **Z**.
6. Select the subordinate vertices at the other end of those rails.
7. Analyze, then Align.

**Stay Within Captured Rail** prevents the tool from extending a target beyond the captured edge-chain extent. Captured rails must be straight within the internal safety tolerance; curved or ambiguous rails are rejected before mutation.

## Pair a series of parents and subordinates

Use **Paired by Rail** when every subordinate should align to its own parent rather than one global anchor.

1. Select all parent vertices and press **Capture Selected Anchor**.
2. Choose **Paired by Rail**.
3. Select the separate edge rails connecting each parent to its subordinate and press **Capture Selected Slide Rails**.
4. Each disconnected rail component must contain exactly one captured parent vertex.
5. Select the subordinate vertices or connected subordinate islands.
6. Enable the coordinate to equalize.
7. Analyze, then Align.

The rail components establish the parent/child mapping explicitly. The tool does not guess by nearest distance or vertex index.

## Preserve relative spacing or shape

Enable **Preserve Relative Spacing / Shape** to translate each target group as one rigid unit. No target vertex changes position relative to the others in its group.

- **Whole Selection** moves the selected targets on each object together.
- **Per Selected Island** moves each disconnected selected region independently.
- **Paired by Rail** automatically treats rail-mapped subordinate islands as separate groups.

When shape preservation and a slide rail are both enabled, one rail-compatible translation must satisfy the entire group. If it cannot, Analyze blocks the operation instead of deforming the shape.

## Custom guide at any angle

Use **Custom Guide** for a 45-degree line or any other arbitrary orientation.

1. Capture the parent anchor.
2. Change **Frame** to **Custom Guide**.
3. Set **Guide Start** and **Guide End** manually, or:
   - select geometry and press **Capture Start** or **Capture End from Selection**;
   - press **Copy Anchor** to place Guide Start exactly on the captured anchor.
4. Choose one custom target:
   - **Match Anchor in Guide Frame**: X follows the guide direction; Y and Z are the two perpendicular custom axes. Enable the custom components to equalize.
   - **Project to Guide Line**: projects targets onto the line while preserving their distance along it.
5. Select subordinates, Analyze, then Align.

## Safety behavior

Analyze and Align cancel before moving anything when they detect:

- missing or stale anchor/rail captures;
- no selected subordinate geometry;
- an impossible multi-axis rail intersection;
- a curved or zero-length rail;
- a required point outside a clamped rail;
- an enabled Vertex Lock on any target;
- a non-invertible object transform;
- a mesh with multiple shape keys;
- ambiguous paired-rail mapping.

The Apply operator is registered for Blender Undo, but interactive Blender 4.5 undo/redo validation remains required for this development build.
