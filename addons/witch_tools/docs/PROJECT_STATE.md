# Witch Tools Project State

Last updated: 2026-07-21

## Identity

- Add-on: Witch Tools
- Canonical role: primary general-purpose N-panel toolkit
- Default target Blender version: 4.5
- Development package identity: `Witch_Tools_Dev`

## Current development build

- Version: `Dev_v2.5.0`
- Artifact: `Witch_Tools_Dev_v2_5_0_Curvature_Sync_MVP_Blender_4_5.zip`
- SHA-256: `258e39794b4a8eee93fb9729f121c4903b237f9123d8506a48884e306d748189`
- Package folder: `Witch_Tools_Dev`
- Declared Blender target: `4.5.0`
- Python source files: 44
- PNG assets: 6
- Shipped cache artifacts: none
- Static Python syntax audit: passed
- Runtime environment tested: Blender Python `5.2.0 LTS`
- Exact Blender 4.5 runtime: pending user test

This build was produced from the user-supplied Dev_v2.4.0 baseline without changing the package folder, operator namespaces, asset paths, or Witch Tools GitHub footer destination.

## Current implementation

Dev_v2.5.0 retains the modular Dev_v2.x N-panel architecture and adds Edit Tools > Curvature Sync MVP:

- explicit A/M/Z capture for selected open curve chains
- automatic selection clearing after each capture
- circular XY/XZ/YZ fitting
- exact middle-axis normalization
- equal segment counts per side of Middle
- multi-chain and multi-object synchronization
- missing-vertex injection
- optional cross-column face splitting
- copied-BMesh dry-run validation
- Vertex Lock / Protected Edit Zone integration and index remapping
- unresolved-column reporting

An existing Vertex Locks unregister failure caused by a missing safe RNA-property deletion helper was also repaired.

## Last completed work

- Inspected the Dev_v2.4.0 source and current Vertex Lock/protected-zone data model.
- Implemented and packaged Curvature Sync MVP as Dev_v2.5.0.
- Added add-on changelog, README workflow, quick-start guide, notes changelogs, and compatibility records.
- Ran static parsing and runtime tests against synthetic geometry and the supplied collar file.
- Confirmed the original uploaded collar file was not overwritten.

## Current known-working state

Under Blender Python 5.2.0 LTS:

- add-on registration/unregistration passed
- synthetic missing-vertex and missing-column repair passed
- strict invalid-selection cancellation passed without mutation
- locked anchor behavior and lock/index preservation passed
- actual two-object collar test completed and saved/reopened
- lower collar remained manifold
- no zero-length edges, duplicate edges, zero-area faces, invalid faces, or new 3D edge intersections were introduced
- matching upper/lower outer interface curves aligned within floating-point tolerance

## Active problems

1. Exact Blender 4.5 installation and UI test are pending.
2. Interactive undo/redo could not be validated in the background Python runtime.
3. The actual user selection workflow must be tested manually on the collar.
4. The upper collar already contains non-manifold/wire/intersection conditions that predate Curvature Sync.
5. The MVP reports but does not resolve every non-connectable column position.
6. Automatic chain discovery, automatic missing-Middle creation, and surplus-vertex dissolution are not implemented.
7. The full Dev_v2.5.0 source tree has not yet been imported into its final canonical repository source location.
8. UI and operator registries still need source-derived generation.

## Next exact implementation step

Install Dev_v2.5.0 in Blender 4.5 and test it on a backup copy of `Collar_Blender_DEV.blend` using explicit A/M/Z and curve-chain selections. Record:

- installation/registration
- Curvature Sync panel rendering
- Analyze output
- Apply output
- interactive undo/redo
- intended upper/lower interface alignment
- unresolved positions or selection failures

Patch only the required Curvature Sync or registration files in response to that test. After the urgent collar workflow is usable, import the full source into the canonical Witch Tools development tree and generate the UI/operator registries.

## Test status

- ZIP integrity and package layout: passed
- Python syntax: passed for all 44 source files
- Blender Python 5.2 registration/unregistration: passed
- synthetic topology repair: passed
- protected-anchor and locked-interior behavior: passed
- actual collar runtime test: passed with reported unresolved columns
- save/reopen: passed
- Blender 4.5 runtime: not performed
- interactive undo/redo: not verified
- public release/update behavior: not modified or tested

## Known remaining issues

Dev_v2.5.0 is an urgent MVP development build, not a public release. It must be tested on a backup in Blender 4.5 before production use or printing decisions.