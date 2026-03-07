"""
Generates nurbsCurvesAndPatch.usda — demonstrates UsdGeomNurbsCurves
(NURBS curves with knot vectors and rational weights) and UsdGeomNurbsPatch
(bicubic NURBS surface with U/V grid topology).

Run:
    python NurbsCurvesAndPatch.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("nurbsCurvesAndPatch.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── NurbsCurves: a single rational cubic arc ──────────────────────────────────
arc = UsdGeom.NurbsCurves.Define(stage, "/World/NurbsArc")
arc.GetCurveVertexCountsAttr().Set([7])
arc.GetPointsAttr().Set([
    Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, 0.5528, 0), Gf.Vec3f(0.5528, 1, 0),
    Gf.Vec3f(0, 1, 0), Gf.Vec3f(-0.5528, 1, 0), Gf.Vec3f(-1, 0.5528, 0),
    Gf.Vec3f(-1, 0, 0),
])
arc.GetWeightsAttr().Set([1.0, 0.7071, 1.0, 0.7071, 1.0, 0.7071, 1.0])
arc.GetOrderAttr().Set([4])
arc.GetKnotsAttr().Set([0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0])
arc.GetRangesAttr().Set([Gf.Vec2d(0, 1)])
w_attr = arc.CreateWidthsAttr()
w_attr.Set([0.04])
arc.SetWidthsInterpolation(UsdGeom.Tokens.constant)
arc.GetExtentAttr().Set([Gf.Vec3f(-1, 0, 0), Gf.Vec3f(1, 1, 0)])
arc.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

# ── NurbsCurves: two open cubic NURBS curves ──────────────────────────────────
two = UsdGeom.NurbsCurves.Define(stage, "/World/TwoNurbsCurves")
two.GetCurveVertexCountsAttr().Set([5, 5])
two.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0.5, 1, 0), Gf.Vec3f(1.5, -0.5, 0),
    Gf.Vec3f(2.5, 1, 0), Gf.Vec3f(3, 0, 0),
    Gf.Vec3f(0, 0, 1), Gf.Vec3f(0.5, 0.5, 1), Gf.Vec3f(1.5, -0.3, 1),
    Gf.Vec3f(2.5, 0.7, 1), Gf.Vec3f(3, 0, 1),
])
two.GetOrderAttr().Set([4, 4])
knots_5_4 = [0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0]
two.GetKnotsAttr().Set(knots_5_4 + knots_5_4)
two.GetRangesAttr().Set([Gf.Vec2d(0, 1), Gf.Vec2d(0, 1)])
w_attr = two.CreateWidthsAttr()
w_attr.Set([0.05])
two.SetWidthsInterpolation(UsdGeom.Tokens.constant)
two.GetExtentAttr().Set([Gf.Vec3f(0, -0.5, 0), Gf.Vec3f(3, 1, 1)])
two.AddTranslateOp().Set(Gf.Vec3d(4, 0, 0))

# ── NurbsPatch: bicubic surface ───────────────────────────────────────────────
patch = UsdGeom.NurbsPatch.Define(stage, "/World/NurbsSurface")
patch.GetUVertexCountAttr().Set(4)
patch.GetVVertexCountAttr().Set(4)
patch.GetUOrderAttr().Set(4)
patch.GetVOrderAttr().Set(4)
patch.GetUKnotsAttr().Set([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0])
patch.GetVKnotsAttr().Set([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0])
patch.GetURangeAttr().Set(Gf.Vec2d(0, 1))
patch.GetVRangeAttr().Set(Gf.Vec2d(0, 1))
patch.GetPointsAttr().Set([
    Gf.Vec3f(-1.5, 0,  1.5), Gf.Vec3f(-0.5, 1,  1.5),
    Gf.Vec3f( 0.5,-1,  1.5), Gf.Vec3f( 1.5, 0,  1.5),
    Gf.Vec3f(-1.5, 0,  0.5), Gf.Vec3f(-0.5, 0.5, 0.5),
    Gf.Vec3f( 0.5,-0.5,0.5), Gf.Vec3f( 1.5, 0,  0.5),
    Gf.Vec3f(-1.5, 0, -0.5), Gf.Vec3f(-0.5, 0.5,-0.5),
    Gf.Vec3f( 0.5,-0.5,-0.5),Gf.Vec3f( 1.5, 0, -0.5),
    Gf.Vec3f(-1.5, 0, -1.5), Gf.Vec3f(-0.5, 1, -1.5),
    Gf.Vec3f( 0.5,-1, -1.5), Gf.Vec3f( 1.5, 0, -1.5),
])
patch.GetPointWeightsAttr().Set([1.0] * 16)
patch.GetExtentAttr().Set([Gf.Vec3f(-1.5, -1, -1.5), Gf.Vec3f(1.5, 1, 1.5)])
patch.GetDoubleSidedAttr().Set(True)
patch.AddTranslateOp().Set(Gf.Vec3d(0, 0, 5))

stage.GetRootLayer().Save()
print("Wrote nurbsCurvesAndPatch.usda")
