## Dev_v2.11.3 — STL export reliability hotfix

- Fixed the integrated 3D Print Tools Export STL path after Blender 5.0.1 runtime testing showed that selecting a folder and pressing Export STL could appear to do nothing.
- The exporter now checks Blender's native/current STL operator return status and verifies that a non-empty STL file was actually created instead of assuming the operator call succeeded.
- Added the legacy STL operator as a compatibility attempt when available.
- Added a self-contained binary STL fallback writer using selected evaluated mesh geometry, applied modifiers, object world transforms, triangulation, and negative-transform winding correction when Blender's STL operator is unavailable or cancels.
- Export failures now report an explicit error instead of silently returning apparent success.
- The UI remains intentionally simple: folder selector + Export STL only; format stays fixed to STL.
- Primary runtime target: Blender 5.0.1. Secondary compatibility target: Blender 4.5. Dev_v2.11.3 runtime export/re-import testing is pending.

## Dev_v2.11.2 — 3D Print Toolbox Analyze parity correction

- Corrected Witch Tools Analyze Mesh after Blender 5.0.1 runtime comparison showed mismatched Non-flat, Thin, Sharp, and Overhang results against the original 3D Print Toolbox.
- Replaced the simplified analyzer approximations with the original Toolbox check semantics: world-transformed distortion/sharp/overhang checks, signed sharp-edge angle test, original 0.1 mm degenerate threshold, original six-sample backwards-ray thickness test, and Toolbox-style BVH intersection handling.
- Kept the integrated Analyze UI intentionally compact; the hidden thresholds remain the standard Toolbox defaults shown in the original panel: 0.1 mm degenerate, 5° non-planar, 1 mm thickness, 160° sharp, 45° overhang.
- Blender 5.0.1 is now the primary Witch Tools development/runtime target. Blender 4.5 remains the secondary compatibility target for BG3 and other workflows that require it. The add-on minimum version remains 4.5 so the same package can still be tested there.
- Blender 5.0.1 runtime comparison that exposed the mismatch: original Toolbox = Non-flat 98 / Thin 0 / Sharp 0 / Overhang 79; Dev_v2.11.1 Witch Tools = 73 / 1 / 1 / 80. Dev_v2.11.2 parity fix requires runtime retest on the same mesh.

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
