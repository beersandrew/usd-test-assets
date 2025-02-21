from pxr import Sdf, UsdGeom, Usd, UsdMedia

stage = Usd.Stage.CreateNew("spatialAudio.usda")

stage.SetStartTimeCode(0)
stage.SetEndTimeCode(240)
stage.SetTimeCodesPerSecond(24)

world = UsdGeom.Xform.Define(stage, "/World")

stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Cube"))
audio = UsdMedia.SpatialAudio.Define(stage, cube.GetPath().AppendPath("Speech"))

audio.CreateFilePathAttr("mySpeech.mp3")
audio.CreateAuralModeAttr("spatial")
audio.CreatePlaybackModeAttr("onceFromStartToEnd")
audio.CreateStartTimeAttr(240.0)
audio.CreateEndTimeAttr(480.0)


audio = UsdMedia.SpatialAudio.Define(stage, world.GetPath().AppendPath("Ambient"))

audio.CreateFilePathAttr("myAmbientTrack.mp3")
audio.CreateAuralModeAttr("nonSpatial")
audio.CreatePlaybackModeAttr("loopFromStage")


stage.GetRootLayer().Save()