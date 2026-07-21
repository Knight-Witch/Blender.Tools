# Add-on Boundaries

## Purpose

This document defines canonical ownership so cross-domain tools are not duplicated or buried in the wrong add-on.

## Witch Tools ownership

Witch Tools owns general-purpose Blender capabilities, including:

- mesh and topology repair
- selection and protected-zone infrastructure
- transforms, origins, cursor, snapping, and mirroring backends
- general armature, weighting, naming, cleanup, and refit operators
- Curvature Sync
- Vertex/Edge Inject
- bulk chain correspondence repair

A feature remains owned by Witch Tools even when its first use case is BG3 or 3D printing, provided the capability is reusable.

## Witch Quickbar ownership

Quickbar owns only its floating-overlay presentation and Quickbar-specific interaction systems:

- draw and gizmo layers
- hit targets and event dispatch
- display states
- drag/reorder/resize controls
- Quickbar preferences and persistence
- Quickbar asset loading
- compact command exposure

Quickbar may contain thin wrapper operators needed to invoke canonical actions safely, but not duplicate geometry algorithms.

## Witch Core ownership

Witch Core owns process-driven manufacturing workflows, such as:

- SVG-to-housing pipelines
- Cauldron Core construction
- print-preparation sequences
- manufacturing validation and presets
- workflow orchestration that combines several generic operators

Reusable geometry primitives stay outside Witch Core.

## BG3 ownership rule

A tool belongs in a BG3 module only when its behavior is fundamentally determined by BG3 data, naming, armatures, export constraints, or game-specific metadata.

A generic topology or modeling tool does not become BG3-owned merely because it was discovered while editing a BG3 asset.

## 3D-print ownership rule

A tool belongs in Witch Core when it is a complete print/manufacturing workflow. Generic topology repair and mesh editing stay in Witch Tools, with print-specific tests and documentation.

## Curvature Sync ownership

- Canonical owner: Witch Tools
- Primary category: topology repair
- Development status: specification/prototype planning
- Quickbar role: optional compact invocation after stable integration
- Witch Core role: optional backend use in print-specific workflows
- Use cases: general modeling, BG3, 3D printing

## Dependency rules

- UI modules may depend on stable backend modules.
- Backend modules must not depend on Quickbar overlay code.
- Generic shared utilities must not import add-on-specific UI.
- Cross-add-on runtime imports require explicit version/availability handling.
- Prefer build-time vendoring for independently installable public packages once build tooling is established.

## Ownership changes

Moving canonical ownership requires an ADR and migration plan. A copied implementation is not an ownership transfer.