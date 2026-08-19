# 3D Print Tools + Transform Decisions

## 2026-08-18 — Preserve Instant Clean section interaction model

Decision:
- Advanced Clean will retain Instant Clean's individual collapsible section structure rather than replacing it with a flat generic category strip.
- Repair, Manifold, Topology, Normals, and Dissolve each have a section-header enable toggle and a section-header play action.
- The main Clean action runs every enabled section.
- A section play action runs only that section, even when its global-enable toggle is off.
- Shift preserves the selection-only behavior for both main Clean and section play actions.

Reason:
The user uses the individual section execution controls and explicitly prefers the original Instant Clean presentation. The first Dev_v2.11.0 integration altered more of the UI than requested.

## 2026-08-18 — Limit UI redesign to explicitly requested controls

Decision:
Keep the original-style Instant Clean body layout unless the user explicitly requested a change.

Requested changes that remain:
- remove Object Data;
- remove Make Planar;
- place Dissolve last, after Normals;
- Manifold Remove Non-Manifold becomes compact Faces / Vertices / Wire toggle buttons;
- Topology Face/Shape angle controls share a row when width permits and split when narrow;
- Topology Compare becomes a responsive Sharp / Seam / UV / Material / VCol toggle bar;
- Normals Clear Data becomes a Split Normals / Sharp Edges toggle bar.

Controls not named above should stay visually/semantically close to Instant Clean.

## 2026-08-18 — Analyze Mesh must reproduce 3D Print Toolbox checks, not approximate them

Decision:
Witch Tools Analyze Mesh will use the same check semantics and standard default thresholds as Blender's 3D Print Toolbox rather than simplified geometric approximations.

The integrated UI will continue hiding the threshold grid because the user explicitly does not need it, but the backend defaults are fixed to the Toolbox values visible in the reference panel:
- Degenerate: 0.1 mm (`0.0001` Blender units)
- Non-Planar: 5 degrees
- Thickness: 1 mm (`0.001` Blender units)
- Sharp: 160 degrees
- Overhang: 45 degrees

Parity-sensitive implementation details include:
- world-transformed BMesh for Non-flat, Thin, Sharp and Overhang checks;
- Toolbox distorted-face loop-normal test;
- Toolbox six-sample backwards-ray thickness test;
- signed manifold-edge angle for Sharp;
- downward-normal angle test for Overhang;
- Toolbox BVH overlap semantics for Intersect Faces;
- the same degenerate threshold for Zero Faces and Zero Edges.

Reason:
Blender 5.0.1 runtime comparison on the same mesh proved the Dev_v2.11.1 approximation was not equivalent. Original Toolbox results were Non-flat 98 / Thin 0 / Sharp 0 / Overhang 79; Witch Tools returned 73 / 1 / 1 / 80.

## 2026-08-18 — Blender 5.0.1 is primary, Blender 4.5 is secondary

Decision:
General Witch Tools development and normal modeling/3D-print workflows use Blender 5.0.1 as the primary runtime target. Blender 4.5 remains a secondary compatibility target, especially for BG3 workflows and tooling that still requires the older environment.

The add-on `bl_info['blender']` minimum remains 4.5.0 so one package can still be installed for secondary compatibility testing. Documentation and build labels must distinguish primary target from minimum/secondary compatibility.

Reason:
The user's normal Blender environment is 5.0.1; 4.5 is used mainly where BG3/Collada workflow constraints require it.
