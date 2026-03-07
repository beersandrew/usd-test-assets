"""
RenderPass.py — generates renderPass.usda programmatically.

Demonstrates UsdRenderPass with hero beauty and shadow pre-pass configurations,
including frame ranges, pipeline commands, and separate RenderSettings prims.

Run:
    python RenderPass.py
"""

from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf, Vt

try:
    from pxr import UsdRender
    HAS_USD_RENDER = True
except ImportError:
    HAS_USD_RENDER = False

stage = Usd.Stage.CreateNew("renderPass.usda")

# Stage-level metadata
stage.SetMetadata("defaultPrim", "World")
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# Root Xform
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# ── HeroBeauty RenderPass ──────────────────────────────────────────────────────
if HAS_USD_RENDER:
    hero_pass = UsdRender.Pass.Define(stage, "/World/HeroBeauty")
    hp = hero_pass.GetPrim()
else:
    hp = stage.DefinePrim("/World/HeroBeauty", "RenderPass")

hp.CreateRelationship("renderSource").SetTargets([Sdf.Path("/World/HeroSettings")])
hp.CreateAttribute("passEnabled",  Sdf.ValueTypeNames.Bool).Set(True)
hp.CreateAttribute("frameStart",   Sdf.ValueTypeNames.Int).Set(1001)
hp.CreateAttribute("frameEnd",     Sdf.ValueTypeNames.Int).Set(1100)
hp.CreateAttribute("frameStride",  Sdf.ValueTypeNames.Int).Set(1)
hp.CreateAttribute("command", Sdf.ValueTypeNames.StringArray).Set(
    Vt.StringArray(["prman", "-t:4", "-statsLevel", "2"])
)

# ── ShadowPass RenderPass ──────────────────────────────────────────────────────
if HAS_USD_RENDER:
    shadow_pass = UsdRender.Pass.Define(stage, "/World/ShadowPass")
    sp = shadow_pass.GetPrim()
else:
    sp = stage.DefinePrim("/World/ShadowPass", "RenderPass")

sp.CreateRelationship("renderSource").SetTargets([Sdf.Path("/World/ShadowSettings")])
sp.CreateAttribute("passEnabled", Sdf.ValueTypeNames.Bool).Set(True)
sp.CreateAttribute("frameStart",  Sdf.ValueTypeNames.Int).Set(1001)
sp.CreateAttribute("frameEnd",    Sdf.ValueTypeNames.Int).Set(1100)

# ── HeroSettings RenderSettings ────────────────────────────────────────────────
if HAS_USD_RENDER:
    hero_rs = UsdRender.Settings.Define(stage, "/World/HeroSettings")
    hrsp = hero_rs.GetPrim()
else:
    hrsp = stage.DefinePrim("/World/HeroSettings", "RenderSettings")

hrsp.CreateAttribute("resolution", Sdf.ValueTypeNames.Int2).Set(
    Gf.Vec2i(2048, 858)  # 2.39:1 cinemascope
)
hrsp.CreateRelationship("camera").SetTargets([Sdf.Path("/World/HeroCamera")])
hrsp.CreateRelationship("products").SetTargets([
    Sdf.Path("/World/HeroSettings/BeautyProduct")
])

# HeroSettings/BeautyProduct
if HAS_USD_RENDER:
    hero_prod = UsdRender.Product.Define(stage, "/World/HeroSettings/BeautyProduct")
    hbp = hero_prod.GetPrim()
else:
    hbp = stage.DefinePrim("/World/HeroSettings/BeautyProduct", "RenderProduct")

hbp.CreateAttribute("productName", Sdf.ValueTypeNames.Token).Set(
    "/renders/hero/beauty.####.exr"
)
hbp.CreateRelationship("orderedVars").SetTargets([
    Sdf.Path("/World/HeroSettings/BeautyProduct/Ci")
])

if HAS_USD_RENDER:
    ci_v = UsdRender.Var.Define(stage, "/World/HeroSettings/BeautyProduct/Ci").GetPrim()
else:
    ci_v = stage.DefinePrim("/World/HeroSettings/BeautyProduct/Ci", "RenderVar")
ci_v.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set("Ci")
ci_v.CreateAttribute("dataType",   Sdf.ValueTypeNames.Token).Set("color3f")
ci_v.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set("raw")

# ── ShadowSettings RenderSettings ─────────────────────────────────────────────
if HAS_USD_RENDER:
    shadow_rs = UsdRender.Settings.Define(stage, "/World/ShadowSettings")
    srsp = shadow_rs.GetPrim()
else:
    srsp = stage.DefinePrim("/World/ShadowSettings", "RenderSettings")

srsp.CreateAttribute("resolution", Sdf.ValueTypeNames.Int2).Set(
    Gf.Vec2i(4096, 4096)  # High-res shadow map
)
srsp.CreateRelationship("camera").SetTargets([Sdf.Path("/World/SunLight")])
srsp.CreateRelationship("products").SetTargets([
    Sdf.Path("/World/ShadowSettings/ShadowProduct")
])

# ShadowSettings/ShadowProduct
if HAS_USD_RENDER:
    shadow_prod = UsdRender.Product.Define(stage, "/World/ShadowSettings/ShadowProduct")
    spp = shadow_prod.GetPrim()
else:
    spp = stage.DefinePrim("/World/ShadowSettings/ShadowProduct", "RenderProduct")

spp.CreateAttribute("productName", Sdf.ValueTypeNames.Token).Set(
    "/renders/shadow/shadow.####.exr"
)
spp.CreateRelationship("orderedVars").SetTargets([
    Sdf.Path("/World/ShadowSettings/ShadowProduct/Z")
])

if HAS_USD_RENDER:
    z_v = UsdRender.Var.Define(stage, "/World/ShadowSettings/ShadowProduct/Z").GetPrim()
else:
    z_v = stage.DefinePrim("/World/ShadowSettings/ShadowProduct/Z", "RenderVar")
z_v.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set("z")
z_v.CreateAttribute("dataType",   Sdf.ValueTypeNames.Token).Set("float")
z_v.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set("raw")

# ── HeroCamera ─────────────────────────────────────────────────────────────────
hero_cam = UsdGeom.Camera.Define(stage, "/World/HeroCamera")
hero_cam.CreateFocalLengthAttr(65.0)
hero_cam.CreateHorizontalApertureAttr(36.0)
hero_cam.CreateVerticalApertureAttr(15.1)
UsdGeom.XformCommonAPI(hero_cam).SetTranslate(Gf.Vec3d(0, 120, 800))

# ── SunLight (DistantLight used as shadow camera proxy) ────────────────────────
try:
    sun = UsdLux.DistantLight.Define(stage, "/World/SunLight")
    sun.CreateAngleAttr(0.53)
    sun.CreateIntensityAttr(100000.0)
except AttributeError:
    # Fallback for older USD versions
    sun_prim = stage.DefinePrim("/World/SunLight", "DistantLight")
    sun_prim.CreateAttribute("inputs:angle",     Sdf.ValueTypeNames.Float).Set(0.53)
    sun_prim.CreateAttribute("inputs:intensity", Sdf.ValueTypeNames.Float).Set(100000.0)
    sun = UsdGeom.Xformable(sun_prim)

UsdGeom.XformCommonAPI(sun).SetRotate(Gf.Vec3f(-60, 30, 0))

stage.GetRootLayer().Save()
print("Saved renderPass.usda")
