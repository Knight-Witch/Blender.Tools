# Magic Branch — Roadmap

## Dev_v2.10.0 candidate — active

- Inject New Magnetic Snap and Branch Auto-Merge.
- independent Inject New X/Y/Z movement toggles.
- multi-edge Slide using a shared relative factor.
- MMB orbit around current live injection/branch.
- Magic Branch Vertex / Edge / Face.
- Single Branch / Persistent.
- Face Paver / Organic.
- shared magnetic target highlighting.
- Edge Doctor regrouping and two-edge L repair.
- saved Edit Tools reordering.

## Immediate validation — planned

- Blender 4.5 registration/unregistration.
- GPU hover rendering and selection priority.
- MMB orbit pivot/resume behavior.
- magnetic vertex/edge/face solves at varied camera angles.
- Auto-Merge topology safety.
- Persistent per-branch Undo.
- Paver/Organic topology, normals, winding and cancellation.
- drag-grip UI reorder; confirm arrow fallback.

## Follow-up — deferred/research

- dynamically add/remove unselected fan edges to Inject New Slide solely by hover;
- A/B/C viewport labels for Edge Doctor;
- arbitrary safe face-interior Auto-Merge/retopology rules;
- curved/polyline drag rails;
- multi-object topology branching;
- richer snap filters/tolerances;
- Witch Dock/Quickbar thin wrappers after Witch Tools runtime acceptance.

## Dev_v2.10.1 Blender 4.5 regression addendum

Dev_v2.10.0 user testing confirmed hover highlighting, Magnetic Snap, Inject New Undo/Redo, Paver, Organic, and the tested Organic vertex-merge path. Failures found were: Edge Solo/Branch restricted to one edge; only one magnetic contact merged; an old unsplit target edge remained through an inserted vertex; Magic Branch reset the view pivot while waiting; no explicit Magic Branch ON/OFF; no Z-wall Paver growth from a horizontal source; Paver return-path overlaps did not all merge; Branch Type did not synchronize Blender Vertex/Edge/Face selection mode; Object Snap did not enter Undo history.

Dev_v2.10.1 implements source fixes for those cases. Blender 4.5 runtime retest remains required.
