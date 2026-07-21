# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Collar embedded-edge / unsplit-face repair

- Inspected `Collar_DESIGN_v6 - Copy.blend` after manual vertex and edge insertion.
- Confirmed the stale-face problem is represented by existing wire edges whose endpoints already belong to one older unsplit face.
- Identified eight unambiguous repair locations:
  - `COLLAR - UPPER.002`: 2
  - `RIGHT EXTENSION`: 6
- Produced an exact-file Blender 4.5 repair script that splits the existing faces along those edges without moving vertices or deleting the new edge network.
- Added transactional baseline checks, material/smoothing preservation, normal update, duplicate/degenerate geometry validation, non-manifold-count preservation, safe output naming, and a JSON repair report.
- Added optional Windows BAT execution plus manual Scripting-workspace instructions.
- Added `WT-CLEAN-001 — Resolve Embedded Edges / Repair Unsplit Faces` to the Witch Tools roadmap for later generalized add-on integration.

## Testing

- Script syntax: passed.
- Exact uploaded file detection: passed under Blender Python 5.2.0 LTS.
- Eight face splits completed in the test copy.
- Vertex and edge counts remained unchanged.
- Face counts increased by exactly eight.
- No new zero-length edges, zero-area faces, duplicate faces, boundary-edge changes, or overlinked-edge changes were introduced.
- Blender 4.5 execution and saved-file verification remain pending user execution.

## Add-on status

- Current Witch Tools build remains Dev_v2.5.1.
- No add-on package, public branch, operator namespace, update URL, or public compatibility surface was changed in this repair pass.
