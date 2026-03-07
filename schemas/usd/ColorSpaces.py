"""
ColorSpaces.py — Demonstrates UsdColorSpaceAPI (single-apply) and
UsdColorSpaceDefinitionAPI (multiple-apply).

UsdColorSpaceAPI marks a prim with the color space token that describes
how its color data (textures, Cd attributes, etc.) is encoded.

UsdColorSpaceDefinitionAPI defines custom named color spaces directly in
the scene, providing primaries, white point, and transfer function data
so renderers can do accurate color management without external config files.
"""

from pxr import Usd, UsdGeom, UsdLux, Gf

stage = Usd.Stage.CreateNew("colorSpaces.usda")

# ------------------------------------------------------------------
# Stage metadata
# ------------------------------------------------------------------
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ------------------------------------------------------------------
# Apply UsdColorSpaceAPI to the World prim (scene default = sRGB)
# ------------------------------------------------------------------
world_prim = world.GetPrim()
world_prim.ApplyAPI("ColorSpaceAPI")
world_prim.CreateAttribute("colorSpace", Usd.ValueTypeNames.Token, custom=False).Set("sRGB")

# ------------------------------------------------------------------
# Ground plane — sRGB albedo texture
# ------------------------------------------------------------------
ground = UsdGeom.Mesh.Define(stage, "/World/Ground")
ground.CreatePointsAttr([
    Gf.Vec3f(-5, 0, -5), Gf.Vec3f(5, 0, -5),
    Gf.Vec3f(5, 0, 5),   Gf.Vec3f(-5, 0, 5),
])
ground.CreateFaceVertexCountsAttr([4])
ground.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
ground.CreateExtentAttr([Gf.Vec3f(-5, 0, -5), Gf.Vec3f(5, 0, 5)])

ground_prim = ground.GetPrim()
ground_prim.ApplyAPI("ColorSpaceAPI")
# Albedo textures are typically sRGB-encoded
ground_prim.CreateAttribute("colorSpace", Usd.ValueTypeNames.Token, custom=False).Set("sRGB")

# ------------------------------------------------------------------
# Wall — linear Rec.709 for normal / roughness maps
# ------------------------------------------------------------------
wall = UsdGeom.Mesh.Define(stage, "/World/Wall")
wall.CreatePointsAttr([
    Gf.Vec3f(-3, 0, 0), Gf.Vec3f(3, 0, 0),
    Gf.Vec3f(3, 4, 0),  Gf.Vec3f(-3, 4, 0),
])
wall.CreateFaceVertexCountsAttr([4])
wall.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
wall.CreateExtentAttr([Gf.Vec3f(-3, 0, 0), Gf.Vec3f(3, 4, 0)])

wall_prim = wall.GetPrim()
wall_prim.ApplyAPI("ColorSpaceAPI")
# Normal / roughness maps are linear — no gamma correction needed
wall_prim.CreateAttribute("colorSpace", Usd.ValueTypeNames.Token, custom=False).Set("lin_rec709")

# ------------------------------------------------------------------
# ColorSpaceLibrary — hosts UsdColorSpaceDefinitionAPI instances
# ------------------------------------------------------------------
lib_prim = stage.DefinePrim("/World/ColorSpaceLibrary")
lib_prim.ApplyAPI("ColorSpaceDefinitionAPI", "studio_wide")
lib_prim.ApplyAPI("ColorSpaceDefinitionAPI", "studio_log")

# studio_wide: P3-D65 wide-gamut HDR mastering space
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:name",
                         Usd.ValueTypeNames.Token).Set("studio_wide")
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:description",
                         Usd.ValueTypeNames.String).Set("P3-D65 wide-gamut HDR mastering space")
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:redPrimary",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.68, 0.32))    # DCI-P3 red
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:greenPrimary",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.265, 0.69))   # DCI-P3 green
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:bluePrimary",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.15, 0.06))    # DCI-P3 blue
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:whitePoint",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.3127, 0.329)) # D65 illuminant
lib_prim.CreateAttribute("colorSpaceDefinition:studio_wide:gamma",
                         Usd.ValueTypeNames.Float).Set(1.0)  # linear transfer function

# studio_log: ACEScg AP1 log-encoded VFX working space
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:name",
                         Usd.ValueTypeNames.Token).Set("studio_log")
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:description",
                         Usd.ValueTypeNames.String).Set("ACEScg log-encoded VFX working space")
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:redPrimary",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.713, 0.293))      # ACES AP1 red
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:greenPrimary",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.165, 0.83))       # ACES AP1 green
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:bluePrimary",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.128, 0.044))      # ACES AP1 blue
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:whitePoint",
                         Usd.ValueTypeNames.Float2).Set(Gf.Vec2f(0.32168, 0.33767))  # ACES D60 white
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:gamma",
                         Usd.ValueTypeNames.Float).Set(1.0)   # log curve, gamma leg unused
lib_prim.CreateAttribute("colorSpaceDefinition:studio_log:linearBias",
                         Usd.ValueTypeNames.Float).Set(0.0)   # no lift offset

# ------------------------------------------------------------------
# Light and camera
# ------------------------------------------------------------------
sun = UsdLux.DistantLight.Define(stage, "/World/SunLight")
sun.CreateAngleAttr(0.53)
sun.CreateIntensityAttr(50000)
UsdGeom.XformCommonAPI(sun).SetRotate(Gf.Vec3f(-45, 30, 0))

cam = UsdGeom.Camera.Define(stage, "/World/MainCam")
cam.CreateFocalLengthAttr(35)
cam.CreateHorizontalApertureAttr(36)
cam.CreateClippingRangeAttr(Gf.Vec2f(0.1, 1000))
UsdGeom.XformCommonAPI(cam).SetTranslate(Gf.Vec3d(0, 3, 10))

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------
stage.GetRootLayer().Save()
