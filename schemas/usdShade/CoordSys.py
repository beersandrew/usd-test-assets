"""
Generates coordSys.usda — demonstrates UsdShadeCoordSysAPI (multiple-apply).

Coordinate systems allow shaders to evaluate textures and procedurals in a named
local space rather than UV or world space. Each named binding points to an Xform
prim whose local frame defines the space.

Run:
    python CoordSys.py
"""

from pxr import Usd, UsdShade, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("coordSys.usda")

# Set stage metadata
root_layer = stage.GetRootLayer()
root_layer.defaultPrim = "World"
stage.SetMetadata("metersPerUnit", 0.01)
stage.SetMetadata("timeCodesPerSecond", 24)
stage.SetMetadata("upAxis", "Y")

world = UsdGeom.Xform.Define(stage, "/World")

# ── Ground plane mesh — receives the coordinate system bindings ───────────────
ground = UsdGeom.Mesh.Define(stage, "/World/GroundPlane")
ground.GetFaceVertexCountsAttr().Set([4])
ground.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])
ground.GetPointsAttr().Set([
    Gf.Vec3f(-5, 0, -5), Gf.Vec3f(5, 0, -5),
    Gf.Vec3f(5, 0,  5), Gf.Vec3f(-5, 0,  5),
])
ground.GetExtentAttr().Set([Gf.Vec3f(-5, 0, -5), Gf.Vec3f(5, 0, 5)])

normals_attr = ground.GetPrim().CreateAttribute(
    "normals", Sdf.ValueTypeNames.Normal3fArray
)
normals_attr.Set([Gf.Vec3f(0, 1, 0)] * 4)
normals_attr.SetMetadata("interpolation", "faceVarying")

# Apply CoordSysAPI (multiple-apply) for two named coordinate systems.
# UsdShadeCoordSysAPI is a multiple-apply schema; each instance binds one coord sys.
projection_api = UsdShade.CoordSysAPI.Apply(ground.GetPrim(), "projection")
triplanar_api  = UsdShade.CoordSysAPI.Apply(ground.GetPrim(), "triplanar")

# ── Coordinate system transforms ──────────────────────────────────────────────
coord_scope = UsdGeom.Scope.Define(stage, "/World/CoordSystems")

# ProjectionXform: overhead planar projection facing downward.
proj_xform = UsdGeom.Xform.Define(stage, "/World/CoordSystems/ProjectionXform")
proj_xform.AddXformOp(UsdGeom.XformOp.TypeTranslate).Set(Gf.Vec3d(0, 5, 0))
proj_xform.AddXformOp(UsdGeom.XformOp.TypeRotateXYZ).Set(Gf.Vec3f(90, 0, 0))

# TriplanarXform: world-aligned frame, scaled to map world coords to UV range.
tri_xform = UsdGeom.Xform.Define(stage, "/World/CoordSystems/TriplanarXform")
tri_xform.AddXformOp(UsdGeom.XformOp.TypeScale).Set(Gf.Vec3f(0.1, 0.1, 0.1))

# Bind the named coord systems to the Xform prims.
# coordSys:<name>:binding is the relationship authored by CoordSysAPI.
proj_binding_rel = ground.GetPrim().CreateRelationship("coordSys:projection:binding")
proj_binding_rel.SetTargets([Sdf.Path("/World/CoordSystems/ProjectionXform")])

tri_binding_rel = ground.GetPrim().CreateRelationship("coordSys:triplanar:binding")
tri_binding_rel.SetTargets([Sdf.Path("/World/CoordSystems/TriplanarXform")])

# ── Material that consumes the named coordinate systems ───────────────────────
mat_scope = UsdGeom.Scope.Define(stage, "/World/Materials")

decal_mat = UsdShade.Material.Define(stage, "/World/Materials/PlanarDecalMaterial")

surface_shader = UsdShade.Shader.Define(
    stage, "/World/Materials/PlanarDecalMaterial/Surface"
)
UsdShade.NodeDefAPI.Apply(surface_shader.GetPrim())
surface_shader.SetShaderId("UsdPreviewSurface")
surface_shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.6)
surface_shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
surface_out = surface_shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)

decal_tex = UsdShade.Shader.Define(
    stage, "/World/Materials/PlanarDecalMaterial/DecalTexture"
)
UsdShade.NodeDefAPI.Apply(decal_tex.GetPrim())
decal_tex.SetShaderId("UsdUVTexture")
decal_tex.CreateInput("file", Sdf.ValueTypeNames.Asset).Set("./textures/decal.png")
decal_tex.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("clamp")
decal_tex.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("clamp")
decal_tex.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("sRGB")
decal_rgb_out = decal_tex.CreateOutput("rgb", Sdf.ValueTypeNames.Color3f)

# Connect diffuseColor from the decal texture.
surface_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
    decal_rgb_out
)

# Wire material surface output.
decal_mat.CreateSurfaceOutput().ConnectToSource(surface_out)

stage.GetRootLayer().Save()
print("Wrote coordSys.usda")
