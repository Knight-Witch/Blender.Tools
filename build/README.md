# Blender.Tools Build System

## Current state

No canonical automated build system is implemented yet.

## Required future behavior

The build system must:

- package Witch Tools, Witch Quickbar, and Witch Core independently
- preserve each top-level add-on package identity
- vendor generated shared modules where required
- exclude caches, temporary files, test fixtures, and unrelated assets
- produce explicit versioned filenames
- generate a build manifest
- calculate archive hashes
- verify required assets and files
- optionally produce compatibility outputs for legacy public paths

## Build manifest minimum

- component
- version
- source branch and commit
- target Blender version
- additional tested versions
- package folder
- included shared modules
- artifact filename and hash
- build date
- test status

## Public compatibility

Do not use the build system to relocate existing update targets until installed public-build tests pass. Legacy compatibility outputs may be necessary.

## Generated code

Vendored/shared generated files must include a notice that they are generated and identify the canonical source path. Do not edit them manually.