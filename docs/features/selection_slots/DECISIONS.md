# Selection Slots Decisions

## SS-D001 — Witch Tools owns the canonical backend

Status: accepted

Selection storage and restoration are general-purpose Blender capabilities. Witch Tools owns the data model and `mesh.wt_selection_slot_*` operators. Quickbar is an optional presentation layer and must not duplicate slot data.

## SS-D002 — Persist markers in mesh custom data

Status: accepted for the initial implementation

Transient BMesh indices are not stable across save/reopen or topology changes. Each slot therefore uses a generated UID and integer custom-data layers on vertex, edge, and face domains, with scene records providing names, modes, counts, order, and object references.

Consequence: selections persist in the `.blend`, but Blender topology operations may delete or propagate markers according to custom-data behavior.

## SS-D003 — Store the active selection domain

Status: accepted

A slot records which mesh-selection modes were active when saved. Reselect restores those modes instead of inferring a domain from incidental selected vertices surrounding an edge or face selection.

## SS-D004 — Save means overwrite

Status: accepted

The Save control replaces prior slot markers. An empty current selection cancels before clearing prior valid data.

## SS-D005 — Clear and Remove are distinct

Status: accepted

Clear erases stored selection data while retaining the row and name. Remove erases both data and row. Clear All retains all rows and names.

## SS-D006 — Preserve one default row

Status: accepted

At least one slot must always exist. Removing the final row creates a new empty Slot 1 so the tool never presents a blank unusable section.

## SS-D007 — Limit initial slot count to 20

Status: accepted

Twenty slots provide substantial flexibility while bounding custom-data proliferation and Quickbar layout/hit-target growth. The limit can be revised after runtime profiling.

## SS-D008 — N-panel and Quickbar use different reorder interactions

Status: accepted

The Witch Tools N-panel uses reliable up/down controls. Quickbar uses its existing short-lived modal drag architecture and a grip hit target. Both invoke the same canonical move operator and preserve slot UID/data.

## SS-D009 — Quickbar remains optional

Status: accepted

Quickbar Dev_v1.4.0 detects the required Witch Tools operators. When unavailable, Quickbar displays an explanatory disabled state and continues running its native features.

## SS-D010 — Do not auto-repair stale selections

Status: accepted

When topology deletes marked elements, Selection Slots restores only surviving markers and reports failure when none remain. It does not guess replacement topology. Diagnostics and explicit repair tools may be considered later.

## SS-D011 — Names are labels, not identity

Status: accepted

Slot identity is the generated UID. Names may be duplicated, changed, or left at defaults without affecting stored markers.

## SS-D012 — Supplied SVGs become runtime PNG assets only

Status: accepted for Quickbar

The five supplied Blender-style SVGs are converted to transparent 64x64 PNGs for the current Quickbar asset loader. SVG source files are not shipped in the distributable ZIP.
