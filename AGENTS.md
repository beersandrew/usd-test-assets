# USD Test Assets — Agent Guide

## Repo Purpose

A collection of test and learning files for [Universal Scene Description (USD)](https://openusd.org).
Each file explores a specific schema, feature, or concept. The `schemas/` section is the primary
focus for ongoing work: it covers every schema module in the official OpenUSD library, with both
hand-authored `.usda` files and Python scripts that programmatically generate them.

## Repo Layout

```
schemas/        # One folder per USD schema module (usdGeom, usdShade, etc.)
Features/       # Standalone test files for specific USD features
Development/    # Build tooling, debug notes, platform-specific USD tools
```

## Schema File Conventions

Every schema module folder should follow this pattern:

```
schemas/<module>/
  <module>.usda          # Overview stage — shows all major schemas in one file
  <concept>.usda         # One file per schema or logical grouping
  <SchemaName>.py        # Python script that generates the matching .usda
```

### Rules for .usda files
- Use a minimal but complete stage: set `metersPerUnit`, `upAxis`, and `timeCodesPerSecond` where relevant.
- Include realistic, non-trivial attribute values — enough to illustrate the schema's purpose.
- Add brief inline comments (`#`) explaining non-obvious attributes or relationships.

### Rules for .py scripts
- Each script must be standalone: run `python <script>.py` to regenerate the matching `.usda`.
- Use `Usd.Stage.CreateNew(...)` and call `stage.GetRootLayer().Save()` at the end.
- Mirror the same prim structure as the hand-authored `.usda`.

## Multi-Agent Execution

Each schema module is implemented in its own branch. This lets multiple Claude Code instances
work in parallel without conflicts and makes per-branch discussion natural.

### Branch Naming Convention

```
claude/schema-<module>-<session-id>
```

Examples: `claude/schema-usdGeom-Abc12`, `claude/schema-usdShade-Xyz99`

The session-id is whatever short suffix Claude Code appends automatically when you launch it.
If you are spinning up agents by hand, pick any unique suffix.

### Dependency Waves

Schemas within the same wave are fully independent and can be developed in parallel.
Start Wave 2 only after the Wave 1 PRs that it depends on are merged into `main`.

**Wave 1 — no dependencies, launch all at once:**

| Branch (prefix) | Schema | Assigned task |
|---|---|---|
| `claude/schema-usdGeom-*` | usdGeom | Geometry prims, cameras, API schemas |
| `claude/schema-usdShade-*` | usdShade | Shaders, materials, binding |
| `claude/schema-usdProc-*` | usdProc | GenerativeProcedural |
| `claude/schema-usd-*` | usd (core) | CollectionAPI, ColorSpaceAPI, ModelAPI, ClipsAPI |
| `claude/schema-usdSemantics-*` | usdSemantics | SemanticsLabelsAPI |
| `claude/schema-usdUI-*` | usdUI | AccessibilityAPI, UI hint utilities |

**Wave 2 — start after Wave 1 PRs are merged:**

| Branch (prefix) | Schema | Depends on |
|---|---|---|
| `claude/schema-usdLux-*` | usdLux | usdGeom, usdShade |
| `claude/schema-usdMtlx-*` | usdMtlx | usdShade |
| `claude/schema-usdPhysics-*` | usdPhysics | usdGeom |
| `claude/schema-usdVol-*` | usdVol | usdGeom |
| `claude/schema-usdHydra-*` | usdHydra | usdProc |

**Wave 3 — start after Wave 2 PRs are merged:**

| Branch (prefix) | Schema | Depends on |
|---|---|---|
| `claude/schema-usdRender-*` | usdRender | usdLux, usdGeom, usdShade |

**Optional (any time, low priority):**

| Branch (prefix) | Schema |
|---|---|
| `claude/schema-usdRi-*` | usdRi |

---

### Orchestration Prompt — Wave 1

Copy the block below and run it as a Claude Code prompt. It launches all Wave 1 schema
agents in parallel. Replace `<SESSION-ID>` placeholders with any short unique suffix
(e.g. the last 5 chars of the current session id visible in your terminal).

> **Tip:** You can find your session id in the Claude Code status line or in the URL
> of a browser-based session.

```
Using the Agent tool, launch the following six agents **in parallel** (all in one message
with six tool calls). Each agent must:

1. Create and check out branch `<branch>` from `main`:
      git fetch origin main && git checkout -b <branch> origin/main
   If the branch already exists remotely:
      git fetch origin <branch> && git checkout <branch>
2. Read AGENTS.md thoroughly before writing any files.
3. Implement every file listed for the schema (see "Schema Completion Plan" in AGENTS.md).
4. Commit each logical unit with message format: `schemas/<module>: add <concept> example`
5. Push with: git push -u origin <branch>
6. Open a PR from <branch> into main when all commits are done.

Agents:

Agent 1 — usdGeom:
  branch: claude/schema-usdGeom-<SESSION-ID>
  task: Implement schemas/usdGeom/ — all 10 commits listed in AGENTS.md under "usdGeom".
        Create the directory. Write each .usda and matching .py file.
        Finish with usdGeom.usda overview file.

Agent 2 — usdShade:
  branch: claude/schema-usdShade-<SESSION-ID>
  task: Implement schemas/usdShade/ — all 3 commits listed in AGENTS.md under "usdShade".
        Create the directory. Write each .usda and matching .py file.
        Finish with usdShade.usda overview file.

Agent 3 — usdProc:
  branch: claude/schema-usdProc-<SESSION-ID>
  task: Implement schemas/usdProc/ — single commit listed in AGENTS.md under "usdProc".
        Create the directory. Write generativeProcedural.usda + GenerativeProcedural.py + usdProc.usda.

Agent 4 — usd (core):
  branch: claude/schema-usd-<SESSION-ID>
  task: Implement schemas/usd/ — all 3 commits listed in AGENTS.md under "usd (core)".
        Create the directory. Write each .usda and matching .py file.

Agent 5 — usdSemantics:
  branch: claude/schema-usdSemantics-<SESSION-ID>
  task: Implement schemas/usdSemantics/ — single commit listed in AGENTS.md under "usdSemantics".
        Create the directory. Write semanticsLabels.usda + SemanticsLabels.py.

Agent 6 — usdUI additions:
  branch: claude/schema-usdUI-<SESSION-ID>
  task: The schemas/usdUI/ directory already exists with several files.
        Add only the two missing items listed under "usdUI" in AGENTS.md:
        accessibilityApi.usda + AccessibilityAPI.py, and uiHints.usda.
        Commit each as a separate commit. Do not modify existing files.
```

---

### Orchestration Prompt — Wave 2

Run this after all Wave 1 PRs are merged.

```
Using the Agent tool, launch the following five agents **in parallel** (all in one message).
Same rules as Wave 1: create branch from main, read AGENTS.md, implement files, commit, push, open PR.

Agent 1 — usdLux:
  branch: claude/schema-usdLux-<SESSION-ID>
  task: Implement schemas/usdLux/ — all 6 commits listed in AGENTS.md under "usdLux".

Agent 2 — usdMtlx:
  branch: claude/schema-usdMtlx-<SESSION-ID>
  task: Implement schemas/usdMtlx/ — single commit listed in AGENTS.md under "usdMtlx".

Agent 3 — usdPhysics:
  branch: claude/schema-usdPhysics-<SESSION-ID>
  task: Implement schemas/usdPhysics/ — all 4 commits listed in AGENTS.md under "usdPhysics".

Agent 4 — usdVol:
  branch: claude/schema-usdVol-<SESSION-ID>
  task: Implement schemas/usdVol/ — all 2 commits listed in AGENTS.md under "usdVol".

Agent 5 — usdHydra:
  branch: claude/schema-usdHydra-<SESSION-ID>
  task: Implement schemas/usdHydra/ — single commit listed in AGENTS.md under "usdHydra".
```

---

### Orchestration Prompt — Wave 3

Run after Wave 2 PRs are merged.

```
Using the Agent tool, launch one agent:

Agent 1 — usdRender:
  branch: claude/schema-usdRender-<SESSION-ID>
  task: Implement schemas/usdRender/ — all commits listed in AGENTS.md under "usdRender".
```

---

### Discussing Work with a Specific Agent

Because each schema has its own branch, you can always open a fresh Claude Code session
focused on that branch's context:

```bash
git checkout claude/schema-usdGeom-Abc12
claude   # or: claude --resume <session-id-from-that-branch>
```

The agent will have the full file tree and git history for that branch available,
making it easy to ask questions like "why did you model the Mesh this way?" or
"add a subdivision surface variant to mesh.usda".

---

## Commit Strategy

Each commit should cover exactly one logical unit of work from the plan below.
Commit messages should follow the pattern:

```
schemas/<module>: add <SchemaName or concept> example
```

Examples:
- `schemas/usdGeom: add Mesh and TetMesh examples`
- `schemas/usdLux: add SphereLight, DiskLight, RectLight examples`
- `schemas/usdUI: add AccessibilityAPI example`

---

## Schema Completion Plan

### Status Legend
- `[ ]` Not started
- `[~]` Partial — see notes
- `[x]` Complete

---

### usdMedia — Media *(complete)*

Located: `schemas/usdMedia/`

- [x] `SpatialAudio` — `spatialAudio.usda` + `SpatialAudio.py`
- [x] `AssetPreviewsAPI` — `usdMedia/assetPreviewsApi.usda` + `AssetPreviewsAPI.py`

---

### usdSkel — Skeletal Animation *(complete)*

Located: `schemas/usdSkel/`

- [x] `SkelRoot`, `Skeleton`, `SkelAnimation` — `usdSkel.usda`
- [x] `SkelBindingAPI` — `skelBindingApi_joints.usda` + `SkelBindingAPI.py`
- [x] `BlendShape` — `blendshapes.usda` + `BlendShape.py`
- [x] Instancing with skeletons — `instancing.usda`

---

### usdUI — UI Schemas *([~] partial)*

Branch: `claude/schema-usdUI-*` | Wave 1

Located: `schemas/usdUI/`

- [x] `Backdrop` — `backdrop.usda` + `Backdrop.py`
- [x] `NodeGraphNodeAPI` — `nodeGraphNodeApi.usda` + `NodeGraphNodeAPI.py`
- [x] `SceneGraphPrimAPI` — `SceneGraphPrimAPI.usda` + `SceneGraphPrimAPI.py`
- [ ] `AccessibilityAPI` (multiple-apply) — `accessibilityApi.usda` + `AccessibilityAPI.py`
- [ ] UI hint utilities — `uiHints.usda`: `ObjectHints`, `PrimHints`, `PropertyHints`, `AttributeHints`
  - Note: these are metadata-based hint dictionaries, not applied API schemas

Suggested commits:
1. `schemas/usdUI: add AccessibilityAPI example`
2. `schemas/usdUI: add ObjectHints, PrimHints, PropertyHints, AttributeHints examples`

---

### usdGeom — Geometry *([  ] not started)*

Branch: `claude/schema-usdGeom-*` | Wave 1

Located: `schemas/usdGeom/` *(to be created)*

Split into the following commits, each with `.usda` + `.py` files:

1. **Xform and Scope** — `xform.usda`
   - `UsdGeomXform`, `UsdGeomScope`, `UsdGeomXformCommonAPI`

2. **Geometric Primitives** — `primitives.usda`
   - `UsdGeomSphere`, `UsdGeomCube`, `UsdGeomCone`
   - `UsdGeomCylinder`, `UsdGeomCylinder_1` (variant with per-end radii)
   - `UsdGeomCapsule`, `UsdGeomCapsule_1` (variant with per-end radii)
   - `UsdGeomPlane`

3. **Mesh** — `mesh.usda`
   - `UsdGeomMesh` (polygon mesh + subdivision surface variants)

4. **TetMesh and GeomSubset** — `tetMeshAndSubset.usda`
   - `UsdGeomTetMesh`, `UsdGeomGeomSubset`

5. **Basis Curves** — `basisCurves.usda`
   - `UsdGeomBasisCurves` (linear, bezier, bspline, catmullRom)

6. **Nurbs Curves and Patch** — `nurbsCurvesAndPatch.usda`
   - `UsdGeomNurbsCurves`, `UsdGeomNurbsPatch`

7. **Hermite Curves** — `hermiteCurves.usda`
   - `UsdGeomHermiteCurves`

8. **Points and Point Instancer** — `points.usda`
   - `UsdGeomPoints`, `UsdGeomPointInstancer`

9. **Camera** — `camera.usda`
   - `UsdGeomCamera`

10. **API Schemas** — `apiSchemas.usda`
    - `UsdGeomPrimvarsAPI`, `UsdGeomMotionAPI`, `UsdGeomVisibilityAPI`, `UsdGeomModelAPI`

Overview file: `usdGeom.usda` — assembled last, references concepts from above.

---

### usdShade — Shading and Materials *([  ] not started)*

Branch: `claude/schema-usdShade-*` | Wave 1

Located: `schemas/usdShade/` *(to be created)*

1. **Shader and NodeGraph** — `shaderAndNodeGraph.usda`
   - `UsdShadeShader`, `UsdShadeNodeGraph`, `UsdShadeNodeDefAPI`, `UsdShadeConnectableAPI`

2. **Material and Binding** — `material.usda`
   - `UsdShadeMaterial`, `UsdShadeMaterialBindingAPI`

3. **Coordinate Systems** — `coordSys.usda`
   - `UsdShadeCoordSysAPI`

Overview file: `usdShade.usda`

---

### usdLux — Lighting *([  ] not started)*

Branch: `claude/schema-usdLux-*` | Wave 2 (needs usdGeom + usdShade merged)

Located: `schemas/usdLux/` *(to be created)*

1. **Punctual Lights** — `punctualLights.usda`
   - `UsdLuxSphereLight`, `UsdLuxDiskLight`, `UsdLuxRectLight`, `UsdLuxCylinderLight`

2. **Environment and Portal Lights** — `envLights.usda`
   - `UsdLuxDistantLight`, `UsdLuxDomeLight`, `UsdLuxDomeLight_1` (configurable pole axis), `UsdLuxPortalLight`

3. **Geometry-based Lights** — `geoLights.usda`
   - `UsdLuxGeometryLight` *(deprecated but documented)*, `UsdLuxMeshLightAPI`, `UsdLuxVolumeLightAPI`

4. **Light Shaping and Shadows** — `shapingAndShadow.usda`
   - `UsdLuxShapingAPI`, `UsdLuxShadowAPI`

5. **Light Filters** — `lightFilter.usda`
   - `UsdLuxLightFilter`, `UsdLuxPluginLightFilter`

6. **Plugin Light and Discovery** — `pluginAndList.usda`
   - `UsdLuxPluginLight`, `UsdLuxLightListAPI`, `UsdLuxLightAPI`

Overview file: `usdLux.usda`

---

### usdRender — Render Settings *([  ] not started)*

Branch: `claude/schema-usdRender-*` | Wave 3 (needs usdLux + usdGeom + usdShade merged)

Located: `schemas/usdRender/` *(to be created)*

Single commit: `schemas/usdRender: add RenderSettings, RenderProduct, RenderPass, RenderVar examples`

- `renderSettings.usda` — `UsdRenderSettings`, `UsdRenderSettingsBase`
- `renderProduct.usda` — `UsdRenderProduct`, `UsdRenderVar`
- `renderPass.usda` — `UsdRenderPass`
- Python generators for each

Overview file: `usdRender.usda`

---

### usdPhysics — Physics Simulation *([  ] not started)*

Branch: `claude/schema-usdPhysics-*` | Wave 2 (needs usdGeom merged)

Located: `schemas/usdPhysics/` *(to be created)*

1. **Scene and Rigid Bodies** — `rigidBody.usda`
   - `UsdPhysicsScene`, `UsdPhysicsRigidBodyAPI`, `UsdPhysicsMassAPI`, `UsdPhysicsMaterialAPI`

2. **Collision** — `collision.usda`
   - `UsdPhysicsCollisionAPI`, `UsdPhysicsMeshCollisionAPI`, `UsdPhysicsCollisionGroup`
   - `UsdPhysicsFilteredPairsAPI`

3. **Joints** — `joints.usda`
   - `UsdPhysicsJoint`, `UsdPhysicsFixedJoint`, `UsdPhysicsRevoluteJoint`
   - `UsdPhysicsPrismaticJoint`, `UsdPhysicsSphericalJoint`, `UsdPhysicsDistanceJoint`
   - `UsdPhysicsLimitAPI` (multiple-apply), `UsdPhysicsDriveAPI` (multiple-apply)

4. **Articulation** — `articulation.usda`
   - `UsdPhysicsArticulationRootAPI`

Overview file: `usdPhysics.usda`

---

### usdVol — Volume Data *([  ] not started)*

Branch: `claude/schema-usdVol-*` | Wave 2 (needs usdGeom merged)

Located: `schemas/usdVol/` *(to be created)*

1. **Core Volumes** — `volume.usda` + `openVDB.usda` + `field3D.usda`
   - `UsdVolVolume`, `UsdVolVolumeFieldBase`, `UsdVolVolumeFieldAsset`
   - `UsdVolOpenVDBAsset`, `UsdVolField3DAsset`

2. **Particle Fields (3D Gaussian Splatting)** — `particleFields.usda`
   - `UsdVolParticleField`, `UsdVolParticleField3DGaussianSplat`
   - Applied APIs: `ParticleFieldPositionAttributeAPI`, `ParticleFieldOrientationAttributeAPI`
   - `ParticleFieldScaleAttributeAPI`, `ParticleFieldOpacityAttributeAPI`
   - `ParticleFieldKernelGaussianEllipsoidAPI`, `ParticleFieldKernelGaussianSurfletAPI`
   - `ParticleFieldKernelConstantSurfletAPI`, `ParticleFieldSphericalHarmonicsAttributeAPI`
   - `ParticleFieldRadianceBaseAPI`

Suggested commits:
1. `schemas/usdVol: add Volume, OpenVDBAsset, Field3DAsset examples`
2. `schemas/usdVol: add ParticleField and 3D Gaussian Splat examples`

Overview file: `usdVol.usda`

---

### usdProc — Procedurals *([  ] not started)*

Branch: `claude/schema-usdProc-*` | Wave 1

Located: `schemas/usdProc/` *(to be created)*

Single commit: `schemas/usdProc: add GenerativeProcedural example`

- `generativeProcedural.usda` — `UsdProcGenerativeProcedural` (abstract base; must be subclassed)
- `GenerativeProcedural.py`

Overview file: `usdProc.usda`

---

### usdHydra — Hydra Procedurals *([  ] not started)*

Branch: `claude/schema-usdHydra-*` | Wave 2 (needs usdProc merged)

Located: `schemas/usdHydra/` *(to be created)*

Single commit: `schemas/usdHydra: add HydraGenerativeProceduralAPI example`

- `hydraGenerativeProcedural.usda` — `UsdHydraGenerativeProceduralAPI` applied to a `UsdProcGenerativeProcedural`
- `HydraGenerativeProcedural.py`

Note: `usdHydra` only defines `HydraGenerativeProceduralAPI`; it extends `usdProc` for Hydra-based evaluation.

---

### usdMtlx — MaterialX Integration *([  ] not started)*

Branch: `claude/schema-usdMtlx-*` | Wave 2 (needs usdShade merged)

Located: `schemas/usdMtlx/` *(to be created)*

Single commit: `schemas/usdMtlx: add MaterialXConfigAPI example`

- `materialXConfig.usda` — `UsdMtlxMaterialXConfigAPI` applied to a `UsdShadeMaterial`
- `MaterialXConfig.py`

Note: `usdMtlx` bridges MaterialX documents with USD shading networks. Its primary value is the
Sdr discovery/parser plugins and `.mtlx` file format support; `MaterialXConfigAPI` stores the
authoring config on a material prim.

---

### usdSemantics — Semantic Labels *([  ] not started)*

Branch: `claude/schema-usdSemantics-*` | Wave 1

Located: `schemas/usdSemantics/` *(to be created)*

Single commit: `schemas/usdSemantics: add SemanticsLabelsAPI example`

- `semanticsLabels.usda` — `UsdSemanticsLabelsAPI` (multiple-apply) showing multiple taxonomies
  (e.g., `:category`, `:style`) with hierarchically-inherited token-valued labels
- `SemanticsLabels.py`

---

### usd (core) — Foundation Schemas *([  ] not started)*

Branch: `claude/schema-usd-*` | Wave 1

Located: `schemas/usd/` *(to be created)*

These schemas live in the base `usd` module and apply universally across all schema domains.

1. **Collections** — `collections.usda`
   - `UsdCollectionAPI` (multiple-apply) — named include/exclude sets and membership expressions

2. **Color Spaces** — `colorSpaces.usda`
   - `UsdColorSpaceAPI` — attaches a `colorSpace` to a prim, inherits hierarchically
   - `UsdColorSpaceDefinitionAPI` (multiple-apply) — defines custom color spaces

3. **Model and Clips** — `modelAndClips.usda`
   - `UsdModelAPI` — `kind` metadata and asset info on models
   - `UsdClipsAPI` — value-clips metadata interface

Suggested commits:
1. `schemas/usd: add CollectionAPI example`
2. `schemas/usd: add ColorSpaceAPI and ColorSpaceDefinitionAPI examples`
3. `schemas/usd: add ModelAPI and ClipsAPI examples`

---

### usdRi — RenderMan Integration *([  ] low priority, some deprecated)*

Branch: `claude/schema-usdRi-*` | Optional, any wave

Located: `schemas/usdRi/` *(to be created, optional)*

Single commit: `schemas/usdRi: add RenderMan API schema examples`

- `statements.usda` — `UsdRiStatementsAPI` (RI attributes and coordinate systems in `ri:` namespace)
- `renderPass.usda` — `UsdRiRenderPassAPI` (camera visibility, matte collections)
- `material.usda` — `UsdRiMaterialAPI` *(deprecated)* (RenderMan surface/displacement/volume outputs)
- `spline.usda` — `UsdRiSplineAPI` *(deprecated)* (general-purpose spline storage)

Note: `usdRi` is RenderMan-specific. Mark deprecated schemas clearly in comments. This module
is optional and should be done last.

---

## Recommended Implementation Order

**Core (foundation for all other work):**
1. `usdGeom` — geometry is required by nearly every other schema
2. `usdShade` — materials used alongside geometry in almost every scene

**Rendering pipeline:**
3. `usdLux` — lighting builds on usdGeom and usdShade
4. `usdRender` — render settings reference lights, geometry, and materials
5. `usdMtlx` — MaterialX integration extends usdShade

**Simulation and volumes:**
6. `usdPhysics` — physics builds on usdGeom geometry prims
7. `usdVol` — volumes build on usdGeom (Volume is a Gprim)

**Procedurals:**
8. `usdProc` — abstract base for procedural systems
9. `usdHydra` — extends usdProc for Hydra-based evaluation

**Foundation and cross-cutting:**
10. `usd` (core) — CollectionAPI, ColorSpaceAPI, ModelAPI, ClipsAPI
11. `usdSemantics` — semantic labeling, standalone

**Complete existing coverage:**
12. `usdUI` additions — AccessibilityAPI, UI hint utilities

**Optional / specialized:**
13. `usdRi` — RenderMan-specific schemas (low priority)
