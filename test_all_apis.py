"""
Complete API Testing Suite for VEDA AI
Tests all APIs and services to ensure they're working properly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_result(test_name, success, message=""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {test_name}")
    if message:
        print(f"      → {message}")

# ============================================================================
# TEST 1: Environment Variables
# ============================================================================
def test_environment_variables():
    """Test if all required environment variables are set"""
    print_header("TEST 1: Environment Variables")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    picovoice_key = os.getenv("PICOVOICE_ACCESS_KEY")
    
    # Test OpenAI Key
    if openai_key and openai_key not in ["your_openai_api_key_here", "YOUR_OPENAI_API_KEY"]:
        print_result("OpenAI API Key", True, f"Found: {openai_key[:20]}...{openai_key[-10:]}")
    else:
        print_result("OpenAI API Key", False, "Not configured or placeholder")
    
    # Test Picovoice Key
    if picovoice_key and picovoice_key not in ["your_picovoice_access_key_here", "YOUR_PICOVOICE_ACCESS_KEY"]:
        print_result("Picovoice API Key", True, f"Found: {picovoice_key[:20]}...{picovoice_key[-10:]}")
    else:
        print_result("Picovoice API Key", False, "Not configured or placeholder")
    
    return bool(openai_key and picovoice_key)

# ============================================================================
# TEST 2: OpenAI API
# ============================================================================
def test_openai_api():
    """Test OpenAI API connection and functionality"""
    print_header("TEST 2: OpenAI API (ChatGPT)")
    
    try:
        from openai import OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_key:
            print_result("OpenAI Import", False, "API key not found")
            return False
        
        print_result("OpenAI Library Import", True, "Successfully imported")
        
        # Initialize client with error handling
        try:
            client = OpenAI(api_key=openai_key)
            print_result("OpenAI Client Init", True, "Client initialized")
        except TypeError as e:
            # Try with timeout parameter for compatibility
            try:
                client = OpenAI(api_key=openai_key, timeout=30.0)
                print_result("OpenAI Client Init", True, "Client initialized (with timeout)")
            except Exception as e2:
                print_result("OpenAI Client Init", False, str(e2))
                return False
        except Exception as e:
            print_result("OpenAI Client Init", False, str(e))
            return False
        
        # Test API call
        try:
            print("      🔄 Testing API call (this may take a few seconds)...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'API test successful' in exactly 3 words."}
                ],
                max_tokens=50,
                temperature=0.5
            )
            
            result = response.choices[0].message.content
            print_result("OpenAI API Call", True, f"Response: {result}")
            return True
            
        except Exception as e:
            print_result("OpenAI API Call", False, str(e))
            return False
            
    except ImportError as e:
        print_result("OpenAI Library", False, "Not installed. Run: pip install openai")
        return False
    except Exception as e:
        print_result("OpenAI Test", False, str(e))
        return False

# ============================================================================
# TEST 3: Picovoice (Wake Word)
# ============================================================================
def test_picovoice_api():
    """Test Picovoice API for wake word detection"""
    print_header("TEST 3: Picovoice API (Wake Word Detection)")
    
    try:
        import pvporcupine
        print_result("Porcupine Library Import", True, "Successfully imported")
        
        picovoice_key = os.getenv("PICOVOICE_ACCESS_KEY")
        
        if not picovoice_key:
            print_result("Picovoice Key", False, "API key not found")
            return False
        
        # Test Porcupine initialization
        try:
            porcupine = pvporcupine.create(
                access_key=picovoice_key,
                keywords=["computer"]
            )
            
            print_result("Porcupine Init", True, "Wake word engine initialized")
            print_result("Sample Rate", True, f"{porcupine.sample_rate} Hz")
            print_result("Frame Length", True, f"{porcupine.frame_length} samples")
            print_result("Version", True, f"{porcupine.version}")
            
            # Check for custom wake word file
            custom_path = os.path.join("python_frontend", "sounds", "Hey-Veda_en_windows_v4_0_0.ppn")
            if os.path.exists(custom_path):
                print_result("Custom Wake Word File", True, f"Found: {custom_path}")
            else:
                print_result("Custom Wake Word File", False, "Not found (using default 'computer')")
            
            porcupine.delete()
            return True
            
        except Exception as e:
            print_result("Porcupine Init", False, str(e))
            return False
            
    except ImportError:
        print_result("Porcupine Library", False, "Not installed. Run: pip install pvporcupine")
        return False
    except Exception as e:
        print_result("Picovoice Test", False, str(e))
        return False

# ============================================================================
# TEST 4: Weather API
# ============================================================================
def test_weather_api():
    """Test weather API functionality"""
    print_header("TEST 4: Weather API")
    
    try:
        import requests
        print_result("Requests Library", True, "Successfully imported")
        
        # Test primary weather API (wttr.in)
        try:
            print("      🔄 Testing wttr.in API...")
            response = requests.get("https://wttr.in/Delhi?format=j1", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['current_condition'][0]['temp_C']
                location = data['nearest_area'][0]['areaName'][0]['value']
                print_result("Primary Weather API (wttr.in)", True, f"{location}: {temp}°C")
            else:
                print_result("Primary Weather API (wttr.in)", False, f"Status: {response.status_code}")
        except Exception as e:
            print_result("Primary Weather API (wttr.in)", False, str(e))
        
        # Test backup weather API (Open-Meteo)
        try:
            print("      🔄 Testing Open-Meteo API...")
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": 28.6139,
                    "longitude": 77.2090,
                    "current_weather": True
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                temp = data['current_weather']['temperature']
                print_result("Backup Weather API (Open-Meteo)", True, f"Temperature: {temp}°C")
                return True
            else:
                print_result("Backup Weather API (Open-Meteo)", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            print_result("Backup Weather API (Open-Meteo)", False, str(e))
            return False
            
    except ImportError:
        print_result("Requests Library", False, "Not installed. Run: pip install requests")
        return False
    except Exception as e:
        print_result("Weather API Test", False, str(e))
        return False

# ============================================================================
# TEST 5: Speech Recognition
# ============================================================================
def test_speech_recognition():
    """Test speech recognition setup"""
    print_header("TEST 5: Speech Recognition")
    
    try:
        import speech_recognition as sr
        print_result("SpeechRecognition Library", True, "Successfully imported")
        
        # Test microphone access
        try:
            recognizer = sr.Recognizer()
            print_result("Recognizer Init", True, "Initialized successfully")
            
            # List available microphones
            mic_list = sr.Microphone.list_microphone_names()
            print_result("Microphone Detection", True, f"Found {len(mic_list)} microphone(s)")
            
            if mic_list:
                print(f"      → Available microphones:")
                for i, mic in enumerate(mic_list[:3]):  # Show first 3
                    print(f"         {i}: {mic}")
            
            return True
            
        except Exception as e:
            print_result("Microphone Access", False, str(e))
            return False
            
    except ImportError:
        print_result("SpeechRecognition Library", False, "Not installed. Run: pip install SpeechRecognition")
        return False
    except Exception as e:
        print_result("Speech Recognition Test", False, str(e))
        return False

# ============================================================================
# TEST 6: Text-to-Speech
# ============================================================================
def test_text_to_speech():
    """Test text-to-speech functionality"""
    print_header("TEST 6: Text-to-Speech (TTS)")
    
    try:
        import pyttsx3
        print_result("pyttsx3 Library", True, "Successfully imported")
        
        try:
            engine = pyttsx3.init()
            print_result("TTS Engine Init", True, "Engine initialized")
            
            # Get voices
            voices = engine.getProperty('voices')
            print_result("Voice Detection", True, f"Found {len(voices)} voice(s)")
            
            # Get current settings
            rate = engine.getProperty('rate')
            volume = engine.getProperty('volume')
            
            print_result("Voice Rate", True, f"{rate} words/min")
            print_result("Voice Volume", True, f"{volume * 100}%")
            
            return True
            
        except Exception as e:
            print_result("TTS Engine", False, str(e))
            return False
            
    except ImportError:
        print_result("pyttsx3 Library", False, "Not installed. Run: pip install pyttsx3")
        return False
    except Exception as e:
        print_result("TTS Test", False, str(e))
        return False

# ============================================================================
# TEST 7: System Control Libraries
# ============================================================================
def test_system_libraries():
    """Test system control libraries"""
    print_header("TEST 7: System Control Libraries")
    
    libraries = [
        ("pyautogui", "Screen control"),
        ("psutil", "System monitoring"),
        ("pycaw", "Audio control"),
        ("comtypes", "COM interfaces"),
    ]
    
    all_ok = True
    for lib_name, description in libraries:
        try:
            __import__(lib_name)
            print_result(f"{lib_name}", True, description)
        except ImportError:
            print_result(f"{lib_name}", False, f"Not installed. Run: pip install {lib_name}")
            all_ok = False
    
    return all_ok

# ============================================================================
# TEST 8: Internet Connection
# ============================================================================
def test_internet_connection():
    """Test internet connectivity"""
    print_header("TEST 8: Internet Connection")
    
    try:
        import socket
        
        # Test DNS resolution
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print_result("Internet Connection", True, "Connected to internet")
            return True
        except OSError:
            print_result("Internet Connection", False, "No internet connection")
            return False
            
    except Exception as e:
        print_result("Connection Test", False, str(e))
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================
def run_all_tests():
    """Run all tests and generate report"""
    
    print("\n" + "🔬" * 35)
    print("  VEDA AI - COMPLETE API & SERVICE TEST SUITE")
    print("🔬" * 35)
    
    results = {}
    
    # Run all tests
    results['Environment Variables'] = test_environment_variables()
    results['Internet Connection'] = test_internet_connection()
    results['OpenAI API'] = test_openai_api()
    results['Picovoice API'] = test_picovoice_api()
    results['Weather API'] = test_weather_api()
    results['Speech Recognition'] = test_speech_recognition()
    results['Text-to-Speech'] = test_text_to_speech()
    results['System Libraries'] = test_system_libraries()
    
    # Generate summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {test_name}")
    
    print("\n" + "-" * 70)
    print(f"  TOTAL: {passed}/{total} tests passed ({int(passed/total*100)}%)")
    print("-" * 70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! VEDA AI is ready to use!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
    
    print("\n")

if __name__ == "__main__":
    run_all_tests()
