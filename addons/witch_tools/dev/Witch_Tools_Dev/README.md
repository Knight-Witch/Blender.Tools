# Witch Tools

**Witch Tools Dev_v2.8.0** is the current Blender add-on development build for Knight Witch workflow tools.

Target build context: **Blender 4.5**

## Dev_v2.8.0 — Align Vertices / Edges / Faces

Edit Tools now includes a guided parent/subordinate alignment workflow. It can match selected world or custom-frame coordinates, preserve the selected shape as a rigid group, slide targets along explicitly captured straight edge rails, and map multiple parent/subordinate pairs through separate rail components. A Custom Guide can be entered numerically or captured from selected geometry for arbitrary-angle alignment.

See `ALIGN_SELECTION_QUICK_START.md` for the exact workflow and current safety limits.

## Dev_v2.6.1 — Selection Slots N-panel hotfix

The Selection Slots backend and workflow remain the same as Dev_v2.6.0. This hotfix restores the expandable N-panel slot rows, makes the title itself clickable, and safely initializes Slot 1 outside the panel draw path.

## Dev_v2.6.0 — Selection Slots

Edit Tools now includes **Selection Slots** immediately below Curvature Sync. Slots can save and restore vertex, edge, face, or combined mesh selections across one or several objects in multi-object Edit Mode.

- Starts with one renameable slot.
- Adds up to 20 slots with the final-row `+` button.
- Saves/overwrites, reselects, clears, deletes, and reorders slots.
- Includes a section-level **Clear All** action.
- Name fields expand with the N-panel width.
- Stores selection data in the `.blend` using persistent mesh-element layers and scene slot records.
- Quickbar Dev_v1.4.0 exposes the same canonical slots through its optional **Select** tab.

See `SELECTION_SLOTS_QUICK_START.md`.

## Dev_v2.5.2 — Curvature Sync correspondence repair

See `CURVATURE_SYNC_QUICK_START.md` for the collar-focused selection and execution workflow.

Edit Tools now includes **Curvature Sync**, a constrained circular topology-repair workflow for selected open edge chains. It is designed for aligned parallel curves on one object, multiple mesh islands, or multiple objects such as matching upper and lower 3D-print parts.

### Core workflow

1. Enter multi-object Edit Mode on every participating mesh.
2. Select one A/start vertex on each intended curve and press **Capture A**. The captured selection is cleared automatically.
3. Select one Middle/apex vertex on each curve and press **Middle**.
4. Select one Z/end vertex on each curve and press **Capture Z**.
5. Select only the open A-to-Z curve edges for all participating parallel chains.
6. Press **Analyze**. Resolve any reported selection or topology error.
7. Press **Apply Curvature Sync**.

### Current behavior

- Fits a circular arc through each chain's captured A/M/Z references.
- Keeps A and Z fixed so straight extensions outside the repair span are not moved.
- By default, normalizes Middle to the exact mathematical centerline of the fitted circle.
- Enforces the same number of segments from A to Middle and Middle to Z across all selected chains and objects.
- Injects missing vertices by splitting selected chain edges.
- Creates missing cross-column edges when corresponding vertices share a face.
- With **Replace Misaligned Column Edges** enabled, dissolves safe interior cross-edges that connect different canonical slots and rebuilds the correct same-slot columns instead of leaving diagonal topology behind.
- Preserves and remaps Vertex Lock, Protected Edit Zone, and captured-anchor references through topology changes.
- Performs a copied-BMesh dry run before changing the real edit meshes.
- Reports unresolved column positions rather than forcing unsafe connections.

### MVP limitations

- Circular planar arcs only: XY, XZ, or YZ.
- Every selected component must be one open, non-branching A-to-Z chain.
- One captured A, Middle, and Z reference is required per selected chain.
- The tool replaces only unambiguous two-face interior column edges. It does not automatically dissolve surplus chain vertices or unsafe boundary/special-data edges.
- Shape-key meshes may be curvature-adjusted only when no vertex injection is required.
- Missing column edges are created only where Blender can safely connect the corresponding vertices through a shared face.
- Misaligned edges carrying Seam, Sharp, Crease, bevel, custom edge data, mixed materials, or mixed smoothing abort before mutation.


## Dev_v2.4.0

Edit Tools now includes a dedicated **Object Snap** section using Blender's `AREA_JOIN_DOWN` icon.

Object Snap supports:
- Vertex anchors: translate the full target object or disconnected mesh island so the target vertex meets the source vertex.
- Edge anchors: translate edge midpoint to edge midpoint, with optional orientation matching.
- Face anchors: translate face center to face center, with optional orientation matching.
- Opposing normals by default, with a compact same-direction toggle.
- Automatic scope detection between whole-object snapping and disconnected-island snapping.

For separate-object snaps, the active edit-mode mesh is the target. For same-object snaps, the most recently selected active anchor defines the target island.

Current default module order:
- Mode Switcher
- Auto Mirror
- Edit Tools
- Quick Modifiers
- Head Tools
- Body Tools
- Armour Tools
- Hair Tools
- Weight Tools
- Armature Tools
- Shape Key Tools
- Export Tools
- Troubleshooting Tools
- Dev footer

First-install behavior:
- Mode Switcher starts expanded.
- Dev footer starts expanded.
- All workflow panels start collapsed.

## Edge / Vertex Inject

Dev_v2.5.2 retains **Edit Tools > Edge / Vertex Inject** from Dev_v2.5.1. Select A, then B, then C individually; the operator projects the missing D relation onto the inferred parallel target chain, splits the target edge, and optionally connects C-D through the shared face. See `VERTEX_INJECT_QUICK_START.md`.
