"""
RigidBody.py — Generate rigidBody.usda programmatically.

Demonstrates PhysicsScene, PhysicsRigidBodyAPI, PhysicsMassAPI,
PhysicsCollisionAPI, and PhysicsMaterialAPI via generic USD attribute
creation (no UsdPhysics plugin required).
"""

from pxr import Usd, UsdGeom, Sdf, Gf, Vt

OUTPUT_PATH = "rigidBody.usda"


def create_rigid_body_stage(path: str) -> Usd.Stage:
    stage = Usd.Stage.CreateNew(path)

    # ── Stage metadata ────────────────────────────────────────────────────────
    stage.SetMetadata("upAxis", "Y")
    stage.SetMetadata("metersPerUnit", 0.01)
    stage.GetRootLayer().defaultPrim = "World"
    stage.SetTimeCodesPerSecond(24)

    # ── World Xform ───────────────────────────────────────────────────────────
    world = UsdGeom.Xform.Define(stage, "/World")

    # ── PhysicsScene ──────────────────────────────────────────────────────────
    scene_prim = stage.DefinePrim("/World/PhysicsScene", "PhysicsScene")
    scene_prim.CreateAttribute(
        "physics:gravityDirection", Sdf.ValueTypeNames.Vector3f
    ).Set(Gf.Vec3f(0.0, -1.0, 0.0))
    scene_prim.CreateAttribute(
        "physics:gravityMagnitude", Sdf.ValueTypeNames.Float
    ).Set(981.0)  # cm/s²

    # ── Ground Plane ──────────────────────────────────────────────────────────
    ground_prim = stage.DefinePrim("/World/Ground", "Plane")
    ground_prim.GetPrimTypeInfo()
    ground_prim.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName("PhysicsCollisionAPI"))
    ground_prim.CreateAttribute(
        "physics:axis", Sdf.ValueTypeNames.Token
    ).Set("Y")

    # ── Rigid Body Cube ───────────────────────────────────────────────────────
    box = stage.DefinePrim("/World/RigidBox", "Cube")
    for schema in ("PhysicsRigidBodyAPI", "PhysicsMassAPI", "PhysicsCollisionAPI"):
        box.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))

    box.CreateAttribute("size", Sdf.ValueTypeNames.Double).Set(50.0)

    # RigidBodyAPI attributes
    box.CreateAttribute("physics:rigidBodyEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    box.CreateAttribute(
        "physics:velocity", Sdf.ValueTypeNames.Vector3f
    ).Set(Gf.Vec3f(0.0, 0.0, 0.0))
    box.CreateAttribute(
        "physics:angularVelocity", Sdf.ValueTypeNames.Vector3f
    ).Set(Gf.Vec3f(0.0, 0.0, 0.0))
    box.CreateAttribute("physics:startAsleep", Sdf.ValueTypeNames.Bool).Set(False)

    # MassAPI attributes
    box.CreateAttribute("physics:mass", Sdf.ValueTypeNames.Float).Set(5.0)
    box.CreateAttribute(
        "physics:centerOfMass", Sdf.ValueTypeNames.Vector3f
    ).Set(Gf.Vec3f(0.0, 0.0, 0.0))
    box.CreateAttribute(
        "physics:diagonalInertia", Sdf.ValueTypeNames.Vector3f
    ).Set(Gf.Vec3f(833.0, 833.0, 833.0))
    box.CreateAttribute("physics:density", Sdf.ValueTypeNames.Float).Set(0.004)

    # Transform
    xform_box = UsdGeom.Xformable(box)
    translate_op = xform_box.AddTranslateOp()
    translate_op.Set(Gf.Vec3d(0.0, 200.0, 0.0))

    # ── Physics Material ──────────────────────────────────────────────────────
    mat_prim = stage.DefinePrim("/World/RubberMaterial", "Material")
    mat_prim.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName("PhysicsMaterialAPI"))
    mat_prim.CreateAttribute(
        "physics:staticFriction", Sdf.ValueTypeNames.Float
    ).Set(0.8)
    mat_prim.CreateAttribute(
        "physics:dynamicFriction", Sdf.ValueTypeNames.Float
    ).Set(0.6)
    mat_prim.CreateAttribute(
        "physics:restitution", Sdf.ValueTypeNames.Float
    ).Set(0.3)
    mat_prim.CreateAttribute(
        "physics:density", Sdf.ValueTypeNames.Float
    ).Set(0.001)

    stage.GetRootLayer().Save()
    return stage


if __name__ == "__main__":
    stage = create_rigid_body_stage(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(stage.GetRootLayer().ExportToString())
