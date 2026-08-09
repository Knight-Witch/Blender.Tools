# Magic Branch Quick Start — Dev_v2.10.1

Target: Blender 4.5

Magic Branch is the persistent click-drag mesh builder in **Witch Tools > Edit Tools**.

## Setup

1. Turn **Magic Branch ON**. This ON/OFF action is separately hotkeyable.
2. Choose **Single Branch** by leaving Persistent off, or turn **Persistent** on to remain armed after every successful branch.
3. Choose Vertex, Edge, or Face. Choosing a type also switches Blender to the matching mesh selection mode.
4. Enable at least one X/Y/Z movement axis. All three are enabled by default for free placement.
5. Turn Magnetic Snap on/off.
6. Turn Auto-Merge on if supported overlapping contacts should weld into existing topology.
7. For Face, choose Paver or Organic.

## Viewport workflow

- Click-drag a source element matching the chosen type.
- Move the mouse to place the live branch.
- Hover a vertex, edge, or face to magnetically target it.
- Release left mouse to commit.
- Plain MMB during a live drag pauses geometry placement and orbits around the current live branch. Shift/Ctrl/Alt+MMB use normal Blender navigation without resetting the branch pivot. Release MMB to resume.
- Esc/right-click exits. If a live uncommitted branch exists, it is cancelled first.

## Vertex

Click-drag a source vertex. A new vertex appears with an edge back to the source.

With Magnetic Snap + Auto-Merge, every supported overlapping created endpoint is reintegrated on commit. Existing vertices weld directly; a contact inside an existing edge subdivides that edge and welds into the inserted split vertex.

## Edge

Click-drag a source edge. A copied edge appears with source-to-copy connections at both endpoints.

Vertex or edge magnetic targets align the nearest compatible copied endpoint while preserving the live copied edge rigidly. Face magnetic targets solve the endpoints independently along their travel lines.

## Face — Organic

Click-drag a source face. The face boundary nearest the drag direction becomes the emitting edge. One connected face grows from that edge; its outer edge follows the mouse and magnetic target.

Use Organic when the destination is arbitrary and you want one face to reach it.

## Face — Paver

Click-drag a source face. The emitting edge is chosen from drag direction. Paver creates repeated source-sized tiles and adds/removes them as drag distance changes.

Paver preserves equal tile size. It does not stretch its final tile just to force an off-grid endpoint. If the source-plane direction is disabled by the movement mask, the mouse-selected enabled axis becomes the growth direction while source tile depth is preserved; for example, Z-only can grow a vertical wall from a horizontal face.

## Hotkeys

`mesh.wt_magic_branch_toggle_active` toggles Magic Branch ON/OFF. `mesh.wt_magic_branch_toggle_persistent` toggles whether it stays armed after a commit. Either can be assigned through Blender keymaps.

## Current candidate limits

- active mesh only;
- arbitrary face-interior Auto-Merge retopology is not generated;
- Paver preserves equal-size tiles;
- per-branch Undo while Persistent is active must be validated in Blender 4.5;
- magnetic GPU highlight, MMB pivot feel, topology data preservation and cancel/Undo behavior still require runtime testing.
