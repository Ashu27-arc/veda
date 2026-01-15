from rembg import remove
from PIL import Image
import os

# Input and output paths
input_path = "python_frontend/assets/veda-logo-bg.png"
output_path = "python_frontend/assets/veda-logo.png"

# Check if input file exists
if not os.path.exists(input_path):
    print(f"Error: {input_path} not found!")
    exit(1)

# Open image
print("Loading image...")
input_image = Image.open(input_path)

# Remove background
print("Removing background...")
output_image = remove(input_image)

# Save the result
print("Saving image...")
output_image.save(output_path)

print(f"✓ Background removed successfully!")
print(f"✓ Saved to: {output_path}")
