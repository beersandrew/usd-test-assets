"""
Generates primitives.usda — demonstrates UsdGeom implicit geometric primitives:
Sphere, Cube, Cone, Cylinder, Cylinder_1, Capsule, Capsule_1, and Plane.

Run:
    python Primitives.py
"""

from pxr import Usd, UsdGeom, Gf, Vt, Sdf

stage = Usd.Stage.CreateNew("primitives.usda")

# Set stage metadata directly on the root layer
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Sphere ────────────────────────────────────────────────────────────────────
ball = UsdGeom.Sphere.Define(stage, "/World/Ball")
ball.GetRadiusAttr().Set(1.0)
ball.GetExtentAttr().Set([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])
ball.AddTranslateOp().Set(Gf.Vec3d(0, 1, 0))

# ── Cube ──────────────────────────────────────────────────────────────────────
block = UsdGeom.Cube.Define(stage, "/World/Block")
block.GetSizeAttr().Set(2.0)
block.GetExtentAttr().Set([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])
block.AddTranslateOp().Set(Gf.Vec3d(4, 1, 0))

# ── Cone ──────────────────────────────────────────────────────────────────────
hat = UsdGeom.Cone.Define(stage, "/World/Hat")
hat.GetHeightAttr().Set(3.0)
hat.GetRadiusAttr().Set(1.0)
hat.GetAxisAttr().Set(UsdGeom.Tokens.y)
hat.GetExtentAttr().Set([Gf.Vec3f(-1, -1.5, -1), Gf.Vec3f(1, 1.5, 1)])
hat.AddTranslateOp().Set(Gf.Vec3d(8, 1.5, 0))

# ── Cylinder ──────────────────────────────────────────────────────────────────
pillar = UsdGeom.Cylinder.Define(stage, "/World/Pillar")
pillar.GetHeightAttr().Set(4.0)
pillar.GetRadiusAttr().Set(0.5)
pillar.GetAxisAttr().Set(UsdGeom.Tokens.y)
pillar.GetExtentAttr().Set([Gf.Vec3f(-0.5, -2, -0.5), Gf.Vec3f(0.5, 2, 0.5)])
pillar.AddTranslateOp().Set(Gf.Vec3d(12, 2, 0))

# ── Cylinder_1: per-end radii ─────────────────────────────────────────────────
tapered = UsdGeom.Cylinder_1.Define(stage, "/World/TaperedPillar")
tapered.GetHeightAttr().Set(4.0)
tapered.GetRadiusBottomAttr().Set(0.8)
tapered.GetRadiusTopAttr().Set(0.3)
tapered.GetAxisAttr().Set(UsdGeom.Tokens.y)
tapered.GetExtentAttr().Set([Gf.Vec3f(-0.8, -2, -0.8), Gf.Vec3f(0.8, 2, 0.8)])
tapered.AddTranslateOp().Set(Gf.Vec3d(16, 2, 0))

# ── Capsule ───────────────────────────────────────────────────────────────────
capsule = UsdGeom.Capsule.Define(stage, "/World/Capsule")
capsule.GetHeightAttr().Set(2.0)
capsule.GetRadiusAttr().Set(0.5)
capsule.GetAxisAttr().Set(UsdGeom.Tokens.y)
capsule.GetExtentAttr().Set([Gf.Vec3f(-0.5, -1.5, -0.5), Gf.Vec3f(0.5, 1.5, 0.5)])
capsule.AddTranslateOp().Set(Gf.Vec3d(20, 1.5, 0))

# ── Capsule_1: per-end radii ──────────────────────────────────────────────────
asym = UsdGeom.Capsule_1.Define(stage, "/World/AsymmetricCapsule")
asym.GetHeightAttr().Set(2.0)
asym.GetRadiusBottomAttr().Set(0.7)
asym.GetRadiusTopAttr().Set(0.3)
asym.GetAxisAttr().Set(UsdGeom.Tokens.y)
asym.GetExtentAttr().Set([Gf.Vec3f(-0.7, -1.7, -0.7), Gf.Vec3f(0.7, 2.3, 0.7)])
asym.AddTranslateOp().Set(Gf.Vec3d(24, 2.0, 0))

# ── Plane ─────────────────────────────────────────────────────────────────────
ground = UsdGeom.Plane.Define(stage, "/World/Ground")
ground.GetWidthAttr().Set(20.0)
ground.GetLengthAttr().Set(20.0)
ground.GetAxisAttr().Set(UsdGeom.Tokens.y)
ground.GetDoubleSidedAttr().Set(False)
ground.GetExtentAttr().Set([Gf.Vec3f(-10, 0, -10), Gf.Vec3f(10, 0, 10)])
ground.AddTranslateOp().Set(Gf.Vec3d(12, 0, 0))

stage.GetRootLayer().Save()
print("Wrote primitives.usda")
