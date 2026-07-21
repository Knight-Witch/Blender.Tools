# Curvature Sync — 3D Printing Use Case

Curvature Sync must treat dimensions and assembly fit as primary constraints.

Print-specific requirements:

- preserve A/M/Z and straight protected extensions
- preserve intended radii, wall spacing, and interface dimensions
- synchronize segmentation across upper/lower fitted solids
- retain separate printable objects unless explicitly joined
- maintain watertight/manifold geometry where input supports it
- correct outward normals and face winding
- avoid remeshing or approximating protected small details
- verify undo before committing production geometry

A slicer does not require aesthetic quad topology, but matching, smooth curved segmentation can be important for print surface quality and later editing. Topology cleanup must never alter fit-critical geometry merely to look cleaner.

The authoritative behavior and tests are defined in `/docs/features/curvature_sync/`.