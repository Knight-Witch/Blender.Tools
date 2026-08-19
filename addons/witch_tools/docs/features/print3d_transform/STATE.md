# 3D Print Tools + Transform State

Last updated: 2026-08-18

## Identity

- Add-on: Witch Tools
- Candidate: `Dev_v2.11.1`
- Development branch: `feature/witch-tools-3d-print-transform-v2-11`
- Parent baseline: `feature/witch-tools-magic-branch` Dev_v2.10.1 packaging head `9ef376505ccf9df3f39720dea630b378470c818b`
- Target Blender: `4.5.0`

## Current correction

User review of the first Dev_v2.11.0 Advanced Clean UI showed that the Instant Clean layout had been over-condensed. The intended design is to preserve Instant Clean's section structure and per-section execution model except where the user explicitly requested changes.

Dev_v2.11.1 source changes:
- restored individual collapsible Repair / Manifold / Topology / Normals / Dissolve sections;
- added an enable toggle and individual play button to each section header;
- individual play buttons run only their own section;
- main Clean runs whichever section-header toggles are enabled;
- Shift applies selection-only behavior to both main and individual section actions;
- restored original-style checkbox/boxed layouts for controls that were not requested to change;
- retained requested compact changes for Manifold Remove Non-Manifold, Topology angles/Compare, and Normals Clear Data;
- kept Dissolve last;
- kept Object Data and Make Planar removed.

## Prior Dev_v2.11.0 integration

- Added top-level Transform directly below Mode Switcher.
- Added editable object Location / Rotation / Scale.
- Added Edit Mode selected-vertex local Location median with delta translation.
- Added top-level 3D Print Tools above Edit Tools.
- Added simplified STL Export.
- Added consolidated Analyze Mesh / Check All results.
- Added Make Manifold.
- Added Auto Fix with Global Fix before Local Fix.
- Added Advanced Clean integration.

## Source modules changed for Dev_v2.11.1

- `panel_print3d.py`
- `instant_clean_core.py`
- `__init__.py`
- `state.py`
- `CHANGELOG.md`
- packaging/compatibility/documentation files required for the candidate update

## Runtime validation not performed

Dev_v2.11.1 has not been run in Blender. Still to test:
- add-on register/unregister;
- empty-label child-panel header rendering with the custom enable toggle + play button;
- main Clean category filtering;
- each individual section play action;
- Shift selection-only behavior for main and individual actions;
- Advanced Clean topology safety/Undo/Redo/attribute preservation;
- Transform runtime behavior;
- Analyze Mesh parity and later click-to-select behavior;
- STL export/reimport;
- Dev_v2.10.1 baseline regression.

The user's Instant Clean reference screenshots show Blender 5.0.1. That is useful UI reference and identifies the user's current test environment, but no Witch Tools 5.0.1 compatibility claim is made from those screenshots. The development target remains Blender 4.5.0.

## Known design limitations

- Analyze Mesh still provides counts only; click-to-select is a required follow-up after detector parity.
- Intersect Volumes remains topology-rebuilding and requires destructive-operation validation.
- Edit-mode Transform Location remains object-local.
- Dev_v2.11.1 custom child-panel header rendering is source/static work until user-tested in Blender.

## Next exact step

Package the full Dev_v2.11.1 candidate and install it in Blender. First verify that Advanced Clean visually matches the intended Instant Clean structure: section toggle in the header, play button in the header, collapsible section body, Dissolve last. Then verify main Clean vs individual section execution before continuing broader 3D Print/Transform testing.
