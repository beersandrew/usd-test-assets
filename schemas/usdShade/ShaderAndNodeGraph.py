"""
Generates shaderAndNodeGraph.usda — demonstrates UsdShadeShader, UsdShadeNodeGraph,
UsdShadeNodeDefAPI, and UsdShadeConnectableAPI.

Run:
    python ShaderAndNodeGraph.py
"""

from pxr import Usd, UsdShade, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("shaderAndNodeGraph.usda")

# Set stage metadata
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── NodeGraph: container for the PBR shader network ──────────────────────────
network = UsdShade.NodeGraph.Define(stage, "/World/PbrNetwork")

# Apply NodeDefAPI to give the NodeGraph a shader identity
UsdShade.NodeDefAPI.Apply(network.GetPrim())

# Interface inputs — promoted to the NodeGraph boundary so callers can drive them.
roughness_input = network.CreateInput("roughness", Sdf.ValueTypeNames.Float)
roughness_input.Set(0.4)

base_color_input = network.CreateInput("baseColor", Sdf.ValueTypeNames.Color3f)
base_color_input.Set(Gf.Vec3f(0.8, 0.3, 0.1))

metallic_input = network.CreateInput("metallic", Sdf.ValueTypeNames.Float)
metallic_input.Set(0.0)

# The NodeGraph's output — wired to the internal surface shader.
network.CreateOutput("surface", Sdf.ValueTypeNames.Token)

# ── Surface shader (UsdPreviewSurface) ───────────────────────────────────────
surface_shader = UsdShade.Shader.Define(stage, "/World/PbrNetwork/SurfaceShader")
UsdShade.NodeDefAPI.Apply(surface_shader.GetPrim())
surface_shader.SetShaderId("UsdPreviewSurface")

# info:implementationSource — "id" means use info:id to find the implementation.
surface_shader.GetPrim().CreateAttribute(
    "info:implementationSource", Sdf.ValueTypeNames.Token,
    variability=Sdf.VariabilityUniform
).Set("id")

# Connect surface shader inputs to NodeGraph interface inputs.
diffuse_in = surface_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f)
UsdShade.ConnectableAPI.ConnectToSource(diffuse_in, base_color_input)

roughness_in = surface_shader.CreateInput("roughness", Sdf.ValueTypeNames.Float)
UsdShade.ConnectableAPI.ConnectToSource(roughness_in, roughness_input)

metallic_in = surface_shader.CreateInput("metallic", Sdf.ValueTypeNames.Float)
UsdShade.ConnectableAPI.ConnectToSource(metallic_in, metallic_input)

# Constant inputs not promoted to the NodeGraph interface.
surface_shader.CreateInput("specularColor", Sdf.ValueTypeNames.Float).Set(1.0)
surface_shader.CreateInput("ior", Sdf.ValueTypeNames.Float).Set(1.5)
surface_shader.CreateInput("opacity", Sdf.ValueTypeNames.Float).Set(1.0)
surface_shader.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(0)

# Outputs of the surface shader.
surface_out = surface_shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
surface_shader.CreateOutput("displacement", Sdf.ValueTypeNames.Token)

# Connect the NodeGraph output to the surface shader output.
network_surface_out = network.GetOutput("surface")
UsdShade.ConnectableAPI.ConnectToSource(network_surface_out, surface_out)

# ── Texture coordinate reader ─────────────────────────────────────────────────
texcoord = UsdShade.Shader.Define(stage, "/World/PbrNetwork/TexCoordReader")
UsdShade.NodeDefAPI.Apply(texcoord.GetPrim())
texcoord.SetShaderId("UsdPrimvarReader_float2")
texcoord.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st")
texcoord_out = texcoord.CreateOutput("result", Sdf.ValueTypeNames.Float2)

# ── Diffuse color texture ─────────────────────────────────────────────────────
diffuse_tex = UsdShade.Shader.Define(stage, "/World/PbrNetwork/DiffuseTexture")
UsdShade.NodeDefAPI.Apply(diffuse_tex.GetPrim())
diffuse_tex.SetShaderId("UsdUVTexture")
diffuse_tex.CreateInput("file", Sdf.ValueTypeNames.Asset).Set("./textures/diffuse.png")
diffuse_st = diffuse_tex.CreateInput("st", Sdf.ValueTypeNames.Float2)
UsdShade.ConnectableAPI.ConnectToSource(diffuse_st, texcoord_out)
diffuse_tex.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
diffuse_tex.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
diffuse_tex.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("sRGB")
diffuse_tex.CreateInput("scale", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(1, 1, 1, 1))
diffuse_tex.CreateInput("bias", Sdf.ValueTypeNames.Float4).Set(Gf.Vec4f(0, 0, 0, 0))
diffuse_tex.CreateOutput("rgb", Sdf.ValueTypeNames.Color3f)
diffuse_tex.CreateOutput("a", Sdf.ValueTypeNames.Float)

# ── Roughness texture ─────────────────────────────────────────────────────────
rough_tex = UsdShade.Shader.Define(stage, "/World/PbrNetwork/RoughnessTexture")
UsdShade.NodeDefAPI.Apply(rough_tex.GetPrim())
rough_tex.SetShaderId("UsdUVTexture")
rough_tex.CreateInput("file", Sdf.ValueTypeNames.Asset).Set("./textures/roughness.png")
rough_st = rough_tex.CreateInput("st", Sdf.ValueTypeNames.Float2)
UsdShade.ConnectableAPI.ConnectToSource(rough_st, texcoord_out)
rough_tex.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("repeat")
rough_tex.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("repeat")
rough_tex.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("raw")
rough_tex.CreateOutput("r", Sdf.ValueTypeNames.Float)

stage.GetRootLayer().Save()
print("Wrote shaderAndNodeGraph.usda")
