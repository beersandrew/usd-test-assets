# USD Test Assets — Agent Guide

## Repo Purpose

A collection of test and learning files for [Universal Scene Description (USD)](https://openusd.org).
Each file explores a specific schema, feature, or concept.

## Repo Layout

```
schemas/        # One folder per USD schema module (usdGeom, usdShade, etc.)
Features/       # Standalone test files for specific USD features
Development/    # Build tooling, debug notes, platform-specific USD tools
```

See each folder's own `AGENTS.md` for detailed conventions and work plans:

- [`schemas/AGENTS.md`](schemas/AGENTS.md) — schema file conventions, completion plan, implementation order
- [`Features/AGENTS.md`](Features/AGENTS.md) — feature file conventions and examples
- [`Development/AGENTS.md`](Development/AGENTS.md) — build tooling and debug notes

## Commit Strategy

Each commit should cover exactly one logical unit of work.
Commit messages should follow the pattern:

```
<folder>/<module>: add <concept or schema> example
```

Examples:
- `schemas/usdGeom: add Mesh and TetMesh examples`
- `schemas/usdLux: add SphereLight, DiskLight, RectLight examples`
- `Features/Lux: add area light example`
