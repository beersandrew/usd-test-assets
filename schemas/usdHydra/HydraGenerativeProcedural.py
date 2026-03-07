"""
Generates hydraGenerativeProcedural.usda — demonstrates UsdHydraGenerativeProceduralAPI.

UsdHydraGenerativeProceduralAPI extends UsdProcGenerativeProcedural for Hydra-based
evaluation. The API adds hydra:proceduralType to identify the Hydra scene index plugin
that will evaluate the prim.

Run:
    python HydraGenerativeProcedural.py
"""

from pxr import Usd, UsdProc, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("hydraGenerativeProcedural.usda")

# Stage metadata
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── HydraScatter: Hydra-evaluated scatter procedural ───────────────────────────
scatter = UsdProc.GenerativeProcedural.Define(stage, "/World/HydraScatter")
scatter_prim = scatter.GetPrim()

# Apply HydraGenerativeProceduralAPI
scatter_prim.ApplyAPI("HydraGenerativeProceduralAPI")

# proceduralSystem routes to Hydra pipeline
scatter.CreateProceduralSystemAttr().Set("hydra")

# hydra:proceduralType identifies the specific plugin
scatter_prim.CreateAttribute(
    "hydra:proceduralType", Sdf.ValueTypeNames.Token, custom=False
).Set("HdScatterProceduralPlugin")

# Custom procedural inputs
scatter_prim.CreateAttribute(
    "primvars:args:sourceAsset", Sdf.ValueTypeNames.Asset, custom=True
).Set(Sdf.AssetPath("./assets/tree.usd"))

scatter_prim.CreateAttribute(
    "primvars:args:instanceCount", Sdf.ValueTypeNames.Int, custom=True
).Set(1000)

scatter_prim.CreateAttribute(
    "primvars:args:seed", Sdf.ValueTypeNames.Int, custom=True
).Set(7)

scatter_prim.CreateAttribute(
    "primvars:args:boundsMin", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(-500, -500))

scatter_prim.CreateAttribute(
    "primvars:args:boundsMax", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(500, 500))

scatter_prim.CreateAttribute(
    "primvars:args:scaleRange", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(0.8, 1.5))

scatter_prim.CreateAttribute(
    "primvars:args:alignToNormal", Sdf.ValueTypeNames.Bool, custom=True
).Set(True)

UsdGeom.XformCommonAPI(scatter).SetTranslate(Gf.Vec3d(0, 0, 0))

# ── HydraTerrain: terrain generation procedural ────────────────────────────────
terrain = UsdProc.GenerativeProcedural.Define(stage, "/World/HydraTerrain")
terrain_prim = terrain.GetPrim()

terrain_prim.ApplyAPI("HydraGenerativeProceduralAPI")
terrain.CreateProceduralSystemAttr().Set("hydra")
terrain_prim.CreateAttribute(
    "hydra:proceduralType", Sdf.ValueTypeNames.Token, custom=False
).Set("HdTerrainProceduralPlugin")

terrain_prim.CreateAttribute(
    "primvars:args:heightmap", Sdf.ValueTypeNames.Asset, custom=True
).Set(Sdf.AssetPath("./textures/terrain_height.exr"))

terrain_prim.CreateAttribute(
    "primvars:args:patchSize", Sdf.ValueTypeNames.Float, custom=True
).Set(1000.0)

terrain_prim.CreateAttribute(
    "primvars:args:maxHeight", Sdf.ValueTypeNames.Float, custom=True
).Set(200.0)

terrain_prim.CreateAttribute(
    "primvars:args:subdivisionLevel", Sdf.ValueTypeNames.Int, custom=True
).Set(6)

stage.GetRootLayer().Save()
print("Wrote hydraGenerativeProcedural.usda")
