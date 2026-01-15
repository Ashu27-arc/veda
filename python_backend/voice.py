import speech_recognition as sr
import pyttsx3
from python_backend.logger import log_info, log_error, log_warning

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure speech engine
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

# Try to set Hindi voice if available
def set_hindi_voice():
    """Set Hindi voice for TTS if available"""
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

set_hindi_voice()

# Configure recognizer for better accuracy - OPTIMIZED FOR INDIAN ACCENT
recognizer.energy_threshold = 300  # Much lower threshold for better sensitivity
recognizer.dynamic_energy_threshold = True  # Auto-adjust to environment
recognizer.pause_threshold = 1.2  # Longer pause for complete phrases
recognizer.phrase_threshold = 0.2  # Lower minimum audio length
recognizer.non_speaking_duration = 0.8  # More tolerance for pauses

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
    """Listen for voice command from microphone"""
    try:
        print("🎤 Initializing microphone...")
        log_info("Initializing microphone...")
        
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise... (please wait 1 second)")
            log_info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Use dynamic threshold - don't reset to fixed value
            print(f"🎤 Listening... Bol sakte ho! (Hindi/English dono chalega)")
            print(f"   Energy threshold: {recognizer.energy_threshold}")
            log_info(f"Listening for command... (threshold: {recognizer.energy_threshold})")
            
            # Listen with much longer timeout and phrase limit
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=20)
            
            print("🔄 Processing speech...")
            log_info("Processing audio...")

        # Try to recognize speech with multiple languages
        print("🌐 Connecting to Google Speech API...")
        
        try:
            # Try Hindi/Hinglish first
            command = recognizer.recognize_google(audio, language='hi-IN')
            print(f"✅ You said (Hindi): '{command}'")
            log_info(f"Recognized (hi-IN): {command}")
            return command
        except:
            try:
                # Try English (India)
                command = recognizer.recognize_google(audio, language='en-IN')
                print(f"✅ You said (English): '{command}'")
                log_info(f"Recognized (en-IN): {command}")
                return command
            except:
                # Try US English
                command = recognizer.recognize_google(audio, language='en-US')
                print(f"✅ You said (US English): '{command}'")
                log_info(f"Recognized (en-US): {command}")
                return command
        
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
