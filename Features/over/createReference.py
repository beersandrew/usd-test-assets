from pxr import Usd, UsdGeom

# Create a new USD stage
stage = Usd.Stage.CreateNew("myScene.usda")

# Define the root Xform
root = UsdGeom.Xform.Define(stage, "/World")

# Add a reference to the red_cube.usda file
redCubeRef = UsdGeom.Xform.Define(stage, "/World/RedCube")
redCubeRef.GetPrim().GetReferences().AddReference("red_cube.usda")

# Optional: Add a transform to position the referenced cube
redCubeRef.AddTranslateOp().Set(value=(5.0, 0.0, 0.0))  # Translate the cube along the X-axis

# Save the USD stage
stage.GetRootLayer().Save()

print("USD file 'myScene.usda' created!")