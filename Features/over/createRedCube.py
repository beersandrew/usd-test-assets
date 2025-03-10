from pxr import Usd, UsdGeom, UsdShade, Gf, Sdf

# Create a new USD stage
stage = Usd.Stage.CreateNew("red_cube.usda")

# Define the root Xform
root = UsdGeom.Xform.Define(stage, "/World")

# Add a cube under the root
cube = UsdGeom.Cube.Define(stage, "/World/Cube")

# Set the size of the cube
cube.GetSizeAttr().Set(2.0)  # Optional: Adjust size as needed

# Create a Material
material = UsdShade.Material.Define(stage, "/World/Materials/RedMaterial")

# Create a Shader for the material
shader = UsdShade.Shader.Define(stage, "/World/Materials/RedMaterial/Shader")
shader.CreateIdAttr("UsdPreviewSurface")

# Set the shader parameters for the red color
shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 0.0, 0.0))  # Red
shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.5)

# Create a surface output for the shader
shaderOutput = shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)

# Bind the shader's surface output to the material's surface output
material.CreateSurfaceOutput().ConnectToSource(shaderOutput)

# Bind the material to the cube
material_binding_api = UsdShade.MaterialBindingAPI(cube)
material_binding_api.Bind(material)
material_binding_api.Apply()

# Save the USD stage
stage.GetRootLayer().Save()

print("USD file 'red_cube.usda' created!")