"""
Joints.py — Generate joints.usda programmatically.

Demonstrates PhysicsFixedJoint, PhysicsRevoluteJoint, PhysicsPrismaticJoint,
PhysicsSphericalJoint, PhysicsDistanceJoint, PhysicsLimitAPI, and
PhysicsDriveAPI via generic USD attribute/relationship creation.
"""

from pxr import Usd, UsdGeom, Sdf, Gf, Vt

OUTPUT_PATH = "joints.usda"


def _add_rigid_box(stage: Usd.Stage, path: str, translate: Gf.Vec3d) -> Usd.Prim:
    """Helper: define a Cube with RigidBodyAPI + CollisionAPI at the given path."""
    prim = stage.DefinePrim(path, "Cube")
    for schema in ("PhysicsRigidBodyAPI", "PhysicsCollisionAPI"):
        prim.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))
    prim.CreateAttribute("size", Sdf.ValueTypeNames.Double).Set(40.0)
    xf = UsdGeom.Xformable(prim)
    xf.AddTranslateOp().Set(translate)
    return prim


def create_joints_stage(path: str) -> Usd.Stage:
    stage = Usd.Stage.CreateNew(path)

    # ── Stage metadata ────────────────────────────────────────────────────────
    stage.SetMetadata("upAxis", "Y")
    stage.SetMetadata("metersPerUnit", 0.01)
    stage.GetRootLayer().defaultPrim = "World"
    stage.SetTimeCodesPerSecond(24)

    # ── World Xform ───────────────────────────────────────────────────────────
    UsdGeom.Xform.Define(stage, "/World")

    # ── Two rigid bodies to connect ───────────────────────────────────────────
    _add_rigid_box(stage, "/World/BoxA", Gf.Vec3d(0, 200, 0))
    _add_rigid_box(stage, "/World/BoxB", Gf.Vec3d(100, 200, 0))

    box_a = Sdf.Path("/World/BoxA")
    box_b = Sdf.Path("/World/BoxB")

    # ── FixedJoint ────────────────────────────────────────────────────────────
    weld = stage.DefinePrim("/World/Weld", "PhysicsFixedJoint")
    weld.CreateRelationship("physics:body0").SetTargets([box_a])
    weld.CreateRelationship("physics:body1").SetTargets([box_b])
    weld.CreateAttribute("physics:collisionEnabled", Sdf.ValueTypeNames.Bool).Set(False)

    # ── RevoluteJoint with LimitAPI:rotX and DriveAPI:rotX ───────────────────
    hinge = stage.DefinePrim("/World/Hinge", "PhysicsRevoluteJoint")
    for schema in ("PhysicsLimitAPI:rotX", "PhysicsDriveAPI:rotX"):
        hinge.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))

    hinge.CreateRelationship("physics:body0").SetTargets([box_a])
    hinge.CreateRelationship("physics:body1").SetTargets([box_b])
    hinge.CreateAttribute(
        "physics:axis", Sdf.ValueTypeNames.Token,
        custom=False, variability=Sdf.VariabilityUniform
    ).Set("X")

    # LimitAPI:rotX
    hinge.CreateAttribute("physics:rotX:low", Sdf.ValueTypeNames.Float).Set(-90.0)
    hinge.CreateAttribute("physics:rotX:high", Sdf.ValueTypeNames.Float).Set(90.0)

    # DriveAPI:rotX
    hinge.CreateAttribute("physics:rotX:stiffness", Sdf.ValueTypeNames.Float).Set(1000.0)
    hinge.CreateAttribute("physics:rotX:damping", Sdf.ValueTypeNames.Float).Set(100.0)
    hinge.CreateAttribute("physics:rotX:maxForce", Sdf.ValueTypeNames.Float).Set(5000.0)
    hinge.CreateAttribute("physics:rotX:targetPosition", Sdf.ValueTypeNames.Float).Set(0.0)
    hinge.CreateAttribute("physics:rotX:type", Sdf.ValueTypeNames.Token).Set("force")

    # ── PrismaticJoint with LimitAPI:transX ──────────────────────────────────
    slider = stage.DefinePrim("/World/Slider", "PhysicsPrismaticJoint")
    slider.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName("PhysicsLimitAPI:transX"))

    slider.CreateRelationship("physics:body0").SetTargets([box_a])
    slider.CreateRelationship("physics:body1").SetTargets([box_b])
    slider.CreateAttribute(
        "physics:axis", Sdf.ValueTypeNames.Token,
        custom=False, variability=Sdf.VariabilityUniform
    ).Set("X")
    slider.CreateAttribute("physics:transX:low", Sdf.ValueTypeNames.Float).Set(-50.0)
    slider.CreateAttribute("physics:transX:high", Sdf.ValueTypeNames.Float).Set(50.0)

    # ── SphericalJoint with LimitAPI:swing ───────────────────────────────────
    ball = stage.DefinePrim("/World/BallSocket", "PhysicsSphericalJoint")
    ball.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName("PhysicsLimitAPI:swing"))

    ball.CreateRelationship("physics:body0").SetTargets([box_a])
    ball.CreateRelationship("physics:body1").SetTargets([box_b])
    ball.CreateAttribute("physics:swing:high", Sdf.ValueTypeNames.Float).Set(45.0)
    ball.CreateAttribute("physics:swing:low", Sdf.ValueTypeNames.Float).Set(-1.0)

    # ── DistanceJoint ─────────────────────────────────────────────────────────
    spring = stage.DefinePrim("/World/Spring", "PhysicsDistanceJoint")
    spring.CreateRelationship("physics:body0").SetTargets([box_a])
    spring.CreateRelationship("physics:body1").SetTargets([box_b])
    spring.CreateAttribute("physics:minEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    spring.CreateAttribute("physics:maxEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    spring.CreateAttribute("physics:minDistance", Sdf.ValueTypeNames.Float).Set(50.0)
    spring.CreateAttribute("physics:maxDistance", Sdf.ValueTypeNames.Float).Set(150.0)

    stage.GetRootLayer().Save()
    return stage


if __name__ == "__main__":
    stage = create_joints_stage(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(stage.GetRootLayer().ExportToString())
