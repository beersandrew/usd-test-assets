"""
Generates generativeProcedural.usda — demonstrates UsdProcGenerativeProcedural.

UsdProcGenerativeProcedural is abstract; it must be subclassed with a concrete
type token.  The procedural system that evaluates the prim is identified by
`proceduralSystem`.  Custom arguments are passed in the `primvars:args:*`
namespace and forwarded verbatim to the procedural at evaluation time.

Run:
    python GenerativeProcedural.py
"""

from pxr import Usd, UsdProc, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("generativeProcedural.usda")

# ── Stage metadata ─────────────────────────────────────────────────────────────
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── ScatterRocks — Hydra-based scatter procedural ──────────────────────────────
scatter = UsdProc.GenerativeProcedural.Define(stage, "/World/ScatterRocks")

# proceduralSystem selects which Hydra scene index plugin will evaluate this prim.
scatter.CreateProceduralSystemAttr().Set("hydra")

# ── Custom procedural arguments in the primvars:args namespace ─────────────────
prim = scatter.GetPrim()

# Seed for deterministic random scatter placement.
prim.CreateAttribute(
    "primvars:args:seed", Sdf.ValueTypeNames.Int, custom=True
).Set(42)

# Number of rock instances to scatter across the surface.
prim.CreateAttribute(
    "primvars:args:instanceCount", Sdf.ValueTypeNames.Int, custom=True
).Set(500)

# Asset reference for the rock geometry library.
prim.CreateAttribute(
    "primvars:args:geometryLibrary", Sdf.ValueTypeNames.Asset, custom=True
).Set(Sdf.AssetPath("./assets/rocks.usd"))

# Bounding region for scatter placement (min X/Z in local space).
prim.CreateAttribute(
    "primvars:args:scatterBoundsMin", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(-10, -10))

# Bounding region for scatter placement (max X/Z in local space).
prim.CreateAttribute(
    "primvars:args:scatterBoundsMax", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(10, 10))

# Uniform scale range applied randomly to each scattered instance.
prim.CreateAttribute(
    "primvars:args:scaleRange", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(0.5, 2.0))

# Y-axis rotation range (degrees) applied randomly per instance.
prim.CreateAttribute(
    "primvars:args:rotationRange", Sdf.ValueTypeNames.Float2, custom=True
).Set(Gf.Vec2f(0, 360))

UsdGeom.XformCommonAPI(scatter).SetTranslate(Gf.Vec3d(0, 0, 0))

# ── CrowdSim — crowd simulation procedural ─────────────────────────────────────
crowd = UsdProc.GenerativeProcedural.Define(stage, "/World/CrowdSim")

# Uses a custom renderer-side crowd evaluation plugin.
crowd.CreateProceduralSystemAttr().Set("crowdSim")

crowd_prim = crowd.GetPrim()

# Path to the animation clip library for agent characters.
crowd_prim.CreateAttribute(
    "primvars:args:agentLibrary", Sdf.ValueTypeNames.Asset, custom=True
).Set(Sdf.AssetPath("./assets/agents.usd"))

# Total number of agents to spawn.
crowd_prim.CreateAttribute(
    "primvars:args:agentCount", Sdf.ValueTypeNames.Int, custom=True
).Set(200)

# Radius of the circular area agents are seeded into.
crowd_prim.CreateAttribute(
    "primvars:args:spawnRadius", Sdf.ValueTypeNames.Float, custom=True
).Set(20.0)

# Goal target all agents move toward (world-space position).
crowd_prim.CreateAttribute(
    "primvars:args:goalPosition", Sdf.ValueTypeNames.Float3, custom=True
).Set(Gf.Vec3f(0, 0, 0))

# Simulated playback speed multiplier (1.0 = real-time).
crowd_prim.CreateAttribute(
    "primvars:args:timeScale", Sdf.ValueTypeNames.Float, custom=True
).Set(1.0)

UsdGeom.XformCommonAPI(crowd).SetTranslate(Gf.Vec3d(0, 0, 0))

stage.GetRootLayer().Save()
print("Wrote generativeProcedural.usda")
