"""
VEDA AI Setup Script
Run this to verify your installation
"""
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    required = [
        'fastapi', 'uvicorn', 'openai', 'speech_recognition',
        'pyttsx3', 'pyaudio', 'pyautogui', 'dotenv', 'pycaw',
        'comtypes', 'pvporcupine', 'mediapipe', 'cv2', 'PIL',
        'pystray', 'psutil', 'websockets'
    ]
    
    missing = []
    for module in required:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - MISSING")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️ Install missing packages: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file is configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("⚠️ Please configure OPENAI_API_KEY in .env")
            return False
    
    print("✅ .env configured")
    return True

def main():
    print("=" * 50)
    print("VEDA AI Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment", check_env_file)
    ]
    
    results = []
    for name, check in checks:
        print(f"\n{name}:")
        results.append(check())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! Run: python run_veda_ai.py")
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
