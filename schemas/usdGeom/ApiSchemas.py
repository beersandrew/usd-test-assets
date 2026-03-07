"""
Generates apiSchemas.usda — demonstrates UsdGeom applied API schemas:
  UsdGeomPrimvarsAPI  — structured primvar channels on geometry
  UsdGeomMotionAPI    — motion blur velocity and sampling hints
  UsdGeomVisibilityAPI — guide/proxy visibility tokens
  UsdGeomModelAPI     — card draw-mode for large-scene stand-ins

Run:
    python ApiSchemas.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("apiSchemas.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── PrimvarsAPI ───────────────────────────────────────────────────────────────
pv_mesh = UsdGeom.Mesh.Define(stage, "/World/PrimvarDemo")
pv_mesh.GetPrim().ApplyAPI(UsdGeom.PrimvarsAPI)
pv_mesh.GetFaceVertexCountsAttr().Set([4])
pv_mesh.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])
pv_mesh.GetPointsAttr().Set([
    Gf.Vec3f(-1, 0, -1), Gf.Vec3f(1, 0, -1),
    Gf.Vec3f(1, 0, 1), Gf.Vec3f(-1, 0, 1),
])
pv_mesh.GetExtentAttr().Set([Gf.Vec3f(-1, 0, -1), Gf.Vec3f(1, 0, 1)])
pv_mesh.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
pv_mesh.GetDoubleSidedAttr().Set(True)
pv_mesh.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

pvAPI = UsdGeom.PrimvarsAPI(pv_mesh)
pvAPI.CreatePrimvar("roughness", Sdf.ValueTypeNames.Float,
                    UsdGeom.Tokens.constant).Set(0.6)
pvAPI.CreatePrimvar("temperature", Sdf.ValueTypeNames.FloatArray,
                    UsdGeom.Tokens.vertex).Set([0.2, 0.8, 1.0, 0.4])
pvAPI.CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray,
                    UsdGeom.Tokens.faceVarying).Set([
    Gf.Vec2f(0, 0), Gf.Vec2f(1, 0), Gf.Vec2f(1, 1), Gf.Vec2f(0, 1),
])
color_pv = pvAPI.CreatePrimvar("colorPalette", Sdf.ValueTypeNames.Color3fArray,
                               UsdGeom.Tokens.constant)
color_pv.Set([Gf.Vec3f(1, 0, 0), Gf.Vec3f(0, 1, 0), Gf.Vec3f(0, 0, 1)])
color_pv.SetIndices([0])

# ── MotionAPI ─────────────────────────────────────────────────────────────────
motion_mesh = UsdGeom.Mesh.Define(stage, "/World/MotionBlurMesh")
motion_mesh.GetPrim().ApplyAPI(UsdGeom.MotionAPI)
motion_mesh.GetFaceVertexCountsAttr().Set([4])
motion_mesh.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])
motion_mesh.GetPointsAttr().Set([
    Gf.Vec3f(-0.5, 0, -0.5), Gf.Vec3f(0.5, 0, -0.5),
    Gf.Vec3f(0.5, 0, 0.5), Gf.Vec3f(-0.5, 0, 0.5),
])
motion_mesh.GetExtentAttr().Set([Gf.Vec3f(-0.5, 0, -0.5), Gf.Vec3f(0.5, 0, 0.5)])
motion_mesh.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
motion_mesh.GetVelocitiesAttr().Set([
    Gf.Vec3f(2, 0, 0), Gf.Vec3f(2, 0, 0),
    Gf.Vec3f(2, 0, 0), Gf.Vec3f(2, 0, 0),
])
motion_mesh.AddTranslateOp().Set(Gf.Vec3d(4, 0.5, 0))

motionAPI = UsdGeom.MotionAPI(motion_mesh)
motionAPI.CreateVelocityScaleAttr(1.5)
motionAPI.CreateNonlinearSampleCountAttr(3)

# ── VisibilityAPI ─────────────────────────────────────────────────────────────
vis_grp = UsdGeom.Xform.Define(stage, "/World/VisibilityGroup")
vis_grp.GetPrim().ApplyAPI(UsdGeom.VisibilityAPI)
visAPI = UsdGeom.VisibilityAPI(vis_grp)
visAPI.CreateGuideVisibilityAttr(UsdGeom.Tokens.invisible)
visAPI.CreateProxyVisibilityAttr(UsdGeom.Tokens.inherited)
vis_grp.AddTranslateOp().Set(Gf.Vec3d(8, 0, 0))

main_geo = UsdGeom.Mesh.Define(stage, "/World/VisibilityGroup/MainGeo")
main_geo.GetFaceVertexCountsAttr().Set([4])
main_geo.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])
main_geo.GetPointsAttr().Set([
    Gf.Vec3f(-1, 0, -1), Gf.Vec3f(1, 0, -1),
    Gf.Vec3f(1, 2, -1), Gf.Vec3f(-1, 2, -1),
])
main_geo.GetExtentAttr().Set([Gf.Vec3f(-1, 0, -1), Gf.Vec3f(1, 2, -1)])
main_geo.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)

guide_geo = UsdGeom.Mesh.Define(stage, "/World/VisibilityGroup/GuideGeo")
guide_geo.GetPrim().ApplyAPI(UsdGeom.VisibilityAPI)
guide_geo.GetFaceVertexCountsAttr().Set([4])
guide_geo.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])
guide_geo.GetPointsAttr().Set([
    Gf.Vec3f(-1.2, 0, -1.2), Gf.Vec3f(1.2, 0, -1.2),
    Gf.Vec3f(1.2, 2.2, -1.2), Gf.Vec3f(-1.2, 2.2, -1.2),
])
guide_geo.GetExtentAttr().Set([Gf.Vec3f(-1.2, 0, -1.2), Gf.Vec3f(1.2, 2.2, -1.2)])
guide_geo.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)

# ── ModelAPI ──────────────────────────────────────────────────────────────────
car_xf = UsdGeom.Xform.Define(stage, "/World/CarModel")
car_prim = car_xf.GetPrim()
car_prim.SetMetadata("kind", "component")
car_prim.ApplyAPI(UsdGeom.ModelAPI)
car_xf.AddTranslateOp().Set(Gf.Vec3d(14, 0, 0))

modelAPI = UsdGeom.ModelAPI(car_prim)
modelAPI.CreateModelDrawModeAttr(UsdGeom.Tokens.cards)
modelAPI.CreateModelApplyDrawModeAttr(True)
modelAPI.CreateModelDrawModeColorAttr(Gf.Vec3f(0.2, 0.3, 0.8))

# Card texture assets
car_prim.CreateAttribute(
    "model:cardTextureXPos", Sdf.ValueTypeNames.Asset).Set("textures/car_front.png")
car_prim.CreateAttribute(
    "model:cardTextureXNeg", Sdf.ValueTypeNames.Asset).Set("textures/car_back.png")
car_prim.CreateAttribute(
    "model:cardTextureYPos", Sdf.ValueTypeNames.Asset).Set("textures/car_top.png")
car_prim.CreateAttribute(
    "model:cardTextureYNeg", Sdf.ValueTypeNames.Asset).Set("textures/car_bottom.png")
car_prim.CreateAttribute(
    "model:cardTextureZPos", Sdf.ValueTypeNames.Asset).Set("textures/car_right.png")
car_prim.CreateAttribute(
    "model:cardTextureZNeg", Sdf.ValueTypeNames.Asset).Set("textures/car_left.png")

extents_attr = car_prim.CreateAttribute(
    "model:extentsHint", Sdf.ValueTypeNames.Float3Array)
extents_attr.Set([Gf.Vec3f(-1.5, 0, -3), Gf.Vec3f(1.5, 1.5, 3)])

# High-res body mesh (only shown in "default" drawMode)
body = UsdGeom.Mesh.Define(stage, "/World/CarModel/Body")
body.GetFaceVertexCountsAttr().Set([4, 4, 4, 4, 4, 4])
body.GetFaceVertexIndicesAttr().Set([
    0, 1, 3, 2,  4, 6, 7, 5,
    0, 4, 5, 1,  2, 3, 7, 6,
    0, 2, 6, 4,  1, 5, 7, 3,
])
body.GetPointsAttr().Set([
    Gf.Vec3f(-1.5, 0, -3), Gf.Vec3f( 1.5, 0, -3),
    Gf.Vec3f(-1.5, 1.5, -3), Gf.Vec3f( 1.5, 1.5, -3),
    Gf.Vec3f(-1.5, 0,  3), Gf.Vec3f( 1.5, 0,  3),
    Gf.Vec3f(-1.5, 1.5,  3), Gf.Vec3f( 1.5, 1.5,  3),
])
body.GetExtentAttr().Set([Gf.Vec3f(-1.5, 0, -3), Gf.Vec3f(1.5, 1.5, 3)])
body.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)

stage.GetRootLayer().Save()
print("Wrote apiSchemas.usda")
