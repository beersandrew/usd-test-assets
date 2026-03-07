"""
Generates camera.usda — demonstrates UsdGeomCamera with perspective,
orthographic, and anamorphic configurations, including animated dolly.

Run:
    python Camera.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("camera.usda")

root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Perspective camera with animated dolly ────────────────────────────────────
persp = UsdGeom.Camera.Define(stage, "/World/PerspectiveCamera")
persp.GetProjectionAttr().Set(UsdGeom.Tokens.perspective)
persp.GetFocalLengthAttr().Set(5.0)          # 50mm lens
persp.GetHorizontalApertureAttr().Set(3.6)   # 36mm full-frame width
persp.GetVerticalApertureAttr().Set(2.4)     # 24mm full-frame height
persp.GetHorizontalApertureOffsetAttr().Set(0.0)
persp.GetVerticalApertureOffsetAttr().Set(0.0)
persp.GetClippingRangeAttr().Set(Gf.Vec2f(0.1, 10000))
persp.GetFStopAttr().Set(2.8)
persp.GetFocusDistanceAttr().Set(500.0)

translate_op = persp.AddTranslateOp()
translate_op.Set(Gf.Vec3d(0, 5, 20), 0)
translate_op.Set(Gf.Vec3d(5, 5, 15), 12)
translate_op.Set(Gf.Vec3d(10, 5, 10), 24)

rotate_op = persp.AddRotateXYZOp()
rotate_op.Set(Gf.Vec3f(-10, 0, 0), 0)
rotate_op.Set(Gf.Vec3f(-10, -20, 0), 12)
rotate_op.Set(Gf.Vec3f(-15, -45, 0), 24)

# ── Orthographic camera ───────────────────────────────────────────────────────
ortho = UsdGeom.Camera.Define(stage, "/World/OrthographicCamera")
ortho.GetProjectionAttr().Set(UsdGeom.Tokens.orthographic)
ortho.GetHorizontalApertureAttr().Set(20.0)
ortho.GetVerticalApertureAttr().Set(15.0)
ortho.GetFocalLengthAttr().Set(5.0)
ortho.GetClippingRangeAttr().Set(Gf.Vec2f(0.1, 5000))

ortho.AddTranslateOp().Set(Gf.Vec3d(0, 50, 0))
ortho.AddRotateXYZOp().Set(Gf.Vec3f(-90, 0, 0))

# ── Anamorphic camera ─────────────────────────────────────────────────────────
anam = UsdGeom.Camera.Define(stage, "/World/AnamorphicCamera")
anam.GetProjectionAttr().Set(UsdGeom.Tokens.perspective)
anam.GetFocalLengthAttr().Set(5.0)
anam.GetHorizontalApertureAttr().Set(4.8)   # 2x anamorphic squeeze
anam.GetVerticalApertureAttr().Set(2.4)
anam.GetClippingRangeAttr().Set(Gf.Vec2f(0.1, 10000))
anam.GetFStopAttr().Set(1.4)
anam.GetFocusDistanceAttr().Set(800.0)
anam.GetClippingPlanesAttr().Set([])

anam.AddTranslateOp().Set(Gf.Vec3d(20, 5, 20))
anam.AddRotateXYZOp().Set(Gf.Vec3f(-5, -45, 0))

stage.GetRootLayer().Save()
print("Wrote camera.usda")
