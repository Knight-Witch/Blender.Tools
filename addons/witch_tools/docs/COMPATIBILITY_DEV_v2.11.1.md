# Witch Tools Dev_v2.11.1 Compatibility Record

- Add-on: Witch Tools
- Version: Dev_v2.11.1
- Intended Blender target: Blender 4.5.0
- Additional Blender versions tested for this candidate: none yet
- User reference UI environment: Blender 5.0.1; reference screenshots only, not a Witch Tools runtime compatibility test
- Static/package validation: passed in GitHub Actions; Python AST parse, duplicate `bl_idname` scan, version/panel-order contracts, Advanced Clean section-routing contracts, package hygiene, ZIP integrity, and SHA-256 verification passed
- Full installable artifact: `Witch_Tools_Dev_v2_11_1_3D_Print_Transform_Blender_4_5.zip`
- Artifact SHA-256: `d6ecf1b893c1d619fc5974ec0ca1836fe7333abd4b9c5724ff497b63859c2441`
- Blender runtime validation: pending
- Known compatibility limitations: Advanced Clean custom section headers and per-section execution are untested in Blender; Transform, Analyze Mesh, repair/cleanup and STL export runtime paths remain pending; no Blender 5.0.1 compatibility claim is made
