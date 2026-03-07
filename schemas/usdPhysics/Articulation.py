"""
Articulation.py — Generate articulation.usda programmatically.

Demonstrates PhysicsArticulationRootAPI applied to a robot-arm hierarchy
with a kinematic base, a dynamic upper arm, and a driven revolute joint
(PhysicsLimitAPI + PhysicsDriveAPI).
"""

from pxr import Usd, UsdGeom, Sdf, Gf

OUTPUT_PATH = "articulation.usda"


def create_articulation_stage(path: str) -> Usd.Stage:
    stage = Usd.Stage.CreateNew(path)

    # ── Stage metadata ────────────────────────────────────────────────────────
    stage.SetMetadata("upAxis", "Y")
    stage.SetMetadata("metersPerUnit", 0.01)
    stage.GetRootLayer().defaultPrim = "World"
    stage.SetTimeCodesPerSecond(24)

    # ── World Xform ───────────────────────────────────────────────────────────
    UsdGeom.Xform.Define(stage, "/World")

    # ── RobotArm Xform (ArticulationRootAPI) ──────────────────────────────────
    robot_arm = UsdGeom.Xform.Define(stage, "/World/RobotArm")
    robot_arm_prim = robot_arm.GetPrim()
    robot_arm_prim.ApplyAPI(
        Usd.SchemaRegistry.GetTypeFromName("PhysicsArticulationRootAPI")
    )

    # ── Base (kinematic rigid body) ───────────────────────────────────────────
    base = stage.DefinePrim("/World/RobotArm/Base", "Cube")
    for schema in ("PhysicsRigidBodyAPI", "PhysicsCollisionAPI"):
        base.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))
    base.CreateAttribute("size", Sdf.ValueTypeNames.Double).Set(80.0)
    base.CreateAttribute(
        "physics:kinematicEnabled", Sdf.ValueTypeNames.Bool
    ).Set(True)

    # ── UpperArm (dynamic rigid body) ─────────────────────────────────────────
    upper_arm = stage.DefinePrim("/World/RobotArm/UpperArm", "Cube")
    for schema in ("PhysicsRigidBodyAPI", "PhysicsCollisionAPI"):
        upper_arm.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))
    upper_arm.CreateAttribute("size", Sdf.ValueTypeNames.Double).Set(30.0)

    xf = UsdGeom.Xformable(upper_arm)
    xf.AddTranslateOp().Set(Gf.Vec3d(0.0, 120.0, 0.0))
    xf.AddScaleOp().Set(Gf.Vec3f(1.0, 3.0, 1.0))

    # ── ShoulderJoint (RevoluteJoint with LimitAPI:rotZ + DriveAPI:rotZ) ──────
    shoulder = stage.DefinePrim("/World/RobotArm/ShoulderJoint", "PhysicsRevoluteJoint")
    for schema in ("PhysicsLimitAPI:rotZ", "PhysicsDriveAPI:rotZ"):
        shoulder.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))

    shoulder.CreateRelationship("physics:body0").SetTargets(
        [Sdf.Path("/World/RobotArm/Base")]
    )
    shoulder.CreateRelationship("physics:body1").SetTargets(
        [Sdf.Path("/World/RobotArm/UpperArm")]
    )
    shoulder.CreateAttribute(
        "physics:axis", Sdf.ValueTypeNames.Token,
        custom=False, variability=Sdf.VariabilityUniform
    ).Set("Z")

    # LimitAPI:rotZ
    shoulder.CreateAttribute("physics:rotZ:low", Sdf.ValueTypeNames.Float).Set(-120.0)
    shoulder.CreateAttribute("physics:rotZ:high", Sdf.ValueTypeNames.Float).Set(120.0)

    # DriveAPI:rotZ
    shoulder.CreateAttribute("physics:rotZ:stiffness", Sdf.ValueTypeNames.Float).Set(5000.0)
    shoulder.CreateAttribute("physics:rotZ:damping", Sdf.ValueTypeNames.Float).Set(500.0)
    shoulder.CreateAttribute(
        "physics:rotZ:targetPosition", Sdf.ValueTypeNames.Float
    ).Set(45.0)
    shoulder.CreateAttribute("physics:rotZ:type", Sdf.ValueTypeNames.Token).Set("force")

    stage.GetRootLayer().Save()
    return stage


if __name__ == "__main__":
    stage = create_articulation_stage(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(stage.GetRootLayer().ExportToString())
