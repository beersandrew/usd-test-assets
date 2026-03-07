from pxr import Usd, UsdGeom, UsdLux, Gf

stage = Usd.Stage.CreateNew("punctualLights.usda")

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ── SphereLight: emits from a sphere surface ──────────────────────────────
key_light = UsdLux.SphereLight.Define(stage, "/World/KeyLight")
# Radius of the sphere light source (in scene units)
key_light.CreateRadiusAttr(5.0)
# Luminous intensity in nits
key_light.CreateIntensityAttr(50000.0)
key_light.CreateColorAttr(Gf.Vec3f(1.0, 0.95, 0.8))
# Treat as a point light (radius=0 behavior) for distant scenes
key_light.CreateTreatAsPointAttr(False)
key_light.CreateNormalizeAttr(True)
UsdGeom.XformCommonAPI(key_light).SetTranslate(Gf.Vec3d(200, 300, 100))

# ── DiskLight: emits from a circular disk ─────────────────────────────────
fill_light = UsdLux.DiskLight.Define(stage, "/World/FillLight")
fill_light.CreateRadiusAttr(30.0)
fill_light.CreateIntensityAttr(20000.0)
fill_light.CreateColorAttr(Gf.Vec3f(0.8, 0.9, 1.0))
UsdGeom.XformCommonAPI(fill_light).SetTranslate(Gf.Vec3d(-300, 200, 50))

# ── RectLight: emits from a rectangular area ──────────────────────────────
window_light = UsdLux.RectLight.Define(stage, "/World/WindowLight")
window_light.CreateWidthAttr(120.0)
window_light.CreateHeightAttr(180.0)
window_light.CreateIntensityAttr(15000.0)
window_light.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 0.95))
# Optional texture on the light surface
window_light.CreateTextureFileAttr("./textures/sky.exr")
UsdGeom.XformCommonAPI(window_light).SetTranslate(Gf.Vec3d(0, 150, -200))

# ── CylinderLight: emits from a cylinder surface ──────────────────────────
tube_light = UsdLux.CylinderLight.Define(stage, "/World/TubeLight")
tube_light.CreateRadiusAttr(2.0)
tube_light.CreateLengthAttr(100.0)
tube_light.CreateIntensityAttr(8000.0)
tube_light.CreateColorAttr(Gf.Vec3f(1.0, 0.85, 0.7))
tube_light.CreateTreatAsLineAttr(False)
UsdGeom.XformCommonAPI(tube_light).SetTranslate(Gf.Vec3d(0, 250, 0))

stage.GetRootLayer().Save()
