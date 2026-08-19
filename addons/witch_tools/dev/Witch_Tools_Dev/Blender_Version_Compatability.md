# Blender Version Compatibility

## Current development candidate — Dev_v2.11.2

- Add-on: Witch Tools
- Version: `Dev_v2.11.2`
- Primary development/runtime target: **Blender 5.0.1**
- Secondary compatibility target: **Blender 4.5.0**
- Minimum Blender version declared by the add-on: **4.5.0**
- Public release branches changed by this candidate: no

### Blender 5.0.1 runtime evidence

Dev_v2.11.1 was run by the user in Blender 5.0.1 and established that:
- the integrated 3D Print Tools panel renders;
- Analyze Mesh > Check All executes and populates results;
- direct same-mesh comparison against Blender's original 3D Print Toolbox is possible.

That comparison exposed an Analyze parity bug in Dev_v2.11.1 on `_CAP 3`:
- original Toolbox: Non-flat `98`, Thin `0`, Sharp `0`, Overhang `79`;
- Dev_v2.11.1 Witch Tools: Non-flat `73`, Thin `1`, Sharp `1`, Overhang `80`.

The other six displayed counts matched on that fixture: Non-manifold `0`, Bad Contiguous `0`, Intersect Faces `0`, Shells `1`, Zero Faces `0`, Zero Edges `0`.

Dev_v2.11.2 replaces the simplified Analyze approximations with 3D Print Toolbox-equivalent check semantics/default thresholds. **The Dev_v2.11.2 parity fix itself has not yet been runtime-tested in Blender 5.0.1.**

### Blender 4.5 status

Blender 4.5 remains a secondary compatibility target, especially for BG3 workflows and tooling that still requires the older environment. Dev_v2.11.2 has not yet received its Blender 4.5 compatibility pass.

Do not infer that every Dev_v2.11.2 path works in 4.5 merely because the add-on minimum remains 4.5.0. Shared/BG3 paths must be tested there separately.

### Static/package validation

The Dev_v2.11.2 full-package validation passed:
- Python AST parse across 67 Python files;
- duplicate operator/UI ID scan;
- version and panel-order contracts;
- Advanced Clean section-routing source contracts;
- Analyze parity source-contract checks;
- cache/package hygiene;
- ZIP integrity;
- SHA-256 verification.

Static/package validation does not establish Blender runtime behavior.

### Known compatibility/testing limitations

Still pending:
- Dev_v2.11.2 Analyze parity retest in Blender 5.0.1;
- exact offending-element identity comparison before Analyze click-to-select is added;
- Transform Edit Mode coordinate/Undo testing;
- Advanced Clean section execution and Shift-selection testing;
- Make Manifold / Auto Fix / Advanced Clean topology-safety testing;
- STL export/re-import testing;
- Dev_v2.10.1 Magic Branch / Inject New / Object Snap regression testing after integration;
- Blender 4.5 secondary compatibility testing.

The Toolbox-equivalent Thin Faces path creates a temporary mesh/object and uses object ray casts, matching the original algorithm. This path specifically needs runtime validation in both 5.0.1 and 4.5.

## Recent compatibility history

- `Dev_v2.11.1`: authored under the former Blender 4.5-primary policy; user runtime in Blender 5.0.1 confirmed 3D Print Tools rendering/Analyze execution and exposed the analyzer parity issue fixed in source by Dev_v2.11.2.
- `Dev_v2.10.1`: Blender 4.5-targeted Magic Branch/Inject/Object Snap runtime-fix candidate; source/static checks passed, but its hotfix paths still require regression retest.
- `Dev_v2.10.0`: Blender 4.5-targeted Magnetic Inject New / Magic Branch / Edge Doctor candidate; partial user runtime evidence is recorded in the project changelogs/state.
- `Dev_v2.5.2`: Curvature Sync column-repair workflow received successful user production feedback; exact compatibility details are retained in repository history/cumulative project documentation.

Older compatibility history remains preserved in Git history and the cumulative Witch Tools documentation/changelogs rather than being represented as current candidate status here.
