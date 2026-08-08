# Precision Edit — Decisions

Last updated: 2026-08-07

## PE-D001 — Witch Tools owns the backend

Coordinate Copy, Planar Edit, and Inject New are general-purpose mesh tools and therefore live canonically in Witch Tools. Witch Dock / Quickbar may expose them later only as a thin caller.

## PE-D002 — Global and Local have explicit meanings

`Global` means world-space capture/application with explicit matrix conversion per object. `Local` means copying numeric object-local values. The implementation must never assume two mesh objects share an origin or transform.

## PE-D003 — No selection-wide median for Coordinate Copy or Level

The core user need is exact coordinates. Selected vertices are individual targets. Selected edge/face regions are grouped only by connected selected components so a whole selected geometric feature can rotate/scale coherently without turning unrelated features into one median target.

## PE-D004 — Rotation and scale are geometry transforms

Vertices, edges, and faces do not own Object transform channels. Coordinate Copy Rotation/Scale therefore uses deterministic geometry frames and extents rather than fabricating object-level rotation/scale values.

## PE-D005 — Plane Lock stores object-local axis references

Plane Lock is persistent modeling protection rather than a one-shot world alignment. Its references are stored in mesh-local BMesh custom layers so ordinary object placement does not invalidate the lock and topology references are not dependent on transient vertex indices.

## PE-D006 — Level is world-space

Level is intended to flatten/even geometry across one or several objects. It therefore captures the source and solves each selected target in world space, converting each result back into that target object's mesh coordinates.

## PE-D007 — Slide is vertex-only

The requested subdivide-like behavior has one unambiguous topology operation: insert a new vertex into an existing edge. Edge/face Slide is excluded rather than guessing destructive topology.

## PE-D008 — X/Y/Z Inject placement means axis movement

For Solo/Branch, X/Y/Z constrain the new geometry to movement along the chosen global axis. The UI calls this **Movement / Move Along** rather than implying a 2D planar constraint. Rail covers arbitrary straight-angle placement.

## PE-D009 — Branch creates branch edges, not extrusion skin

Branch duplicates the selected source and creates source-to-copy edges for corresponding source vertices. It does not create side faces. Automatic side-face generation would turn Branch into an extrusion tool and requires separate manifold/material rules.

## PE-D010 — Rail is a straight segment for this candidate

Rail uses a captured endpoint and the source point as a straight movement segment. Curved/polyline rails are deferred because they require path parameterization and junction behavior.

## PE-D011 — Existing auto-aligned inject remains separate

`mesh.wt_vertex_inject_auto_aligned` is a specialized A/B/C → D repair workflow and remains available as **Edge / Vertex Inject**. New **Inject New** is a manual creation/placement workflow and does not replace the repair operator.

## PE-D012 — Protection systems must cooperate

Coordinate Copy and Level preflight existing Vertex Locks and Plane Locks before mutation. Inject New suspends both guards while it performs its own modal topology transaction, restores existing Vertex Lock references afterward, and clears Plane Lock data from newly created vertices.

## PE-D013 — Runtime claims remain conservative

No Blender executable is available in the implementation environment. Source/static checks may be recorded as passed; Blender 4.5 registration, UI, modal interaction, undo/redo, topology rollback, save/reopen, and compatibility must remain explicitly untested until run in Blender.

## Inherited documentation conflict

The pre-existing Dev_v2.8.0 roadmap references `/docs/features/align_selection/`, but that directory is not present on the current source branch. This is an inherited documentation gap, not evidence that the feature did not exist. This Precision Edit work does not fabricate the missing historical packet; the gap is recorded for later baseline cleanup.


## Dev_v2.10.0 addendum
- Inject New and Magic Branch share `precision_edit_drag.py` and `precision_edit_topology.py` as canonical drag/snap/topology layers.
- Magnetic priority is vertex > edge > face.
- Face placement uses per-endpoint travel lines, not one target median.
- Auto-Merge is conservative; arbitrary face-interior retopology is deferred.
- Multi-edge Slide operates on the preselected edge set; cursor hover chooses the driver among those selected rails.
- MMB navigation is passed through to Blender after assigning live geometry as the pivot candidate; runtime behavior must be tested.
