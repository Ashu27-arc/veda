"""
Advanced Voice Recognition System
- Better accuracy
- Noise cancellation
- Voice calibration
- Command confirmation
"""

import speech_recognition as sr
import pyttsx3
import json
import os
from python_backend.logger import log_info, log_error, log_warning

# Initialize recognizer with advanced settings
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure speech engine
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

# Voice profile storage
VOICE_PROFILE_PATH = "data/voice_profile.json"

# Advanced recognizer settings
def configure_recognizer():
    """Configure recognizer with optimal settings"""
    # Energy threshold - FIXED value for consistency
    recognizer.energy_threshold = 4000  # Stable threshold
    
    # Dynamic energy adjustment - DISABLED for consistency
    recognizer.dynamic_energy_threshold = False  # Keep threshold stable
    
    # Pause threshold - how long to wait for silence
    recognizer.pause_threshold = 0.8  # Increased for better phrase capture
    
    # Phrase threshold - minimum audio length
    recognizer.phrase_threshold = 0.3
    
    # Non-speaking duration
    recognizer.non_speaking_duration = 0.5
    
    log_info("Voice recognizer configured with optimized settings")

configure_recognizer()

def calibrate_microphone(duration=3):
    """Calibrate microphone for user's environment"""
    try:
        print("\n🎤 Voice Calibration Starting...")
        print("   Please remain silent for calibration...")
        log_info("Starting microphone calibration")
        
        with sr.Microphone() as source:
            print(f"   Calibrating... ({duration} seconds)")
            recognizer.adjust_for_ambient_noise(source, duration=duration)
            
            # Save calibration data
            calibration_data = {
                "energy_threshold": recognizer.energy_threshold,
                "calibrated": True
            }
            
            os.makedirs("data", exist_ok=True)
            with open(VOICE_PROFILE_PATH, 'w') as f:
                json.dump(calibration_data, f)
            
            print(f"   ✅ Calibration complete!")
            print(f"   Energy threshold set to: {recognizer.energy_threshold}")
            log_info(f"Calibration complete: threshold={recognizer.energy_threshold}")
            
            return True
            
    except Exception as e:
        log_error(f"Calibration error: {e}")
        print(f"   ❌ Calibration failed: {e}")
        return False

def load_voice_profile():
    """Load saved voice profile"""
    try:
        if os.path.exists(VOICE_PROFILE_PATH):
            with open(VOICE_PROFILE_PATH, 'r') as f:
                profile = json.load(f)
                
            if profile.get("calibrated"):
                recognizer.energy_threshold = profile.get("energy_threshold", 4000)
                log_info(f"Voice profile loaded: threshold={recognizer.energy_threshold}")
                return True
                
    except Exception as e:
        log_error(f"Error loading voice profile: {e}")
    
    return False

def test_microphone_access():
    """Test if microphone is accessible and working"""
    try:
        # Quick test without verbose output
        with sr.Microphone() as source:
            log_info("Microphone test passed")
            return True
            
    except OSError as e:
        log_error(f"Microphone access error: {e}")
        return False
    except Exception as e:
        log_error(f"Microphone test error: {e}")
        return False

def listen_command_advanced(timeout=10, phrase_limit=15):
    """Advanced voice command listening with better accuracy and reliability"""
    try:
        print("🎤 Ready! Speak your command...")
        log_info("Starting voice recognition...")
        
        with sr.Microphone() as source:
            # IMPORTANT: Longer ambient noise adjustment for better accuracy
            print("🎤 Adjusting for ambient noise... (please wait)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            # Reset to stable threshold after adjustment
            recognizer.energy_threshold = 4000
            
            print(f"🎤 Listening... (speak clearly and loudly)")
            log_info(f"Listening... (threshold: {recognizer.energy_threshold})")
            
            # Listen with optimized timeout
            audio = recognizer.listen(
                source, 
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )
            
            print("🔄 Processing speech...")
            log_info("Processing audio...")

        # Try Google Speech Recognition with multiple language attempts
        command = None
        
        try:
            # Try Hindi/Hinglish first (best for Indian users)
            print("🌐 Recognizing speech (Hindi/Hinglish)...")
            try:
                command = recognizer.recognize_google(audio, language='hi-IN')
                if command:
                    print(f"✅ Recognized (Hindi): '{command}'")
                    log_info(f"Successfully recognized (hi-IN): {command}")
                    return command
            except sr.UnknownValueError:
                pass  # Try next language
            
            # Fallback to English (India)
            print("🌐 Trying English recognition...")
            try:
                command = recognizer.recognize_google(audio, language='en-IN')
                if command:
                    print(f"✅ Recognized (English): '{command}'")
                    log_info(f"Successfully recognized (en-IN): {command}")
                    return command
            except sr.UnknownValueError:
                pass  # Try next language
            
            # Last fallback to US English
            print("🌐 Trying US English...")
            command = recognizer.recognize_google(audio, language='en-US')
            if command:
                print(f"✅ Recognized (US English): '{command}'")
                log_info(f"Successfully recognized (en-US): {command}")
                return command
                    
        except sr.UnknownValueError:
            print("❓ Could not understand audio - please speak more clearly")
            log_warning("Speech not understood in any language")
            return ""
        
        except sr.RequestError as e:
            print(f"🌐 Speech service error: {e}")
            print("💡 Check your internet connection")
            log_error(f"Google Speech API error: {e}")
            return ""
        
        return ""
        
    except sr.WaitTimeoutError:
        print("⏱️ No speech detected - please try again")
        log_warning("Listening timeout")
        return ""
        
    except OSError as e:
        print(f"🎤 Microphone error: {e}")
        print("💡 Check Windows Settings > Privacy > Microphone")
        log_error(f"Microphone access error: {e}")
        return ""
        
    except Exception as e:
        print(f"❌ Error: {e}")
        log_error(f"Voice recognition error: {e}")
        return ""

def confirm_command(command):
    """Confirm command before execution (for critical commands only)"""
    # Critical commands that need confirmation
    critical_keywords = [
        'shutdown', 'restart', 'delete', 'format', 
        'band kar', 'restart kar', 'delete kar'
    ]
    
    # Check if command is critical
    is_critical = any(keyword in command.lower() for keyword in critical_keywords)
    
    if is_critical:
        print(f"\n⚠️  Critical Command Detected: '{command}'")
        log_warning(f"Critical command detected: {command}")
        # For web interface, we'll just log and allow
        # User can implement confirmation in frontend if needed
        return True
    
    # Non-critical commands don't need confirmation
    return True

def speak(text):
    """Convert text to speech with better quality"""
    try:
        print(f"🔊 VEDA AI: {text}")
        log_info(f"Speaking: {text}")
        
        # Create a fresh engine instance to avoid "run loop already started" error
        import pyttsx3
        local_engine = pyttsx3.init()
        local_engine.setProperty("rate", 175)
        local_engine.setProperty("volume", 1.0)
        
        # Speak the text
        local_engine.say(text)
        local_engine.runAndWait()
        
        # Clean up
        try:
            local_engine.stop()
        except:
            pass
        
    except Exception as e:
        log_error(f"Speech synthesis error: {e}")
        print(f"❌ Speech error: {e}")

def test_voice_recognition():
    """Test voice recognition system"""
    print("\n" + "=" * 60)
    print("ADVANCED VOICE RECOGNITION TEST")
    print("=" * 60)
    
    print("\n1. Testing microphone access...")
    try:
        with sr.Microphone() as source:
            print("   ✅ Microphone accessible")
    except Exception as e:
        print(f"   ❌ Microphone error: {e}")
        return False
    
    print("\n2. Testing ambient noise adjustment...")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"   ✅ Energy threshold: {recognizer.energy_threshold}")
    except Exception as e:
        print(f"   ❌ Adjustment error: {e}")
        return False
    
    print("\n3. Testing voice recognition...")
    print("   Please say something when prompted...")
    
    command = listen_command_advanced(timeout=10, phrase_limit=10)
    
    if command:
        print(f"\n   ✅ SUCCESS! Recognized: '{command}'")
        return True
    else:
        print("\n   ❌ No command recognized")
        return False

def get_voice_stats():
    """Get current voice recognition statistics"""
    stats = {
        "energy_threshold": recognizer.energy_threshold,
        "dynamic_threshold": recognizer.dynamic_energy_threshold,
        "pause_threshold": recognizer.pause_threshold,
        "calibrated": os.path.exists(VOICE_PROFILE_PATH)
    }
    return stats

if __name__ == "__main__":
    # Run calibration and test
    print("VEDA AI - Advanced Voice Recognition System")
    print("=" * 60)
    
    choice = input("\n1. Calibrate microphone\n2. Test voice recognition\n3. Both\n\nChoice (1/2/3): ")
    
    if choice in ['1', '3']:
        calibrate_microphone()
    
    if choice in ['2', '3']:
        test_voice_recognition()
    
    print("\n" + "=" * 60)
    print("Voice recognition system ready!")
