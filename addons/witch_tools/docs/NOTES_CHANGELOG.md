# Witch Tools Notes Changelog — Latest Update

Date: 2026-08-18

## Dev_v2.11.1 — Advanced Clean Instant Clean-style restoration

- Corrected Dev_v2.11.0 Advanced Clean after user review showed the integration had changed more of Instant Clean's UI than requested.
- Restored Repair / Manifold / Topology / Normals / Dissolve as individual collapsible sections with section-header enable toggles and per-section play buttons.
- Main Clean runs the enabled section set; each play button runs only its own section, even if that section's global-enable toggle is off. Shift selection-only behavior applies to both paths.
- Restored original-style body layout for controls that were not explicitly requested to change.
- Retained the deliberate customizations: Object Data and Make Planar removed, Dissolve last, compact Manifold Remove Non-Manifold, responsive Topology angle/Compare rows, compact Normals Clear Data.
- Added a feature decisions file and expanded the Blender test plan for header rendering and individual-section execution.
- Built the full installable `Witch_Tools_Dev_v2_11_1_3D_Print_Transform_Blender_4_5.zip`; GitHub Actions static/package validation and independent ZIP/SHA verification passed.
- Artifact SHA-256: `d6ecf1b893c1d619fc5974ec0ca1836fe7333abd4b9c5724ff497b63859c2441`.
- Candidate: `Dev_v2.11.1`; target Blender `4.5.0`; Blender runtime validation pending. User reference screenshots show Blender 5.0.1, but no 5.0.1 compatibility claim is made yet.
