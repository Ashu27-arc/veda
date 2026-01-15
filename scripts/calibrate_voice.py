"""
Quick Voice Calibration Script
Run this to calibrate your microphone for better accuracy
"""

from python_backend.voice_advanced import calibrate_microphone, test_voice_recognition

print("=" * 70)
print("VEDA AI - VOICE CALIBRATION")
print("=" * 70)

print("\n🎯 This will calibrate your microphone for better voice recognition.")
print("   It takes only 3 seconds!")

input("\nPress Enter to start calibration...")

# Run calibration
success = calibrate_microphone(duration=3)

if success:
    print("\n" + "=" * 70)
    print("✅ CALIBRATION SUCCESSFUL!")
    print("=" * 70)
    
    print("\n💡 Your voice recognition is now optimized!")
    print("   VEDA AI will understand your voice much better.")
    
    test_choice = input("\n🎤 Would you like to test voice recognition now? (yes/no): ")
    
    if test_choice.lower() in ['yes', 'y', 'haan', 'ha']:
        print("\n" + "=" * 70)
        test_voice_recognition()
        print("=" * 70)
    
    print("\n🚀 You're all set! Run VEDA AI:")
    print("   python run_veda_ai.py")
    
else:
    print("\n" + "=" * 70)
    print("❌ CALIBRATION FAILED")
    print("=" * 70)
    
    print("\n💡 Troubleshooting:")
    print("   1. Check if microphone is connected")
    print("   2. Check microphone permissions")
    print("   3. Try running as administrator")
    print("   4. Check microphone in Windows Settings")

print("\n" + "=" * 70)
