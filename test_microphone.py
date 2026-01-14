"""
VEDA AI - Microphone Test & Diagnostic Tool
Run this to test your microphone setup
"""

import speech_recognition as sr
import sys

def test_microphone_detailed():
    """Comprehensive microphone test"""
    print("\n" + "=" * 70)
    print("VEDA AI - MICROPHONE DIAGNOSTIC TEST")
    print("=" * 70)
    
    # Test 1: List microphones
    print("\n[TEST 1] Detecting Microphones...")
    print("-" * 70)
    try:
        mic_list = sr.Microphone.list_microphone_names()
        
        if not mic_list:
            print("❌ FAILED: No microphones detected!")
            print("\n💡 Solutions:")
            print("   • Connect a microphone to your computer")
            print("   • Check if microphone is properly plugged in")
            print("   • Try a different USB port")
            return False
        
        print(f"✅ PASSED: Found {len(mic_list)} microphone(s)")
        for i, mic_name in enumerate(mic_list):
            print(f"   [{i}] {mic_name}")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 2: Microphone access
    print("\n[TEST 2] Testing Microphone Access...")
    print("-" * 70)
    try:
        with sr.Microphone() as source:
            print("✅ PASSED: Microphone is accessible")
    except OSError as e:
        print(f"❌ FAILED: Cannot access microphone")
        print(f"   Error: {e}")
        print("\n💡 Solutions:")
        print("   • Go to Windows Settings > Privacy > Microphone")
        print("   • Enable 'Allow apps to access your microphone'")
        print("   • Enable 'Allow desktop apps to access your microphone'")
        print("   • Close other apps using microphone (Zoom, Teams, Discord)")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 3: Ambient noise adjustment
    print("\n[TEST 3] Testing Ambient Noise Adjustment...")
    print("-" * 70)
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("   Adjusting for ambient noise... (please wait)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"✅ PASSED: Energy threshold set to {recognizer.energy_threshold}")
            
            if recognizer.energy_threshold < 100:
                print("   ⚠️  WARNING: Very low threshold - room might be too quiet")
            elif recognizer.energy_threshold > 8000:
                print("   ⚠️  WARNING: Very high threshold - room might be too noisy")
            else:
                print("   ✅ Threshold is in good range")
                
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 4: Audio capture
    print("\n[TEST 4] Testing Audio Capture...")
    print("-" * 70)
    print("   Please say something when prompted...")
    print("   (You have 5 seconds)")
    
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\n   🎤 SPEAK NOW! Say anything...")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("✅ PASSED: Audio captured successfully")
            except sr.WaitTimeoutError:
                print("❌ FAILED: No audio detected within timeout")
                print("\n💡 Solutions:")
                print("   • Speak louder")
                print("   • Move microphone closer")
                print("   • Check microphone volume in Windows Settings")
                print("   • Test microphone in Windows Sound Settings")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    # Test 5: Speech recognition
    print("\n[TEST 5] Testing Speech Recognition...")
    print("-" * 70)
    print("   Please say a simple phrase when prompted...")
    print("   (Example: 'Hello VEDA' or 'Test one two three')")
    
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\n   🎤 SPEAK NOW! Say a simple phrase...")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("   🔄 Processing speech...")
                
                # Try to recognize
                text = recognizer.recognize_google(audio, language='en-IN')
                print(f"✅ PASSED: Recognized: '{text}'")
                
            except sr.WaitTimeoutError:
                print("❌ FAILED: No speech detected")
                return False
            except sr.UnknownValueError:
                print("⚠️  WARNING: Audio captured but could not understand speech")
                print("   This might be okay - try speaking more clearly")
                return True  # Still consider it a pass
            except sr.RequestError as e:
                print(f"❌ FAILED: Speech recognition service error")
                print(f"   Error: {e}")
                print("\n💡 Solutions:")
                print("   • Check your internet connection")
                print("   • Try again in a few moments")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    success = test_microphone_detailed()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("\nYour microphone is working correctly.")
        print("You can now use VEDA AI voice commands.")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before using voice commands.")
        print("\nQuick Checklist:")
        print("  ☐ Microphone is connected")
        print("  ☐ Microphone permissions enabled in Windows Settings")
        print("  ☐ No other app is using the microphone")
        print("  ☐ Internet connection is active")
        print("  ☐ Microphone volume is not muted")
    
    print("=" * 70)
    
    input("\nPress Enter to exit...")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
