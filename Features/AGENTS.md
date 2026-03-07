# Features/ — Agent Guide

## Purpose

Standalone test files for specific USD features. Unlike `schemas/`, which organizes files by schema
module, `Features/` organizes files by concept or use case — things that cut across multiple schemas
or demonstrate end-to-end workflows.

## Folder Layout

```
Features/
  Animation/      # Time-sampled transforms and animated attributes
  Lux/            # Lighting setups and light rig examples
  MaterialX/      # MaterialX document integration
  Physics/        # Rigid body simulations and colliders
  Skel/           # Skeletal rigs, blend shapes, and skin binding
  TextureTest/    # UV mapping and texture asset resolution
  Validation/     # Files that exercise USD validation rule checkers
  nesting/        # Layer composition via references and sublayers
  over/           # Override (over) prim examples
  variants/       # VariantSet authoring and switching
```

## File Conventions

- Each subfolder should contain a focused, self-contained example.
- Prefer `.usda` (ASCII) format so files are human-readable.
- Include a brief comment at the top of each `.usda` explaining what it demonstrates.
- Companion `.py` scripts are welcome but not required for every example.
- Large binary assets (textures, `.usdz` packages) belong inside the subfolder they support.

## Adding a New Feature Example

1. Create a subfolder under `Features/` named for the feature or concept (e.g., `Features/Instancing/`).
2. Add a minimal `.usda` file that isolates and demonstrates the feature.
3. Optionally add a `.py` script that generates the same file programmatically.
4. Commit with the message pattern:
   ```
   Features/<folder>: add <concept> example
   ```
