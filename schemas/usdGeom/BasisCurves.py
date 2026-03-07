"""
Generates basisCurves.usda — demonstrates UsdGeomBasisCurves with linear,
bezier, bspline, catmullRom basis types, and a periodic (closed) variant.

Run:
    python BasisCurves.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("basisCurves.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Linear curves ─────────────────────────────────────────────────────────────
linear = UsdGeom.BasisCurves.Define(stage, "/World/LinearCurves")
linear.GetTypeAttr().Set(UsdGeom.Tokens.linear)
linear.GetCurveVertexCountsAttr().Set([4, 3])
linear.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(1, 0, 0), Gf.Vec3f(1, 1, 0), Gf.Vec3f(1, 2, 0),
    Gf.Vec3f(3, 0, 0), Gf.Vec3f(4, 1, 0), Gf.Vec3f(5, 0, 0),
])
widths_attr = linear.CreateWidthsAttr()
widths_attr.Set([0.05, 0.05, 0.05, 0.05,  0.08, 0.08, 0.08])
linear.SetWidthsInterpolation(UsdGeom.Tokens.vertex)
linear.GetExtentAttr().Set([Gf.Vec3f(0, 0, 0), Gf.Vec3f(5, 2, 0)])
linear.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

# ── Bezier curves ─────────────────────────────────────────────────────────────
bezier = UsdGeom.BasisCurves.Define(stage, "/World/BezierCurves")
bezier.GetTypeAttr().Set(UsdGeom.Tokens.cubic)
bezier.GetBasisAttr().Set(UsdGeom.Tokens.bezier)
bezier.GetCurveVertexCountsAttr().Set([4])
bezier.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0, 2, 0),
    Gf.Vec3f(2, -1, 0), Gf.Vec3f(2, 1, 0),
])
w_attr = bezier.CreateWidthsAttr()
w_attr.Set([0.05, 0.1])
bezier.SetWidthsInterpolation(UsdGeom.Tokens.varying)
bezier.GetExtentAttr().Set([Gf.Vec3f(0, -1, 0), Gf.Vec3f(2, 2, 0)])
bezier.AddTranslateOp().Set(Gf.Vec3d(0, 0, 3))

# ── BSpline curves ────────────────────────────────────────────────────────────
bspline = UsdGeom.BasisCurves.Define(stage, "/World/BSplineCurves")
bspline.GetTypeAttr().Set(UsdGeom.Tokens.cubic)
bspline.GetBasisAttr().Set(UsdGeom.Tokens.bspline)
bspline.GetCurveVertexCountsAttr().Set([6])
bspline.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0.5, 1, 0), Gf.Vec3f(1, 0, 0),
    Gf.Vec3f(1.5, -1, 0), Gf.Vec3f(2, 0, 0), Gf.Vec3f(2.5, 1, 0),
])
w_attr = bspline.CreateWidthsAttr()
w_attr.Set([0.06, 0.06, 0.06, 0.06])
bspline.SetWidthsInterpolation(UsdGeom.Tokens.varying)
bspline.GetExtentAttr().Set([Gf.Vec3f(0, -1, 0), Gf.Vec3f(2.5, 1, 0)])
bspline.AddTranslateOp().Set(Gf.Vec3d(0, 0, 6))

# ── CatmullRom curves ─────────────────────────────────────────────────────────
catmull = UsdGeom.BasisCurves.Define(stage, "/World/CatmullRomCurves")
catmull.GetTypeAttr().Set(UsdGeom.Tokens.cubic)
catmull.GetBasisAttr().Set(UsdGeom.Tokens.catmullRom)
catmull.GetCurveVertexCountsAttr().Set([6])
catmull.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0.5, 0.8, 0), Gf.Vec3f(1, 0.2, 0),
    Gf.Vec3f(1.5, 1.0, 0), Gf.Vec3f(2, 0.3, 0), Gf.Vec3f(2.5, 0.7, 0),
])
w_attr = catmull.CreateWidthsAttr()
w_attr.Set([0.06, 0.06, 0.06, 0.06])
catmull.SetWidthsInterpolation(UsdGeom.Tokens.varying)
catmull.GetExtentAttr().Set([Gf.Vec3f(0, 0, 0), Gf.Vec3f(2.5, 1, 0)])
catmull.AddTranslateOp().Set(Gf.Vec3d(0, 0, 9))

# ── Periodic (closed) BSpline ─────────────────────────────────────────────────
closed = UsdGeom.BasisCurves.Define(stage, "/World/ClosedBSpline")
closed.GetTypeAttr().Set(UsdGeom.Tokens.cubic)
closed.GetBasisAttr().Set(UsdGeom.Tokens.bspline)
closed.GetWrapAttr().Set(UsdGeom.Tokens.periodic)
closed.GetCurveVertexCountsAttr().Set([6])
closed.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0.5, 1, 0), Gf.Vec3f(1.5, 1, 0),
    Gf.Vec3f(2, 0, 0), Gf.Vec3f(1.5, -1, 0), Gf.Vec3f(0.5, -1, 0),
])
w_attr = closed.CreateWidthsAttr()
w_attr.Set([0.08])
closed.SetWidthsInterpolation(UsdGeom.Tokens.constant)
closed.GetExtentAttr().Set([Gf.Vec3f(0, -1, 0), Gf.Vec3f(2, 1, 0)])
closed.AddTranslateOp().Set(Gf.Vec3d(0, 0, 12))

stage.GetRootLayer().Save()
print("Wrote basisCurves.usda")
