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

Located: `schemas/usdUI/`

- [x] `Backdrop` — `backdrop.usda` + `Backdrop.py`
- [x] `NodeGraphNodeAPI` — `nodeGraphNodeApi.usda` + `NodeGraphNodeAPI.py`
- [x] `SceneGraphPrimAPI` — `SceneGraphPrimAPI.usda` + `SceneGraphPrimAPI.py`
- [ ] `AccessibilityAPI` — `accessibilityApi.usda` + `AccessibilityAPI.py`
- [ ] `NodeGraphNodeAPI` hints — `ObjectHints.py`, `PrimHints.py`, `PropertyHints.py`, `AttributeHints.py`

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
   - `UsdGeomSphere`, `UsdGeomCube`, `UsdGeomCone`, `UsdGeomCylinder`, `UsdGeomCapsule`, `UsdGeomPlane`

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

2. **Environment and Geometry Lights** — `envAndGeoLights.usda`
   - `UsdLuxDistantLight`, `UsdLuxDomeLight`, `UsdLuxGeometryLight`, `UsdLuxPortalLight`

3. **Geometry-based Light APIs** — `lightApis.usda`
   - `UsdLuxMeshLightAPI`, `UsdLuxVolumeLightAPI`

4. **Light Shaping and Shadows** — `shapingAndShadow.usda`
   - `UsdLuxShapingAPI`, `UsdLuxShadowAPI`

5. **Light Filters** — `lightFilter.usda`
   - `UsdLuxLightFilter`, `UsdLuxPluginLightFilter`

6. **Plugin Light and LightListAPI** — `pluginAndList.usda`
   - `UsdLuxPluginLight`, `UsdLuxLightListAPI`, `UsdLuxLightAPI`

Overview file: `usdLux.usda`

---

### usdRender — Render Settings *([  ] not started)*

Located: `schemas/usdRender/` *(to be created)*

Single commit: `schemas/usdRender: add RenderSettings, RenderProduct, RenderPass, RenderVar examples`

- `RenderSettings.usda` — `UsdRenderSettings`, `UsdRenderSettingsBase`
- `RenderProduct.usda` — `UsdRenderProduct`, `UsdRenderVar`
- `RenderPass.usda` — `UsdRenderPass`
- Python generators for each

Overview file: `usdRender.usda`

---

### usdPhysics — Physics Simulation *([  ] not started)*

Located: `schemas/usdPhysics/` *(to be created)*

1. **Scene and Rigid Bodies** — `rigidBody.usda`
   - `UsdPhysicsScene`, `UsdPhysicsRigidBodyAPI`, `UsdPhysicsMassAPI`, `UsdPhysicsMaterialAPI`

2. **Collision** — `collision.usda`
   - `UsdPhysicsMeshCollisionAPI`

3. **Joints** — `joints.usda`
   - `UsdPhysicsJoint`, `UsdPhysicsFixedJoint`, `UsdPhysicsRevoluteJoint`,
     `UsdPhysicsPrismaticJoint`, `UsdPhysicsSphericalJoint`, `UsdPhysicsLimitAPI`

Overview file: `usdPhysics.usda`

---

### usdVol — Volume Data *([  ] not started)*

Located: `schemas/usdVol/` *(to be created)*

Single commit: `schemas/usdVol: add Volume, OpenVDBAsset, Field3DAsset examples`

- `volume.usda` — `UsdVolVolume`, `UsdVolFieldBase`, `UsdVolFieldAsset`
- `openVDB.usda` — `UsdVolOpenVDBAsset`
- `field3D.usda` — `UsdVolField3DAsset`
- Python generators for each

Overview file: `usdVol.usda`

---

### usdProc — Procedurals *([  ] not started)*

Located: `schemas/usdProc/` *(to be created)*

Single commit: `schemas/usdProc: add GenerativeProcedural example`

- `generativeProcedural.usda` — `UsdProcGenerativeProcedural`
- `GenerativeProcedural.py`

Overview file: `usdProc.usda`

---

## Recommended Implementation Order

1. `usdGeom` — foundation for all geometry; many other schemas depend on it
2. `usdShade` — shading/materials used alongside geometry in nearly every scene
3. `usdLux` — lighting builds on usdGeom and usdShade
4. `usdRender` — render settings reference lights, geometry, and materials
5. `usdPhysics` — physics builds on usdGeom geometry prims
6. `usdVol` — volumes are a standalone geometry concept
7. `usdProc` — small, self-contained
8. `usdUI` additions — complete the partial coverage
