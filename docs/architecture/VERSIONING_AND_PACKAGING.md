# Versioning and Packaging

## Component versions

Each independently distributed add-on has its own version:

- Witch Tools
- Witch Quickbar
- Witch Core

Experimental modules may use independent `Dev_v###` versions. Once integrated, the owning add-on version becomes authoritative.

## Public and development correlation

Record how a public release maps to its internal build.

Example:

```text
Public v1.0.2
Internal source build: Dev_v1.2.8
Source branch: Witch_Quick_Access
Source commit: <sha>
```

Do not infer this relationship from version numbers alone.

## Artifact names

Use explicit component, version, and Blender target names:

```text
Witch_Tools_Dev_v2.1.0_Blender_4.5.zip
Witch_Quickbar_v1.0.2_Blender_4.5.zip
Witch_Core_Dev_v0.3.0_Blender_4.5.zip
```

Never use ambiguous names such as `latest.zip`, `fixed.zip`, or `new.zip` as the only delivered artifact.

## Build registry

Every generated artifact must update `docs/project_state/BUILD_REGISTRY.md` with:

- component
- version
- source branch and commit
- artifact filename
- package/add-on folder
- target Blender version
- additional tested versions
- archive hash
- included modules
- test status
- known limitations
- superseded build

## Package identity

The following are compatibility surfaces:

- top-level add-on package folder
- `bl_info` name and version
- add-on preference `bl_idname`
- operator IDs
- keymap IDs
- persisted preference/property names

Do not change them during repository reorganization without a migration plan and installed-upgrade test.

## Packaging exclusions

Exclude:

- `__pycache__`
- `.pyc` and `.pyo`
- temporary files
- editor/project files
- local test outputs
- source reference assets not required at runtime
- unrelated documentation and archives
- secrets or personal paths

## Shared code

The source repository may maintain one canonical shared module tree. Independently installable release packages may vendor the required subset during build. Vendored files must be generated, not manually edited as a second source.

## Release checklist minimum

- version metadata updated
- changelog updated
- documentation state updated
- Blender target recorded
- package folder verified
- clean install tested
- upgrade from prior public version tested where applicable
- unregister/re-register tested
- update button and URLs tested
- archive contents inspected
- archive hash recorded
- no cache/temp files

## Public URL preservation

Before changing any release or branch path, verify all in-code and external links. Prefer stable release URLs or compatibility manifests in future releases, but do not retroactively break installed public builds.