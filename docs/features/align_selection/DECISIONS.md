# Align Vertices / Edges / Faces Decisions

## ADR-AS-001 — Witch Tools owns the backend

Accepted. Guided alignment is a reusable mesh-transform capability. Witch Dock/Quickbar may expose the canonical Witch Tools contract later but must not duplicate geometry logic.

## ADR-AS-002 — Analyze and solve in world space

Accepted. Multi-object Edit Mode objects may have different transforms. Results are converted back through each object's inverse matrix after planning.

## ADR-AS-003 — Separate alignment target from permitted movement

Accepted. “Which coordinate should match?” and “how may this geometry move?” are independent questions. The UI therefore separates World/Custom target controls from Free/Rail movement controls.

## ADR-AS-004 — Explicit parent capture

Accepted. Selection order is not a reliable persistent contract across arbitrary mesh domains and multiple objects.

## ADR-AS-005 — Active Element and Median references

Accepted. Active Element supports a precise chosen parent; Median supports an anchor set. Captured edges and faces resolve to participating vertices.

## ADR-AS-006 — Disabled components remain unchanged

Accepted. The user explicitly selects which world or custom-frame components are matched. An unchecked component is not modified.

## ADR-AS-007 — Custom X follows the guide direction

Accepted. Guide Start to Guide End defines custom X. A deterministic perpendicular basis defines custom Y and Z.

## ADR-AS-008 — Projection to guide line matches custom Y/Z only

Accepted. This projects to the arbitrary line while preserving distance along custom X.

## ADR-AS-009 — Captured rails are movement constraints, not protected edges

Accepted. The blue edges in the user's example define permitted slide paths. They do not need to be locked from editing or conflated with Protected Edit Zones.

## ADR-AS-010 — Straight rails only in Dev_v2.8.0

Accepted. A point can be solved safely as `p + t*d` on a straight line. Curved/polyline motion requires a separate design for arc length, junctions, rigid groups, and possible rotation.

## ADR-AS-011 — Rail constraints must share one parameter

Accepted. When multiple coordinate components are enabled, every component must imply the same rail parameter within tolerance. An incompatible solution cancels before movement.

## ADR-AS-012 — Pairing is explicit through disconnected rail components

Accepted. In Paired by Rail mode, each subordinate island touches one rail and each rail contains exactly one captured parent vertex. The backend never guesses by nearest distance or vertex index.

## ADR-AS-013 — Target islands touching multiple rails are ambiguous

Accepted. Ambiguous mapping cancels the complete operation instead of silently choosing a rail.

## ADR-AS-014 — Shape preservation means one rigid translation per group

Accepted. Every vertex in a preserved group receives one identical world-space translation. The tool does not scale, rotate, or deform the group.

## ADR-AS-015 — Selected topology defines subordinate islands

Accepted. The user explicitly selects the geometry to move. Unselected connected mesh geometry is not silently included.

## ADR-AS-016 — Cancel the entire operation on any invalid group

Accepted. Partial destructive movement is difficult to detect and undo correctly. Every result is planned before mutation.

## ADR-AS-017 — Persistent marker layers with count verification

Accepted for the candidate. Topology changes can invalidate or propagate markers; count mismatches require recapture rather than guessing.

## ADR-AS-018 — Multiple shape keys are rejected

Accepted for Dev_v2.8.0. Correct relative-key coordinate handling is outside current scope.

## ADR-AS-019 — Rebuild from the last verified complete source

Accepted. The committed Dev_v2.7.0 snapshot parts are truncated and cannot reconstruct the documented Dev_v2.7.1 source. Dev_v2.8.0 uses the verified Dev_v2.6.1 source baseline and records the conflict explicitly.

## ADR-AS-020 — Witch Dock/Quickbar waits for backend validation

Accepted per the user's requested order. Witch Tools is implemented and tested first; overlay integration follows only after the final workflow and contract are accepted.
