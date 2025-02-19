from pxr import Sdf, UsdGeom, Usd, UsdUI, UsdShade

stage = Usd.Stage.CreateNew("SceneGraphPrimAPI.usda")

world = UsdGeom.Xform.Define(stage, "/World")

stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Cube"))
material = UsdShade.Material.Define(stage, world.GetPath().AppendPath("MyMaterial"))
mtlx_surface_output = material.CreateOutput("mtlx:surface", Sdf.ValueTypeNames.Token)

preview_surface = UsdShade.Shader.Define(stage, material.GetPath().AppendPath("PreviewSurface"))
preview_surface.CreateIdAttr("ND_UsdPreviewSurface_surfaceshader")
preview_surface.CreateOutput("out", Sdf.ValueTypeNames.Token)
mtlx_surface_output.ConnectToSource(preview_surface.GetOutput("out"))

color = UsdShade.Shader.Define(stage, material.GetPath().AppendPath("Color"))
color.CreateIdAttr("ND_constant_color3")
color.CreateInput("value", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.023, 0.701))
color.CreateOutput("out", Sdf.ValueTypeNames.Color3f)

preview_surface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(color.GetOutput("out"))


material_binding_api = UsdShade.MaterialBindingAPI.Apply(cube.GetPrim())
material_binding_api.Bind(material)

scene_graph_api = UsdUI.SceneGraphPrimAPI.Apply(preview_surface.GetPrim())
scene_graph_api.CreateDisplayGroupAttr().Set("MyMaterial Nodes")
scene_graph_api.CreateDisplayNameAttr().Set("Preview Surface Node")

scene_graph_api = UsdUI.SceneGraphPrimAPI.Apply(color.GetPrim())
scene_graph_api.CreateDisplayGroupAttr().Set("MyMaterial Nodes")
scene_graph_api.CreateDisplayNameAttr().Set("Color Node")

stage.GetRootLayer().Save()