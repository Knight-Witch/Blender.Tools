# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Update: Selection Slots development builds

- Implemented Witch Tools `Dev_v2.6.0` with persistent **Selection Slots** below Curvature Sync.
- Added vertex, edge, face, combined-domain, and multi-object Edit Mode save/reselect support using scene slot records and per-mesh custom element markers.
- Added rename, save/overwrite, reselect, clear, Clear All, add, remove, and reorder controls plus a stable `mesh.wt_selection_slot_*` operator family.
- Implemented Witch Quickbar `Dev_v1.4.0` with a populated **Select** tab that invokes the canonical Witch Tools operators.
- Added responsive Quickbar slot names, full-name tooltips, rename dialog, all slot actions, grip drag reorder, and a safe missing-backend state.
- Converted the five supplied LONGDISPLAY, FILE_TICK, TRASH, REMOVE, and ADD SVGs into packaged transparent PNG icons.
- Produced:
  - `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`, SHA-256 `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`;
  - `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`, SHA-256 `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`.
- Added the complete Selection Slots feature packet and updated add-on state/roadmap/notes, Quickbar overlay/input/asset/integration contracts, build registry, compatibility registry, documentation index, and umbrella project state.

## Testing

- Both ZIPs passed integrity, safe-path, Python syntax/compile, duplicate operator-ID, and cache/package-hygiene checks.
- Quickbar asset resolution and synthetic multi-slot layout construction passed.
- Blender 4.5 Selection Slots and Quickbar Select-tab runtime testing remain pending.
- The previously user-validated Dev_v2.5.2 production Curvature Sync workflow remains included in Dev_v2.6.0.

## Public compatibility

No public branch, Quickbar update destination, package identity, existing operator namespace, inherited asset path, external release link, or public download location changed.
