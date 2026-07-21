# Selection Slots Reference Cases

## RC-01 — Collar Curvature Sync chains

Problem:

The collar model contains many parallel open edge chains. Alt-click loop selection stops at poles, triangles, n-gons, and fragmented topology, so rebuilding the complete Curvature Sync selection required many manual clicks.

Expected workflow:

1. Manually complete the intended chain selection once.
2. Save it as a named slot such as `Collar Curvature Chains`.
3. Run Analyze/Apply tests, inspect, undo, or reopen the file.
4. Reselect the saved chain set with one action.
5. Overwrite the slot after correcting a missed edge.

This is the production-driving case for Dev_v2.6.0.

## RC-02 — Multi-object upper/lower assembly

Save selected edge families across an upper and lower fitted print part while both objects are in multi-object Edit Mode. Reselect should restore both objects, Edit Mode, Edge Select mode, and each object's marked edges.

## RC-03 — Non-contiguous vertex cleanup set

Save scattered vertices requiring later manual inspection. The slot should restore only surviving marked vertices after unrelated modeling work.

## RC-04 — Face-region review

Save several disconnected faces before testing material, normal, or topology operations. Clear should erase the saved data while preserving the descriptive row name.

## RC-05 — Overwrite after correction

A user discovers that one edge was omitted. They add it to the current selection and press Save on the same slot. The prior marker set is replaced rather than accumulated, and the name/order remain unchanged.

## RC-06 — Topology deletion

A saved edge is dissolved. Reselect restores the remaining marked edges and reports restored counts. It does not invent a replacement for the deleted edge.

## RC-07 — Marker propagation

A saved edge is subdivided or duplicated by an operation that copies custom data. The resulting elements may inherit the slot marker. Runtime tests must record Blender 4.5 behavior, and the tool must not falsely describe these markers as immutable element UUIDs.

## RC-08 — Quickbar without Witch Tools

Quickbar is enabled while Witch Tools is disabled or too old. The Select tab remains visible with a clear requirement message. Main/Edit tools and viewport pass-through continue to work.

## RC-09 — Long descriptive names

A slot is named `Upper + Lower Collar Curvature Chains — Final A/M/Z Span`. The N-panel field and Quickbar display remain compact at normal width, expand when widened, and provide access to the full name through editing/tooltip behavior.
