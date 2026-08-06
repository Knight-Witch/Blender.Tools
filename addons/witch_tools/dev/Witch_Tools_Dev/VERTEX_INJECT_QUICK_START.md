# Edge / Vertex Inject Quick Start

Build: Witch Tools Dev_v2.5.1
Target: Blender 4.5

## Auto-Aligned Vertex Inject

This operator places a missing vertex on an existing parallel target edge/chain by copying the local relationship of a known neighboring column.

### Selection order

In Edit Mode, use Vertex Select and click exactly three vertices individually:

1. **A** — source vertex on the parallel target chain.
2. **B** — source vertex connected to A by the known column edge.
3. **C** — corresponding row vertex connected to B. C must be active/selected last.

The intended missing vertex is **D**. The operator uses `D ideal = C + (A - B)`, follows the edge chain leaving A in the B-to-C direction, and splits the nearest valid target edge.

### Options

- **Connect & Split Face**: enabled by default. Connects C to D and splits their shared face.
- **Projection Tolerance**: maximum target-chain offset as a fraction of A-B length. Increase only when the inferred chain is correct but imperfect.
- **Existing Vertex Tolerance**: reuses a nearby existing vertex instead of creating a duplicate.

### Safety

- The operation performs a copied-BMesh preflight before modifying the real mesh.
- A-B and B-C must be real edges.
- Ambiguous forks, excessive projection error, missing shared faces, shape keys, and degenerate results cancel without applying the real edit.
- Existing Vertex Lock and Curvature Sync anchor references are remapped after topology changes.
- The result leaves C and D selected for inspection.

### Current limits

- Operates on the active mesh object.
- Automatic bulk injection is not included in this patch.
- Curved-chain traversal uses the straightest valid continuation and aborts on ambiguous forks.
