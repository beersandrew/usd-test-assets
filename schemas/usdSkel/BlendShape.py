from pxr import Usd, UsdGeom, UsdSkel, Vt
import math

stage = Usd.Stage.CreateNew("blendshapes.usda")

xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(xform.GetPrim())
stage.SetStartTimeCode(1.0)
stage.SetEndTimeCode(17.0)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

skel_root = UsdSkel.Root.Define(stage, "/World/MorphingTri")
root_binding = UsdSkel.BindingAPI.Apply(skel_root.GetPrim())
skeleton = UsdSkel.Skeleton.Define(stage, skel_root.GetPath().AppendChild("Skel"))

root_binding.CreateSkeletonRel().SetTargets([skeleton.GetPath()])

mesh = UsdGeom.Mesh.Define(stage, "/World/MorphingTri/Mesh")
mesh_binding = UsdSkel.BindingAPI.Apply(mesh.GetPrim())
mesh_binding.CreateSkeletonRel().SetTargets([skeleton.GetPath()])


eq_tri_height = math.sqrt(3) / 2

points = Vt.Vec3fArray([
    (0.5, 0, 0), (0, eq_tri_height, 0), (-0.5, 0, 0)
])

face_vert_indices = [
    0, 1, 2
]

face_vert_counts = [3]

mesh.CreatePointsAttr(points)
mesh.CreateFaceVertexIndicesAttr(face_vert_indices)
mesh.CreateFaceVertexCountsAttr(face_vert_counts)
mesh.CreateExtentAttr().Set([(-0.5, 0, 0), (0.5, eq_tri_height, 0)])

isosceles = UsdSkel.BlendShape.Define(stage, mesh.GetPath().AppendChild("iso"))
isosceles.CreateOffsetsAttr().Set([(0, eq_tri_height, 0)])
isosceles.CreatePointIndicesAttr().Set([1])

right = UsdSkel.BlendShape.Define(stage, mesh.GetPath().AppendChild("right"))
right.CreateOffsetsAttr().Set([(-0.5, 1-eq_tri_height, 0)])
right.CreatePointIndicesAttr().Set([1])


mesh_binding.CreateBlendShapesAttr().Set(["iso", "right"])
mesh_binding.CreateBlendShapeTargetsRel().SetTargets([isosceles.GetPath(), right.GetPath()])

anim = UsdSkel.Animation.Define(stage, skel_root.GetPath().AppendChild("Anim"))

# Frame 1
anim.CreateBlendShapesAttr().Set(["iso", "right"])
anim.CreateBlendShapeWeightsAttr().Set([0.0, 0.0], 1.0)

# Frame 5
anim.CreateBlendShapeWeightsAttr().Set([1.0, 0.0], 5.0)

# Frame 9
anim.CreateBlendShapeWeightsAttr().Set([0.0, 0.0], 9.0)

# Frame 13
anim.CreateBlendShapeWeightsAttr().Set([0.0, 1.0], 13.0)

# Frame 17
anim.CreateBlendShapeWeightsAttr().Set([1.0, 1.0], 17.0)


root_binding.CreateAnimationSourceRel().AddTarget(anim.GetPath())

stage.Save()

