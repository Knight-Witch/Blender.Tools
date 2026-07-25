# Witch Tools UI Map

Last updated: 2026-07-24  
Current development build: `Dev_v2.7.1`

## Edit Tools

Current runtime ordering in `panel_edit_tools.py`:

1. Vertex Snap;
2. Object Snap;
3. Edge / Vertex Inject;
4. Curvature Sync;
5. **Align Selection**;
6. Selection Slots;
7. Vertex Locks / remaining Edit Tools controls.

## Align Selection

Header: **Align Selection**  
Header icon: `PIVOT_ACTIVE`

Controls:

- Median / Active Element source-reference dropdown
- Capture Source
- captured-source status
- X / Y / Z
- Match Coordinates / Translate-Preserve Shape
- Capture Target Anchor(s), shown in Translate mode
- Whole Selection / Per Connected Island, shown in Translate mode
- Apply
- Clear

The backend is implemented outside panel drawing. Quickbar uses the stable `mesh.wt_align_*` operator and scene-property contract rather than duplicating geometry logic.
