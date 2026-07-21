# Curvature Sync — BG3 Use Case

Curvature Sync may be used on BG3-related meshes when imported or edited topology has uneven/missing correspondence across intended curved hard-surface regions.

BG3-specific considerations must be documented per actual asset workflow, including:

- armature, weighting, and shape-key constraints
- game/export topology requirements
- left/right orientation caveats in BG3 workflows
- material/custom-data preservation
- whether the asset is expected to deform

Curvature Sync remains a general Witch Tools topology operator. BG3-specific use must not change the canonical geometry implementation or duplicate it in a BG3 module.

The current feature is not yet implemented or validated on BG3 assets.