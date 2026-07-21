# Witch Tools Notes Changelog — Latest Update

Date: 2026-07-21

## Dev_v2.5.1 — Auto-Aligned Vertex Inject

- Added Edit Tools > Edge / Vertex Inject to the Curvature Sync MVP build.
- Added ordered A/B/C selection, ideal D calculation, target-chain inference, strict fork rejection, projected edge splitting, existing-vertex reuse, and default C-D shared-face splitting.
- Added copied-BMesh preflight, shape-key rejection, zero-area-face validation, and lock/edit-zone/anchor remapping.
- Added projection and existing-vertex tolerances plus `VERTEX_INJECT_QUICK_START.md`.
- Packaged `Witch_Tools_Dev_v2_5_1_Vertex_Inject_Curvature_Sync_Blender_4_5.zip`.

## Testing

- Complete package syntax audit: passed for 45 Python files.
- Registration/unregistration in Blender Python 5.2.0 LTS: passed.
- Synthetic vertex injection and C-D face split: passed.
- Curvature Sync synthetic regression: passed.
- Exact Blender 4.5 UI, real collar injection, and interactive undo/redo: pending user test.
