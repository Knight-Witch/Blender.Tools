# Blender.Tools Use Cases

Use-case documents explain how canonical tools apply to different domains. They do not own duplicate implementations.

## Domains

- `bg3/` — Baldur's Gate 3 asset, rig, naming, orientation, and export workflows
- `general_modeling/` — reusable Blender modeling and topology workflows
- `3d_printing/` — dimensional, manifold, assembly, and manufacturing constraints

## Rule

Feature ownership is defined in `docs/architecture/ADDON_BOUNDARIES.md`.

Example: Curvature Sync is implemented once in Witch Tools, with domain-specific tests and workflow notes under each relevant use-case directory.

## Current state

Detailed prior BG3, modeling, and printing documents still need to be imported and reconciled from existing project sources. Do not reconstruct them incompletely from chat memory.