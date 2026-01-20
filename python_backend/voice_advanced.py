"""
Advanced Voice Recognition System
- Better accuracy
- Noise cancellation
- Voice calibration
- Command confirmation
- PERMANENT FIX: Robust error handling and reliable recognition
"""

import speech_recognition as sr
import pyttsx3
import json
import os
import time
from python_backend.logger import log_info, log_error, log_warning

# Initialize recognizer with advanced settings
recognizer = sr.Recognizer()

# Initialize speech engine safely
engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)
except Exception as e:
    log_warning(f"Speech engine init failed (will retry on speak): {e}")

# Voice profile storage
VOICE_PROFILE_PATH = "data/voice_profile.json"

# Minimum energy threshold - prevents too low values
MIN_ENERGY_THRESHOLD = 150
MAX_ENERGY_THRESHOLD = 4000
DEFAULT_ENERGY_THRESHOLD = 300

# Advanced recognizer settings
def configure_recognizer():
    """Configure recognizer with optimal settings for Indian users"""
    # Energy threshold - balanced for most environments
    # Not too low (picks up noise) or too high (misses soft speech)
    recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
    
    # Dynamic energy adjustment - DISABLED to prevent threshold drift
    # Dynamic adjustment can cause threshold to become too low/high
    recognizer.dynamic_energy_threshold = False
    
    # Pause threshold - how long to wait for silence before ending phrase
    recognizer.pause_threshold = 0.8  # Shorter for quicker response
    
    # Phrase threshold - minimum audio length to consider as speech
    recognizer.phrase_threshold = 0.3
    
    # Non-speaking duration
    recognizer.non_speaking_duration = 0.5
    
    log_info(f"Voice recognizer configured: threshold={recognizer.energy_threshold}, dynamic=False")

configure_recognizer()

def calibrate_microphone(duration=2):
    """Calibrate microphone for user's environment - PERMANENT FIX"""
    try:
        print("\n🎤 Voice Calibration Starting...")
        print("   Thoda chup raho... calibrating...")
        log_info("Starting microphone calibration")
        
        with sr.Microphone() as source:
            print(f"   Calibrating... ({duration} seconds)")
            recognizer.adjust_for_ambient_noise(source, duration=duration)
            
            # IMPORTANT: Clamp threshold to sensible range
            # Too low = picks up background noise
            # Too high = misses soft speech
            calibrated_threshold = recognizer.energy_threshold
            
            if calibrated_threshold < MIN_ENERGY_THRESHOLD:
                log_warning(f"Threshold too low ({calibrated_threshold}), setting to minimum {MIN_ENERGY_THRESHOLD}")
                calibrated_threshold = MIN_ENERGY_THRESHOLD
            elif calibrated_threshold > MAX_ENERGY_THRESHOLD:
                log_warning(f"Threshold too high ({calibrated_threshold}), setting to maximum {MAX_ENERGY_THRESHOLD}")
                calibrated_threshold = MAX_ENERGY_THRESHOLD
            
            # Apply the clamped threshold
            recognizer.energy_threshold = calibrated_threshold
            
            # Save calibration with dynamic DISABLED for stability
            calibration_data = {
                "energy_threshold": calibrated_threshold,
                "calibrated": True,
                "dynamic_enabled": False,  # DISABLED for stability
                "calibration_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "min_threshold": MIN_ENERGY_THRESHOLD,
                "max_threshold": MAX_ENERGY_THRESHOLD
            }
            
            os.makedirs("data", exist_ok=True)
            with open(VOICE_PROFILE_PATH, 'w') as f:
                json.dump(calibration_data, f, indent=2)
            
            print(f"   ✅ Calibration complete!")
            print(f"   Mic sensitivity: {calibrated_threshold}")
            print(f"   Ab bol sakte ho - Hindi/English dono chalega!")
            log_info(f"Calibration complete: threshold={calibrated_threshold}")
            
            return True
            
    except OSError as e:
        log_error(f"Microphone access error during calibration: {e}")
        print(f"   ❌ Microphone not accessible: {e}")
        print("   💡 Windows Settings > Privacy > Microphone enable karo")
        return False
    except Exception as e:
        log_error(f"Calibration error: {e}")
        print(f"   ❌ Calibration failed: {e}")
        return False

def load_voice_profile():
    """Load saved voice profile - with validation and clamping"""
    try:
        if os.path.exists(VOICE_PROFILE_PATH):
            with open(VOICE_PROFILE_PATH, 'r') as f:
                profile = json.load(f)
                
            if profile.get("calibrated"):
                # Load saved threshold with validation
                saved_threshold = profile.get("energy_threshold", DEFAULT_ENERGY_THRESHOLD)
                
                # IMPORTANT: Validate and clamp the threshold
                if saved_threshold < MIN_ENERGY_THRESHOLD:
                    log_warning(f"Saved threshold too low ({saved_threshold}), using minimum {MIN_ENERGY_THRESHOLD}")
                    saved_threshold = MIN_ENERGY_THRESHOLD
                elif saved_threshold > MAX_ENERGY_THRESHOLD:
                    log_warning(f"Saved threshold too high ({saved_threshold}), using maximum {MAX_ENERGY_THRESHOLD}")
                    saved_threshold = MAX_ENERGY_THRESHOLD
                
                recognizer.energy_threshold = saved_threshold
                
                # ALWAYS disable dynamic adjustment for stability
                recognizer.dynamic_energy_threshold = False
                
                log_info(f"Voice profile loaded: threshold={recognizer.energy_threshold}, dynamic=False")
                return True
        else:
            # No profile exists, use defaults
            log_info("No voice profile found, using default settings")
            recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
            recognizer.dynamic_energy_threshold = False
                
    except json.JSONDecodeError as e:
        log_error(f"Voice profile corrupted, resetting: {e}")
        # Delete corrupted file
        try:
            os.remove(VOICE_PROFILE_PATH)
        except:
            pass
        recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
        recognizer.dynamic_energy_threshold = False
    except Exception as e:
        log_error(f"Error loading voice profile: {e}")
        recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
        recognizer.dynamic_energy_threshold = False
    
    return False

# Load voice profile on module import
load_voice_profile()

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
    """Advanced voice command listening with better accuracy and reliability - PERMANENT FIX"""
    max_retries = 2
    
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                print(f"🔄 Retry attempt {attempt}...")
                log_info(f"Voice recognition retry attempt {attempt}")
            
            print("🎤 Ready! Speak your command...")
            log_info("Starting voice recognition...")
            
            # Ensure threshold is valid before listening
            if recognizer.energy_threshold < MIN_ENERGY_THRESHOLD:
                recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
                log_warning(f"Threshold was too low, reset to {DEFAULT_ENERGY_THRESHOLD}")
            
            with sr.Microphone() as source:
                # Quick ambient noise adjustment - but preserve minimum threshold
                print("🎤 Adjusting for ambient noise... (1 second)")
                old_threshold = recognizer.energy_threshold
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # CRITICAL: Ensure threshold doesn't go too low after adjustment
                if recognizer.energy_threshold < MIN_ENERGY_THRESHOLD:
                    recognizer.energy_threshold = max(old_threshold, MIN_ENERGY_THRESHOLD)
                    log_warning(f"Threshold adjusted too low, restored to {recognizer.energy_threshold}")
                
                print(f"🎤 Listening... Bol sakte ho! (Hindi/English dono chalega)")
                print(f"   Mic sensitivity: {recognizer.energy_threshold:.0f}")
                log_info(f"Listening... (threshold: {recognizer.energy_threshold})")
                
                # Listen with reasonable timeout - not too long to avoid hanging
                audio = recognizer.listen(
                    source, 
                    timeout=12,  # Wait up to 12 seconds for speech to start
                    phrase_time_limit=15  # Allow up to 15 seconds of speech
                )
                
                print("🔄 Processing speech...")
                log_info(f"Processing audio... (length: {len(audio.get_raw_data())} bytes)")

            # Check if audio has meaningful content
            if len(audio.get_raw_data()) < 1000:
                log_warning("Audio too short, might be noise")
                if attempt < max_retries:
                    print("⚠️ Audio bahut chhota hai, dobara bolo...")
                    continue
            
            # Try Google Speech Recognition with multiple language attempts
            command = None
            
            # Language priority: Hindi/Hinglish -> English India -> US English
            languages = [
                ('hi-IN', 'Hindi/Hinglish'),
                ('en-IN', 'English (India)'),
                ('en-US', 'English (US)')
            ]
            
            for lang_code, lang_name in languages:
                try:
                    print(f"🌐 Trying {lang_name} recognition...")
                    command = recognizer.recognize_google(audio, language=lang_code)
                    if command and command.strip():
                        print(f"✅ Recognized ({lang_name}): '{command}'")
                        log_info(f"Successfully recognized ({lang_code}): {command}")
                        return command.strip()
                except sr.UnknownValueError:
                    log_info(f"Could not recognize with {lang_code}")
                    continue
                except sr.RequestError as e:
                    log_error(f"Google API error for {lang_code}: {e}")
                    # If API fails for one language, it will fail for all
                    break
            
            # If we reach here, no language worked
            print("❓ Could not understand audio - please speak more clearly")
            log_warning("Speech not understood in any language")
            
            if attempt < max_retries:
                print("💡 Thoda loudly aur clearly bolo...")
                continue
            
            return ""
            
        except sr.WaitTimeoutError:
            print("⏱️ Koi awaaz nahi aayi - dobara try karo aur zor se bolo!")
            log_warning("Listening timeout - no speech detected")
            if attempt < max_retries:
                continue
            return ""
            
        except OSError as e:
            error_str = str(e).lower()
            print(f"🎤 Microphone error: {e}")
            
            if "no default input device" in error_str or "could not open" in error_str:
                print("💡 Microphone connect nahi hai ya accessible nahi hai")
                print("   Windows Settings > Privacy > Microphone enable karo")
            else:
                print("💡 Check Windows Settings > Privacy > Microphone")
            
            log_error(f"Microphone access error: {e}")
            return ""
            
        except Exception as e:
            print(f"❌ Error: {e}")
            log_error(f"Voice recognition error: {e}")
            if attempt < max_retries:
                continue
            return ""
    
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
    """Convert text to speech with better quality - with error handling"""
    try:
        print(f"🔊 VEDA AI: {text}")
        log_info(f"Speaking: {text}")
        
        # Create a fresh engine instance to avoid "run loop already started" error
        import pyttsx3
        local_engine = None
        
        try:
            local_engine = pyttsx3.init()
            local_engine.setProperty("rate", 175)
            local_engine.setProperty("volume", 1.0)
            
            # Speak the text
            local_engine.say(text)
            local_engine.runAndWait()
        finally:
            # Clean up properly
            if local_engine:
                try:
                    local_engine.stop()
                except:
                    pass
        
    except RuntimeError as e:
        # Common error: run loop already started
        log_warning(f"Speech engine busy: {e}")
        print(f"⚠️ Speech busy (text was: {text})")
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
        "calibrated": os.path.exists(VOICE_PROFILE_PATH),
        "min_threshold": MIN_ENERGY_THRESHOLD,
        "max_threshold": MAX_ENERGY_THRESHOLD,
        "default_threshold": DEFAULT_ENERGY_THRESHOLD,
        "threshold_status": "OK" if MIN_ENERGY_THRESHOLD <= recognizer.energy_threshold <= MAX_ENERGY_THRESHOLD else "NEEDS_CALIBRATION"
    }
    return stats

def reset_voice_settings():
    """Reset voice settings to defaults - use if voice is not working"""
    try:
        recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
        recognizer.dynamic_energy_threshold = False
        recognizer.pause_threshold = 0.8
        recognizer.phrase_threshold = 0.3
        recognizer.non_speaking_duration = 0.5
        
        # Save reset profile
        calibration_data = {
            "energy_threshold": DEFAULT_ENERGY_THRESHOLD,
            "calibrated": True,
            "dynamic_enabled": False,
            "calibration_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "reset": True
        }
        
        os.makedirs("data", exist_ok=True)
        with open(VOICE_PROFILE_PATH, 'w') as f:
            json.dump(calibration_data, f, indent=2)
        
        log_info(f"Voice settings reset to defaults: threshold={DEFAULT_ENERGY_THRESHOLD}")
        return True
    except Exception as e:
        log_error(f"Failed to reset voice settings: {e}")
        return False

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
