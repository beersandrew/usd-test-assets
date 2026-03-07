"""Generate volume.usda, openVDB.usda, and field3D.usda programmatically.

Run:
    python Volume.py
"""

from pxr import Usd, UsdGeom, Sdf, Vt

# ── volume.usda ───────────────────────────────────────────────────────────────

stage = Usd.Stage.CreateNew("volume.usda")
stage.SetDefaultPrim(stage.DefinePrim("/World"))
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

world = UsdGeom.Xform.Define(stage, "/World")

# UsdVolVolume prim — contains relationships to field prims
explosion = stage.DefinePrim("/World/PyroExplosion", "Volume")

# Field relationships in the "field:<name>" namespace
density_rel = explosion.CreateRelationship("field:density")
density_rel.SetTargets([Sdf.Path("/World/PyroExplosion/DensityField")])

temp_rel = explosion.CreateRelationship("field:temperature")
temp_rel.SetTargets([Sdf.Path("/World/PyroExplosion/TemperatureField")])

vel_rel = explosion.CreateRelationship("field:velocity")
vel_rel.SetTargets([Sdf.Path("/World/PyroExplosion/VelocityField")])

# Translate the volume up in Y
translate_attr = explosion.CreateAttribute("xformOp:translate", Sdf.ValueTypeNames.Double3)
translate_attr.Set((0.0, 100.0, 0.0))
xform_order = explosion.CreateAttribute(
    "xformOpOrder", Sdf.ValueTypeNames.TokenArray, custom=False, variability=Sdf.VariabilityUniform
)
xform_order.Set(Vt.TokenArray(["xformOp:translate"]))

# OpenVDBAsset: density field
density_field = stage.DefinePrim("/World/PyroExplosion/DensityField", "OpenVDBAsset")
density_field.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./vdb/explosion_0001.vdb")
)
density_field.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("density")
density_field.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float")
density_field.CreateAttribute("fieldIndex", Sdf.ValueTypeNames.Int).Set(1)

# OpenVDBAsset: temperature field
temp_field = stage.DefinePrim("/World/PyroExplosion/TemperatureField", "OpenVDBAsset")
temp_field.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./vdb/explosion_0001.vdb")
)
temp_field.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("temperature")
temp_field.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float")

# OpenVDBAsset: velocity field (float3 for vector data)
vel_field = stage.DefinePrim("/World/PyroExplosion/VelocityField", "OpenVDBAsset")
vel_field.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./vdb/explosion_velocity_0001.vdb")
)
vel_field.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("vel")
vel_field.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float3")

stage.GetRootLayer().Save()
print("Saved volume.usda")

# ── openVDB.usda ──────────────────────────────────────────────────────────────

stage2 = Usd.Stage.CreateNew("openVDB.usda")
stage2.SetDefaultPrim(stage2.DefinePrim("/World"))
UsdGeom.SetStageMetersPerUnit(stage2, 0.01)
UsdGeom.SetStageUpAxis(stage2, UsdGeom.Tokens.y)
stage2.SetTimeCodesPerSecond(24)

UsdGeom.Xform.Define(stage2, "/World")

# Smoke column: fog volume with time-varying VDB sequence
smoke = stage2.DefinePrim("/World/SmokeColumn", "Volume")
smoke.CreateRelationship("field:density").SetTargets(
    [Sdf.Path("/World/SmokeColumn/SmokeDensity")]
)
smoke.CreateRelationship("field:albedo").SetTargets(
    [Sdf.Path("/World/SmokeColumn/SmokeAlbedo")]
)

smoke_density = stage2.DefinePrim("/World/SmokeColumn/SmokeDensity", "OpenVDBAsset")
smoke_density.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./vdb/smoke.####.vdb")  # #### = frame number placeholder
)
smoke_density.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("density")
smoke_density.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float")
smoke_density.CreateAttribute("fieldPurpose", Sdf.ValueTypeNames.Token).Set("default")

smoke_albedo = stage2.DefinePrim("/World/SmokeColumn/SmokeAlbedo", "OpenVDBAsset")
smoke_albedo.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./vdb/smoke.####.vdb")
)
smoke_albedo.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("albedo")
smoke_albedo.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float3")

# Water surface: level set (signed distance field)
water = stage2.DefinePrim("/World/WaterSurface", "Volume")
water.CreateRelationship("field:levelSet").SetTargets(
    [Sdf.Path("/World/WaterSurface/SdfField")]
)

sdf_field = stage2.DefinePrim("/World/WaterSurface/SdfField", "OpenVDBAsset")
sdf_field.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./vdb/water_sdf.vdb")
)
sdf_field.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("surface")
sdf_field.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float")
sdf_field.CreateAttribute("fieldPurpose", Sdf.ValueTypeNames.Token).Set("default")

stage2.GetRootLayer().Save()
print("Saved openVDB.usda")

# ── field3D.usda ──────────────────────────────────────────────────────────────

stage3 = Usd.Stage.CreateNew("field3D.usda")
stage3.SetDefaultPrim(stage3.DefinePrim("/World"))
UsdGeom.SetStageMetersPerUnit(stage3, 0.01)
UsdGeom.SetStageUpAxis(stage3, UsdGeom.Tokens.y)
stage3.SetTimeCodesPerSecond(24)

UsdGeom.Xform.Define(stage3, "/World")

# Cloud volume using Field3D format (older ILM/Houdini format)
cloud = stage3.DefinePrim("/World/CloudVolume", "Volume")
cloud.CreateRelationship("field:density").SetTargets(
    [Sdf.Path("/World/CloudVolume/CloudDensity")]
)

cloud_density = stage3.DefinePrim("/World/CloudVolume/CloudDensity", "Field3DAsset")
cloud_density.CreateAttribute("filePath", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./f3d/cumulus_cloud.f3d")
)
cloud_density.CreateAttribute("fieldName", Sdf.ValueTypeNames.Token).Set("density")
cloud_density.CreateAttribute("fieldDataType", Sdf.ValueTypeNames.Token).Set("float")
cloud_density.CreateAttribute("fieldPurpose", Sdf.ValueTypeNames.Token).Set("default")

stage3.GetRootLayer().Save()
print("Saved field3D.usda")
