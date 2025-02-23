from pxr import Gf, Usd, UsdGeom, UsdSkel

stage = Usd.Stage.CreateNew("skelBindingApi_joints.usda")

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(10)
UsdGeom.SetStageMetersPerUnit(stage, 0.1)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

world = UsdGeom.Xform.Define(stage, "/World")

skelRoot = UsdSkel.Root.Define(stage, world.GetPath().AppendChild("SkelRoot"))
skelRootBinding = UsdSkel.BindingAPI.Apply(skelRoot.GetPrim())


# Skeleton
skeleton = UsdSkel.Skeleton.Define(stage, skelRoot.GetPath().AppendChild("Skeleton"))
skelBinding = UsdSkel.BindingAPI.Apply(skeleton.GetPrim())

joints = ["Shoulder", "Shoulder/Elbow", "Shoulder/Elbow/Hand"]
skeleton.GetJointsAttr().Set(joints)

bindTransforms = [
    Gf.Matrix4d(1).SetTranslate(Gf.Vec3d(0, 0, 0)),  # Identity matrix
    Gf.Matrix4d(1).SetTranslate(Gf.Vec3d(0, 0, 2)),  
    Gf.Matrix4d(1).SetTranslate(Gf.Vec3d(0, 0, 4))
]
skeleton.GetBindTransformsAttr().Set(bindTransforms)

# Define rest transforms
restTransforms = [
    Gf.Matrix4d(1).SetTranslate(Gf.Vec3d(0, 0, 0)),  
    Gf.Matrix4d(1).SetTranslate(Gf.Vec3d(0, 0, 2)),  
    Gf.Matrix4d(1).SetTranslate(Gf.Vec3d(0, 0, 2))  
]
skeleton.GetRestTransformsAttr().Set(restTransforms)


# Animation
animation = UsdSkel.Animation.Define(stage, skeleton.GetPath().AppendChild("Animation"))
animation.GetJointsAttr().Set(["Shoulder/Elbow"])
animation.GetTranslationsAttr().Set([Gf.Vec3f(0, 0, 2)])

animation.GetRotationsAttr().Set([Gf.Quatf(1, 0, 0, 0)], 1.0)
animation.GetRotationsAttr().Set([Gf.Quatf(0.7071, 0.7071, 0, 0)], 10.0)


animation.GetScalesAttr().Set([Gf.Vec3h(1, 1, 1)])

skelBinding.CreateAnimationSourceRel().AddTarget(animation.GetPath())


# Mesh

mesh = UsdGeom.Mesh.Define(stage, skelRoot.GetPath().AppendChild("Mesh"))

meshBinding = UsdSkel.BindingAPI.Apply(mesh.GetPrim())

# Define face counts and indices
mesh.GetFaceVertexCountsAttr().Set([4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
mesh.GetFaceVertexIndicesAttr().Set([
    2, 3, 1, 0, 6, 7, 5, 4, 8, 9, 7, 6, 3, 2, 9, 8, 10, 11, 4, 5, 0, 1, 11, 10,
    7, 9, 10, 5, 9, 2, 0, 10, 3, 8, 11, 1, 8, 6, 4, 11
])

# Define points
mesh.GetPointsAttr().Set([
    Gf.Vec3f(0.5, -0.5, 4), Gf.Vec3f(-0.5, -0.5, 4), Gf.Vec3f(0.5, 0.5, 4), Gf.Vec3f(-0.5, 0.5, 4),
    Gf.Vec3f(-0.5, -0.5, 0), Gf.Vec3f(0.5, -0.5, 0), Gf.Vec3f(-0.5, 0.5, 0), Gf.Vec3f(0.5, 0.5, 0),
    Gf.Vec3f(-0.5, 0.5, 2), Gf.Vec3f(0.5, 0.5, 2), Gf.Vec3f(0.5, -0.5, 2), Gf.Vec3f(-0.5, -0.5, 2)
])

# Define Joint Indices (One per vertex)
jointIndices = [2,2,2,2, 0,0,0,0, 1,1,1,1]
meshBinding.CreateJointIndicesPrimvar(False, 1).Set(jointIndices)

# Define Joint Weights
jointWeights = [1,1,1,1, 1,1,1,1, 1,1,1,1]
meshBinding.CreateJointWeightsPrimvar(False, 1).Set(jointWeights)

# Define Geom Bind Transform
geomBindTransform = Gf.Matrix4d(1)

meshBinding.CreateGeomBindTransformAttr(geomBindTransform)

meshBinding.CreateSkeletonRel().AddTarget(skeleton.GetPath())

stage.GetRootLayer().Save()