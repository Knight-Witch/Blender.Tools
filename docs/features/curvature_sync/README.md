# Curvature Sync

## Ownership

- Owning add-on: Witch Tools
- Category: Edit / Topology Repair
- Current status: specification; implementation not started
- Default target: Blender 4.5

## Purpose

Curvature Sync repairs malformed hard-surface topology where multiple parallel curved edge chains have inconsistent vertex counts, missing corresponding vertices/edges, flat or uneven curve sections, and mismatched segmentation across separate objects or mesh islands.

The initial production reference is a split 3D-print collar whose upper and lower pieces fit geometrically but were constructed with unrelated edge segmentation. Curvature Sync must create a common, symmetrical column lattice so corresponding loops align across all participating chains and fitted objects while preserving straight extensions and print-critical dimensions.

## Related systems

- Auto-Aligned Vertex Inject
- Bulk Missing Correspondence Injection
- Connect/Split Face
- Protected/ignored zones
- Vertex Lock integration
- shared topology and attribute-preservation utilities

## Primary documents

- `SPEC.md` — intended behavior
- `STATE.md` — actual implementation state
- `ROADMAP.md` — implementation phases and later ideas
- `TEST_PLAN.md` — acceptance and regression tests
- `DECISIONS.md` — feature decisions and rationale
- `REFERENCE_CASES.md` — production problem cases

## Core model

The first supported model is a planar circular arc bounded by explicit A and Z endpoints and an explicit or derived middle M column. Multiple parallel chains share:

- one analysis plane
- one center/symmetry axis
- one angular span
- one canonical set of column angles

Each chain retains its own radius and axial/height offset.

## Non-goals for the first version

- automatic remeshing of arbitrary meshes
- generic organic retopology
- arbitrary 3D spline fitting
- automatic dissolution of all surplus topology
- silent guessing through branches, poles, non-manifold regions, or ambiguous paths

## Safety principle

Analyze and preview before mutation. Curvature Sync must stop rather than invent topology when correspondence or traversal is ambiguous.