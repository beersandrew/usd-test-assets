from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

stage = Usd.Stage.CreateNew("envLights.usda")

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ── DistantLight: infinitely distant directional light (e.g., sun) ────────
sun = UsdLux.DistantLight.Define(stage, "/World/Sun")
# Angular diameter in degrees (sun = 0.53°)
sun.CreateAngleAttr(0.53)
sun.CreateIntensityAttr(100000.0)
sun.CreateColorAttr(Gf.Vec3f(1.0, 0.98, 0.9))
xform_api = UsdGeom.XformCommonAPI(sun)
xform_api.SetRotate(Gf.Vec3f(-45, 30, 0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

# ── DomeLight: environment IBL dome ───────────────────────────────────────
sky_dome = UsdLux.DomeLight.Define(stage, "/World/SkyDome")
sky_dome.CreateIntensityAttr(1.0)
sky_dome.CreateTextureFileAttr("./textures/hdri_sky.exr")
sky_dome.CreateTextureFormatAttr(UsdLux.Tokens.latlong)
UsdGeom.XformCommonAPI(sky_dome).SetRotate(
    Gf.Vec3f(0, 45, 0), UsdGeom.XformCommonAPI.RotationOrderXYZ
)

# PortalLight must be a child of DomeLight
portal = UsdLux.PortalLight.Define(stage, "/World/SkyDome/WindowPortal")
portal.CreateWidthAttr(200.0)
portal.CreateHeightAttr(300.0)
UsdGeom.XformCommonAPI(portal).SetTranslate(Gf.Vec3d(0, 150, -250))

# ── DomeLight_1: newer dome with configurable pole axis ───────────────────
night_sky = UsdLux.DomeLight_1.Define(stage, "/World/NightSky")
night_sky.CreateIntensityAttr(0.5)
night_sky.CreateTextureFileAttr("./textures/night_sky.exr")
# guideRadius: hint for visualizers
night_sky.GetPrim().CreateAttribute(
    "guideRadius", Sdf.ValueTypeNames.Float
).Set(500.0)

stage.GetRootLayer().Save()
