# Witch Tools Dev_v2.11.3 Compatibility Record

- Add-on: Witch Tools
- Version: Dev_v2.11.3
- Primary development/runtime target: Blender 5.0.1
- Secondary compatibility target: Blender 4.5.0
- Add-on minimum version in `bl_info`: Blender 4.5.0

## Runtime evidence inherited from prior candidates

Blender 5.0.1:
- Witch Tools 3D Print Tools rendered.
- Analyze Mesh executed; Dev_v2.11.1 detector parity failed on Non-flat/Thin/Sharp/Overhang and was corrected at source level in Dev_v2.11.2.
- User attempted Export STL after selecting a folder; no expected STL file/result appeared.

## Dev_v2.11.3 STL export correction

Source now validates Blender exporter completion and actual file creation, tries current and legacy Blender STL operator paths, and falls back to a direct binary STL writer using selected evaluated mesh geometry if Blender's operator paths fail or cancel.

The fallback is designed to include evaluated modifiers and object world transforms and to correct triangle winding for negative transforms.

## Runtime validation still required

Blender 5.0.1:
- one selected mesh STL export and re-import;
- multiple selected mesh export;
- modifier-evaluated geometry;
- transformed/negative-scale geometry;
- overwrite behavior and explicit failure reporting;
- Dev_v2.11.2 Analyze parity retest remains pending.

Blender 4.5:
- register/unregister and STL export compatibility smoke test;
- shared/BG3 workflow compatibility remains separately test-gated.

No Blender 5.0.1 or 4.5 export-success claim is made for Dev_v2.11.3 until those runtime tests pass.
