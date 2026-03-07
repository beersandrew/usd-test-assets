from pxr import Usd, UsdGeom, UsdLux, Gf

stage = Usd.Stage.CreateNew("shapingAndShadow.usda")

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetTimeCodesPerSecond(24)

# ── SphereLight with ShapingAPI for spotlight-like cone control ───────────
spotlight = UsdLux.SphereLight.Define(stage, "/World/Spotlight")
spotlight.CreateIntensityAttr(30000.0)
spotlight.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 0.9))

# Apply ShapingAPI for cone/IES control
shaping_api = UsdLux.ShapingAPI.Apply(spotlight.GetPrim())
# Half-angle of the cone in degrees
shaping_api.CreateShapingConeAngleAttr(30.0)
# Softness of the cone edge
shaping_api.CreateShapingConeSoftnessAttr(0.2)
# Concentrates light toward center
shaping_api.CreateShapingFocusAttr(5.0)
# IES profile for realistic light distribution
shaping_api.CreateShapingIesFileAttr("./ies/spot_par38.ies")
shaping_api.CreateShapingIesAngleScaleAttr(1.0)

# ── RectLight with ShadowAPI for fine-grained shadow control ─────────────
shadow_caster = UsdLux.RectLight.Define(stage, "/World/ShadowCaster")
shadow_caster.CreateWidthAttr(80.0)
shadow_caster.CreateHeightAttr(80.0)
shadow_caster.CreateIntensityAttr(25000.0)

# Apply ShadowAPI to enable and configure shadow casting
shadow_api = UsdLux.ShadowAPI.Apply(shadow_caster.GetPrim())
shadow_api.CreateShadowEnableAttr(True)
shadow_api.CreateShadowColorAttr(Gf.Vec3f(0.0, 0.0, 0.0))
# Max distance for shadow casters
shadow_api.CreateShadowDistanceAttr(1000.0)
# Falloff start distance
shadow_api.CreateShadowFalloffAttr(100.0)
shadow_api.CreateShadowFalloffGammaAttr(1.0)
shadow_api.CreateShadowBiasAttr(0.01)

stage.GetRootLayer().Save()
