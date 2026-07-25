# Witch Tools UI Map

Last updated: 2026-07-24  
Current development build: `Dev_v2.7.0`

## Edit Tools

Relevant current ordering:

1. existing transform/object-edit controls;
2. Object Snap;
3. **Align Selection**;
4. Vertex Inject;
5. Curvature Sync;
6. Selection Slots;
7. remaining Edit Tools sections.

## Align Selection

Header: **Align Selection**

Controls:

- Capture Source
- Capture Target Anchor
- Clear
- Match Coordinates / Move Shape
- X / Y / Z
- Whole Selection / Per Selected Island
- Respect Vertex Locks
- Apply Align Selection

The backend is implemented outside panel drawing. Quickbar uses the stable `mesh.wt_align_*` operator and scene-property contract rather than duplicating geometry logic.
