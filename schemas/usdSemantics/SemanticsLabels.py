"""
SemanticsLabels.py

Generates semanticsLabels.usda demonstrating UsdSemanticsLabelsAPI (multiple-apply)
with multiple taxonomy instances applied to different prims.

Usage:
    python SemanticsLabels.py
"""

from pxr import Usd, UsdGeom, Sdf


def main():
    stage = Usd.Stage.CreateNew("semanticsLabels.usda")

    # Set stage-level metadata
    stage.SetMetadata("metersPerUnit", 0.01)
    stage.SetMetadata("timeCodesPerSecond", 24)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # ── World root prim ────────────────────────────────────────────────────────
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # ── SportsCar: category + style taxonomies ─────────────────────────────────
    sports_car = UsdGeom.Xform.Define(stage, "/World/SportsCar")
    sports_car_prim = sports_car.GetPrim()

    # Apply two taxonomy instances of SemanticsLabelsAPI (multiple-apply schema)
    sports_car_prim.ApplyAPI(Sdf.Token("SemanticsLabelsAPI"), Sdf.Token("category"))
    sports_car_prim.ApplyAPI(Sdf.Token("SemanticsLabelsAPI"), Sdf.Token("style"))

    # category taxonomy: what kind of object this is
    cat_attr = sports_car_prim.CreateAttribute(
        "semantics:category:labels", Sdf.ValueTypeNames.TokenArray, True  # uniform
    )
    cat_attr.SetVariability(Sdf.VariabilityUniform)
    cat_attr.Set(["vehicle", "car", "automobile"])

    # style taxonomy: visual/design style descriptors
    style_attr = sports_car_prim.CreateAttribute(
        "semantics:style:labels", Sdf.ValueTypeNames.TokenArray, True
    )
    style_attr.SetVariability(Sdf.VariabilityUniform)
    style_attr.Set(["sporty", "modern", "low-profile"])

    # Child prim with its own category labels
    body = UsdGeom.Mesh.Define(stage, "/World/SportsCar/Body")
    body_prim = body.GetPrim()
    body_prim.ApplyAPI(Sdf.Token("SemanticsLabelsAPI"), Sdf.Token("category"))

    body_cat_attr = body_prim.CreateAttribute(
        "semantics:category:labels", Sdf.ValueTypeNames.TokenArray, True
    )
    body_cat_attr.SetVariability(Sdf.VariabilityUniform)
    body_cat_attr.Set(["car-body", "exterior"])

    # ── OakTree: category + environment taxonomies ─────────────────────────────
    oak_tree = UsdGeom.Xform.Define(stage, "/World/OakTree")
    oak_tree_prim = oak_tree.GetPrim()

    oak_tree_prim.ApplyAPI(Sdf.Token("SemanticsLabelsAPI"), Sdf.Token("category"))
    oak_tree_prim.ApplyAPI(Sdf.Token("SemanticsLabelsAPI"), Sdf.Token("environment"))

    oak_cat_attr = oak_tree_prim.CreateAttribute(
        "semantics:category:labels", Sdf.ValueTypeNames.TokenArray, True
    )
    oak_cat_attr.SetVariability(Sdf.VariabilityUniform)
    oak_cat_attr.Set(["vegetation", "tree", "deciduous"])

    # environment taxonomy: contextual placement descriptors
    env_attr = oak_tree_prim.CreateAttribute(
        "semantics:environment:labels", Sdf.ValueTypeNames.TokenArray, True
    )
    env_attr.SetVariability(Sdf.VariabilityUniform)
    env_attr.Set(["outdoor", "natural", "forest"])

    # Save the stage
    stage.GetRootLayer().Save()
    print("Saved semanticsLabels.usda")


if __name__ == "__main__":
    main()
