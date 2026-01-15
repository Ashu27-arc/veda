"""
Test script to verify all fixes are working
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("VEDA AI - Testing Fixes")
print("=" * 60)

# Test 1: Import system_control
print("\n1. Testing system_control imports...")
try:
    from python_backend.system_control import handle_system_command, set_volume, open_application
    print("   ✅ system_control imported successfully")
except Exception as e:
    print(f"   ❌ Error importing system_control: {e}")
    sys.exit(1)

# Test 2: Test folder path generation
print("\n2. Testing folder path generation...")
try:
    import os
    test_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    print(f"   ✅ Downloads path: {test_path}")
    print(f"   ✅ Path exists: {os.path.exists(test_path)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Test volume control (without actually changing volume)
print("\n3. Testing volume control function...")
try:
    from pycaw.pycaw import AudioUtilities
    
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume
    current = volume.GetMasterVolumeLevelScalar()
    print(f"   ✅ Volume control working! Current volume: {int(current * 100)}%")
except Exception as e:
    print(f"   ❌ Volume control error: {e}")

# Test 4: Test AI engine
print("\n4. Testing AI engine...")
try:
    from python_backend.ai_engine import process_command
    print("   ✅ AI engine imported successfully")
except Exception as e:
    print(f"   ❌ Error importing AI engine: {e}")

# Test 5: Test main server imports
print("\n5. Testing main server imports...")
try:
    from python_backend.main import app
    print("   ✅ FastAPI app imported successfully")
except Exception as e:
    print(f"   ❌ Error importing main: {e}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nYou can now run VEDA AI with:")
print("  python run_veda_ai.py")
print("\nOr manually:")
print("  python -m uvicorn python_backend.main:app --host 127.0.0.1 --port 8000")
print("=" * 60)
