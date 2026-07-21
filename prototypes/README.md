# Prototypes and Witch Dev Modules

## Purpose

This directory is for isolated experimental implementations that are not yet stable enough for their owning add-on.

## Rules

- A prototype must identify its owning add-on and feature packet.
- It may use an independent `Dev_v###` version.
- It must not be represented as public release scope.
- It must follow the owning add-on's operator and safety contracts.
- It must not create a throwaway architecture that requires a full rewrite to integrate.
- It must include a state file and test plan.
- Once integrated, the owning add-on version becomes authoritative.

## Planned initial prototype

```text
prototypes/curvature_sync/
```

This directory must not be created with implementation code until the current Witch Tools baseline and Vertex Lock architecture are imported and audited.