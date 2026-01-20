import speech_recognition as sr
import pyttsx3
from python_backend.logger import log_info, log_error, log_warning

recognizer = sr.Recognizer()

# Initialize engine safely
engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)
except Exception as e:
    log_warning(f"Speech engine init failed (will retry on speak): {e}")

# Voice threshold constants - SAME AS voice_advanced.py for consistency
MIN_ENERGY_THRESHOLD = 150
MAX_ENERGY_THRESHOLD = 4000
DEFAULT_ENERGY_THRESHOLD = 300

# Try to set Hindi voice if available
def set_hindi_voice():
    """Set Hindi voice for TTS if available"""
    global engine
    if not engine:
        return False
    try:
        voices = engine.getProperty('voices')
        for voice in voices:
            # Look for Hindi voice (hi-IN or Hindi)
            if 'hindi' in voice.name.lower() or 'hi-in' in voice.id.lower() or 'hi_IN' in voice.id:
                engine.setProperty('voice', voice.id)
                log_info(f"Hindi voice set: {voice.name}")
                return True
        log_warning("Hindi voice not found, using default")
        return False
    except Exception as e:
        log_error(f"Error setting Hindi voice: {e}")
        return False

if engine:
    set_hindi_voice()

# Configure recognizer for better accuracy - PERMANENT FIX
# Using fixed threshold instead of dynamic for stability
recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
recognizer.dynamic_energy_threshold = False  # DISABLED for stability - prevents threshold drift
recognizer.pause_threshold = 0.8  # Shorter for quicker response
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

def test_microphone():
    """Test if microphone is accessible"""
    try:
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        
        if not mic_list:
            log_error("No microphones detected")
            print("❌ No microphones found!")
            print("💡 Please connect a microphone and try again")
            return False
        
        print(f"✅ Found {len(mic_list)} microphone(s)")
        log_info(f"Found {len(mic_list)} microphone(s)")
        
        # Test default microphone
        with sr.Microphone() as source:
            log_info("Microphone test successful")
            print("✅ Microphone is working")
            return True
            
    except OSError as e:
        log_error(f"Microphone access error: {e}")
        print(f"❌ Microphone error: {e}")
        print("💡 Check Windows Settings > Privacy > Microphone")
        return False
    except Exception as e:
        log_error(f"Microphone test failed: {e}")
        print(f"❌ Test failed: {e}")
        return False

def listen_command():
    """Listen for voice command from microphone - PERMANENT FIX"""
    try:
        print("🎤 Initializing microphone...")
        log_info("Initializing microphone...")
        
        # Ensure threshold is valid
        if recognizer.energy_threshold < MIN_ENERGY_THRESHOLD:
            recognizer.energy_threshold = DEFAULT_ENERGY_THRESHOLD
            log_warning(f"Threshold was too low, reset to {DEFAULT_ENERGY_THRESHOLD}")
        
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise... (please wait 1 second)")
            log_info("Adjusting for ambient noise...")
            
            old_threshold = recognizer.energy_threshold
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # CRITICAL: Ensure threshold doesn't go too low after adjustment
            if recognizer.energy_threshold < MIN_ENERGY_THRESHOLD:
                recognizer.energy_threshold = max(old_threshold, MIN_ENERGY_THRESHOLD)
                log_warning(f"Threshold adjusted too low, restored to {recognizer.energy_threshold}")
            
            print(f"🎤 Listening... Bol sakte ho! (Hindi/English dono chalega)")
            print(f"   Energy threshold: {recognizer.energy_threshold:.0f}")
            log_info(f"Listening for command... (threshold: {recognizer.energy_threshold})")
            
            # Listen with reasonable timeout
            audio = recognizer.listen(source, timeout=12, phrase_time_limit=15)
            
            print("🔄 Processing speech...")
            log_info(f"Processing audio... ({len(audio.get_raw_data())} bytes)")

        # Try to recognize speech with multiple languages
        print("🌐 Connecting to Google Speech API...")
        
        # Language priority: Hindi -> English India -> US English
        languages = [
            ('hi-IN', 'Hindi'),
            ('en-IN', 'English'),
            ('en-US', 'US English')
        ]
        
        for lang_code, lang_name in languages:
            try:
                command = recognizer.recognize_google(audio, language=lang_code)
                if command and command.strip():
                    print(f"✅ You said ({lang_name}): '{command}'")
                    log_info(f"Recognized ({lang_code}): {command}")
                    return command.strip()
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                log_error(f"Google API error: {e}")
                break
        
        # If we reach here, no language worked
        print("❓ Samajh nahi aaya. Thoda clear bolo.")
        log_warning("Could not understand audio in any language")
        return ""
        
    except sr.WaitTimeoutError:
        error_msg = "Koi awaaz nahi aayi. Dobara try karo aur zor se bolo!"
        print(f"⏱️ {error_msg}")
        log_warning("Listening timeout - no speech detected")
        return ""
        
    except sr.UnknownValueError:
        error_msg = "Samajh nahi aaya. Thoda clear bolo."
        print(f"❓ {error_msg}")
        log_warning("Could not understand audio")
        return ""
        
    except sr.RequestError as e:
        error_msg = f"Speech recognition service error: {e}"
        print(f"🌐 {error_msg}")
        log_error(f"Google Speech API error: {e}")
        return ""
        
    except OSError as e:
        error_msg = f"Microphone error: {e}"
        print(f"🎤 {error_msg}")
        log_error(f"Microphone access error: {e}")
        print("💡 Check Windows Settings > Privacy > Microphone")
        return ""
        
    except Exception as e:
        error_msg = f"Voice recognition error: {e}"
        print(f"❌ {error_msg}")
        log_error(f"Voice recognition error: {e}")
        return ""

def speak(text):
    """Convert text to speech with personality"""
    try:
        # Show who is speaking
        print(f"🔊 VEDA: {text}")
        log_info(f"Speaking: {text}")
        
        # Create fresh engine instance to avoid "run loop already started" error
        import pyttsx3
        local_engine = pyttsx3.init()
        local_engine.setProperty("rate", 175)
        local_engine.setProperty("volume", 1.0)
        
        # Try to set Hindi voice
        try:
            voices = local_engine.getProperty('voices')
            for voice in voices:
                if 'hindi' in voice.name.lower() or 'hi-in' in voice.id.lower() or 'hi_IN' in voice.id:
                    local_engine.setProperty('voice', voice.id)
                    break
        except:
            pass
        
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
        print(f"❌ Speech synthesis error: {e}")

def test_microphone():
    """Test if microphone is accessible"""
    try:
        with sr.Microphone() as source:
            log_info("Microphone test successful")
            return True
    except Exception as e:
        log_error(f"Microphone test failed: {e}")
        return False
