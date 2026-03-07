"""
ModelAndClips.py — Demonstrates UsdModelAPI (kind metadata + assetInfo) and
UsdClipsAPI (value clips for externally-animated attributes).

UsdModelAPI is a codeless schema that exposes helpers for reading and writing
the `kind` metadata and `assetInfo` dictionary on model prims.  Kinds define
a hierarchy:  assembly > group > component > subcomponent.

UsdClipsAPI lets a prim pull time-sampled attribute values from external clip
layers, enabling shot-level animation overrides without modifying the asset.
"""

from pxr import Usd, UsdGeom, UsdLux, UsdUtils, Sdf, Gf, Vt, Kind

stage = Usd.Stage.CreateNew("modelAndClips.usda")

# ------------------------------------------------------------------
# Stage metadata
# ------------------------------------------------------------------
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ------------------------------------------------------------------
# Scene assembly — top-level grouping of multiple components
# ------------------------------------------------------------------
scene = UsdGeom.Xform.Define(stage, "/World/Scene")
scene_prim = scene.GetPrim()

# UsdModelAPI: set kind metadata so pipeline tools can recognise this prim
Usd.ModelAPI(scene_prim).SetKind(Kind.Tokens.assembly)

# assetInfo stores pipeline-relevant metadata (name, version, identifier)
Usd.ModelAPI(scene_prim).SetAssetInfo({
    "identifier": Sdf.AssetPath("./scene.usd"),
    "name": "ParkingLot",
    "version": "2.1",
})

# ------------------------------------------------------------------
# Car — leaf-level publishable component with value clips on wheels
# ------------------------------------------------------------------
car = UsdGeom.Xform.Define(stage, "/World/Scene/Car")
car_prim = car.GetPrim()
Usd.ModelAPI(car_prim).SetKind(Kind.Tokens.component)
Usd.ModelAPI(car_prim).SetAssetInfo({
    "identifier": Sdf.AssetPath("./car.usd"),
    "name": "SportsCar",
    "version": "1.0",
})

# ------------------------------------------------------------------
# UsdClipsAPI — route wheel rotation from external clip layers
# ------------------------------------------------------------------
clips_api = Usd.ClipsAPI(car_prim)

# List the clip layer files (two separate shot segments)
clips_api.SetClipAssetPaths(
    [Sdf.AssetPath("./wheels_anim_001.usda"), Sdf.AssetPath("./wheels_anim_002.usda")],
    "default"
)

# Map stage time ranges to clip indices:
#   frames  0–47  → clip 0 (wheels_anim_001.usda)
#   frames 48–95  → clip 1 (wheels_anim_002.usda)
clips_api.SetClipActive(
    [(0.0, 0), (48.0, 1)],
    "default"
)

# Remap stage time → clip-internal time (looping each 24-frame clip)
clips_api.SetClipTimes(
    [(0.0, 0.0), (24.0, 24.0), (48.0, 0.0), (72.0, 24.0)],
    "default"
)

# Prim path inside each clip layer that provides the animated attributes
clips_api.SetClipPrimPath("/Car", "default")

# ------------------------------------------------------------------
# Car body — static mesh
# ------------------------------------------------------------------
body = UsdGeom.Mesh.Define(stage, "/World/Scene/Car/Body")
body.CreatePointsAttr([
    Gf.Vec3f(-1.1, 0.0, -2.4), Gf.Vec3f( 1.1, 0.0, -2.4),
    Gf.Vec3f( 1.1, 1.5, -2.4), Gf.Vec3f(-1.1, 1.5, -2.4),
    Gf.Vec3f(-1.1, 0.0,  2.4), Gf.Vec3f( 1.1, 0.0,  2.4),
    Gf.Vec3f( 1.1, 1.5,  2.4), Gf.Vec3f(-1.1, 1.5,  2.4),
])
body.CreateFaceVertexCountsAttr([4, 4, 4, 4, 4, 4])
body.CreateFaceVertexIndicesAttr([0, 1, 2, 3, 4, 5, 6, 7, 0, 4, 5, 1, 3, 2, 6, 7, 0, 3, 7, 4, 1, 5, 6, 2])
body.CreateExtentAttr([Gf.Vec3f(-1.1, 0, -2.4), Gf.Vec3f(1.1, 1.5, 2.4)])
body.CreateDisplayColorAttr([Gf.Vec3f(0.1, 0.1, 0.8)])  # deep blue paint

# ------------------------------------------------------------------
# Helper to create a wheel xform + cylinder
# ------------------------------------------------------------------
def create_wheel(path: str, tx: float, ty: float, tz: float):
    wheel = UsdGeom.Xform.Define(stage, path)
    UsdGeom.XformCommonAPI(wheel).SetTranslate(Gf.Vec3d(tx, ty, tz))
    # rotateX driven by value clips at runtime; default is 0
    wheel.GetPrim().CreateAttribute(
        "xformOp:rotateX", Usd.ValueTypeNames.Float
    ).Set(0.0)
    wheel.CreateXformOpOrderAttr(["xformOp:translate", "xformOp:rotateX"])

    tire = UsdGeom.Cylinder.Define(stage, path + "/Tire")
    tire.CreateHeightAttr(0.25)   # tyre width
    tire.CreateRadiusAttr(0.35)   # tyre radius
    return wheel


create_wheel("/World/Scene/Car/WheelFL", -1.0, 0.35,  1.8)  # front-left
create_wheel("/World/Scene/Car/WheelFR",  1.0, 0.35,  1.8)  # front-right

# ------------------------------------------------------------------
# Props group — logical grouping (not a publishable asset)
# ------------------------------------------------------------------
props = UsdGeom.Xform.Define(stage, "/World/Scene/Props")
Usd.ModelAPI(props.GetPrim()).SetKind(Kind.Tokens.group)

# Street lamppost — a component inside the props group
lamp = UsdGeom.Xform.Define(stage, "/World/Scene/Props/Lamppost")
lamp_prim = lamp.GetPrim()
Usd.ModelAPI(lamp_prim).SetKind(Kind.Tokens.component)
Usd.ModelAPI(lamp_prim).SetAssetInfo({
    "identifier": Sdf.AssetPath("./lamppost.usd"),
    "name": "StreetLamp",
    "version": "3.0",
})

pole = UsdGeom.Cylinder.Define(stage, "/World/Scene/Props/Lamppost/Pole")
pole.CreateHeightAttr(5.0)   # 5 m tall
pole.CreateRadiusAttr(0.05)  # thin steel pole
pole.CreateDisplayColorAttr([Gf.Vec3f(0.4, 0.4, 0.4)])  # galvanised grey

lamp_head = UsdGeom.Sphere.Define(stage, "/World/Scene/Props/Lamppost/LampHead")
lamp_head.CreateRadiusAttr(0.2)
UsdGeom.XformCommonAPI(lamp_head).SetTranslate(Gf.Vec3d(0, 5.2, 0))
lamp_head.CreateDisplayColorAttr([Gf.Vec3f(1.0, 0.95, 0.8)])  # warm white

# ------------------------------------------------------------------
# Lighting and camera
# ------------------------------------------------------------------
sun = UsdLux.DistantLight.Define(stage, "/World/SunLight")
sun.CreateIntensityAttr(50000)
sun.CreateAngleAttr(0.53)
UsdGeom.XformCommonAPI(sun).SetRotate(Gf.Vec3f(-50, 20, 0))

cam = UsdGeom.Camera.Define(stage, "/World/MainCam")
cam.CreateFocalLengthAttr(50)
cam.CreateHorizontalApertureAttr(36)
cam.CreateClippingRangeAttr(Gf.Vec2f(0.1, 2000))
UsdGeom.XformCommonAPI(cam).SetTranslate(Gf.Vec3d(5, 4, 12))
UsdGeom.XformCommonAPI(cam).SetRotate(Gf.Vec3f(-15, 20, 0))

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------
stage.GetRootLayer().Save()
