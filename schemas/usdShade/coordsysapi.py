from pxr import Usd, UsdShade, UsdGeom, Sdf, Gf

# Create a new stage
print("flag 1:")
stage = Usd.Stage.CreateNew("coordsys_example.usda")

# Set up basic stage metadata
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Create a root xform
root = UsdGeom.Xform.Define(stage, "/Root")

# Create a material scope
materialScope = UsdGeom.Scope.Define(stage, "/Root/Materials")

# Create a coordinate system at the root level
rootCoordSys = UsdShade.CoordSysAPI.Apply(root.GetPrim(), "worldSpace")
rootXform = UsdGeom.Xformable(root.GetPrim())
rootXform.AddTransformOp().Set(Gf.Matrix4d().SetIdentity())

# Create a material with a coordinate system binding
material = UsdShade.Material.Define(stage, "/Root/Materials/StandardMaterial")

# Create a shader within the material
shader = UsdShade.Shader.Define(stage, "/Root/Materials/StandardMaterial/PBRShader")
shader.CreateIdAttr("UsdPreviewSurface")

# Create a normal map shader that will use a specific coordinate system
normalMapShader = UsdShade.Shader.Define(stage, "/Root/Materials/StandardMaterial/NormalMapShader")
normalMapShader.CreateIdAttr("UsdUVTexture")
normalMapShader.CreateInput("file", Sdf.ValueTypeNames.Asset).Set("textures/normal.png")

# Connect the normal map to the main shader
shader.CreateInput("normal", Sdf.ValueTypeNames.Normal3f).ConnectToSource(
    normalMapShader.CreateOutput("rgb", Sdf.ValueTypeNames.Float3))

# Create a coordinate system specifically for normal maps
materialCoordSys = UsdShade.CoordSysAPI.Apply(material.GetPrim(), "normalMapSpace")

# Set a transform for this coordinate system (for example, flipping Y for normal maps)
flipY = Gf.Matrix4d().SetIdentity()
flipY.SetScale(Gf.Vec3d(1.0, -1.0, 1.0))
materialXform = UsdGeom.Xformable(material.GetPrim())
materialXform.AddTransformOp().Set(flipY)

# Bind the normal map shader to use this coordinate system
UsdShade.CoordSysAPI.Bind(normalMapShader.GetPrim(), "normalSpace", "normalMapSpace")

# Create a mesh that will use the material
mesh = UsdGeom.Mesh.Define(stage, "/Root/Geometry/Cube")

# Set basic mesh attributes (simplified cube)
points = [
    (-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1),
    (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1)
]
faceVertexCounts = [4] * 6
faceVertexIndices = [
    0, 1, 2, 3,  # bottom
    4, 5, 6, 7,  # top
    0, 3, 7, 4,  # left
    1, 5, 6, 2,  # right
    0, 4, 5, 1,  # back
    3, 2, 6, 7   # front
]

mesh.CreatePointsAttr(points)
mesh.CreateFaceVertexCountsAttr(faceVertexCounts)
mesh.CreateFaceVertexIndicesAttr(faceVertexIndices)

# Assign the material to the mesh
UsdShade.MaterialBindingAPI(mesh).Bind(material)

# Create a local coordinate system for the mesh
meshCoordSys = UsdShade.CoordSysAPI.Apply(mesh.GetPrim(), "objectSpace")

# Set a transform for this coordinate system
objectTransform = Gf.Matrix4d().SetIdentity()
objectTransform.SetTranslate(Gf.Vec3d(0.0, 0.0, 5.0))
meshXform = UsdGeom.Xformable(mesh.GetPrim())
meshXform.AddTransformOp().Set(objectTransform)

# Demonstrate how to find and use coordinate systems
print("Demonstrating coordinate system queries:")

# Find coordinate system bound to the material
boundCoordSys = UsdShade.CoordSysAPI.GetBoundCoordSys(normalMapShader.GetPrim(), "normalSpace")
print(f"Bound coordinate system for normal map: {boundCoordSys}")

# Find all available coordinate systems from the mesh's perspective
try:
    availableCoordSys = UsdShade.CoordSysAPI.FindAllCoordSysAPIs(mesh.GetPrim())
    print("Available coordinate systems from mesh:")
    for cs in availableCoordSys:
        name = cs.GetName()
        prim = cs.GetPrim()
        print(f"  - {name} on {prim.GetPath()}")
except Exception as e:
    print(f"Error finding coordinate systems: {e}")

# Save the stage
stage.GetRootLayer().Save()
print(f"USDA file written to: coordsys_example.usda")
