# Align Selection Decisions

## ADR-AS-001 — Witch Tools owns the backend

Accepted. Align Selection is a reusable mesh transform capability. Quickbar exposes the canonical Witch Tools operators only.

## ADR-AS-002 — Use world-space coordinates

Accepted. Multi-object Edit Mode objects may have different transforms. Results are converted back through each object's inverse matrix.

## ADR-AS-003 — Separate Match Coordinates and Move Shape

Accepted. Figure A intentionally assigns coordinates; Figure B requires one translation applied to a complete shape.

## ADR-AS-004 — Explicit source and anchor captures

Accepted. Blender selection order is not a reliable persistent contract for arbitrary multi-domain and multi-object selections.

## ADR-AS-005 — Arithmetic-mean reference positions

Accepted for Dev_v2.7.0. Optional Active Element mode is deferred.

## ADR-AS-006 — Selected-edge connectivity defines islands

Accepted. The user explicitly selects the complete move set; unselected mesh geometry is not silently roped in.

## ADR-AS-007 — Cancel complete operation on invalid island

Accepted. Partial movement is destructive and difficult to detect.

## ADR-AS-008 — Persistent marker layers with count verification

Accepted for the MVP. Topology changes may require recapture.

## ADR-AS-009 — Quickbar source remains local for this update

Accepted per explicit user instruction. Witch Tools development source is updated on `Blender_Dev`; Quickbar Dev_v1.5.0 is delivered as a local ZIP only.
