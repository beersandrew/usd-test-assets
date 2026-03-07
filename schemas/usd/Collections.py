"""
Collections.py — Demonstrates UsdCollectionAPI (multiple-apply schema).

Two named collections are created on the World prim:
  - "geometry": includes Cube and Sphere mesh prims
  - "lights":   includes the SunLight distant light prim

CollectionAPI is a multiple-apply schema, so each instance is identified by
a unique name token appended to the schema name (e.g. "CollectionAPI:geometry").
"""

from pxr import Usd, UsdGeom, UsdLux, Vt, Gf

stage = Usd.Stage.CreateNew("collections.usda")

# ------------------------------------------------------------------
# Stage metadata
# ------------------------------------------------------------------
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ------------------------------------------------------------------
# Geometry prims
# ------------------------------------------------------------------
cube = UsdGeom.Mesh.Define(stage, "/World/Cube")
cube.CreatePointsAttr([
    Gf.Vec3f(-0.5, -0.5,  0.5), Gf.Vec3f( 0.5, -0.5,  0.5),
    Gf.Vec3f( 0.5,  0.5,  0.5), Gf.Vec3f(-0.5,  0.5,  0.5),
    Gf.Vec3f(-0.5, -0.5, -0.5), Gf.Vec3f( 0.5, -0.5, -0.5),
    Gf.Vec3f( 0.5,  0.5, -0.5), Gf.Vec3f(-0.5,  0.5, -0.5),
])
cube.CreateFaceVertexCountsAttr([4, 4, 4, 4, 4, 4])
cube.CreateFaceVertexIndicesAttr([0, 1, 2, 3, 4, 5, 6, 7, 0, 4, 5, 1, 3, 2, 6, 7, 0, 3, 7, 4, 1, 5, 6, 2])
cube.CreateExtentAttr([Gf.Vec3f(-0.5, -0.5, -0.5), Gf.Vec3f(0.5, 0.5, 0.5)])
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(-2, 0, 0))

sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
sphere.CreateRadiusAttr(1.0)
sphere.CreateExtentAttr([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])
UsdGeom.XformCommonAPI(sphere).SetTranslate(Gf.Vec3d(2, 0, 0))

# ------------------------------------------------------------------
# Light prim
# ------------------------------------------------------------------
sun = UsdLux.DistantLight.Define(stage, "/World/SunLight")
sun.CreateAngleAttr(0.53)       # angular diameter of the sun (degrees)
sun.CreateIntensityAttr(50000)  # physically-plausible outdoor illuminance
UsdGeom.XformCommonAPI(sun).SetRotate(Gf.Vec3f(-45, 30, 0))

# ------------------------------------------------------------------
# Camera
# ------------------------------------------------------------------
cam = UsdGeom.Camera.Define(stage, "/World/MainCam")
cam.CreateFocalLengthAttr(35)
cam.CreateHorizontalApertureAttr(36)
cam.CreateClippingRangeAttr(Gf.Vec2f(0.1, 1000))
UsdGeom.XformCommonAPI(cam).SetTranslate(Gf.Vec3d(0, 2, 12))

# ------------------------------------------------------------------
# CollectionAPI — "geometry" collection (mesh prims)
# ------------------------------------------------------------------
geom_col = Usd.CollectionAPI.Apply(world.GetPrim(), "geometry")
geom_col.CreateExpansionRuleAttr("expandPrims")  # traverse and include child prims
geom_col.CreateIncludesRel().SetTargets([cube.GetPath(), sphere.GetPath()])

# ------------------------------------------------------------------
# CollectionAPI — "lights" collection (light prims)
# ------------------------------------------------------------------
lights_col = Usd.CollectionAPI.Apply(world.GetPrim(), "lights")
lights_col.CreateExpansionRuleAttr("expandPrims")
lights_col.CreateIncludesRel().SetTargets([sun.GetPath()])
lights_col.CreateExcludesRel()  # explicit empty excludes relationship

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------
stage.GetRootLayer().Save()
