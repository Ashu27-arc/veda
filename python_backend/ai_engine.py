from python_backend.system_control import handle_system_command
from python_backend.voice import speak
from python_backend.utils import is_online
from python_backend.online_ai import chatgpt_response
from python_backend.local_ai import local_ai_response
from python_backend.logger import log_info, log_error, log_warning
import time

# Track last command and timestamp to handle repeated commands
_last_command = None
_last_command_time = 0
_last_response = None
_command_cooldown = 1.0  # 1 second cooldown - allows repeated commands after 1 second

def process_command(command: str, auto_speak: bool = True):
    """Process user command and return response
    
    Args:
        command: User command string
        auto_speak: If True, automatically speak the response (default: True)
    """
    global _last_command, _last_command_time, _last_response
    
    if not command or not isinstance(command, str):
        return "Invalid command"
    
    command = command.lower().strip()
    
    # Prevent command injection
    if any(char in command for char in [';', '&', '|', '`', '\n', '(', ')']):
        log_warning(f"Potentially malicious command blocked: {command}")
        return "Invalid command format"
    
    # Check if this is a duplicate command within cooldown period
    current_time = time.time()
    time_since_last = current_time - _last_command_time
    
    # Allow repeated commands - just log but don't block
    if command == _last_command and time_since_last < _command_cooldown:
        log_info(f"Repeated command detected ({time_since_last:.2f}s): {command} - Processing again")
    
    # Update last command tracking
    _last_command = command
    _last_command_time = current_time
    
    log_info(f"Processing command: {command} (time since last: {time_since_last:.2f}s)")

    try:
        # 1️⃣ WEATHER COMMAND
        if "weather" in command or "mausam" in command or "मौसम" in command:
            from python_backend.weather import get_weather_by_city, get_weather_multiple_cities
            
            # Detect language - default to Hinglish for better Hindi support
            language = 'hinglish' if any(word in command for word in ['mausam', 'मौसम', 'kaisa', 'kaise', 'कैसा', 'कैसे']) else 'english'
            
            # Check for multiple cities (e.g., "delhi aur mumbai ka mausam")
            cities = []
            if " aur " in command or " और " in command or " and " in command:
                # Multiple cities detected
                separator = " aur " if " aur " in command else (" और " if " और " in command else " and ")
                
                # Extract cities
                parts = command.replace(" और ", " aur ").replace(" and ", " aur ").split(" aur ")
                for part in parts:
                    # Extract city name from each part
                    if " mein " in part or " में " in part:
                        city_part = part.replace(" में ", " mein ").split(" mein ")[0].strip()
                        words = city_part.split()
                        if words:
                            cities.append(words[-1])
                    elif " ka " in part or " के " in part:
                        city_part = part.replace(" के ", " ka ").split(" ka ")[0].strip()
                        words = city_part.split()
                        if words:
                            cities.append(words[-1])
                    else:
                        # Try to extract city name
                        words = part.strip().split()
                        for word in words:
                            if len(word) > 2 and word not in ['mausam', 'weather', 'kaisa', 'kaise', 'hai', 'the', 'in']:
                                cities.append(word)
                                break
                
                if len(cities) > 1:
                    log_info(f"Multiple cities detected: {cities} | Language: {language}")
                    response = get_weather_multiple_cities(cities, language)
                    _last_response = response
                    if auto_speak:
                        speak(response)
                    log_info(f"Weather response: {response}")
                    return response
            
            # Single city extraction
            city = ""
            
            # Try different patterns to extract city
            if " in " in command:
                city = command.split(" in ")[-1].strip()
            elif " mein " in command or " में " in command:
                # Handle "Delhi mein mausam kaisa hai"
                parts = command.replace(" में ", " mein ").split(" mein ")
                if len(parts) > 0:
                    # Get the word before "mein"
                    words = parts[0].strip().split()
                    if words:
                        city = words[-1].strip()
            elif " ka " in command or " के " in command:
                parts = command.replace(" के ", " ka ").split(" ka ")
                if len(parts) > 1:
                    city = parts[0].split()[-1].strip()
            
            log_info(f"Extracted city: '{city}' | Language: {language}")
            
            response = get_weather_by_city(city, language)
            _last_response = response
            if auto_speak:
                speak(response)
            log_info(f"Weather response: {response}")
            return response
        
        # 2️⃣ SYSTEM COMMAND
        system_response = handle_system_command(command)
        if system_response:
            _last_response = system_response
            if auto_speak:
                speak(system_response)
            log_info(f"System response: {system_response}")
            return system_response

        # 3️⃣ AI MODE
        response = None
        if is_online():
            try:
                response = chatgpt_response(command)
                log_info("Using online AI")
            except Exception as e:
                log_error(f"Online AI failed: {e}")
                response = None
        
        # Fallback to local AI if online fails or offline
        if not response or "not configured" in response.lower():
            response = local_ai_response(command)
            log_info("Using offline AI")

        # Cache the response for repeated commands
        _last_response = response
        
        if auto_speak:
            speak(response)
        return response
        
    except Exception as e:
        log_error(f"Error processing command: {e}")
        error_msg = "Sorry, I encountered an error processing your command."
        _last_response = error_msg
        if auto_speak:
            speak(error_msg)
        return error_msg
