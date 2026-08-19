## Dev_v2.11.1 — Advanced Clean layout/section-run correction

- Restored the Advanced Clean presentation much closer to Instant Clean instead of flattening the section controls into a generic compact toggle strip.
- Repair, Manifold, Topology, Normals, and Dissolve are again individual collapsible sections with their own enable toggle and play button in the section header.
- The play button runs only that individual cleanup section; the main Clean button runs whichever section-header toggles are enabled.
- Restored the original-style checkbox/boxed layouts where the user had not requested a redesign: Repair, Topology methods, Normals controls, and Dissolve Protect.
- Retained the requested deliberate changes: no Object Data, no Make Planar, Dissolve remains last, Manifold Remove Non-Manifold is the compact Faces / Vertices / Wire toggle bar, Topology angle/Compare controls remain responsive, and Normals Clear Data is a compact toggle bar.
- Target Blender remains 4.5.0. Blender runtime validation is pending; the user's reference screenshots were taken in Blender 5.0.1 and do not by themselves establish Witch Tools 5.0 compatibility.

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
