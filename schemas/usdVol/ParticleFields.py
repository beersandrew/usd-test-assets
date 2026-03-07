"""Generate particleFields.usda programmatically.

Demonstrates UsdVolParticleField with 3D Gaussian Splatting and Surflet kernels,
including applied APIs for position, orientation, scale, opacity, SH radiance, etc.

Run:
    python ParticleFields.py
"""

from pxr import Usd, UsdGeom, Sdf, Vt

stage = Usd.Stage.CreateNew("particleFields.usda")
stage.SetDefaultPrim(stage.DefinePrim("/World"))
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

UsdGeom.Xform.Define(stage, "/World")

# ── 3D Gaussian Splat particle field ─────────────────────────────────────────
# ParticleField prim type with multiple applied APIs for Gaussian splatting

splat_prim = stage.DefinePrim("/World/GaussianSplats", "ParticleField")
splat_prim.SetMetadata(
    "apiSchemas",
    Vt.TokenArray([
        "ParticleFieldPositionAttributeAPI",
        "ParticleFieldOrientationAttributeAPI",
        "ParticleFieldScaleAttributeAPI",
        "ParticleFieldOpacityAttributeAPI",
        "ParticleFieldKernelGaussianEllipsoidAPI",
        "ParticleFieldSphericalHarmonicsAttributeAPI",
        "ParticleFieldRadianceBaseAPI",
    ]),
)

# PositionAttributeAPI: which attribute holds per-particle positions
splat_prim.CreateAttribute(
    "particleField:positionAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("points")

splat_prim.CreateAttribute("points", Sdf.ValueTypeNames.Point3fArray).Set(
    Vt.Vec3fArray([(0, 0, 0), (10, 5, 0), (-5, 10, 3), (7, -3, 8)])
)

# OrientationAttributeAPI: per-particle quaternion orientations
splat_prim.CreateAttribute(
    "particleField:orientationAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("orientations")

# quath (half-precision quaternion) stored as float4 arrays
splat_prim.CreateAttribute("orientations", Sdf.ValueTypeNames.QuathArray).Set(
    Vt.QuathArray([
        (1, 0, 0, 0),
        (0.707, 0.707, 0, 0),
        (1, 0, 0, 0),
        (0.5, 0.5, 0.5, 0.5),
    ])
)

# ScaleAttributeAPI: per-particle 3D ellipsoid radii
splat_prim.CreateAttribute(
    "particleField:scaleAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("scales")

splat_prim.CreateAttribute("scales", Sdf.ValueTypeNames.Float3Array).Set(
    Vt.Vec3fArray([
        (0.1, 0.1, 0.1),
        (0.2, 0.15, 0.1),
        (0.08, 0.08, 0.12),
        (0.15, 0.2, 0.1),
    ])
)

# OpacityAttributeAPI: per-particle opacity values in [0, 1]
splat_prim.CreateAttribute(
    "particleField:opacityAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("opacities")

splat_prim.CreateAttribute("opacities", Sdf.ValueTypeNames.FloatArray).Set(
    Vt.FloatArray([0.9, 0.7, 0.85, 0.6])
)

# SphericalHarmonicsAttributeAPI: view-dependent color via SH coefficients
splat_prim.CreateAttribute(
    "particleField:shAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("shCoeffs")

# Degree-1 SH: 4 coefficients × 3 channels (RGB) = 12 floats
splat_prim.CreateAttribute("shCoeffs", Sdf.ValueTypeNames.FloatArray).Set(
    Vt.FloatArray([
        0.5, 0.4, 0.3,   # DC (band 0) - base color
        0.1, 0.0, 0.0,   # band 1 Y(-1,1)
        0.0, 0.1, 0.0,   # band 1 Y(0,1)
        0.0, 0.0, 0.1,   # band 1 Y(1,1)
    ])
)

# RadianceBaseAPI: overall radiance scale factor
splat_prim.CreateAttribute(
    "particleField:radianceScale", Sdf.ValueTypeNames.Float
).Set(1.0)

# ── Surflet-based particle field ──────────────────────────────────────────────
# Uses KernelGaussianSurfletAPI: oriented disc (2.5D) kernel

surflet_prim = stage.DefinePrim("/World/SurfletField", "ParticleField")
surflet_prim.SetMetadata(
    "apiSchemas",
    Vt.TokenArray([
        "ParticleFieldPositionAttributeAPI",
        "ParticleFieldScaleAttributeAPI",
        "ParticleFieldOpacityAttributeAPI",
        "ParticleFieldKernelGaussianSurfletAPI",
        "ParticleFieldRadianceBaseAPI",
    ]),
)

surflet_prim.CreateAttribute(
    "particleField:positionAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("points")

surflet_prim.CreateAttribute("points", Sdf.ValueTypeNames.Point3fArray).Set(
    Vt.Vec3fArray([(5, 0, 0), (10, 3, 2), (15, 0, 1)])
)

surflet_prim.CreateAttribute(
    "particleField:scaleAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("scales")

surflet_prim.CreateAttribute("scales", Sdf.ValueTypeNames.Float3Array).Set(
    Vt.Vec3fArray([(0.05, 0.05, 0.05), (0.07, 0.07, 0.07), (0.06, 0.06, 0.06)])
)

surflet_prim.CreateAttribute(
    "particleField:opacityAttr",
    Sdf.ValueTypeNames.Token,
    custom=False,
    variability=Sdf.VariabilityUniform,
).Set("opacities")

surflet_prim.CreateAttribute("opacities", Sdf.ValueTypeNames.FloatArray).Set(
    Vt.FloatArray([0.8, 0.75, 0.9])
)

# RadianceBaseAPI: slightly reduced radiance for surflet representation
surflet_prim.CreateAttribute(
    "particleField:radianceScale", Sdf.ValueTypeNames.Float
).Set(0.8)

stage.GetRootLayer().Save()
print("Saved particleFields.usda")
