# Magic Branch — Decisions

Last updated: 2026-08-08

## D1 — One shared drag/snap backend

Inject New and Magic Branch use `precision_edit_drag.py` for viewport picking, X/Y/Z projection, magnetic target resolution, hover drawing, target-edge materialization, welding, and orbit-pivot support. They must not maintain separate canonical magnetic solvers.

## D2 — One shared topology backend

Common source duplication, branch-edge creation, Organic face creation, Paver tile creation, and zero-geometry checks live in `precision_edit_topology.py`.

## D3 — Magnetic target priority

Cursor priority is vertex, then edge, then face. This makes precise point/edge intent win over a face occupying the same screen area.

## D4 — Face snapping is per-endpoint travel, not median translation

A face hover solves each live endpoint along its own parallel travel ray to the face plane. This is required for angled target walls and avoids collapsing an edge/face placement into one face-center snap.

## D5 — Auto-Merge is conservative

Vertex and edge contacts may weld/split. Two resolved face-boundary contacts may connect through a target face where Blender permits it. Arbitrary face-interior retopology is not auto-generated in Dev_v2.10.0 because no safe universal topology rule has been accepted.

## D6 — Paver preserves tile size

Paver repeats source-sized tiles. It does not stretch the final tile to force an arbitrary destination. Organic is the mode intended for a one-face arbitrary reach.

## D7 — MMB uses Blender viewport navigation

The modal operators pass MMB events through rather than implementing a duplicate orbit system. Before pass-through, the current live geometry center is assigned as the view location/pivot candidate. Runtime feel must be validated in Blender 4.5.

## D8 — Persistent Undo is not claimed until tested

Persistent mode attempts a per-branch Undo boundary through Blender's Undo push API after a successful commit, but modal Undo semantics must be proven in Blender before this is considered accepted.

## D9 — Active-object topology only

Magic Branch and Inject New topology changes operate on one active mesh. Cross-object topology creation remains deferred.

## D10 — Multi-edge Slide is preselected-set based

Dev_v2.10.0 Slide accepts one or more selected edges, injects one vertex into each, and uses the selected edge nearest the cursor as the driver rail. All injected vertices share the same relative factor. Dynamically adding unselected fan edges to the active Slide set merely by hovering is deferred until rollback/selection semantics are proven.

## D11 — A/B/C viewport letters deferred

Edge Doctor retains ordered A/B/C selection and adds two-edge L repair. Drawing literal A/B/C labels beside selected vertices is useful QoL but is deferred because it requires a separate viewport-overlay state/cleanup contract and is not necessary for the repair backend.

## D12 — Edit Tools ordering is preference-level state

Top-level Edit Tools order is stored in add-on preferences rather than scene data, so the user's layout follows their Blender installation rather than changing per `.blend`. A compact reorder mode provides a drag grip and explicit up/down fallback.

## D13 — Planar Edit remains a top-level tool

The new requested order omitted Planar Edit but did not request removal. Since Planar Edit was an explicit earlier requirement and remains an independent precision workflow, its default position stays directly after Coordinate Copy. It can be moved anywhere through the new reordering system.
