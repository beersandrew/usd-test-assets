from pxr import Usd, UsdGeom, UsdProc, UsdHydra, Sdf, Gf

def main():
    # Create a new stage
    stage = Usd.Stage.CreateNew("rockscatter.usda")

    # ---------------------------------------------------------------------
    # /World Xform
    # ---------------------------------------------------------------------
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # ---------------------------------------------------------------------
    # 1) /World/Terrain   (simple quad mesh)
    # ---------------------------------------------------------------------
    terrain = UsdGeom.Mesh.Define(stage, "/World/Terrain")

    terrainPoints = [
        Gf.Vec3f(-5.0, 0.0, -5.0),
        Gf.Vec3f( 5.0, 0.0, -5.0),
        Gf.Vec3f( 5.0, 0.0,  5.0),
        Gf.Vec3f(-5.0, 0.0,  5.0),
    ]

    terrain.GetPointsAttr().Set(terrainPoints)
    terrain.GetFaceVertexCountsAttr().Set([4])
    terrain.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])
    terrain.GetSubdivisionSchemeAttr().Set("none")

    # ---------------------------------------------------------------------
    # 2) /World/Prototypes/Rock   (simple little pyramid rock)
    # ---------------------------------------------------------------------
    prototypesXf = UsdGeom.Xform.Define(stage, "/World/Prototypes")
    rock = UsdGeom.Mesh.Define(stage, "/World/Prototypes/Rock")

    rockPoints = [
        Gf.Vec3f(-0.3, 0.0, -0.3),
        Gf.Vec3f( 0.3, 0.0, -0.3),
        Gf.Vec3f( 0.3, 0.0,  0.3),
        Gf.Vec3f(-0.3, 0.0,  0.3),
        Gf.Vec3f( 0.0, 0.5,  0.0),
    ]

    rock.GetPointsAttr().Set(rockPoints)
    rock.GetFaceVertexCountsAttr().Set([3, 3, 3, 3])
    rock.GetFaceVertexIndicesAttr().Set([
        0, 1, 4,
        1, 2, 4,
        2, 3, 4,
        3, 0, 4,
    ])
    rock.GetSubdivisionSchemeAttr().Set("none")

    # ---------------------------------------------------------------------
    # 3) /World/RockScatter  (UsdProc + UsdHydra generative procedural)
    # ---------------------------------------------------------------------
    # Define the UsdProc.GenerativeProcedural schema prim
    proc = UsdProc.GenerativeProcedural.Define(stage, "/World/RockScatter")
    procPrim = proc.GetPrim()

    # Apply the UsdHydra.GenerativeProceduralAPI
    hydraApi = UsdHydra.GenerativeProceduralAPI.Apply(procPrim)

    # Set which procedural system should evaluate this prim.
    # (Default is already "hydraGenerativeProcedural", but we author it explicitly
    #  to match the .usda example.)
    hydraApi.CreateProceduralSystemAttr().Set(
        UsdHydra.Tokens.hydraGenerativeProcedural
    )

    # Set which HdGp plugin name to use (this is your C++ plugin id)
    hydraApi.CreateProceduralTypeAttr().Set("RockScatter")

    # ---------------------------------------------------------------------
    # Procedural parameters, authored as primvars:* attributes
    # ---------------------------------------------------------------------
    # int primvars:rockCount = 200
    procPrim.CreateAttribute(
        "primvars:rockCount", Sdf.ValueTypeNames.Int
    ).Set(200)

    # double primvars:seed = 42.0
    procPrim.CreateAttribute(
        "primvars:seed", Sdf.ValueTypeNames.Double
    ).Set(42.0)

    # asset primvars:sourceMesh = </World/Prototypes/Rock>
    procPrim.CreateAttribute(
        "primvars:sourceMesh", Sdf.ValueTypeNames.Asset
    ).Set(Sdf.AssetPath("/World/Prototypes/Rock"))

    # asset primvars:terrain = </World/Terrain>
    procPrim.CreateAttribute(
        "primvars:terrain", Sdf.ValueTypeNames.Asset
    ).Set(Sdf.AssetPath("/World/Terrain"))

    # float primvars:radius = 10.0
    procPrim.CreateAttribute(
        "primvars:radius", Sdf.ValueTypeNames.Float
    ).Set(10.0)

    # Save to disk
    stage.GetRootLayer().Save()

if __name__ == "__main__":
    main()