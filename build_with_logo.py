"""
VEDA AI - Complete Build Script with Logo
Cross-platform (Windows/Linux/Mac)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show progress"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e}")
        return False

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    required = ['PIL', 'PyInstaller']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package} installed")
        except ImportError:
            print(f"  ❌ {package} not found")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        run_command("pip install pillow pyinstaller", "Installing dependencies")
    
    return True

def convert_logo():
    """Convert PNG logo to ICO"""
    print("\n🎨 Converting VEDA logo to ICO format...")
    
    if not os.path.exists("convert_logo_to_ico.py"):
        print("❌ convert_logo_to_ico.py not found!")
        return False
    
    return run_command("python convert_logo_to_ico.py", "Logo Conversion")

def build_exe():
    """Build EXE with PyInstaller"""
    print("\n🔨 Building EXE with VEDA logo...")
    
    # Check if icon exists
    if not os.path.exists("veda-icon.ico"):
        print("❌ veda-icon.ico not found! Run logo conversion first.")
        return False
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=veda-icon.ico",
        "--name=VEDA_AI",
        "--add-data", "python_frontend;python_frontend",
        "--add-data", "data;data",
        "--add-data", "python_backend;python_backend",
        "--hidden-import=pyttsx3",
        "--hidden-import=speech_recognition",
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "run_veda_ai.py"
    ]
    
    # Join command for display
    cmd_str = " ".join(cmd)
    print(f"Command: {cmd_str}\n")
    
    return run_command(cmd_str, "Building EXE")

def cleanup():
    """Clean up build artifacts"""
    print("\n🧹 Cleaning up...")
    
    # Remove build folder
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("  ✅ Removed build folder")
    
    # Remove spec file
    if os.path.exists("VEDA_AI.spec"):
        os.remove("VEDA_AI.spec")
        print("  ✅ Removed spec file")
    
    return True

def show_results():
    """Show build results"""
    print("\n" + "="*60)
    print("  🎉 BUILD COMPLETE!")
    print("="*60)
    
    exe_path = Path("dist/VEDA_AI.exe")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n📦 Your EXE file with VEDA logo:")
        print(f"   Location: {exe_path}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"\n🚀 Test karne ke liye:")
        print(f"   cd dist")
        print(f"   VEDA_AI.exe")
        print(f"\n💡 Distribution:")
        print(f"   - GitHub Releases pe upload karo")
        print(f"   - Google Drive/Dropbox pe share karo")
        print(f"   - Installer banao (Inno Setup)")
    else:
        print("\n❌ EXE file not found in dist folder!")
        print("Build may have failed. Check errors above.")

def main():
    """Main build process"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║           VEDA AI - EXE Builder with Logo             ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed!")
        sys.exit(1)
    
    # Step 2: Convert logo
    if not convert_logo():
        print("\n❌ Logo conversion failed!")
        sys.exit(1)
    
    # Step 3: Build EXE
    if not build_exe():
        print("\n❌ Build failed!")
        sys.exit(1)
    
    # Step 4: Cleanup
    cleanup()
    
    # Step 5: Show results
    show_results()
    
    print("\n✨ All done! Happy distributing! ✨\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
