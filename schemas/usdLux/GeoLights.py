from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

stage = Usd.Stage.CreateNew("geoLights.usda")

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# Define the mesh geometry used as a light source
emissive_panel = UsdGeom.Mesh.Define(stage, "/World/EmissivePanel")

# ── MeshLightAPI: turn any mesh into an area light ────────────────────────
emissive_panel_light = UsdGeom.Xform.Define(stage, "/World/EmissivePanelLight")
# Apply MeshLightAPI schema to enable mesh-based lighting
mesh_light_api = UsdLux.MeshLightAPI.Apply(emissive_panel_light.GetPrim())
# The mesh light references the geometry
emissive_panel_light.GetPrim().CreateRelationship("light:geometry").SetTargets(
    [Sdf.Path("/World/EmissivePanel")]
)
mesh_light_api.CreateIntensityAttr(5000.0)
mesh_light_api.CreateColorAttr(Gf.Vec3f(0.9, 0.95, 1.0))

# ── GeometryLight (deprecated): references external geometry ──────────────
# DEPRECATED: use MeshLightAPI instead
legacy_geo_light = UsdLux.GeometryLight.Define(stage, "/World/LegacyGeoLight")
legacy_geo_light.CreateGeometryRel().SetTargets([Sdf.Path("/World/EmissivePanel")])
legacy_geo_light.CreateIntensityAttr(3000.0)

# Define a volume for the volume light
fire_volume = stage.DefinePrim("/World/FireVolume", "Volume")

# ── VolumeLightAPI: emit light from a volume ──────────────────────────────
volume_light_wrapper = UsdGeom.Xform.Define(stage, "/World/VolumeLightWrapper")
volume_light_api = UsdLux.VolumeLightAPI.Apply(volume_light_wrapper.GetPrim())
volume_light_wrapper.GetPrim().CreateRelationship("light:geometry").SetTargets(
    [Sdf.Path("/World/FireVolume")]
)
volume_light_api.CreateIntensityAttr(2000.0)
volume_light_api.CreateColorAttr(Gf.Vec3f(1.0, 0.5, 0.1))

stage.GetRootLayer().Save()
