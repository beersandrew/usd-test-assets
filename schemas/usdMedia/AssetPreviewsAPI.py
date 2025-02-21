from pxr import Sdf, UsdGeom, Usd, UsdMedia

stage = Usd.Stage.CreateNew("assetPreviewsApi.usda")

world = UsdGeom.Xform.Define(stage, "/World")

stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Cube"))

mediaAPI = UsdMedia.AssetPreviewsAPI.Apply(world.GetPrim())
thumbnails = UsdMedia.AssetPreviewsAPI.Thumbnails(defaultImage = Sdf.AssetPath("defaultThumbnail.jpg"))

print(thumbnails)
mediaAPI.SetDefaultThumbnails(thumbnails)


stage.GetRootLayer().Save()