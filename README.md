[README.md](https://github.com/user-attachments/files/26504212/README.md)
# Witch Bones

**Witch Bones** is a Blender addon in development for transferring custom bone-driven armor parts from external game rigs into **Baldur’s Gate 3**, starting with **OVA cloak and jacket workflows**.

The immediate goal is to remove as much of the repetitive, error-prone rigging and weight-transfer work as possible while still keeping the user in control of every dangerous step.

This tool is being developed under the broader **Knight Witch Blender Tools** ecosystem.

> **Copyright / Usage Notice**  
> This project is proprietary and all rights are reserved. No copying, redistribution, modification, derivative distribution, commercial use, or reposting is permitted without prior written permission from Knight Witch.

## What It Is

Witch Bones is a staged transfer tool for cases where a source armor uses its own auxiliary bone chains, such as cloak bones, skirt bones, or similar secondary rig elements, and those need to be recreated cleanly on a BG3 armature.

The first version is focused specifically on:

- **OVA** source rigs
- **BG3** target rigs
- **cloak / jacket** custom bone transfer
- `B_Cloak_*`-style source bone chains

This is not intended to be a full universal rigging solution on day one. The first release is intentionally narrow so the core workflow can be made stable before the scope expands.

## What Problem It Solves

Porting armors with custom physics-style bone chains is usually messy for a few reasons:

- source rigs contain a lot of irrelevant bone noise
- different games use different naming conventions
- meshes are often weighted to more bones than expected
- custom bones need to be recreated with correct hierarchy and orientation
- weights need to transfer before final renaming
- some source support weights do not have a clean one-to-one match in BG3
- one bad step can easily damage a file or force manual recovery

Witch Bones is designed to turn that into a guided pipeline with safety checks, staging, and rollback tools.

## Planned Core Workflow

At a high level, the tool is being designed to do the following:

1. Select source armature, target armature, source mesh, and target mesh
2. Run preflight checks before anything destructive happens
3. Recommend and create a versioned backup copy of the project
4. Make hidden internal working backups of the source data
5. Filter out obvious junk bones from the source rig
6. Let the user narrow the working set with category presets like cloak or jacket
7. Detect which bones the source mesh is *actually* weighted to
8. Auto-include any required extra bones outside the preset if they are truly in use
9. Classify source influences into:
   - new custom bones to clone
   - direct BG3 matches
   - aliased BG3 matches
   - unresolved orphan groups
10. Create a helper clone rig and optional helper mesh for manual alignment
11. Commit new custom cloak bones into the BG3 armature
12. Prepare matching target vertex groups
13. Transfer weights safely
14. Stop and force orphan review if any unresolved groups still need decisions
15. Rename the new custom bones and matching vertex groups into BG3 naming
16. Apply BG3 cloth flags where relevant
17. Preserve restore points and cleanup options throughout the process

## Key Features

### Source Bone Filtering
The addon will strip known junk bones from a source working copy, then let the user review the remaining bone set with search, filtering, and category presets.

### Mesh-Driven Bone Detection
Preset categories are only a starting point. The tool will also inspect the selected source mesh and detect which bones are genuinely influencing it, so important weighted bones do not get left behind just because a preset missed them.

### Helper Clone Stage
Before new bones are committed into the BG3 armature, the addon will create a helper clone armature and optional mesh clone that can be repositioned as a unit. This gives the user a clean staging step before the real target rig is modified.

### Delayed Rename Workflow
Custom source bones will keep source-compatible names during transfer. Renaming into BG3 convention happens only after weights are safely on the target mesh.

### Orphan Detection and Resolution
If the source mesh is weighted to support bones that do not have a known BG3 equivalent, the tool will flag those groups as unresolved and block finalization until they are handled.

Planned orphan actions include:

- merge into an existing BG3 group
- replace a destination BG3 group
- park the orphan state for manual handling later

### Backup and Restore Safety
The addon is being built with several layers of recovery:

- versioned `.blend` backup copies
- automatic backup saves before destructive phases
- hidden internal source backups
- hidden orphan-state backups
- restore buttons for addon-managed orphan operations
- session pause / resume support

## Safety Philosophy

This tool is being designed around the assumption that rigging and weight operations are dangerous enough to deserve real safety systems.

The goal is not to automate blindly. The goal is to automate the repetitive work while keeping destructive choices visible, reviewable, and recoverable.

That means the workflow favors:

**detect → review → confirm → apply**

rather than silent automatic mutation.

## Current Scope

The initial release is focused on getting one workflow truly solid:

**OVA cloak/jacket custom-bone transfer into BG3**

That includes:

- source cleanup
- keep-set filtering
- weight-based detection
- helper staging
- custom bone commit
- target group prep
- weight transfer
- orphan blocking
- delayed rename
- BG3 cloth flagging
- backup / restore protections

## Planned Later Expansion

Once the cloak workflow is stable, the broader system is intended to expand into things like:

- additional OVA categories
- BDO source support
- skirt workflows
- hair workflows
- richer source-to-target alias libraries
- import/export of profile data
- community-reviewed source profiles
- expanded tooltip modes
- first-time-user onboarding

These are planned *after* the core cloak transfer pipeline is proven.

## Profile System

Witch Bones is being built around the idea of source rig profiles. A profile tells the addon how to interpret a source game rig, including things like:

- rig detection fingerprints
- known junk-bone rules
- default category groups
- clone rules
- rename rules
- alias mappings
- notes about unresolved support chains

The first bundled source profile target is **OVA**.

Later support is expected to use structured profile data rather than hardcoded one-off logic.

## UI / UX Direction

The intended UI approach is compact and utility-focused:

- collapsible panels
- low clutter
- sensible icon use
- clean status summaries
- lite tooltips first

A later addon preference will likely allow switching between **lite tooltips** and **expansive tooltips**, where the expansive mode gives more detailed explanations of buttons and process stages.

A simple first-time-user onboarding/tutorial flow may also be added later.

## Development Status

Witch Bones is currently in the planning/specification stage.

The development order is roughly:

1. foundation and session architecture
2. OVA profile + source prep
3. detection and classification
4. helper clone stage
5. commit + target group prep
6. transfer + rename
7. orphan resolution safeguards
8. BG3 finalization and cleanup

## Repository Structure

This tool lives under the broader Knight Witch Blender tools repository:

- **Repo umbrella:** `Knight-Witch/Blender.Tools`
- **Current tool path:** `Witch_Bones_Armature_Transfer`

## Documentation

The internal master planning document for this tool is being kept separately as the development roster / implementation spec.

Recommended repo docs structure:

- `README.md` — public-facing overview
- `docs/WITCH_BONES_MASTER_SPEC.md` — full internal development roster
- later:
  - `docs/WITCH_BONES_IMPLEMENTATION_SPEC.md`
  - `docs/WITCH_BONES_PROFILE_SCHEMA.md`

## Intended Audience

This tool is primarily being built for modders and armor porters working in Blender who need to move custom rigged pieces from one game skeleton to another without doing every stage manually.

The first real target audience is people doing **OVA → BG3** custom cloak/jacket transfers.

## Notes

This README describes the planned public-facing behavior and development direction of the tool. It is not yet a finished user manual.

Once the addon is functional, a proper usage guide and step-by-step directions will be added.
