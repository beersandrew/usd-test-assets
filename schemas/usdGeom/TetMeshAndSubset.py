"""
Generates tetMeshAndSubset.usda — demonstrates UsdGeomTetMesh (tetrahedral
volume mesh for FEM simulation) and UsdGeomGeomSubset (face partitioning
for material binding or physics grouping).

Run:
    python TetMeshAndSubset.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("tetMeshAndSubset.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Simple TetMesh: a single tetrahedron ──────────────────────────────────────
simple_tet = UsdGeom.TetMesh.Define(stage, "/World/SimpleTet")
simple_tet.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(2, 0, 0),
    Gf.Vec3f(1, 0, -2), Gf.Vec3f(1, 2, -1),
])
simple_tet.GetTetVertexIndicesAttr().Set([Gf.Vec4i(0, 1, 2, 3)])
simple_tet.GetFaceVertexCountsAttr().Set([3, 3, 3, 3])
simple_tet.GetFaceVertexIndicesAttr().Set([0, 2, 1,  0, 1, 3,  1, 2, 3,  0, 3, 2])
simple_tet.GetExtentAttr().Set([Gf.Vec3f(0, 0, -2), Gf.Vec3f(2, 2, 0)])
simple_tet.AddTranslateOp().Set(Gf.Vec3d(-4, 0, 0))

# ── Double TetMesh: two tets sharing a face ───────────────────────────────────
double_tet = UsdGeom.TetMesh.Define(stage, "/World/DoubleTet")
double_tet.GetPointsAttr().Set([
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(2, 0, 0),
    Gf.Vec3f(1, 0, -2), Gf.Vec3f(1, 2, -1),
    Gf.Vec3f(3, 2, -1),
])
double_tet.GetTetVertexIndicesAttr().Set([
    Gf.Vec4i(0, 1, 2, 3),
    Gf.Vec4i(1, 4, 2, 3),
])
double_tet.GetFaceVertexCountsAttr().Set([3, 3, 3, 3, 3, 3])
double_tet.GetFaceVertexIndicesAttr().Set([
    0, 2, 1,
    0, 1, 3,
    0, 3, 2,
    1, 4, 3,
    1, 2, 4,
    2, 3, 4,
])
double_tet.GetExtentAttr().Set([Gf.Vec3f(0, 0, -2), Gf.Vec3f(3, 2, 0)])
double_tet.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

# ── Mesh with GeomSubsets ─────────────────────────────────────────────────────
box = UsdGeom.Mesh.Define(stage, "/World/BoxWithSubsets")
box.GetFaceVertexCountsAttr().Set([4, 4, 4, 4, 4, 4])
box.GetFaceVertexIndicesAttr().Set([
    0, 1, 3, 2,
    4, 6, 7, 5,
    0, 4, 5, 1,
    2, 3, 7, 6,
    0, 2, 6, 4,
    1, 5, 7, 3,
])
box.GetPointsAttr().Set([
    Gf.Vec3f(-1, -1, -1), Gf.Vec3f( 1, -1, -1),
    Gf.Vec3f(-1,  1, -1), Gf.Vec3f( 1,  1, -1),
    Gf.Vec3f(-1, -1,  1), Gf.Vec3f( 1, -1,  1),
    Gf.Vec3f(-1,  1,  1), Gf.Vec3f( 1,  1,  1),
])
box.GetExtentAttr().Set([Gf.Vec3f(-1,-1,-1), Gf.Vec3f(1,1,1)])
box.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
box.AddTranslateOp().Set(Gf.Vec3d(6, 1, 0))

# Top face subset
top = UsdGeom.GeomSubset.Define(stage, "/World/BoxWithSubsets/Top")
top.GetPrim().ApplyAPI(Sdf.Path("MaterialBindingAPI"))
top.GetElementTypeAttr().Set(UsdGeom.Tokens.face)
top.GetFamilyNameAttr().Set("materialBind")
top.GetIndicesAttr().Set([3])

# Bottom face subset
bottom = UsdGeom.GeomSubset.Define(stage, "/World/BoxWithSubsets/Bottom")
bottom.GetPrim().ApplyAPI(Sdf.Path("MaterialBindingAPI"))
bottom.GetElementTypeAttr().Set(UsdGeom.Tokens.face)
bottom.GetFamilyNameAttr().Set("materialBind")
bottom.GetIndicesAttr().Set([2])

# Sides subset
sides = UsdGeom.GeomSubset.Define(stage, "/World/BoxWithSubsets/Sides")
sides.GetPrim().ApplyAPI(Sdf.Path("MaterialBindingAPI"))
sides.GetElementTypeAttr().Set(UsdGeom.Tokens.face)
sides.GetFamilyNameAttr().Set("materialBind")
sides.GetIndicesAttr().Set([0, 1, 4, 5])

stage.GetRootLayer().Save()
print("Wrote tetMeshAndSubset.usda")
