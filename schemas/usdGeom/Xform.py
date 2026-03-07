"""
Generates xform.usda — demonstrates UsdGeomXform, UsdGeomScope, and UsdGeomXformCommonAPI.

Run:
    python Xform.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("xform.usda")

# Set stage metadata directly on the root layer (do not use UsdGeom.SetStageUpAxis)
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
root_layer.pseudoRoot.SetInfo("upAxis", "Y")

# Use Sdf to set upAxis metadata
stage.SetMetadata("upAxis", "Y")

# ── World Xform ──────────────────────────────────────────────────────────────
world = UsdGeom.Xform.Define(stage, "/World")

# ── AnimatedXform: translate + rotateXYZ animated over 24 frames ─────────────
anim_xf = UsdGeom.Xform.Define(stage, "/World/AnimatedXform")

translate_op = anim_xf.AddTranslateOp()
translate_op.Set(Gf.Vec3d(0, 0, 0), 0)
translate_op.Set(Gf.Vec3d(5, 3, 0), 12)
translate_op.Set(Gf.Vec3d(10, 0, 0), 24)

rotate_op = anim_xf.AddRotateXYZOp()
rotate_op.Set(Gf.Vec3f(0, 0, 0), 0)
rotate_op.Set(Gf.Vec3f(0, 180, 0), 24)

anim_xf.AddScaleOp().Set(Gf.Vec3d(1, 1, 1))

# ── Scope: lightweight grouping prim with no transform ───────────────────────
scope = UsdGeom.Scope.Define(stage, "/World/Props")

# ── PivotedBox with XformCommonAPI ───────────────────────────────────────────
pivoted = UsdGeom.Xform.Define(stage, "/World/Props/PivotedBox")
pivoted.GetPrim().ApplyAPI(UsdGeom.XformCommonAPI)
xca = UsdGeom.XformCommonAPI(pivoted)
xca.SetTranslate(Gf.Vec3d(2, 0, -3))
xca.SetRotate(Gf.Vec3f(0, 45, 0))   # 45-degree Y rotation
xca.SetScale(Gf.Vec3f(1.5, 1.5, 1.5))
xca.SetPivot(Gf.Vec3f(0.5, 0.5, 0.5))  # pivot at corner of box

# ── Vehicle with nested wheels ───────────────────────────────────────────────
vehicle = UsdGeom.Xform.Define(stage, "/World/Props/Vehicle")
vehicle.AddTranslateOp().Set(Gf.Vec3d(0, 0, 5))

for side, x in [("FL", -1), ("FR", 1)]:
    wheel = UsdGeom.Xform.Define(stage, f"/World/Props/Vehicle/Wheel_{side}")
    wheel.AddTranslateOp().Set(Gf.Vec3d(x, 0, 1))
    spin_op = wheel.AddRotateYOp()
    spin_op.Set(0.0, 0)
    spin_op.Set(720.0, 24)  # two full spins per second at 24fps

# ── WorldSpaceMarker: resetXformStack breaks parent transform inheritance ─────
marker = UsdGeom.Xform.Define(stage, "/World/WorldSpaceMarker")
marker.AddXformOp(UsdGeom.XformOp.TypeTransform, UsdGeom.XformOp.PrecisionDouble,
                  "resetXformStack")
# Use the !resetXformStack! sentinel then a translate
marker_prim = marker.GetPrim()
xform_op_order_attr = marker_prim.CreateAttribute(
    "xformOpOrder", Sdf.ValueTypeNames.TokenArray, variability=Sdf.VariabilityUniform
)
xform_op_order_attr.Set(["!resetXformStack!", "xformOp:translate"])
marker_prim.CreateAttribute(
    "xformOp:translate", Sdf.ValueTypeNames.Double3, variability=Sdf.VariabilityVarying
).Set(Gf.Vec3d(100, 0, 0))

stage.GetRootLayer().Save()
print("Wrote xform.usda")
