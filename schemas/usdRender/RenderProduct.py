"""
RenderProduct.py — generates renderProduct.usda programmatically.

Demonstrates a stereo render setup using UsdRenderProduct and UsdRenderVar,
with separate left/right eye cameras and per-eye render products.

Run:
    python RenderProduct.py
"""

from pxr import Usd, UsdGeom, Gf, Sdf

try:
    from pxr import UsdRender
    HAS_USD_RENDER = True
except ImportError:
    HAS_USD_RENDER = False

stage = Usd.Stage.CreateNew("renderProduct.usda")

# Stage-level metadata
stage.SetMetadata("defaultPrim", "World")
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# Root Xform
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# ── StereoRender RenderSettings ────────────────────────────────────────────────
if HAS_USD_RENDER:
    stereo_rs = UsdRender.Settings.Define(stage, "/World/StereoRender")
    rs_prim = stereo_rs.GetPrim()
else:
    rs_prim = stage.DefinePrim("/World/StereoRender", "RenderSettings")

rs_prim.CreateAttribute("resolution", Sdf.ValueTypeNames.Int2).Set(
    Gf.Vec2i(3840, 1080)  # Side-by-side stereo
)
rs_prim.CreateRelationship("products").SetTargets([
    Sdf.Path("/World/StereoRender/LeftEye"),
    Sdf.Path("/World/StereoRender/RightEye"),
])

# Helper to define a RenderProduct with Beauty and Depth vars
def define_eye_product(eye_name, file_prefix, camera_path):
    prod_path = f"/World/StereoRender/{eye_name}"
    if HAS_USD_RENDER:
        prod = UsdRender.Product.Define(stage, prod_path).GetPrim()
    else:
        prod = stage.DefinePrim(prod_path, "RenderProduct")

    prod.CreateAttribute("productName", Sdf.ValueTypeNames.Token).Set(
        f"/renders/stereo/{file_prefix}.####.exr"
    )
    prod.CreateAttribute("productType", Sdf.ValueTypeNames.Token).Set("raster")
    prod.CreateRelationship("camera").SetTargets([Sdf.Path(camera_path)])
    prod.CreateRelationship("orderedVars").SetTargets([
        Sdf.Path(f"{prod_path}/Beauty"),
        Sdf.Path(f"{prod_path}/Depth"),
    ])

    # Beauty RenderVar
    if HAS_USD_RENDER:
        bv = UsdRender.Var.Define(stage, f"{prod_path}/Beauty").GetPrim()
    else:
        bv = stage.DefinePrim(f"{prod_path}/Beauty", "RenderVar")
    bv.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set("Ci")
    bv.CreateAttribute("dataType",   Sdf.ValueTypeNames.Token).Set("color3f")
    bv.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set("raw")

    # Depth RenderVar
    if HAS_USD_RENDER:
        dv = UsdRender.Var.Define(stage, f"{prod_path}/Depth").GetPrim()
    else:
        dv = stage.DefinePrim(f"{prod_path}/Depth", "RenderVar")
    dv.CreateAttribute("sourceName", Sdf.ValueTypeNames.Token).Set("z")
    dv.CreateAttribute("dataType",   Sdf.ValueTypeNames.Token).Set("float")
    dv.CreateAttribute("sourceType", Sdf.ValueTypeNames.Token).Set("raw")

define_eye_product("LeftEye",  "left",  "/World/LeftCamera")
define_eye_product("RightEye", "right", "/World/RightCamera")

# ── Stereo cameras ─────────────────────────────────────────────────────────────
left_cam = UsdGeom.Camera.Define(stage, "/World/LeftCamera")
left_cam.CreateFocalLengthAttr(50.0)
left_cam.CreateHorizontalApertureAttr(36.0)
left_cam.CreateVerticalApertureAttr(24.0)
# Inter-ocular offset: -32 mm (left eye)
UsdGeom.XformCommonAPI(left_cam).SetTranslate(Gf.Vec3d(-32, 150, 600))

right_cam = UsdGeom.Camera.Define(stage, "/World/RightCamera")
right_cam.CreateFocalLengthAttr(50.0)
right_cam.CreateHorizontalApertureAttr(36.0)
right_cam.CreateVerticalApertureAttr(24.0)
# Inter-ocular offset: +32 mm (right eye)
UsdGeom.XformCommonAPI(right_cam).SetTranslate(Gf.Vec3d(32, 150, 600))

stage.GetRootLayer().Save()
print("Saved renderProduct.usda")
