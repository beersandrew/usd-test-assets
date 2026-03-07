"""
Generates mesh.usda — demonstrates UsdGeomMesh: polygon mesh and
Catmull-Clark subdivision surface variants, plus an animated deforming mesh.

Run:
    python Mesh.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("mesh.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# Shared cube topology
FACE_VERTEX_COUNTS = [4, 4, 4, 4, 4, 4]
FACE_VERTEX_INDICES = [
    0, 1, 3, 2,
    4, 6, 7, 5,
    0, 4, 5, 1,
    2, 3, 7, 6,
    0, 2, 6, 4,
    1, 5, 7, 3,
]
CUBE_POINTS = [
    Gf.Vec3f(-1, -1, -1), Gf.Vec3f( 1, -1, -1),
    Gf.Vec3f(-1,  1, -1), Gf.Vec3f( 1,  1, -1),
    Gf.Vec3f(-1, -1,  1), Gf.Vec3f( 1, -1,  1),
    Gf.Vec3f(-1,  1,  1), Gf.Vec3f( 1,  1,  1),
]

# ── Simple polygon mesh ───────────────────────────────────────────────────────
poly = UsdGeom.Mesh.Define(stage, "/World/PolyMeshCube")
poly.GetFaceVertexCountsAttr().Set(FACE_VERTEX_COUNTS)
poly.GetFaceVertexIndicesAttr().Set(FACE_VERTEX_INDICES)
poly.GetPointsAttr().Set(CUBE_POINTS)

normals = []
for n in [(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)]:
    normals.extend([Gf.Vec3f(*n)] * 4)
poly.GetNormalsAttr().Set(normals)
poly.SetNormalsInterpolation(UsdGeom.Tokens.faceVarying)

uv_face = [Gf.Vec2f(0,0), Gf.Vec2f(1,0), Gf.Vec2f(1,1), Gf.Vec2f(0,1)]
uvs = uv_face * 6
st_primvar = UsdGeom.PrimvarsAPI(poly).CreatePrimvar(
    "st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying)
st_primvar.Set(uvs)

poly.GetExtentAttr().Set([Gf.Vec3f(-1,-1,-1), Gf.Vec3f(1,1,1)])
poly.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
poly.AddTranslateOp().Set(Gf.Vec3d(-4, 1, 0))

# ── Catmull-Clark subdivision surface ─────────────────────────────────────────
subdiv = UsdGeom.Mesh.Define(stage, "/World/SubdivCube")
subdiv.GetFaceVertexCountsAttr().Set(FACE_VERTEX_COUNTS)
subdiv.GetFaceVertexIndicesAttr().Set(FACE_VERTEX_INDICES)
subdiv.GetPointsAttr().Set(CUBE_POINTS)
subdiv.GetExtentAttr().Set([Gf.Vec3f(-1,-1,-1), Gf.Vec3f(1,1,1)])
subdiv.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.catmullClark)
subdiv.GetInterpolateBoundaryAttr().Set(UsdGeom.Tokens.edgeAndCorner)
# Crease along one edge
subdiv.GetCreaseIndicesAttr().Set([4, 0])
subdiv.GetCreaseLengthsAttr().Set([2])
subdiv.GetCreaseSharpnessesAttr().Set([5.0])
subdiv.AddTranslateOp().Set(Gf.Vec3d(0, 1, 0))

# ── Animated deforming mesh ───────────────────────────────────────────────────
wavy = UsdGeom.Mesh.Define(stage, "/World/WavyPlane")
wavy.GetFaceVertexCountsAttr().Set([4, 4, 4, 4])
wavy.GetFaceVertexIndicesAttr().Set([0, 1, 4, 3,  1, 2, 5, 4,  3, 4, 7, 6,  4, 5, 8, 7])

base_pts = [
    Gf.Vec3f(-2, 0, -2), Gf.Vec3f(0, 0, -2), Gf.Vec3f(2, 0, -2),
    Gf.Vec3f(-2, 0,  0), Gf.Vec3f(0, 0,  0), Gf.Vec3f(2, 0,  0),
    Gf.Vec3f(-2, 0,  2), Gf.Vec3f(0, 0,  2), Gf.Vec3f(2, 0,  2),
]
wavy.GetPointsAttr().Set(base_pts)

pts_attr = wavy.GetPointsAttr()
pts_attr.Set([
    Gf.Vec3f(-2, 0, -2), Gf.Vec3f(0, 0.5, -2), Gf.Vec3f(2, 0, -2),
    Gf.Vec3f(-2, 0,  0), Gf.Vec3f(0, 0,    0), Gf.Vec3f(2, 0,  0),
    Gf.Vec3f(-2, 0,  2), Gf.Vec3f(0,-0.5,  2), Gf.Vec3f(2, 0,  2),
], 0)
pts_attr.Set([
    Gf.Vec3f(-2, 0.5, -2), Gf.Vec3f(0, 0, -2), Gf.Vec3f(2, 0.5, -2),
    Gf.Vec3f(-2, 0,    0), Gf.Vec3f(0, 0,   0), Gf.Vec3f(2, 0,    0),
    Gf.Vec3f(-2,-0.5,  2), Gf.Vec3f(0, 0,   2), Gf.Vec3f(2,-0.5,  2),
], 12)
pts_attr.Set([
    Gf.Vec3f(-2, 0, -2), Gf.Vec3f(0, 0.5, -2), Gf.Vec3f(2, 0, -2),
    Gf.Vec3f(-2, 0,  0), Gf.Vec3f(0, 0,    0), Gf.Vec3f(2, 0,  0),
    Gf.Vec3f(-2, 0,  2), Gf.Vec3f(0,-0.5,  2), Gf.Vec3f(2, 0,  2),
], 24)

wavy.GetExtentAttr().Set([Gf.Vec3f(-2, -0.5, -2), Gf.Vec3f(2, 0.5, 2)])
wavy.GetSubdivisionSchemeAttr().Set(UsdGeom.Tokens.none)
wavy.GetDoubleSidedAttr().Set(True)
wavy.AddTranslateOp().Set(Gf.Vec3d(6, 0, 0))

stage.GetRootLayer().Save()
print("Wrote mesh.usda")
