"""
VEDA AI - Microphone Fix & Calibration Tool
Run this to fix common microphone issues
"""

import speech_recognition as sr
import json
import os

def fix_microphone():
    """Fix common microphone issues"""
    print("\n" + "=" * 70)
    print("VEDA AI - MICROPHONE FIX & CALIBRATION")
    print("=" * 70)
    
    # Step 1: Check microphone
    print("\n[STEP 1] Checking microphone...")
    try:
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("❌ No microphones found!")
            print("\n💡 Please connect a microphone and run this script again.")
            input("\nPress Enter to exit...")
            return False
        
        print(f"✅ Found {len(mic_list)} microphone(s)")
        for i, mic_name in enumerate(mic_list):
            print(f"   [{i}] {mic_name}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 2: Test access
    print("\n[STEP 2] Testing microphone access...")
    try:
        with sr.Microphone() as source:
            print("✅ Microphone is accessible")
    except OSError as e:
        print(f"❌ Cannot access microphone: {e}")
        print("\n💡 Fix:")
        print("   1. Open Windows Settings")
        print("   2. Go to Privacy > Microphone")
        print("   3. Enable 'Allow apps to access your microphone'")
        print("   4. Enable 'Allow desktop apps to access your microphone'")
        input("\nPress Enter to exit...")
        return False
    
    # Step 3: Calibrate
    print("\n[STEP 3] Calibrating microphone...")
    print("   Please remain SILENT for 3 seconds...")
    
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("   Calibrating...")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            
            threshold = recognizer.energy_threshold
            print(f"✅ Calibration complete!")
            print(f"   Energy threshold: {threshold}")
            
            # Save calibration
            os.makedirs("data", exist_ok=True)
            calibration_data = {
                "energy_threshold": threshold,
                "calibrated": True
            }
            
            with open("data/voice_profile.json", 'w') as f:
                json.dump(calibration_data, f, indent=2)
            
            print("✅ Calibration saved to data/voice_profile.json")
            
    except Exception as e:
        print(f"❌ Calibration failed: {e}")
        return False
    
    # Step 4: Test recording
    print("\n[STEP 4] Testing audio recording...")
    print("   Say something when prompted (you have 5 seconds)...")
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\n   🎤 SPEAK NOW!")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("✅ Audio recorded successfully!")
            except sr.WaitTimeoutError:
                print("⚠️  No audio detected")
                print("   Try speaking louder or moving microphone closer")
                
    except Exception as e:
        print(f"❌ Recording test failed: {e}")
        return False
    
    # Step 5: Test recognition
    print("\n[STEP 5] Testing speech recognition...")
    print("   Say a simple phrase (Example: 'Hello VEDA')...")
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("\n   🎤 SPEAK NOW!")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("   🔄 Processing...")
                
                text = recognizer.recognize_google(audio, language='en-IN')
                print(f"✅ Recognized: '{text}'")
                print("\n🎉 SUCCESS! Your microphone is working perfectly!")
                
            except sr.WaitTimeoutError:
                print("⚠️  No speech detected")
            except sr.UnknownValueError:
                print("⚠️  Could not understand speech")
                print("   But audio was captured - try speaking more clearly")
            except sr.RequestError as e:
                print(f"❌ Internet connection error: {e}")
                print("   Please check your internet connection")
                return False
                
    except Exception as e:
        print(f"❌ Recognition test failed: {e}")
        return False
    
    return True

def main():
    """Main function"""
    success = fix_microphone()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ MICROPHONE FIXED & CALIBRATED!")
        print("\nYour microphone is now ready for VEDA AI.")
        print("You can start using voice commands.")
    else:
        print("❌ SOME ISSUES REMAIN")
        print("\nPlease check the error messages above.")
    
    print("=" * 70)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
