import zipfile
import os

# Create directories for the test
os.makedirs("usdz_test", exist_ok=True)

# Create a simple USD file
usd_content = """#usda 1.0
(
    defaultPrim = "Scene"
    metersPerUnit = 0.01
    upAxis = "Y"
)

def Scope "Scene" 
{
    
    def Cube "MyCube" 
    {
    }
}
"""
with open("usdz_test/test.usda", "w") as f:
    f.write(usd_content)
    
# Create a valid USDZ file
with zipfile.ZipFile("valid.usdz", "w") as z:
    z.write("usdz_test/test.usda", arcname="test.usda")


print("Created 'misaligned.usdz' with a misaligned asset (texture.jpg).")