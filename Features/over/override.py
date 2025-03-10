from pxr import Usd, UsdShade, Gf, Sdf

# Open the existing scene with the red cube as a root layer
stage = Usd.Stage.Open("myScene.usda")

# Add an override for the material color
# Assuming the material is at /World/RedCube/World/Materials/RedMaterial/Shader
shaderPath = "/World/RedCube/World/Materials/RedMaterial/Shader"
shaderPrim = stage.OverridePrim(shaderPath)

# Ensure the shader prim exists and set the new color
if shaderPrim:
    shader = UsdShade.Shader(shaderPrim)
    shaderInput = shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f)
    shaderInput.Set(Gf.Vec3f(0.0, 1.0, 0.0))  # Green color
else:
    print(f"Shader at {shaderPath} does not exist. Please check the path.")

# Save the override to a new file
stage.GetRootLayer().Export("mySceneOverride.usda")

print("USD override file 'mySceneOverride.usda' created!")