# Physics


# Goal:
To discover if a single USDZ file can be used for physics on both iOS and visionOS

# iOS

## Example
See iOSBounce.usdz & iOSBounce.usda

## Structure

### Gravity
iOS enables gravity in the environment with the creationg of a gravity prim

```
def Xform "Gravity"
{
    double3 physics:gravitationalForce:acceleration = (0, -9.800000190734863, 0)
}
```

### Collision
[Apple Docs - Preliminary_PhysicsColliderAPI](https://developer.apple.com/documentation/arkit/usdz_schemas_for_ar/simulated_physical_interaction/preliminary_physicscolliderapi)

In order to have a collision the following must be true:
1. `Preliminary_PhysicsColliderAPI` schema must be applied
2. Within that prim there must exists a relationship `rel preliminary:physics:collider:convexShape = <colliderPrim>` where colliderPrim is a SdfPath
3. A collider prim that looks like the following:
```
over Sphere "collider"
{
    float3[] extent = [(-0.040882755, -0.040935293, -0.040882755), (0.040882755, 0.040935293, 0.040882755)]
    uniform token purpose = "guide"
    double radius = 0.04088275507092476
    quatf xformOp:orient = (0, 0, 0, 0)
    double3 xformOp:scale = (1, 1, 1)
    double3 xformOp:translate = (0, 0, 0)
    uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
}
```


#### Materials
[Apple Docs - Preliminary_PhysicsMaterialAPI](https://developer.apple.com/documentation/arkit/usdz_schemas_for_ar/simulated_physical_interaction/preliminary_physicsmaterialapi)

In order to have a physics material the following must be true:
1. As a child Xfrom from the prim with `Preliminary_PhysicsColliderAPI` & `Preliminary_PhysicsRigidBodyAPI` applied, create a Material prim with the `Preliminary_PhysicsMaterialAPI` applied
2. Within that prim there must exists a primvar `uniform double preliminary:physics:material:friction:dynamic = 0.62`
3. Within that prim there must exists a primvar `uniform double preliminary:physics:material:friction:static = 0.62`
4. Within that prim there must exists a primvar `uniform double preliminary:physics:material:restitution = 0.62` (This is bounciness)

### RigidBody

[Apple Docs - Preliminary_PhysicsMaterialAPI](https://developer.apple.com/documentation/arkit/usdz_schemas_for_ar/simulated_physical_interaction/preliminary_physicsmaterialapi)

In order to have a collision the following must be true:
1. `Preliminary_PhysicsRigidBodyAPI` schema must be applied
2. Within that prim there must exists a primvar `uniform double preliminary:physics:rigidBody:mass = 1.1`


# visionOS


## Example
See visionOSBounce.usdz & visionOSBounce.usda

## Structure
Physics works with specific RealityKitComponent prims underneath a Mesh

### Gravity
visionOS enables gravity on each RigidBody by default, to disable gravity on a rigid body set: `bool gravityEnabled = 0` on the RigidBody prim

### Collision
I can't find official docs...

In order to have a collision the following must be true:
1. You must have a RealityKitComponent "Collider" with type "RealityKit.Collider"
2. shape can be Box, Sphere, or Capsule
#### Example prim
```
def RealityKitComponent "Collider"
{
    uint group = 1
    uniform token info:id = "RealityKit.Collider"
    uint mask = 4294967295
    token type = "Default"

    def RealityKitStruct "Shape"
    {
        float3 extent = (0.2, 0.2, 0.2)
        token shapeType = "Box"

        def RealityKitStruct "pose"
        {
        }
    }
}
```

#### Materials
[Apple Docs - Preliminary_PhysicsMaterialAPI](https://developer.apple.com/documentation/arkit/usdz_schemas_for_ar/simulated_physical_interaction/preliminary_physicsmaterialapi)

In order to have a physics material the following must be true:
1. As a child Xfrom from the prim with `Preliminary_PhysicsColliderAPI` & `Preliminary_PhysicsRigidBodyAPI` applied, create a Material prim with the `Preliminary_PhysicsMaterialAPI` applied
2. Within that prim there must exists a primvar `uniform double preliminary:physics:material:friction:dynamic = 0.62`
3. Within that prim there must exists a primvar `uniform double preliminary:physics:material:friction:static = 0.62`
4. Within that prim there must exists a primvar `uniform double preliminary:physics:material:restitution = 0.62` (This is bounciness)

### RigidBody

[Apple Docs - Preliminary_PhysicsMaterialAPI](https://developer.apple.com/documentation/arkit/usdz_schemas_for_ar/simulated_physical_interaction/preliminary_physicsmaterialapi)

In order to have a collision the following must be true:
1. `Preliminary_PhysicsRigidBodyAPI` schema must be applied
2. Within that prim there must exists a primvar `uniform double preliminary:physics:rigidBody:mass = 1.1`


## Approaches

It appears that starting with the iOS Structure and adding in the RealityKitComponents underneath the Prim that applies the `Preliminary_PhysicsColliderAPI` & `Preliminary_PhysicsRigidBodyAPI` schemas causes both OS's to simulate some physics

### Issues
1. Bouncing with mixedBounce.usdz on visionOS is significantly stronger than on iOS
2. mixedBounce.usdz does not let me close it out on visionOS, I have to force quit QuickLook
3. mixedBounce.usdz seems to retain physics within it's scene, rotating the scene always makes the ball bounce towards the cube, not towards the ground (with respect to the visionOS user)
