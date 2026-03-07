"""
Generates hermiteCurves.usda — demonstrates UsdGeomHermiteCurves, which
require both control points and tangent vectors at each point. The curve
passes through every control point; the tangent governs the local slope.

Run:
    python HermiteCurves.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("hermiteCurves.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Single sine-like Hermite curve ────────────────────────────────────────────
sine = UsdGeom.HermiteCurves.Define(stage, "/World/SineLikeCurve")
sine.GetCurveVertexCountsAttr().Set([4])
sine.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(1, 1, 0),
    Gf.Vec3f(2, -1, 0), Gf.Vec3f(3, 0, 0),
])
sine.GetTangentsAttr().Set([
    Gf.Vec3f(1, 2, 0), Gf.Vec3f(1, 0, 0),
    Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, 2, 0),
])
w_attr = sine.CreateWidthsAttr()
w_attr.Set([0.05])
sine.SetWidthsInterpolation(UsdGeom.Tokens.constant)
sine.GetExtentAttr().Set([Gf.Vec3f(0, -1, 0), Gf.Vec3f(3, 1, 0)])

# ── Two curves demonstrating tangent influence ────────────────────────────────
demo = UsdGeom.HermiteCurves.Define(stage, "/World/TangentDemo")
demo.GetCurveVertexCountsAttr().Set([2, 2])
demo.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(2, 0, 0),
    Gf.Vec3f(0, 0, 1), Gf.Vec3f(2, 0, 1),
])
demo.GetTangentsAttr().Set([
    Gf.Vec3f(1, 3, 0),  Gf.Vec3f(1, 3, 0),
    Gf.Vec3f(1, -3, 0), Gf.Vec3f(1, -3, 0),
])
w_attr = demo.CreateWidthsAttr()
w_attr.Set([0.04])
demo.SetWidthsInterpolation(UsdGeom.Tokens.constant)
demo.GetExtentAttr().Set([Gf.Vec3f(0, -1, 0), Gf.Vec3f(2, 1, 1)])
demo.AddTranslateOp().Set(Gf.Vec3d(5, 0, 0))

# ── Animated Hermite curve ────────────────────────────────────────────────────
anim = UsdGeom.HermiteCurves.Define(stage, "/World/AnimatedCurve")
anim.GetCurveVertexCountsAttr().Set([3])
anim.GetPointsAttr().Set([
    Gf.Vec3f(-1, 0, 0), Gf.Vec3f(0, 0, 0), Gf.Vec3f(1, 0, 0),
])
tang_attr = anim.GetTangentsAttr()
tang_attr.Set([Gf.Vec3f(1, 2, 0), Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, -2, 0)], 0)
tang_attr.Set([Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, 0, 0)], 12)
tang_attr.Set([Gf.Vec3f(1,-2, 0), Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, 2, 0)], 24)
w_attr = anim.CreateWidthsAttr()
w_attr.Set([0.06])
anim.SetWidthsInterpolation(UsdGeom.Tokens.constant)
anim.GetExtentAttr().Set([Gf.Vec3f(-1, -1, 0), Gf.Vec3f(1, 1, 0)])
anim.AddTranslateOp().Set(Gf.Vec3d(11, 0, 0))

stage.GetRootLayer().Save()
print("Wrote hermiteCurves.usda")
