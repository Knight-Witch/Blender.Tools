# Witch Tools Notes Changelog — Latest Update

## 2026-08-08 — Dev_v2.10.1 Runtime Fix Pass

- Recorded Blender 4.5 user-test results from Dev_v2.10.0: magnetic hover/snapping, Inject New Undo/Redo, Paver, Organic, and tested Organic vertex merge worked; multi-edge Edge injection, multi-contact Auto-Merge, Paver overlap reintegration, Magic Branch navigation/activation, Paver out-of-plane growth, and Object Snap Undo need correction.
- Inject New Edge Solo/Branch now accepts multiple selected edges.
- Auto-Merge now resolves all created-vertex overlaps at commit and subdivides existing target edges before welding interior contacts.
- Magic Branch now has explicit ON/OFF activation, selection-mode-sync branch buttons, corrected MMB modifier handling, and Paver out-of-plane growth for axis-constrained wall building.
- Object Snap now explicitly creates an undo-history boundary after a successful snap.
- Version bumped to `Dev_v2.10.1`, target Blender `4.5.0`. Static Python syntax validation passed; Blender runtime retest remains required.
