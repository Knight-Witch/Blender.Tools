# Shared Blender Infrastructure

## Purpose

This directory is the planned canonical source for reusable backend modules that may be consumed by more than one add-on.

Potential areas:

- geometry calculations
- topology traversal and safe BMesh operations
- protected-zone queries
- selection utilities
- logging/reporting
- Blender compatibility helpers
- build-time vendoring support

## Rules

- Shared modules must not import Quickbar overlay or add-on-specific panel UI.
- A shared module must have a clear owner and public/internal API contract.
- Add-ons should not manually fork shared source.
- Independently distributable packages may receive generated vendored copies during build.
- Vendoring is not yet implemented; do not move runtime code here until package/import behavior is designed and tested.

## Current state

Documentation placeholder only. No current public source was moved.