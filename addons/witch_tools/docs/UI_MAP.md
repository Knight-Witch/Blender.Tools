# Witch Tools UI Map

Last updated: 2026-08-05  
Current development candidate: `Dev_v2.8.0`

## Edit Tools

Current runtime ordering in `panel_edit_tools.py`:

1. Vertex Snap
2. Object Snap
3. Edge / Vertex Inject
4. Curvature Sync
5. **Align Vertices / Edges / Faces**
6. Selection Slots
7. Vertex Locks / remaining Edit Tools controls

## Align Vertices / Edges / Faces

Header icon: `PIVOT_ACTIVE`

The section is intentionally organized as four numbered steps rather than a flat control list.

### 1. Capture Parent Anchor

- Anchor Reference: `Active Element` or `Median`
- `Capture Selected Anchor`
- captured anchor count/status

A selected edge or face is stored through its participating vertices. Active Element uses the active vertex, edge endpoints, or face vertices marked during capture. Median uses all captured parent vertices.

### 2. Choose Alignment Target

- Frame:
  - `World XYZ`
  - `Custom Guide`
- Match coordinate toggles: X, Y, Z
- Custom Guide controls, when enabled:
  - editable `Guide Start`
  - `Capture Start`
  - `Copy Anchor`
  - editable `Guide End`
  - `Capture End from Selection`
  - target mode:
    - `Match Anchor in Guide Frame`
    - `Project to Guide Line`

World XYZ uses Blender world coordinates. In a Custom Guide frame, custom X follows the guide direction and custom Y/Z are perpendicular frame axes. Project to Guide Line constrains custom Y/Z to zero while preserving distance along custom X.

### 3. Choose How Targets May Move

- Move Along:
  - `Free Coordinates`
  - `Captured Rails`
- Relationship:
  - `One Anchor to All`
  - `Paired by Rail`
- `Capture Selected Slide Rails`, when rails are enabled
- `Stay Within Captured Rail`
- `Preserve Relative Spacing / Shape`
- Grouping:
  - `Whole Selection`
  - `Per Selected Island`
- `Respect Vertex Locks`

Captured rails are explicit existing mesh edges. They are movement constraints, not Protected Edit Zones and not topology locks. The Dev_v2.8.0 candidate accepts straight rail components only.

Paired by Rail maps each subordinate island to its own parent through a disconnected captured rail component containing exactly one captured parent vertex. The backend does not guess pairings by nearest distance or vertex index.

### 4. Select Subordinates and Apply

- `Analyze`
- `Align`
- persistent result/status line
- `Clear All Captures`

Analyze performs the same preflight and coordinate planning as Apply without moving geometry. Align mutates coordinates only after every participating target passes preflight.

## Persistent contract

Operators:

- `mesh.wt_guided_align_capture_anchor`
- `mesh.wt_guided_align_capture_rails`
- `mesh.wt_guided_align_capture_guide_point`
- `mesh.wt_guided_align_copy_anchor_to_guide_start`
- `mesh.wt_guided_align_clear`
- `mesh.wt_guided_align_analyze`
- `mesh.wt_guided_align_apply`

Marker layers:

- vertex parent marker: `wt_align_selection_source`
- edge rail marker: `wt_align_selection_rail`

Witch Dock/Quickbar integration is not present in Dev_v2.8.0. Any later compact UI must call this Witch Tools contract rather than duplicating geometry logic.
