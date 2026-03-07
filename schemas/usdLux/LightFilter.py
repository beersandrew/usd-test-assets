from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

stage = Usd.Stage.CreateNew("lightFilter.usda")

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ── LightFilter: modifies the light contribution on objects ───────────────
barn_doors = UsdLux.LightFilter.Define(stage, "/World/BarnDoors")
# LightFilters are referenced from lights via light:filters
barn_doors_prim = barn_doors.GetPrim()
barn_doors_prim.CreateAttribute("light:filterType", Sdf.ValueTypeNames.Token).Set("barnDoors")
barn_doors_prim.CreateAttribute("inputs:barnDoors:left", Sdf.ValueTypeNames.Float).Set(0.1)
barn_doors_prim.CreateAttribute("inputs:barnDoors:right", Sdf.ValueTypeNames.Float).Set(0.1)
barn_doors_prim.CreateAttribute("inputs:barnDoors:bottom", Sdf.ValueTypeNames.Float).Set(0.05)
barn_doors_prim.CreateAttribute("inputs:barnDoors:top", Sdf.ValueTypeNames.Float).Set(0.05)

# ── SphereLight referencing the filter ───────────────────────────────────
studio_light = UsdLux.SphereLight.Define(stage, "/World/StudioLight")
studio_light.CreateIntensityAttr(40000.0)
# Reference the light filter
studio_light.GetPrim().CreateRelationship("light:filters").SetTargets(
    [Sdf.Path("/World/BarnDoors")]
)

# ── PluginLightFilter: renderer-specific filter plugin ───────────────────
custom_filter = UsdLux.PluginLightFilter.Define(stage, "/World/CustomFilter")
custom_filter_prim = custom_filter.GetPrim()
custom_filter_prim.CreateAttribute("info:id", Sdf.ValueTypeNames.Token).Set("PxrGoboLightFilter")
custom_filter_prim.CreateAttribute("inputs:map", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./textures/gobo_pattern.exr")
)
custom_filter_prim.CreateAttribute("inputs:density", Sdf.ValueTypeNames.Float).Set(1.0)

stage.GetRootLayer().Save()
