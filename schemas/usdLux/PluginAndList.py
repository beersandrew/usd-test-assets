from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

stage = Usd.Stage.CreateNew("pluginAndList.usda")

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ── PluginLight: renderer-specific light type ─────────────────────────────
custom_light = UsdLux.PluginLight.Define(stage, "/World/CustomLight")
custom_light_prim = custom_light.GetPrim()
custom_light_prim.CreateAttribute("info:id", Sdf.ValueTypeNames.Token).Set("PxrMeshLight")
custom_light.CreateIntensityAttr(10000.0)

# ── LightListAPI: caches a list of lights in the scene for fast traversal ─
light_manager = UsdGeom.Xform.Define(stage, "/World/LightManager")
light_list_api = UsdLux.LightListAPI.Apply(light_manager.GetPrim())
# valid, consumedByRenderer, or consumedByUSD
light_list_api.CreateLightListCacheBehaviorAttr(UsdLux.Tokens.consumedByRenderer)
light_list_api.GetLightListRel().SetTargets([
    Sdf.Path("/World/KeyLight"),
    Sdf.Path("/World/SkyDome"),
])

# ── LightAPI: the common light interface applied to any prim ──────────────
generic_light = UsdGeom.Xform.Define(stage, "/World/GenericLight")
light_api = UsdLux.LightAPI.Apply(generic_light.GetPrim())
light_api.CreateIntensityAttr(5000.0)
light_api.CreateColorAttr(Gf.Vec3f(1.0, 0.9, 0.8))
light_api.CreateExposureAttr(0.0)
light_api.CreateEnableColorTemperatureAttr(True)
light_api.CreateColorTemperatureAttr(5500.0)
light_api.CreateDiffuseAttr(1.0)
light_api.CreateSpecularAttr(1.0)

stage.GetRootLayer().Save()
