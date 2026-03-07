"""
Collision.py — Generate collision.usda programmatically.

Demonstrates PhysicsCollisionAPI, PhysicsMeshCollisionAPI,
PhysicsCollisionGroup, and PhysicsFilteredPairsAPI via generic USD
attribute/relationship creation (no UsdPhysics plugin required).
"""

from pxr import Usd, UsdGeom, Sdf, Gf, Vt

OUTPUT_PATH = "collision.usda"


def create_collision_stage(path: str) -> Usd.Stage:
    stage = Usd.Stage.CreateNew(path)

    # ── Stage metadata ────────────────────────────────────────────────────────
    stage.SetMetadata("upAxis", "Y")
    stage.SetMetadata("metersPerUnit", 0.01)
    stage.GetRootLayer().defaultPrim = "World"
    stage.SetTimeCodesPerSecond(24)

    # ── World Xform ───────────────────────────────────────────────────────────
    UsdGeom.Xform.Define(stage, "/World")

    # ── Mesh with CollisionAPI + MeshCollisionAPI ─────────────────────────────
    mesh = UsdGeom.Mesh.Define(stage, "/World/ComplexRock")
    mesh_prim = mesh.GetPrim()

    for schema in ("PhysicsCollisionAPI", "PhysicsMeshCollisionAPI"):
        mesh_prim.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))

    mesh.CreatePointsAttr(
        Vt.Vec3fArray([
            Gf.Vec3f(-50, 0, -50),
            Gf.Vec3f(50, 0, -50),
            Gf.Vec3f(0, 100, 0),
            Gf.Vec3f(-50, 0, 50),
            Gf.Vec3f(50, 0, 50),
        ])
    )
    mesh.CreateFaceVertexCountsAttr(Vt.IntArray([3, 3, 3, 3]))
    mesh.CreateFaceVertexIndicesAttr(Vt.IntArray([0, 1, 2, 1, 4, 2, 4, 3, 2, 3, 0, 2]))

    mesh_prim.CreateAttribute(
        "physics:collisionEnabled", Sdf.ValueTypeNames.Bool
    ).Set(True)
    mesh_prim.CreateAttribute(
        "physics:approximation", Sdf.ValueTypeNames.Token,
        custom=False, variability=Sdf.VariabilityUniform
    ).Set("convexDecomposition")

    # ── PlayerGroup (PhysicsCollisionGroup) ───────────────────────────────────
    player_group = stage.DefinePrim("/World/PlayerGroup", "PhysicsCollisionGroup")
    player_group.CreateAttribute(
        "physics:mergeGroupName", Sdf.ValueTypeNames.Bool
    ).Set(False)
    player_group.CreateRelationship("physics:filteredGroups").SetTargets(
        [Sdf.Path("/World/EnemyGroup")]
    )
    player_group.CreateRelationship("collection:colliders:includes").SetTargets(
        [Sdf.Path("/World/ComplexRock")]
    )

    # ── EnemyGroup (PhysicsCollisionGroup) ───────────────────────────────────
    enemy_group = stage.DefinePrim("/World/EnemyGroup", "PhysicsCollisionGroup")
    enemy_group.CreateRelationship("physics:filteredGroups").SetTargets(
        [Sdf.Path("/World/PlayerGroup")]
    )

    # ── Ragdoll with FilteredPairsAPI ─────────────────────────────────────────
    ragdoll = UsdGeom.Xform.Define(stage, "/World/Ragdoll")
    ragdoll_prim = ragdoll.GetPrim()
    ragdoll_prim.ApplyAPI(
        Usd.SchemaRegistry.GetTypeFromName("PhysicsFilteredPairsAPI")
    )
    ragdoll_prim.CreateRelationship("physics:filteredPairs").SetTargets(
        [Sdf.Path("/World/ComplexRock")]
    )

    # Torso child cube
    torso = stage.DefinePrim("/World/Ragdoll/Torso", "Cube")
    for schema in ("PhysicsCollisionAPI", "PhysicsRigidBodyAPI"):
        torso.ApplyAPI(Usd.SchemaRegistry.GetTypeFromName(schema))
    torso.CreateAttribute("size", Sdf.ValueTypeNames.Double).Set(60.0)
    torso.CreateAttribute(
        "physics:collisionEnabled", Sdf.ValueTypeNames.Bool
    ).Set(True)

    stage.GetRootLayer().Save()
    return stage


if __name__ == "__main__":
    stage = create_collision_stage(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(stage.GetRootLayer().ExportToString())
