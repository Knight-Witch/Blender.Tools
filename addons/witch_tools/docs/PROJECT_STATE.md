# Witch Tools Project State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit and reusable mesh/topology backend
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Current candidate: `Dev_v2.11.1`
- Target Blender: `4.5.0`
- Package folder: `Witch_Tools_Dev`
- Public/release branches modified: no
- Witch Dock / Quickbar modified: no

## Current artifact

- Full installable ZIP: `Witch_Tools_Dev_v2_11_1_3D_Print_Transform_Blender_4_5.zip`
- SHA-256: `d6ecf1b893c1d619fc5974ec0ca1836fe7333abd4b9c5724ff497b63859c2441`
- GitHub Actions packaging/validation: passed
- Local SHA-256 verification of downloaded inner add-on ZIP: passed
- Local ZIP integrity check: passed
- Blender runtime: pending

## Last completed work

User review of Dev_v2.11.0 identified a UI/behavior mismatch in Advanced Clean: the integration had over-condensed Instant Clean instead of preserving its section interaction model.

Dev_v2.11.1 corrects that integration:
- Repair / Manifold / Topology / Normals / Dissolve are again separate collapsible Advanced Clean child sections.
- Every section header has its own enable toggle and play button.
- The main Clean action runs the sections whose header toggles are enabled.
- A section play action runs only that individual section, even if its parent-enable toggle is off.
- Shift selection-only behavior applies to main Clean and individual section actions.
- Repair, Topology Methods, Normals controls, and Dissolve Protect were returned to an original-style Instant Clean presentation where no redesign had been requested.
- Requested customizations remain: no Object Data, no Make Planar, Dissolve last, compact Manifold Remove Non-Manifold toggles, responsive Topology angle/Compare controls, compact Normals Clear Data toggles.
- Version metadata advanced to Dev_v2.11.1.
- Feature specification/state/roadmap/test plan/decisions, global roadmap/UI map/changelogs and compatibility documentation were synchronized with the correction.
- Full Dev_v2.11.1 package was built and static/package validation passed.

## Current known-working state

Inherited runtime results remain those previously recorded for Dev_v2.10.0. Dev_v2.11.1 itself has not been executed in Blender yet. Static/package validation establishes source/package integrity only, not Blender runtime behavior.

The user's supplied Instant Clean reference screenshots show Blender 5.0.1. That establishes the visual reference environment only. It does not establish Witch Tools 5.0.1 compatibility. The authored target remains Blender 4.5.0 unless explicitly changed.

## Active problems / limitations

1. Dev_v2.11.1 register/unregister is runtime-untested.
2. The custom Advanced Clean child-panel headers must be visually checked in Blender: disclosure triangle, section toggle, play button, and no duplicate/blank title artifact.
3. Main Clean category filtering and every per-section play action require runtime testing.
4. Shift selection-only behavior requires runtime testing for global and individual actions.
5. Advanced Clean topology-changing operations still require Undo/Redo, mode, normals/winding, materials/edge/custom-data, manifold, malformed-selection, and failure-safety tests.
6. Transform Edit Mode coordinate editing remains runtime-untested.
7. Analyze Mesh detector counts still require direct parity comparison with Blender's original 3D Print Toolbox.
8. Analyze result click-to-select is required after detector parity but not yet implemented.
9. Auto Fix/Make Manifold/STL export remain runtime-untested.
10. Dev_v2.10.1 Magic Branch/Inject/Object Snap fixes still require their existing regression retest.
11. No compatibility claim is made for Blender versions beyond the 4.5 target.

## Next exact implementation step

Install the full Dev_v2.11.1 ZIP and test Advanced Clean before continuing the wider feature test plan. First check the five child headers visually. Then test main Clean with only one section enabled at a time. Then test each section play button, including a case where its enable toggle is off. Then test Shift selection-only behavior.

If that passes, resume Transform and Analyze Mesh parity testing. Do not begin click-to-select implementation until analyzer parity is established.

## Files changed for Dev_v2.11.1

Source:
- `panel_print3d.py`
- `instant_clean_core.py`
- `__init__.py`
- `state.py`
- `CHANGELOG.md`

Build/compatibility:
- `.github/workflows/package-witch-tools-v2-11.yml`
- `docs/COMPATIBILITY_DEV_v2.11.1.md`

Documentation:
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/UI_MAP.md`
- `docs/NOTES_CHANGELOG.md`
- `docs/NOTES_CHANGELOG_FULL.md`
- `docs/features/print3d_transform/SPEC.md`
- `STATE.md`
- `ROADMAP.md`
- `TEST_PLAN.md`
- new `DECISIONS.md`

## Test status

- Current Dev_v2.10.1 baseline confirmation: previously performed
- Dev_v2.11.1 source implementation: performed
- Static Python parse/identifier/version/panel-order/section-routing checks: passed in GitHub Actions
- Package hygiene and ZIP integrity: passed
- Downloaded inner add-on ZIP SHA-256 verification: passed
- Blender 4.5 runtime: not performed
- Blender 5.0.1 Witch Tools runtime: not performed/claimed
- Public release branches changed: no
