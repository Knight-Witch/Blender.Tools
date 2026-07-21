# Witch Quickbar Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v1.4.0 — Blender 4.5 Select-tab validation

- The user installed Quickbar Dev_v1.4.0 and reported that the Selection Slots implementation worked perfectly in the tested workflow.
- This confirms the primary Select-tab rendering and Witch Tools operator-invocation path in the user's Blender 4.5 environment.
- Quickbar Dev_v1.4.0 remains compatible with Witch Tools Dev_v2.6.1 because the N-panel hotfix preserves the `mesh.wt_selection_slot_*` operator contract.
- No Quickbar rebuild is required for the Witch Tools N-panel-only patch.

## Remaining validation

- full pass-through, canceled drag, resize, lock, minimize/maximize, file-load recovery, unregister/re-register, undo/redo, and backend-unavailable tests remain pending;
- public/dev side-by-side install and update-button launch remain pending.

## Public compatibility

No public branch, `Witch_Quick_Access` update destination, package identity, existing operator namespace, inherited asset path, or public release location changed.