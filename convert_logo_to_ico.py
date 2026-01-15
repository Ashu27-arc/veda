"""
VEDA AI - Logo ko ICO format mein convert karne ka script
"""

from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path, sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]):
    """
    PNG image ko ICO format mein convert karta hai
    Multiple sizes ke saath (Windows ke liye best)
    """
    try:
        # PNG image load karo
        img = Image.open(png_path)
        
        # Transparent background ke liye RGBA mode
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Multiple sizes ke icons banao
        icon_sizes = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icon_sizes.append(resized)
        
        # ICO file save karo
        icon_sizes[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in icon_sizes],
            append_images=icon_sizes[1:]
        )
        
        print(f"✅ Success! ICO file created: {ico_path}")
        print(f"📏 Sizes included: {sizes}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Input aur output paths
    png_file = "python_frontend/assets/veda-logo.png"
    ico_file = "veda-icon.ico"
    
    print("🎨 Converting VEDA logo to ICO format...")
    print(f"📂 Input: {png_file}")
    print(f"📂 Output: {ico_file}")
    print()
    
    # Check if PNG exists
    if not os.path.exists(png_file):
        print(f"❌ Error: {png_file} not found!")
        exit(1)
    
    # Convert
    success = convert_png_to_ico(png_file, ico_file)
    
    if success:
        print()
        print("🎉 Conversion complete!")
        print(f"📦 Ab aap EXE banate waqt use kar sakte ho:")
        print(f"   pyinstaller --icon={ico_file} run_veda_ai.py")
    else:
        print()
        print("❌ Conversion failed. Please check the error above.")
