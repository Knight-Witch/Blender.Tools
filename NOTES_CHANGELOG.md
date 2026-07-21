# Blender.Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Update: Witch Tools Dev_v2.5.1 Auto-Aligned Vertex Inject

- Added Edit Tools > Edge / Vertex Inject to the existing Curvature Sync MVP build.
- Added ordered A/B/C selection, A-B and B-C edge validation, ideal D calculation, target-chain inference, strict fork rejection, projected target-edge splitting, existing-vertex reuse, and default C-D shared-face splitting.
- Added copied-BMesh preflight, shape-key rejection, zero-area-face checks, and Vertex Lock / Protected Edit Zone / Curvature Sync anchor remapping.
- Added projection and existing-vertex tolerance controls.
- Packaged `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip` with SHA-256 `fe8972980c9f3c6ec29653db44695133107d7124d8efcfc8cce77448daa253d3`.
- Added package quick-start, changelog, compatibility, state, roadmap, and build-registry updates.
- Confirmed full package syntax, registration/unregistration, synthetic vertex injection, synthetic face splitting, and Curvature Sync regression under Blender Python 5.2.0 LTS.

## Public compatibility

No public branch, Quickbar update destination, package identity, existing operator namespace, external release link, or asset path was changed.

## Testing limitation

Exact Blender 4.5 panel rendering, real collar A/B/C selection, and interactive undo/redo remain pending user validation.
