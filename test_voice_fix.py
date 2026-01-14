"""
Test Voice Recognition Fix
Quick test to verify voice recognition is working properly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from python_backend.voice_advanced import (
    test_microphone_access,
    listen_command_advanced,
    calibrate_microphone,
    get_voice_stats
)

def test_voice_fix():
    """Test that voice recognition fix is working"""
    
    print("=" * 70)
    print("🎤 VEDA AI - Voice Recognition Fix Test")
    print("=" * 70)
    
    # Test 1: Microphone Access
    print("\n[Test 1/4] Testing microphone access...")
    if test_microphone_access():
        print("✅ Microphone is accessible")
    else:
        print("❌ Microphone not accessible")
        print("💡 Please check microphone connection and permissions")
        return False
    
    # Test 2: Voice Stats
    print("\n[Test 2/4] Checking voice recognition settings...")
    stats = get_voice_stats()
    print(f"✅ Energy threshold: {stats['energy_threshold']}")
    print(f"✅ Dynamic threshold: {stats['dynamic_threshold']}")
    print(f"✅ Pause threshold: {stats['pause_threshold']}")
    print(f"✅ Calibrated: {stats['calibrated']}")
    
    # Test 3: Calibration (Optional)
    print("\n[Test 3/4] Calibration check...")
    if not stats['calibrated']:
        print("⚠️  Not calibrated yet")
        choice = input("Would you like to calibrate now? (y/n): ").strip().lower()
        if choice in ['y', 'yes', 'haan', 'ha']:
            print("\nCalibrating... Please remain silent for 3 seconds...")
            if calibrate_microphone(duration=3):
                print("✅ Calibration successful!")
            else:
                print("❌ Calibration failed")
    else:
        print("✅ Already calibrated")
    
    # Test 4: Multiple Voice Commands
    print("\n[Test 4/4] Testing multiple voice commands...")
    print("This will test if you can give multiple commands without errors.")
    print("\nYou will be asked to speak 3 commands in a row.")
    
    input("\nPress ENTER to start voice test (or Ctrl+C to skip)...")
    
    success_count = 0
    for i in range(1, 4):
        print(f"\n--- Command {i}/3 ---")
        command = listen_command_advanced(timeout=10, phrase_limit=15)
        
        if command:
            print(f"✅ Command {i} recognized: '{command}'")
            success_count += 1
        else:
            print(f"❌ Command {i} failed")
        
        if i < 3:
            print("Ready for next command...")
            import time
            time.sleep(1)  # Small delay between commands
    
    # Results
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print(f"Commands recognized: {success_count}/3")
    
    if success_count == 3:
        print("✅ PERFECT! All commands recognized!")
        print("✅ Voice recognition is working properly!")
        return True
    elif success_count >= 2:
        print("⚠️  GOOD! Most commands recognized.")
        print("💡 Try speaking more clearly or calibrating again.")
        return True
    else:
        print("❌ NEEDS IMPROVEMENT")
        print("💡 Suggestions:")
        print("   1. Run calibration: python calibrate_voice.py")
        print("   2. Check microphone volume in Windows Settings")
        print("   3. Reduce background noise")
        print("   4. Speak louder and clearer")
        print("   5. Check internet connection")
        return False

if __name__ == "__main__":
    try:
        print("\n🚀 Starting Voice Recognition Test...\n")
        success = test_voice_fix()
        
        if success:
            print("\n" + "=" * 70)
            print("✅ VOICE RECOGNITION FIX VERIFIED!")
            print("=" * 70)
            print("\n🎯 You can now use VEDA AI with voice commands!")
            print("🚀 Start VEDA: python run_veda_ai.py")
        else:
            print("\n" + "=" * 70)
            print("⚠️  VOICE RECOGNITION NEEDS ATTENTION")
            print("=" * 70)
            print("\n📖 See VOICE_TROUBLESHOOTING.md for detailed help")
        
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Test error: {e}")
        print("Please check your setup and try again")
