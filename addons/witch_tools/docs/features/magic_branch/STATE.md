# Magic Branch — State

Last updated: 2026-08-08

- Add-on: Witch Tools
- Candidate: `Dev_v2.10.0`
- Branch: `feature/witch-tools-magic-branch`
- Target Blender: `4.5.0`
- Runtime status: untested source candidate

## Implemented in source

- shared Inject New / Magic Branch drag and magnetic-snap backend;
- vertex/edge/face hover target highlighting;
- independent X/Y/Z movement masks;
- vertex/edge rigid-endpoint magnetic snap;
- per-endpoint face travel-line magnetic placement;
- conservative vertex/edge Auto-Merge with target-edge splitting;
- MMB pass-through orbit with live-geometry pivot assignment;
- Inject New multi-edge Slide with common relative factor and hovered selected-edge driver;
- Magic Branch Single/Persistent modes;
- Magic Branch Vertex/Edge/Face workflows;
- Face Paver and Organic modes;
- persistent hotkeyable Persistent toggle operator;
- Edge Doctor regrouping and two-edge L repair;
- preference-backed top-level Edit Tools reordering with drag grip + arrow fallback.

## Known limitations / unresolved validation

- no Blender executable is available in the implementation environment;
- GPU hover overlay rendering is not runtime-verified;
- MMB pivot feel is not runtime-verified;
- persistent per-branch Undo behavior is not runtime-verified;
- drag-grip reorder behavior from an N-panel button is not runtime-verified; up/down controls are the fallback;
- Auto-Merge does not invent arbitrary face-interior retopology;
- Paver will not stretch an off-grid final tile;
- topology tools operate on the active mesh only;
- Inject New Slide uses the preselected edge set; hover chooses the driver among those selected rails, not arbitrary unselected fan edges;
- A/B/C viewport letter overlays are deferred.

## Next exact step

Install/package the branch as Witch Tools Dev_v2.10.0 for Blender 4.5 and execute `TEST_PLAN.md`, beginning with registration/UI/GPU drawing, then Inject New magnetic behavior, then Magic Branch, MMB orbit, Auto-Merge, cancellation and Undo/Redo.

## Dev_v2.10.1 Blender 4.5 regression addendum

Dev_v2.10.0 user testing confirmed hover highlighting, Magnetic Snap, Inject New Undo/Redo, Paver, Organic, and the tested Organic vertex-merge path. Failures found were: Edge Solo/Branch restricted to one edge; only one magnetic contact merged; an old unsplit target edge remained through an inserted vertex; Magic Branch reset the view pivot while waiting; no explicit Magic Branch ON/OFF; no Z-wall Paver growth from a horizontal source; Paver return-path overlaps did not all merge; Branch Type did not synchronize Blender Vertex/Edge/Face selection mode; Object Snap did not enter Undo history.

Dev_v2.10.1 implements source fixes for those cases. Blender 4.5 runtime retest remains required.
