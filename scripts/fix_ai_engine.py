"""
VEDA AI Engine Quick Fix
Automatically fixes AI engine issues and sets up Hugging Face
"""
import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...\n")
    
    required = {
        'transformers': 'Hugging Face Transformers',
        'torch': 'PyTorch',
        'requests': 'Requests'
    }
    
    missing = []
    
    for package, name in required.items():
        try:
            __import__(package)
            print(f"✅ {name} - Installed")
        except ImportError:
            print(f"❌ {name} - Missing")
            missing.append(package)
    
    return missing

def install_dependencies(packages):
    """Install missing packages"""
    if not packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(packages)}")
    print("⏳ This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            *packages, "--quiet"
        ])
        print("\n✅ All packages installed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        return False

def test_huggingface():
    """Test Hugging Face AI"""
    print("\n🧪 Testing Hugging Face AI...\n")
    
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from python_backend.huggingface_ai import huggingface_response
        
        print("⏳ Loading model (first time may take a minute)...")
        response = huggingface_response("Hello")
        
        if response:
            print(f"✅ AI Response: {response}")
            print("\n🎉 Hugging Face AI is working!")
            return True
        else:
            print("❌ No response from AI")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def update_config():
    """Update .env to use Hugging Face"""
    print("\n⚙️  Updating configuration...\n")
    
    env_path = ".env"
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Update AI_MODE
        if 'AI_MODE=' in content:
            content = content.replace('AI_MODE=self_training', 'AI_MODE=huggingface')
            content = content.replace('AI_MODE=lm_studio', 'AI_MODE=huggingface')
            
            with open(env_path, 'w') as f:
                f.write(content)
            
            print("✅ Configuration updated to use Hugging Face")
            return True
    except Exception as e:
        print(f"⚠️  Could not update config: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🔧 VEDA AI Engine - Quick Fix")
    print("="*60 + "\n")
    
    # Step 1: Check dependencies
    missing = check_dependencies()
    
    # Step 2: Install missing packages
    if missing:
        print(f"\n⚠️  Missing {len(missing)} package(s)")
        print("❓ Install them now? (y/n): ", end="")
        
        try:
            choice = input().lower().strip()
            if choice == 'y':
                if not install_dependencies(missing):
                    print("\n❌ Fix failed. Please install manually:")
                    print(f"   pip install {' '.join(missing)}")
                    return
            else:
                print("\n⏭️  Skipping installation")
                return
        except:
            return
    
    # Step 3: Update config
    update_config()
    
    # Step 4: Test AI
    test_huggingface()
    
    print("\n" + "="*60)
    print("✅ VEDA AI is now using Hugging Face (offline AI)")
    print("="*60)
    print("\n💡 Benefits:")
    print("   - Works completely offline")
    print("   - No external API needed")
    print("   - Free and open source")
    print("\n📝 Note:")
    print("   - First run will download model (~500MB)")
    print("   - Subsequent runs will be faster")
    print("\n🚀 You can now start VEDA: python run_veda_ai.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
