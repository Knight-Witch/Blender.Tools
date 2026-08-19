## Dev_v2.11.0 — 3D Print Tools + Transform integration

- Rebased the requested 3D Print/Transform integration onto the current Dev_v2.10.1 Magic Branch baseline instead of the older Dev_v2.9.0 precision-edit branch.
- Added top-level **Transform** immediately below Mode Switcher with object Location/Rotation/Scale and Edit Mode selected-vertex local Location editing.
- Added top-level **3D Print Tools** above Edit Tools with simplified STL Export, consolidated Analyze Mesh results, Make Manifold, Auto Fix, and Advanced Clean.
- Auto Fix presents Global Fix before Local Fix. Advanced Clean retains Repair, Manifold, Topology, Normals, and Dissolve with requested compact/responsive toggle layouts.
- Preserved Dev_v2.10.1 Magic Branch, Inject New, Edge Doctor, Object Snap, Edit Tools ordering, and current registration contracts.
- Intentionally omitted Volume/Area, separate Solid/Intersections/Shells controls, Hollow, Bisect, Align XY, Scale To, export options, Instant Clean Object Data, and Make Planar.
- Analyze result click-to-select parity is planned after detector/count parity is validated against Blender's original 3D Print Toolbox.
- Target Blender: 4.5.0. Static package validation is performed during packaging; Blender 4.5 runtime validation remains pending.

## Dev_v2.10.1 — Runtime topology/navigation hotfix

- Inject New Edge Solo/Branch accepts one or more selected edges as one rigid source set.
- Branch/Magic Branch Auto-Merge evaluates supported contacts across created vertices and can split existing target edges before welding interior contacts.
- Magic Branch has explicit ON/OFF plus separate Persistent behavior; Branch Type synchronizes Blender mesh selection mode.
- Paver can grow out of plane when enabled axes require it, including Z-only floor-to-wall cases.
- Added an explicit Object Snap undo boundary candidate.
- Dev_v2.10.1 remains a Blender 4.5 runtime-retest candidate.

## Dev_v2.10.0 — Magnetic Mesh Editing / Magic Branch

- Expanded Inject New with multi-axis placement, Magnetic Snap, Branch Auto-Merge, multi-edge Slide, and MMB navigation.
- Added Magic Branch Vertex/Edge/Face workflows with Paver/Organic face modes.
- Added Edge Doctor regrouping and preference-backed Edit Tools reordering.
- Added shared drag/snap/topology backends and Blender 4.5 packaging.

## Earlier history

Earlier Witch Tools development history remains preserved in repository history and in `addons/witch_tools/docs/NOTES_CHANGELOG_FULL.md`.
