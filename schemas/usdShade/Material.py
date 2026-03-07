"""
Generates material.usda — demonstrates UsdShadeMaterial and UsdShadeMaterialBindingAPI.

Run:
    python Material.py
"""

from pxr import Usd, UsdShade, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("material.usda")

# Set stage metadata
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Material library ──────────────────────────────────────────────────────────
materials_scope = UsdGeom.Scope.Define(stage, "/World/Materials")

# ── RedPlastic material ───────────────────────────────────────────────────────
red_plastic = UsdShade.Material.Define(stage, "/World/Materials/RedPlastic")
# Apply MaterialBindingAPI on the material itself is not standard;
# it is applied on geometry. But we can show it on a material to demonstrate
# the schema. (Normally MaterialBindingAPI is applied to geometry prims.)
UsdShade.MaterialBindingAPI.Apply(red_plastic.GetPrim())

pbr_surface = UsdShade.Shader.Define(stage, "/World/Materials/RedPlastic/PbrSurface")
UsdShade.NodeDefAPI.Apply(pbr_surface.GetPrim())
pbr_surface.SetShaderId("UsdPreviewSurface")

pbr_surface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.9, 0.1, 0.05))
pbr_surface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.25)
pbr_surface.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
pbr_surface.CreateInput("ior", Sdf.ValueTypeNames.Float).Set(1.46)   # polystyrene IOR
pbr_surface.CreateInput("opacity", Sdf.ValueTypeNames.Float).Set(1.0)
surface_out = pbr_surface.CreateOutput("surface", Sdf.ValueTypeNames.Token)
disp_out = pbr_surface.CreateOutput("displacement", Sdf.ValueTypeNames.Token)

# Wire material outputs to shader outputs.
red_plastic.CreateSurfaceOutput().ConnectToSource(surface_out)
red_plastic.CreateDisplacementOutput().ConnectToSource(disp_out)

# ── BrushedGold material ──────────────────────────────────────────────────────
brushed_gold = UsdShade.Material.Define(stage, "/World/Materials/BrushedGold")

gold_surface = UsdShade.Shader.Define(stage, "/World/Materials/BrushedGold/GoldSurface")
UsdShade.NodeDefAPI.Apply(gold_surface.GetPrim())
gold_surface.SetShaderId("UsdPreviewSurface")

gold_surface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 0.765, 0.336))
gold_surface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.35)   # brushed — not mirror-like
gold_surface.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(1.0)     # fully metallic
gold_surface.CreateInput("ior", Sdf.ValueTypeNames.Float).Set(0.47)         # gold complex IOR (n)
gold_out = gold_surface.CreateOutput("surface", Sdf.ValueTypeNames.Token)

brushed_gold.CreateSurfaceOutput().ConnectToSource(gold_out)

# ── ClearGlass material ───────────────────────────────────────────────────────
clear_glass = UsdShade.Material.Define(stage, "/World/Materials/ClearGlass")

glass_surface = UsdShade.Shader.Define(stage, "/World/Materials/ClearGlass/GlassSurface")
UsdShade.NodeDefAPI.Apply(glass_surface.GetPrim())
glass_surface.SetShaderId("UsdPreviewSurface")

glass_surface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.9, 0.95, 1.0))
glass_surface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.02)   # near-perfect glass
glass_surface.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
glass_surface.CreateInput("ior", Sdf.ValueTypeNames.Float).Set(1.52)          # borosilicate glass
glass_surface.CreateInput("opacity", Sdf.ValueTypeNames.Float).Set(0.05)      # nearly transparent
glass_surface.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(0)
glass_out = glass_surface.CreateOutput("surface", Sdf.ValueTypeNames.Token)

clear_glass.CreateSurfaceOutput().ConnectToSource(glass_out)

# ── Geometry with material bindings ───────────────────────────────────────────
props_scope = UsdGeom.Scope.Define(stage, "/World/Props")

# PlasticBall — direct material binding.
plastic_ball = UsdGeom.Sphere.Define(stage, "/World/Props/PlasticBall")
plastic_ball.GetRadiusAttr().Set(1.0)
plastic_ball.GetExtentAttr().Set([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])
UsdGeom.XformCommonAPI(plastic_ball).SetTranslate(Gf.Vec3d(0, 1, 0))

binding_api = UsdShade.MaterialBindingAPI.Apply(plastic_ball.GetPrim())
# material:binding is the default binding — used when no purpose is specified.
binding_api.Bind(red_plastic)

# GoldBlock — direct binding to brushed gold.
gold_block = UsdGeom.Cube.Define(stage, "/World/Props/GoldBlock")
gold_block.GetSizeAttr().Set(2.0)
gold_block.GetExtentAttr().Set([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])
UsdGeom.XformCommonAPI(gold_block).SetTranslate(Gf.Vec3d(4, 1, 0))

gold_binding = UsdShade.MaterialBindingAPI.Apply(gold_block.GetPrim())
gold_binding.Bind(brushed_gold)

# GlassOrb — full binding for offline renderers, preview binding for viewport.
glass_orb = UsdGeom.Sphere.Define(stage, "/World/Props/GlassOrb")
glass_orb.GetRadiusAttr().Set(0.8)
glass_orb.GetExtentAttr().Set([Gf.Vec3f(-0.8, -0.8, -0.8), Gf.Vec3f(0.8, 0.8, 0.8)])
UsdGeom.XformCommonAPI(glass_orb).SetTranslate(Gf.Vec3d(8, 0.8, 0))

glass_binding = UsdShade.MaterialBindingAPI.Apply(glass_orb.GetPrim())
# Full binding used by offline renderers.
glass_binding.Bind(clear_glass)
# Preview binding used by fast interactive viewers.
glass_binding.Bind(red_plastic, UsdShade.Tokens.weakerThanDescendants, "preview")

stage.GetRootLayer().Save()
print("Wrote material.usda")
