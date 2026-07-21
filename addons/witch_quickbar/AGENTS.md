# Witch Quickbar Local Agent Instructions

All root `PROJECT_RULES.md` and `AGENTS.md` requirements apply.

## Architecture boundary

Witch Quickbar is a separately distributed floating-overlay add-on. It is not an N-panel implementation.

Before changing Quickbar, read:

- `docs/PROJECT_STATE.md`
- `docs/OVERLAY_ARCHITECTURE.md`
- `docs/INPUT_EVENT_CONTRACT.md`
- `docs/ASSET_MANIFEST.md`
- `docs/INTEGRATION_WITH_WITCH_TOOLS.md`
- latest notes changelog
- current source and version metadata

## Systems that must be preserved

- custom overlay drawing
- gizmo hit targets and event routing
- drag, resize, lock, reorder, minimize, maximize, close, and launcher behavior
- pass-through outside active controls
- persistent preferences and display state
- asset paths and fallbacks
- file-load recovery
- UI-only versus undoable scene-operation separation

## Public compatibility

The public `Witch_Quick_Access` branch and installed update behavior are compatibility surfaces. Do not move files, rename the branch/package, alter update URLs, or change package identity until the audit and installed-update tests are complete.

## Integration rule

Quickbar may expose Witch Tools features through thin wrappers or operator calls. It must not contain duplicate canonical implementations of Curvature Sync, Vertex Inject, or other complex Witch Tools systems.

## Testing

Any Quickbar update must test:

- open/close and auto-start
- all display states
- dragging and resizing
- lock and section reorder
- event pass-through
- undo/redo for scene-changing controls
- no undo pollution from UI-only controls
- file-load recovery
- unregister/re-register
- hotkey assignment and persistence
- update/check link

Default target: Blender 4.5 unless explicitly changed.