# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-18

## Dev_v2.11.2 — 3D Print Toolbox Analyze parity correction

- Blender 5.0.1 runtime comparison on the same `_CAP 3` mesh proved Dev_v2.11.1 Analyze Mesh did not match the original 3D Print Toolbox on four checks.
- Original Toolbox: Non-flat 98, Thin 0, Sharp 0, Overhang 79. Dev_v2.11.1 Witch Tools: 73, 1, 1, 80. The other six displayed counts matched on that fixture.
- Replaced the simplified Analyze approximations with Toolbox-equivalent semantics: original BVH intersection handling, 0.1 mm degenerate threshold, world-transformed 5° distorted-face test, six-sample backwards-ray 1 mm thickness test, signed 160° sharp-edge test, and world-transformed 45° downward-normal overhang test.
- Kept the Analyze UI compact and did not restore the original threshold/settings grid; the backend uses the standard Toolbox defaults invisibly.
- Blender 5.0.1 is now the primary Witch Tools development/runtime target. Blender 4.5 remains a secondary compatibility target for BG3 and workflows that still require it; the add-on minimum remains 4.5.0 so the same package can still be tested there.
- Advanced Clean Dev_v2.11.1 layout/section-run behavior is retained unchanged.
- Analyze click-to-select remains gated on count parity plus actual offending-element identity comparison.
- Built full installable `Witch_Tools_Dev_v2_11_2_3D_Print_Transform_Blender_5_0_1.zip`.
- GitHub Actions static/package validation, ZIP integrity, and independent downloaded-inner-ZIP SHA verification passed.
- Artifact SHA-256: `37493258a6a995b6fd1799e60a56d0a55c4f2afda1a772a0dfecaa13ae90daef`.
- Candidate: `Dev_v2.11.2`; Blender 5.0.1 parity retest pending.
