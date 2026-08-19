# 3D Print Tools + Transform Decisions

## 2026-08-18 — Preserve Instant Clean section interaction model

Decision:
- Advanced Clean retains Instant Clean's individual collapsible section structure rather than replacing it with a flat generic category strip.
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
Witch Tools Analyze Mesh uses the same check semantics and standard default thresholds as Blender's 3D Print Toolbox rather than simplified geometric approximations. The threshold grid remains hidden.

Defaults:
- Degenerate: 0.1 mm
- Non-Planar: 5 degrees
- Thickness: 1 mm
- Sharp: 160 degrees
- Overhang: 45 degrees

Reason:
Blender 5.0.1 runtime comparison on the same mesh proved the Dev_v2.11.1 approximation was not equivalent.

## 2026-08-18 — Blender 5.0.1 is primary, Blender 4.5 is secondary

Decision:
General Witch Tools development and normal modeling/3D-print workflows use Blender 5.0.1 as the primary runtime target. Blender 4.5 remains a secondary compatibility target, especially for BG3 workflows and tooling that still requires the older environment.

The add-on `bl_info['blender']` minimum remains 4.5.0 so one package can still be installed for secondary compatibility testing.

## 2026-08-18 — STL export must verify success and have an internal fallback

Decision:
- The compact Export UI remains folder + one Export STL button; STL stays the fixed format.
- Prefer Blender's native/current STL operator so normal Blender export behavior remains the first path.
- An operator call is not success by itself: Witch Tools must inspect the returned status and verify that an output file was created.
- Try the legacy STL operator when present as a compatibility path.
- If Blender's STL operator paths are unavailable or cancel/fail, use a canonical Witch Tools binary STL fallback built from selected evaluated mesh geometry rather than silently doing nothing.
- The fallback applies evaluated modifiers and world transforms, triangulates geometry, corrects winding for negative transforms, and writes transactionally via a temporary file.
- If every path fails, report the failure rather than returning an apparent success.

Reason:
Blender 5.0.1 runtime testing showed the prior integrated Export STL path could produce no expected file/result while the code still unconditionally proceeded to its success report. A print-export button must provide deterministic success/failure behavior and must not depend on one version-sensitive operator path.
