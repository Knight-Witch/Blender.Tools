# Witch Tools Roadmap

Statuses: `planned`, `active`, `blocked`, `deferred`, `research`, `rejected`, `complete`.

## Current development candidate — Dev_v2.10.0

Target Blender: `4.5.0`  
Branch: `feature/witch-tools-magic-branch`  
Runtime validation: pending

### WT-PREC-001 — Coordinate Copy

- Status: active candidate; retained from Dev_v2.9.0.
- Global/Local; XYZ; Location/Rotation/Scale; vertex/edge/face capture; independent targets; multi-object conversion; protection preflight; Ctrl+Shift+C Apply.
- Remaining: Blender 4.5 acceptance, especially edge/face frames and transformed objects.

### WT-PREC-002 — Planar Edit

- Status: active candidate; retained from Dev_v2.9.0.
- Plane Lock persistent object-local axis constraints.
- Level exact per-target world coordinate assignment.
- Remaining: real transform guard, persistence, multi-object, Undo/Redo.

### WT-VINJ-002 — Inject New magnetic expansion

- Status: active candidate in Dev_v2.10.0.
- Solo / Branch / multi-edge Slide.
- independent X/Y/Z masks plus retained straight Rail.
- vertex/edge/face Magnetic Snap with target highlight.
- per-endpoint face travel-line solve.
- Branch Auto-Merge for compatible vertex/edge contacts.
- MMB pass-through orbit around live injection.
- Remaining: Blender 4.5 modal, GPU, merge, cancellation, Undo/Redo, normals/winding/material/attribute tests.

### WT-MBR-001 — Magic Branch

- Status: active candidate in Dev_v2.10.0.
- Feature packet: `/docs/features/magic_branch/`.
- Single Branch / Persistent.
- Vertex / Edge / Face.
- XYZ movement, Magnetic Snap, Auto-Merge, MMB orbit.
- Face Paver / Organic.
- Remaining: full Blender 4.5 test plan, especially Persistent Undo and Paver rebuild/cancel behavior.

### WT-EDOC-001 — Edge Doctor regrouping

- Status: active candidate.
- Parent section contains Missing Vertex / Edge Injector, Alignment Fixer, Curvature Sync.
- Missing Injector retains the existing A/B/C solver and adds two-edge L repair.
- A/B/C viewport letter overlay: deferred QoL.

### WT-UI-001 — Reorderable Edit Tools

- Status: active candidate.
- Preference-backed custom top-level order.
- Compact drag-grip reorder mode plus up/down fallback and default reset.
- Remaining: validate N-panel drag modal and restart persistence.

### WT-PREC-003 — Blender 4.5 production validation

- Status: planned immediate.
- Execute `/docs/features/precision_edit/TEST_PLAN.md` and `/docs/features/magic_branch/TEST_PLAN.md` before integration or Quickbar work.

## Guided Align / Alignment Fixer

### WT-ALIGN-001

- Status: active candidate retained from Dev_v2.8.0 and nested under Edge Doctor as Alignment Fixer.
- Existing canonical `mesh.wt_guided_align_*` backend remains unchanged.
- Inherited documentation conflict remains: older roadmap references missing `/docs/features/align_selection/`; do not fabricate historical contents.

### WT-ALIGN-003 — Witch Dock / Quickbar thin wrapper

- Status: deferred until canonical Witch Tools backend passes Blender validation.

### WT-ALIGN-004 — Curved/polyline movement rails

- Status: research.

## Precision / Magic Branch follow-up

### WT-PREC-004 — Curved/polyline Inject rails

- Status: research.

### WT-PREC-005 — Branch extrusion/side-face mode

- Status: deferred; requires explicit manifold/winding/material/attribute rules.

### WT-PREC-006 — Multi-object topology creation

- Status: deferred.

### WT-PREC-007 — Plane Lock world-frame mode

- Status: research.

### WT-PREC-010 — Dynamic hover-added Slide fan

- Status: deferred.
- Dev_v2.10.0 multi-edge Slide operates on the preselected edge set and uses hover only to choose its current driver.

### WT-MBR-002 — Arbitrary face-interior Auto-Merge retopology

- Status: research.
- Current candidate deliberately avoids inventing an unsafe universal face-interior topology rule.

### WT-MBR-003 — A/B/C / repair viewport labels

- Status: deferred QoL.

### WT-PREC-009 — Witch Dock / Quickbar wrappers

- Status: deferred until Dev_v2.10.0 is accepted in Blender 4.5.

## Baseline preservation

### WT-BASE-001

- Status: complete.
- Verified direct source remains `addons/witch_tools/dev/Witch_Tools_Dev/`.
- Dev_v2.8.0 Guided Align baseline commit: `fc94b7c27d0b850699e79b973a0548a2193eb525`.
- Dev_v2.10.0 branch was created from the then-current `feature/witch-tools-precision-edit` head `a5fe4bbccc954b25ac645489f2092b3d3d7618c5`.
- Public release branches remain unchanged.

### WT-BASE-002 — Integrate into Blender_Dev

- Status: planned only after Blender runtime validation.

## Selection / topology / protection retained

- WT-SEL-001 Selection Slots: active retained.
- WT-VINJ-001 old Auto-Aligned Vertex Inject backend: active retained through Edge Doctor wrapper.
- WT-CURV-001 Curvature Sync: active retained, user-validated production workflow from earlier versions; new nesting requires UI regression check.
- WT-PROT-001 Vertex Locks: active retained and consulted by magnetic Auto-Merge targets.
- WT-PROT-003 Plane Lock: active candidate.

## Immediate next step

Package/install Dev_v2.10.0 in Blender 4.5 and execute the two current test plans. Fix observed failures without broadening into deferred work. Do not modify Witch Dock/Quickbar until Witch Tools drag/snap/topology behavior is accepted.

## Dev_v2.10.1 runtime correction pass — active

Multi-edge Edge Solo/Branch, commit-wide overlap integration with true target-edge subdivision, Magic Branch navigation/ON-OFF/selection-mode sync, Paver out-of-plane growth, Paver return-path merge, and Object Snap Undo are implemented as a bugfix candidate. Blender 4.5 regression retest is the immediate gate before additional feature scope or Quickbar exposure.
