"""
Generates points.usda — demonstrates UsdGeomPoints (point cloud with widths,
per-point color, and velocities) and UsdGeomPointInstancer (instancing
prototypes at arbitrary positions with per-instance transforms).

Run:
    python Points.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("points.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Point cloud ───────────────────────────────────────────────────────────────
stars = UsdGeom.Points.Define(stage, "/World/StarField")
stars.GetPointsAttr().Set([
    Gf.Vec3f(0, 1, 2), Gf.Vec3f(1.5, 0.5, 0), Gf.Vec3f(-1, 2, 1),
    Gf.Vec3f(2, 0, -1), Gf.Vec3f(-2, 1.5, -0.5), Gf.Vec3f(0.5, -0.5, 1.5),
    Gf.Vec3f(-1.5, 0, 2.5), Gf.Vec3f(1, 3, 0.5), Gf.Vec3f(-0.5, 1, -2),
])
widths_attr = stars.CreateWidthsAttr()
widths_attr.Set([0.1, 0.15, 0.08, 0.12, 0.2, 0.09, 0.11, 0.07, 0.14])
stars.SetWidthsInterpolation(UsdGeom.Tokens.vertex)

color_primvar = UsdGeom.PrimvarsAPI(stars).CreatePrimvar(
    "displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.vertex)
color_primvar.Set([
    Gf.Vec3f(1, 1, 0), Gf.Vec3f(0.8, 0.9, 1), Gf.Vec3f(1, 0.8, 0.6),
    Gf.Vec3f(0.9, 1, 0.9), Gf.Vec3f(1, 1, 1), Gf.Vec3f(0.7, 0.8, 1),
    Gf.Vec3f(1, 0.9, 0.7), Gf.Vec3f(0.8, 1, 0.8), Gf.Vec3f(1, 1, 0.8),
])
stars.GetIdsAttr().Set([0, 1, 2, 3, 4, 5, 6, 7, 8])
stars.GetVelocitiesAttr().Set([
    Gf.Vec3f(0, 0.1, 0), Gf.Vec3f(-0.05, 0, 0.05), Gf.Vec3f(0, 0.08, -0.02),
    Gf.Vec3f(0.1, 0, 0), Gf.Vec3f(0, 0.05, 0.05), Gf.Vec3f(-0.03, 0.03, 0),
    Gf.Vec3f(0, -0.05, 0.02), Gf.Vec3f(0.02, 0, -0.04), Gf.Vec3f(-0.01, 0.06, 0),
])
stars.GetExtentAttr().Set([Gf.Vec3f(-2, -0.5, -2), Gf.Vec3f(2, 3, 2.5)])
stars.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

# ── PointInstancer ────────────────────────────────────────────────────────────
instancer = UsdGeom.PointInstancer.Define(stage, "/World/GrassField")
instancer.GetProtoIndicesAttr().Set([0, 1, 0, 1, 0, 0, 1, 0, 1])
instancer.GetPositionsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(1, 0, 0.5), Gf.Vec3f(2, 0, 0),
    Gf.Vec3f(0, 0, 1), Gf.Vec3f(1, 0, 1.5), Gf.Vec3f(2, 0, 1),
    Gf.Vec3f(0, 0, 2), Gf.Vec3f(1, 0, 2.5), Gf.Vec3f(2, 0, 2),
])
instancer.GetOrientationsAttr().Set([
    Gf.Quath(1, 0, 0, 0), Gf.Quath(0.9659, 0, 0.2588, 0), Gf.Quath(1, 0, 0, 0),
    Gf.Quath(0.9659, 0, -0.2588, 0), Gf.Quath(1, 0, 0, 0), Gf.Quath(0.9659, 0, 0.2588, 0),
    Gf.Quath(1, 0, 0, 0), Gf.Quath(0.9659, 0, -0.2588, 0), Gf.Quath(1, 0, 0, 0),
])
instancer.GetScalesAttr().Set([
    Gf.Vec3f(1, 1, 1), Gf.Vec3f(1, 1.2, 1), Gf.Vec3f(1, 0.9, 1),
    Gf.Vec3f(1, 1.1, 1), Gf.Vec3f(1, 1.3, 1), Gf.Vec3f(1, 0.8, 1),
    Gf.Vec3f(1, 1, 1), Gf.Vec3f(1, 1.15, 1), Gf.Vec3f(1, 1.05, 1),
])
instancer.GetIdsAttr().Set([10, 11, 12, 13, 14, 15, 16, 17, 18])
instancer.GetVelocitiesAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0.01, 0, 0), Gf.Vec3f(0, 0, 0),
    Gf.Vec3f(0, 0, 0.01), Gf.Vec3f(0, 0, 0), Gf.Vec3f(0, 0, -0.01),
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(-0.01, 0, 0), Gf.Vec3f(0, 0, 0),
])
instancer.GetExtentAttr().Set([Gf.Vec3f(-0.5, 0, -0.5), Gf.Vec3f(2.5, 1.3, 2.5)])
instancer.AddTranslateOp().Set(Gf.Vec3d(6, 0, 0))

# Prototypes scope
proto_scope = UsdGeom.Scope.Define(stage, "/World/GrassField/Prototypes")

# Prototype 0: thin blade
thin = UsdGeom.Cylinder.Define(stage, "/World/GrassField/Prototypes/BladeThin")
thin.GetHeightAttr().Set(1.0)
thin.GetRadiusAttr().Set(0.04)
thin.GetAxisAttr().Set(UsdGeom.Tokens.y)
thin.GetExtentAttr().Set([Gf.Vec3f(-0.04, -0.5, -0.04), Gf.Vec3f(0.04, 0.5, 0.04)])
thin_prim = thin.GetPrim()
thin_prim.SetMetadata("active", False)

# Prototype 1: wide blade
wide = UsdGeom.Cylinder.Define(stage, "/World/GrassField/Prototypes/BladeWide")
wide.GetHeightAttr().Set(1.0)
wide.GetRadiusAttr().Set(0.07)
wide.GetAxisAttr().Set(UsdGeom.Tokens.y)
wide.GetExtentAttr().Set([Gf.Vec3f(-0.07, -0.5, -0.07), Gf.Vec3f(0.07, 0.5, 0.07)])
wide_prim = wide.GetPrim()
wide_prim.SetMetadata("active", False)

# Link prototypes relationship
instancer.GetPrototypesRel().AddTarget("/World/GrassField/Prototypes/BladeThin")
instancer.GetPrototypesRel().AddTarget("/World/GrassField/Prototypes/BladeWide")

stage.GetRootLayer().Save()
print("Wrote points.usda")
