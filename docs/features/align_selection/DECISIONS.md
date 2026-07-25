# Align Selection Decisions

## ADR-AS-001 — Witch Tools owns the backend

Accepted. Align Selection is a reusable mesh transform capability. Quickbar exposes the canonical Witch Tools operators only.

## ADR-AS-002 — Use world-space coordinates

Accepted. Multi-object Edit Mode objects may have different transforms. Results are converted back through each object's inverse matrix.

## ADR-AS-003 — Separate Match Coordinates and Move Shape

Accepted. Figure A intentionally assigns coordinates; Figure B requires one translation applied to a complete shape.

## ADR-AS-004 — Explicit source and anchor captures

Accepted. Blender selection order is not a reliable persistent contract for arbitrary multi-domain and multi-object selections.

## ADR-AS-005 — Median and Active Element source references

Accepted for the current Witch Tools development build. Median supports arbitrary source sets; Active Element uses the active vertex, edge center, or face center. Quickbar exposure is a separate local-only UI task.

## ADR-AS-006 — Selected-edge connectivity defines islands

Accepted. The user explicitly selects the complete move set; unselected mesh geometry is not silently roped in.

## ADR-AS-007 — Cancel complete operation on invalid island

Accepted. Partial movement is destructive and difficult to detect.

## ADR-AS-008 — Persistent marker layers with count verification

Accepted for the MVP. Topology changes may require recapture.

## ADR-AS-009 — Quickbar source remains local for this update

Accepted per explicit user instruction. Witch Tools development source is updated on `Blender_Dev`; Quickbar Dev_v1.5.0 remains a local ZIP only.

## ADR-AS-010 — Dev_v2.7.1 uses the exact user-tested replacement build as its patch baseline

Accepted. The replacement Dev_v2.7.0 ZIP installed by the user had SHA-256 `53381952406a39d23ab457dd8db3b5a577c53ec55c8fb06597a6275559693def`, which differed from the earlier Dev_v2.7.0 snapshot identity recorded in repository documentation. Dev_v2.7.1 records this discrepancy, uses the exact failing package as the repair baseline, and supersedes both Dev_v2.7.0 identities rather than silently treating them as identical.
