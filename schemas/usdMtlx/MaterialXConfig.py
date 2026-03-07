"""
Generates materialXConfig.usda — demonstrates UsdMtlxMaterialXConfigAPI.

UsdMtlxMaterialXConfigAPI is applied to UsdShadeMaterial prims to store
the MaterialX specification version and color management system used when
authoring the material's shading network.

Run:
    python MaterialXConfig.py
"""

from pxr import Usd, UsdShade, Sdf, Gf

stage = Usd.Stage.CreateNew("materialXConfig.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

from pxr import UsdGeom
world = UsdGeom.Xform.Define(stage, "/World")

# ── MetalMaterial with MaterialXConfigAPI ─────────────────────────────────────
metal_mat = UsdShade.Material.Define(stage, "/World/MetalMaterial")
metal_prim = metal_mat.GetPrim()

# Apply MaterialXConfigAPI via schema
metal_prim.ApplyAPI("MaterialXConfigAPI")

# Set MaterialX config attributes
metal_prim.CreateAttribute(
    "mtlx:version", Sdf.ValueTypeNames.Token, custom=False
).Set("1.38")

metal_prim.CreateAttribute(
    "mtlx:colorManagementSystem", Sdf.ValueTypeNames.Token, custom=False
).Set("ocio")

# Create shader
pbr_shader = UsdShade.Shader.Define(stage, "/World/MetalMaterial/PBRShader")
pbr_shader.CreateIdAttr("ND_standard_surface_surfaceshader")
pbr_shader.CreateInput("metalness", Sdf.ValueTypeNames.Float).Set(1.0)
pbr_shader.CreateInput("specular_roughness", Sdf.ValueTypeNames.Float).Set(0.2)
pbr_shader.CreateInput("specular_IOR", Sdf.ValueTypeNames.Float).Set(1.5)
surface_output = pbr_shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)

# Texture shader
tex_shader = UsdShade.Shader.Define(stage, "/World/MetalMaterial/BaseColorTex")
tex_shader.CreateIdAttr("ND_image_color3")
tex_shader.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(
    Sdf.AssetPath("./textures/metal_basecolor.png")
)
tex_output = tex_shader.CreateOutput("out", Sdf.ValueTypeNames.Color3f)

# Connect texture to shader base_color
pbr_base_color = pbr_shader.CreateInput("base_color", Sdf.ValueTypeNames.Color3f)
pbr_base_color.ConnectToSource(tex_output)

# Connect shader to material surface output
metal_surface = metal_mat.CreateSurfaceOutput()
metal_surface.ConnectToSource(surface_output)

# ── PlasticMaterial ────────────────────────────────────────────────────────────
plastic_mat = UsdShade.Material.Define(stage, "/World/PlasticMaterial")
plastic_prim = plastic_mat.GetPrim()
plastic_prim.ApplyAPI("MaterialXConfigAPI")
plastic_prim.CreateAttribute(
    "mtlx:version", Sdf.ValueTypeNames.Token, custom=False
).Set("1.38")
plastic_prim.CreateAttribute(
    "mtlx:colorManagementSystem", Sdf.ValueTypeNames.Token, custom=False
).Set("acescg")

plastic_shader = UsdShade.Shader.Define(stage, "/World/PlasticMaterial/PlasticShader")
plastic_shader.CreateIdAttr("ND_standard_surface_surfaceshader")
plastic_shader.CreateInput("base_color", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.2, 0.4, 0.8))
plastic_shader.CreateInput("metalness", Sdf.ValueTypeNames.Float).Set(0.0)
plastic_shader.CreateInput("specular_roughness", Sdf.ValueTypeNames.Float).Set(0.5)
plastic_surface_out = plastic_shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)

plastic_surface = plastic_mat.CreateSurfaceOutput()
plastic_surface.ConnectToSource(plastic_surface_out)

stage.GetRootLayer().Save()
print("Wrote materialXConfig.usda")
