# 3D Print Tools + Transform Decisions

## 2026-08-18 — Analyze uses the installed 3D Print Toolbox as the single source of truth

Decision:
- Dev_v2.11.4 removes Witch Tools' independently implemented Analyze detector.
- Witch Tools `Check All` invokes the installed 3D Print Toolbox `mesh.print3d_check_all` operator directly.
- Witch Tools reads and displays the report produced by that same installed Toolbox instance.
- In Edit Mode, selectable Witch Tools result buttons invoke the original `mesh.print3d_select_report` operator with the original report index.
- Witch Tools does not keep an alternate Analyze fallback. If the Toolbox operator/report cannot be resolved, Analyze reports an explicit error.
- The compact Witch Tools Analyze UI remains; only the backend/report/selection source is delegated.

Reason:
The user requires exact parity, not approximate semantic equivalence. Dev_v2.11.3 still returned Non-flat 73 vs Toolbox 98 and Overhang 80 vs Toolbox 79 on the same unchanged `_CAP 3` mesh. Maintaining a second implementation creates unnecessary divergence risk. Invoking the installed Toolbox itself makes the version actually running in the user's Blender environment authoritative.

Consequence:
- 3D Print Toolbox must remain installed/enabled for Witch Tools Analyze in Dev_v2.11.4.
- This dependency applies only to Analyze/report selection, not Transform, Export, Clean & Repair, or the rest of Witch Tools.
- If a future self-contained Witch Tools package must eliminate that dependency, first obtain and vendor the exact current Toolbox source package. Do not recreate the detector algorithms by hand again.

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

## 2026-08-18 — Analyze must never be approximated

Decision history:
Dev_v2.11.2 attempted to reproduce the original 3D Print Toolbox algorithms/defaults locally after Dev_v2.11.1 approximations failed parity. Dev_v2.11.3 runtime evidence proved that even this locally reconstructed parity implementation still differed from the installed current Toolbox. This decision is superseded by the direct-backend decision above.

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

Runtime result:
The user confirmed Dev_v2.11.3 now produces the STL file in Blender 5.0.1. Broader re-import/transform/fallback testing remains pending.
