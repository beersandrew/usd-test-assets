import zipfile
import os

# Create directories for the test
os.makedirs("usdz_test", exist_ok=True)

# Create a simple USD file
usd_content = """#usda 1.0
(
    doc = "Test file"
)
def "Test"
{
}
"""
with open("usdz_test/test.usda", "w") as f:
    f.write(usd_content)

# Create a simple JPG file as a placeholder
jpg_content = b"\xFF\xD8\xFF\xE0" + b"\x00" * 1024  # Simulated minimal JPEG header
with open("usdz_test/texture.jpg", "wb") as f:
    f.write(jpg_content)

# Create a USDZ file with an uncompressed USD file and a compressed JPG
compressed_usdz_path = "compressed.usdz"
with zipfile.ZipFile(compressed_usdz_path, "w") as z:
    # Write the USD file without compression
    z.write("usdz_test/test.usda", arcname="test.usda", compress_type=zipfile.ZIP_STORED)
    
    # Write the JPG file with compression
    z.write("usdz_test/texture.jpg", arcname="texture.jpg", compress_type=zipfile.ZIP_DEFLATED)

print(f"Created '{compressed_usdz_path}' with a compressed JPG.")

# Create a parent USDZ file containing the first compressed USDZ
parent_usdz_path = "parent.usdz"
with zipfile.ZipFile(parent_usdz_path, "w") as z:
    # Add the compressed USDZ as a regular file
    z.write(compressed_usdz_path, arcname="compressed.usdz")

print(f"Created '{parent_usdz_path}' containing the compressed USDZ as a child.")