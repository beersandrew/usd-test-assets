from pxr import Sdf, UsdGeom, Usd

stage = Usd.Stage.CreateNew("accessibilityApi.usda")

world = UsdGeom.Xform.Define(stage, "/World")

stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
stage.SetTimeCodesPerSecond(24)

# Define a Mesh prim with AccessibilityAPI:default applied
button = UsdGeom.Mesh.Define(stage, world.GetPath().AppendPath("Button"))
button_prim = button.GetPrim()
button_prim.ApplyAPI("AccessibilityAPI", "default")

# Human-readable label for the element
button_prim.CreateAttribute("accessibility:default:label", Sdf.ValueTypeNames.Token, custom=False).Set("Submit Button")
# Longer description for screen readers
button_prim.CreateAttribute("accessibility:default:description", Sdf.ValueTypeNames.String, custom=False).Set("Submits the current form data")
# Priority level: high, medium, low
button_prim.CreateAttribute("accessibility:default:priority", Sdf.ValueTypeNames.Token, custom=False).Set("high")

# Define an Xform prim with two AccessibilityAPI instances applied
panel = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Panel"))
panel_prim = panel.GetPrim()
panel_prim.ApplyAPI("AccessibilityAPI", "default")
panel_prim.ApplyAPI("AccessibilityAPI", "navigation")

panel_prim.CreateAttribute("accessibility:default:label", Sdf.ValueTypeNames.Token, custom=False).Set("Main Control Panel")
panel_prim.CreateAttribute("accessibility:default:description", Sdf.ValueTypeNames.String, custom=False).Set("Primary UI control surface")
panel_prim.CreateAttribute("accessibility:default:priority", Sdf.ValueTypeNames.Token, custom=False).Set("medium")

# Second instance for navigation-specific accessibility
panel_prim.CreateAttribute("accessibility:navigation:label", Sdf.ValueTypeNames.Token, custom=False).Set("Navigation Panel")
panel_prim.CreateAttribute("accessibility:navigation:priority", Sdf.ValueTypeNames.Token, custom=False).Set("low")

stage.GetRootLayer().Save()
