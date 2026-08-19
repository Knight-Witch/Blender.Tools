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

## 2026-08-18 — Compatibility target remains Blender 4.5

Decision:
Dev_v2.11.1 remains authored for Blender 4.5.0. The user's reference screenshots show Blender 5.0.1, so 5.0.1 may be recorded as an additional runtime test environment if the candidate is tested there. No 5.0.1 compatibility claim is made before such testing.
