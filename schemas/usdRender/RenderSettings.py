"""
RenderSettings.py — generates renderSettings.usda programmatically.

Demonstrates UsdRenderSettings, UsdRenderProduct, and UsdRenderVar using
the UsdRender module where available, falling back to generic prim/attribute
creation otherwise.

Run:
    python RenderSettings.py
"""

from pxr import Usd, UsdGeom, Gf, Sdf

try:
    from pxr import UsdRender
    HAS_USD_RENDER = True
except ImportError:
    HAS_USD_RENDER = False

stage = Usd.Stage.CreateNew("renderSettings.usda")

# Stage-level metadata
root_layer = stage.GetRootLayer()
stage.SetMetadata("defaultPrim", "World")
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# Root Xform
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# ── RenderSettings prim ────────────────────────────────────────────────────────
if HAS_USD_RENDER:
    render_settings = UsdRender.Settings.Define(stage, "/World/RenderSettings")
    rs_prim = render_settings.GetPrim()
else:
    rs_prim = stage.DefinePrim("/World/RenderSettings", "RenderSettings")

# Camera relationship
rs_prim.CreateRelationship("camera").SetTargets([Sdf.Path("/World/Camera")])

# Resolution
res_attr = rs_prim.CreateAttribute("resolution", Sdf.ValueTypeNames.Int2)
res_attr.Set(Gf.Vec2i(1920, 1080))

# Pixel aspect ratio
rs_prim.CreateAttribute("pixelAspectRatio", Sdf.ValueTypeNames.Float).Set(1.0)

# Aspect ratio conform policy
rs_prim.CreateAttribute(
    "aspectRatioConformPolicy", Sdf.ValueTypeNames.Token
).Set("expandAperture")

# Data window (normalized)
rs_prim.CreateAttribute("dataWindowNDC", Sdf.ValueTypeNames.Float4).Set(
    Gf.Vec4f(0, 0, 1, 1)
)

# Shutter
rs_prim.CreateAttribute("instantaneousShutter", Sdf.ValueTypeNames.Bool).Set(False)
rs_prim.CreateAttribute("shutterInterval", Sdf.ValueTypeNames.Float2).Set(
    Gf.Vec2f(0.0, 0.5)
)

# Products relationship
rs_prim.CreateRelationship("products").SetTargets([
    Sdf.Path("/World/RenderSettings/Beauty"),
    Sdf.Path("/World/RenderSettings/AOVs"),
])

# ── Beauty RenderProduct ───────────────────────────────────────────────────────
if HAS_USD_RENDER:
    beauty_product = UsdRender.Product.Define(stage, "/World/RenderSettings/Beauty")
    bp = beauty_product.GetPrim()
else:
    bp = stage.DefinePrim("/World/RenderSettings/Beauty", "RenderProduct")

bp.CreateAttribute("productName", Sdf.ValueTypeNames.Token).Set(
    "/renders/beauty/beauty.####.exr"
)
bp.CreateAttribute("productType", Sdf.ValueTypeNames.Token).Set("raster")
bp.CreateRelationship("camera").SetTargets([Sdf.Path("/World/Camera")])
bp.CreateRelationship("orderedVars").SetTargets([
    Sdf.Path("/World/RenderSettings/Beauty/Ci"),
    Sdf.Path("/World/RenderSettings/Beauty/Alpha"),
])

# Beauty/Ci RenderVar
if HAS_USD_RENDER:
    ci_var = UsdRender.Var.Define(stage, "/World/RenderSettings/Beauty/Ci")
    ci = ci_var.GetPrim()
else:
    ci = stage.DefinePrim("/World/RenderSettings/Beauty/Ci", "RenderVar")
ci.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set("Ci")
ci.CreateAttribute("dataType", Sdf.ValueTypeNames.Token).Set("color3f")
ci.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set("raw")

# Beauty/Alpha RenderVar
if HAS_USD_RENDER:
    alpha_var = UsdRender.Var.Define(stage, "/World/RenderSettings/Beauty/Alpha")
    alpha = alpha_var.GetPrim()
else:
    alpha = stage.DefinePrim("/World/RenderSettings/Beauty/Alpha", "RenderVar")
alpha.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set("a")
alpha.CreateAttribute("dataType", Sdf.ValueTypeNames.Token).Set("float")
alpha.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set("raw")

# ── AOVs RenderProduct ────────────────────────────────────────────────────────
if HAS_USD_RENDER:
    aovs_product = UsdRender.Product.Define(stage, "/World/RenderSettings/AOVs")
    ap = aovs_product.GetPrim()
else:
    ap = stage.DefinePrim("/World/RenderSettings/AOVs", "RenderProduct")

ap.CreateAttribute("productName", Sdf.ValueTypeNames.Token).Set(
    "/renders/aovs/aov.####.exr"
)
ap.CreateAttribute("productType", Sdf.ValueTypeNames.Token).Set("raster")
ap.CreateRelationship("orderedVars").SetTargets([
    Sdf.Path("/World/RenderSettings/AOVs/Diffuse"),
    Sdf.Path("/World/RenderSettings/AOVs/Specular"),
    Sdf.Path("/World/RenderSettings/AOVs/Normal"),
    Sdf.Path("/World/RenderSettings/AOVs/Z"),
])

# AOV vars
aov_vars = [
    ("Diffuse",  "diffuse",  "color3f",   "raw"),
    ("Specular", "specular", "color3f",   "raw"),
    ("Normal",   "Nn",       "normal3f",  "raw"),
    ("Z",        "z",        "float",     "raw"),
]
for name, src, dtype, stype in aov_vars:
    path = f"/World/RenderSettings/AOVs/{name}"
    if HAS_USD_RENDER:
        v = UsdRender.Var.Define(stage, path).GetPrim()
    else:
        v = stage.DefinePrim(path, "RenderVar")
    v.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set(src)
    v.CreateAttribute("dataType",   Sdf.ValueTypeNames.Token).Set(dtype)
    v.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set(stype)

# ── Camera ─────────────────────────────────────────────────────────────────────
cam = UsdGeom.Camera.Define(stage, "/World/Camera")
cam.CreateClippingRangeAttr(Gf.Vec2f(1, 10000))
cam.CreateFocalLengthAttr(50.0)
cam.CreateFocusDistanceAttr(500.0)
cam.CreateFStopAttr(5.6)
cam.CreateHorizontalApertureAttr(36.0)
cam.CreateVerticalApertureAttr(24.0)
UsdGeom.XformCommonAPI(cam).SetTranslate(Gf.Vec3d(0, 150, 600))

stage.GetRootLayer().Save()
print("Saved renderSettings.usda")
