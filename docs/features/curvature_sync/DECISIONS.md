# Curvature Sync Decisions

## CS-D001 — Witch Tools owns Curvature Sync

Status: accepted

Context: The feature arose from a 3D-print collar and is also useful for BG3 and general modeling.

Decision: Curvature Sync is a general topology-repair feature owned by Witch Tools. Quickbar may later expose it; Witch Core may invoke its backend.

Consequence: one canonical implementation serves all use cases.

## CS-D002 — Circular planar arcs first

Status: accepted

Context: The production reference is an approximately semicircular hard-surface part. Generic spline fitting creates ambiguity and larger risk.

Decision: The first implementation supports explicit planar circular open arcs only.

Consequence: deterministic geometry and testable tolerances; generic spline support remains research.

## CS-D003 — Canonical column lattice

Status: accepted

Context: Independently smoothing parallel chains can preserve curve appearance while leaving vertical/radial columns mismatched.

Decision: Create one authoritative angular lattice and apply it to every participating chain/object.

Consequence: correspondence and equal segmentation are primary, not incidental.

## CS-D004 — A/M/Z anchors

Status: accepted

Context: Straight extensions must remain straight, and a real symmetry-center column is required.

Decision: A and Z define the movable curved span; M defines the center column and symmetry split. Preserve all three by default.

Consequence: geometry outside A/Z is excluded, and total column count is odd in symmetrical mode.

## CS-D005 — Shared center, per-chain radius

Status: accepted for initial collar mode

Decision: Parallel chains share a center, plane, angular span, and column angles while retaining their own radii and height/axial offsets.

Consequence: concentric/profile spacing is preserved without independently fitting each row.

## CS-D006 — Connect and split is default

Status: accepted

Context: Injecting a missing vertex is normally intended to create the missing column and turn one face into two.

Decision: Auto-Aligned Vertex Inject defaults to `Connect & Split Face = ON`, with a toggle to disable.

Consequence: one operation performs the full repair primitive.

## CS-D007 — Native face split over delete/refill

Status: accepted

Decision: When C and D share a face boundary, use BMesh connect/split behavior rather than deleting and manually refilling the face.

Consequence: better winding and custom-data preservation, fewer invalid-face risks.

## CS-D008 — Proper normals are mandatory

Status: accepted

Decision: Store source orientation/attributes, preserve winding, validate child normals, and update affected normals as part of the operation.

Consequence: normals are not an optional cleanup pass.

## CS-D009 — Protected coordinates may still accept boundary topology

Status: accepted

Context: Treating protected as absolutely untouchable could leave holes when a valid new column must connect to an anchor.

Decision: Protection has distinct permissions. Position may be locked while boundary connection and adjacent face splitting are allowed.

Consequence: protected-zone data must be more expressive than one boolean.

## CS-D010 — Leave surplus vertices by default

Status: accepted

Decision: Do not automatically dissolve unmatched existing vertices in the first version. Leave them and select/report them.

Consequence: lower destructive risk; cleanup automation can be added after proven topology rules.

## CS-D011 — Preview and preflight before bulk mutation

Status: accepted

Decision: Bulk operations analyze and report planned injections, edges, face splits, movements, and conflicts before apply.

Consequence: ambiguous topology must stop rather than guess.

## CS-D012 — Multi-object synchronization uses one analysis frame

Status: accepted

Decision: Transform every participating object into a declared master/world analysis frame, solve there, and convert destinations back to object-local coordinates.

Consequence: aligned upper/lower print components can share exact column planes despite separate objects and transforms.