# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v2.6.0 — Selection Slots

- Added **Edit Tools > Selection Slots** immediately below Curvature Sync.
- Added persistent renameable slots for vertex, edge, face, and combined mesh selection modes.
- Added multi-object Edit Mode save/reselect behavior.
- Added save/overwrite, reselect, clear, Clear All, add, remove, rename, and reorder controls.
- Added one automatic Slot 1 and a maximum of 20 slots.
- Added scene slot records with generated UIDs, stored selection modes/counts/object references, and per-mesh vertex/edge/face integer custom-data markers.
- Added stable `mesh.wt_selection_slot_*` operators for optional Quickbar invocation.
- Added responsive N-panel name fields and LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD native icons.
- Produced `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`, SHA-256 `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`.
- Added package quick-start, README, changelog, compatibility, feature packet, project state, roadmap, build registry, and notes updates.

## Testing

- ZIP integrity and safe-path checks passed.
- Static parsing/compile passed for all 46 Python files.
- Duplicate operator-ID scan passed.
- No `__pycache__`, `.pyc`, `.pyo`, or unrelated source assets were shipped.
- Blender 4.5 Selection Slots registration, UI, save/reselect, persistence, multi-object, topology-change, and undo/redo testing remain pending.

## Preserved state

- The previously user-validated Dev_v2.5.2 Curvature Sync workflow remains included.
- No public branch, Quickbar update destination, package identity, prior operator namespace, asset path, footer URL, or public release location changed.
