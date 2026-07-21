# Blender.Tools Project State

Last updated: 2026-07-21

## Current baseline

- Repository: `Knight-Witch/Blender.Tools`
- Development integration branch: `Blender_Dev`
- Branch origin: `Witch_Quick_Access`
- Default repository branch: `Witch_Main_Tools`
- Default Witch Tools target Blender version: `4.5`

## Current development builds

### Witch Tools

- Current build: `Dev_v2.6.0`
- Artifact: `Witch_Tools_Dev_v2_6_0_Selection_Slots_Blender_4_5.zip`
- Package: `Witch_Tools_Dev`
- SHA-256: `b4aa8d587f1fe1ed3e39161b1cd680bcd49130ab345693cc1a62a2380d9cc547`
- Based on supplied baseline: `Dev_v2.4.0`
- Supersedes: `Dev_v2.5.2`
- Target: Blender `4.5.0`
- Selection Slots runtime: pending
- Retained Curvature Sync production workflow: user-reported passed in Blender 4.5 under Dev_v2.5.2

### Witch Quickbar

- Current build: `Dev_v1.4.0`
- Artifact: `witch_quickbar_dev_Dev_v1_4_0_Select_Tab_Blender_4_5.zip`
- Package: `witch_quickbar_dev`
- SHA-256: `be2453f4ea2425e94b4da9c764c04b2efbf61d21d3401e75f74e61ab451866ea`
- Supersedes: `Dev_v1.3.18`
- Target: Blender `4.5.0`
- Update destination: `Witch_Quick_Access` public branch
- Runtime test: pending

### Witch's Dev Modules

- Version: `Dev_v0.0.9`
- Artifact: `witch_dev_modules.zip`
- Package: `witch_dev_modules`
- SHA-256: `e5306886a1e5edd1bb57fcf106f9a4ca51503060e0ecb5b4a0ed8a1bcead28f6`
- Packaging defect: original archive contains 34 `.pyc` files
- Runtime test: pending

## Last completed work

- Established repository rules, architecture, documentation tracking, and non-breaking branch safeguards on `Blender_Dev`.
- Audited supplied Witch Tools, Quickbar, and Dev Modules baselines.
- Implemented and user-validated the primary Curvature Sync production collar workflow through Dev_v2.5.2.
- Implemented Witch Tools Dev_v2.6.0 **Selection Slots**:
  - persistent vertex/edge/face/mixed selection slots;
  - multi-object Edit Mode;
  - save/reselect/overwrite/clear/Clear All/add/remove/rename/reorder;
  - scene records plus mesh custom-data markers;
  - N-panel UI below Curvature Sync;
  - stable operator contract.
- Implemented Quickbar Dev_v1.4.0:
  - populated Select tab;
  - thin optional invocation of Witch Tools Selection Slots;
  - responsive names, tooltips, rename, actions, and grip reorder;
  - five supplied icons converted to packaged PNGs;
  - safe unavailable-backend state.
- Produced and statically audited both versioned ZIPs.
- Created the Selection Slots feature packet and updated Witch Tools, Quickbar, build, compatibility, asset, integration, and state documentation.
- Preserved all public branches, update URLs, package identities, existing operator namespaces, inherited asset paths, and external release locations.

## Current known-working state

Witch Tools Dev_v2.6.0 static validation:

- 46 Python files parse/compile;
- no duplicate operator IDs;
- ZIP integrity/safe paths/package hygiene passed;
- package identity and footer URL preserved.

Quickbar Dev_v1.4.0 static validation:

- 13 Python files parse/compile;
- 36 packaged PNG assets and all icon mappings verified;
- no duplicate operator IDs;
- synthetic multi-slot layout construction passed;
- package identity and public update URL preserved.

Previously user-validated runtime state:

- Witch Tools Dev_v2.5.2 installed in Blender 4.5;
- saved Curvature Sync anchors/chains loaded;
- Analyze/Apply completed on the production collar;
- user reported the curvature and corrected column topology worked beautifully.

No Blender runtime claim is made yet for the new Selection Slots or Quickbar Select tab.

## Active problems

1. Witch Tools Dev_v2.6.0 Selection Slots require Blender 4.5 registration, UI, selection-domain, multi-object, save/reopen, topology-change, and undo/redo tests.
2. Quickbar Dev_v1.4.0 requires Blender 4.5 overlay, dependency, drag/reorder, resize, tooltip, pass-through, file-load recovery, and undo tests.
3. Public/dev side-by-side installation and update-button launch remain untested.
4. Selection markers are persistent custom element data rather than immutable topology IDs; delete/split/duplicate behavior must be recorded.
5. Final collar normals/manifold/print-fit inspection remains pending independently of Selection Slots.
6. Full canonical source imports and source-derived UI/operator/asset registries remain pending.
7. Public Witch Tools distribution/update strategy remains unresolved.
8. Witch Core source import remains pending.

## Next exact implementation step

1. Install Witch Tools Dev_v2.6.0 in Blender 4.5 and test Selection Slots thoroughly.
2. Install Quickbar Dev_v1.4.0 after Witch Tools and test the Select tab plus the full overlay regression matrix.
3. Test Quickbar with Witch Tools disabled.
4. Patch only failures found in these runtime tests.
5. Complete final collar inspection before slicing.
6. Import both successful development source trees canonically and generate registries/manifests.

## Test status

- Dev_v2.5.2 Blender 4.5 production Curvature Sync: user-reported passed
- Dev_v2.6.0 static ZIP/package checks: passed
- Dev_v1.4.0 static ZIP/package/asset/layout checks: passed
- Selection Slots Blender 4.5 runtime: not performed
- Quickbar Select tab Blender 4.5 runtime: not performed
- Interactive undo/redo for new features: not verified
- Save/reopen for Selection Slots: not performed
- Public branches modified: no
- Public Quickbar update URL modified: no

## Known remaining issues

Dev_v2.6.0 and Quickbar Dev_v1.4.0 are development builds, not public releases. Their new Selection Slots workflow is statically validated but requires installed Blender 4.5 testing before release or reliance on long-term saved selections.
