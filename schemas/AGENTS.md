# schemas/ — Agent Guide

## Purpose

One folder per USD schema module. The `schemas/` directory is the primary focus for ongoing work:
it covers every schema module in the official OpenUSD library, with both hand-authored `.usda`
files and Python scripts that programmatically generate them.

## File Conventions

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

Located: `schemas/usdRender/` *(to be created)*

Single commit: `schemas/usdRender: add RenderSettings, RenderProduct, RenderPass, RenderVar examples`

- `renderSettings.usda` — `UsdRenderSettings`, `UsdRenderSettingsBase`
- `renderProduct.usda` — `UsdRenderProduct`, `UsdRenderVar`
- `renderPass.usda` — `UsdRenderPass`
- Python generators for each

Overview file: `usdRender.usda`

---

### usdPhysics — Physics Simulation *([  ] not started)*

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

Located: `schemas/usdProc/` *(to be created)*

Single commit: `schemas/usdProc: add GenerativeProcedural example`

- `generativeProcedural.usda` — `UsdProcGenerativeProcedural` (abstract base; must be subclassed)
- `GenerativeProcedural.py`

Overview file: `usdProc.usda`

---

### usdHydra — Hydra Procedurals *([  ] not started)*

Located: `schemas/usdHydra/` *(to be created)*

Single commit: `schemas/usdHydra: add HydraGenerativeProceduralAPI example`

- `hydraGenerativeProcedural.usda` — `UsdHydraGenerativeProceduralAPI` applied to a `UsdProcGenerativeProcedural`
- `HydraGenerativeProcedural.py`

Note: `usdHydra` only defines `HydraGenerativeProceduralAPI`; it extends `usdProc` for Hydra-based evaluation.

---

### usdMtlx — MaterialX Integration *([  ] not started)*

Located: `schemas/usdMtlx/` *(to be created)*

Single commit: `schemas/usdMtlx: add MaterialXConfigAPI example`

- `materialXConfig.usda` — `UsdMtlxMaterialXConfigAPI` applied to a `UsdShadeMaterial`
- `MaterialXConfig.py`

Note: `usdMtlx` bridges MaterialX documents with USD shading networks. Its primary value is the
Sdr discovery/parser plugins and `.mtlx` file format support; `MaterialXConfigAPI` stores the
authoring config on a material prim.

---

### usdSemantics — Semantic Labels *([  ] not started)*

Located: `schemas/usdSemantics/` *(to be created)*

Single commit: `schemas/usdSemantics: add SemanticsLabelsAPI example`

- `semanticsLabels.usda` — `UsdSemanticsLabelsAPI` (multiple-apply) showing multiple taxonomies
  (e.g., `:category`, `:style`) with hierarchically-inherited token-valued labels
- `SemanticsLabels.py`

---

### usd (core) — Foundation Schemas *([  ] not started)*

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
