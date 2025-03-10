from pxr import Usd, UsdGeom, UsdLux, Gf, Sdf

# Create a new stage
stage = Usd.Stage.CreateNew('hello_world.usda')

# Define the root Xform (World)
world = UsdGeom.Xform.Define(stage, '/World')

# Define the Geom Xform
geom = UsdGeom.Xform.Define(stage, '/World/Geom')

# Define the Cube
cube = UsdGeom.Cube.Define(stage, '/World/Geom/Cube')
cube.GetSizeAttr().Set(2.0)

# Define the Lights Xform
lights = UsdGeom.Xform.Define(stage, '/World/Lights')

# Define the SphereLight
sphereLight = UsdLux.SphereLight.Define(stage, '/World/Lights/PointLight')
sphereLight.GetIntensityAttr().Set(500.0)
sphereLight.GetColorAttr().Set(Gf.Vec3f(1.0, 1.0, 1.0))
sphereLight.GetRadiusAttr().Set(0.5)

# Set the transform for the SphereLight
lightXform = sphereLight.AddTransformOp()
lightXform.Set(Gf.Matrix4d(1.0).SetTranslate(Gf.Vec3d(5.0, 5.0, 5.0)))

# Set the default prim
stage.SetDefaultPrim(world.GetPrim())

# Save the stage to a file
stage.GetRootLayer().Save()

print("USD file 'hello_world.usda' created successfully.")