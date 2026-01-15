from python_backend.system_control import handle_system_command, open_application, close_application
from python_backend.voice import speak
from python_backend.utils import is_online
from python_backend.online_ai import chatgpt_response
from python_backend.local_ai import local_ai_response
from python_backend.logger import log_info, log_error, log_warning
from python_backend.jarvis_personality import get_jarvis
import subprocess
import os
import webbrowser

def execute_direct_action(command: str):
    """Execute direct action commands that weren't caught by system_control"""
    jarvis = get_jarvis()
    command_lower = command.lower().strip()
    
    try:
        # Enhanced command parsing for natural language
        log_info(f"Parsing direct action: {command_lower}")
        
        # Common Hindi/Hinglish patterns
        hinglish_patterns = {
            'kholo': 'open',
            'band': 'close',
            'chalu': 'start',
            'shuru': 'start',
            'karo': 'do',
            'dijiye': 'please',
            'kripya': 'please'
        }
        
        # Normalize command
        normalized_command = command_lower
        for hindi, english in hinglish_patterns.items():
            normalized_command = normalized_command.replace(hindi, english)
        
        # Extract app/action name by removing trigger words
        app_name = normalized_command
        trigger_words = ['open', 'start', 'launch', 'run', 'close', 'stop', 'exit', 'quit',
                        'do', 'please', 'karo', 'kar', 'dijiye', 'kripya']
        
        for word in trigger_words:
            app_name = app_name.replace(word, '')
        
        app_name = app_name.strip()
        
        # Determine action type
        is_open = any(word in normalized_command for word in ['open', 'start', 'launch', 'run'])
        is_close = any(word in normalized_command for word in ['close', 'stop', 'exit', 'quit'])
        
        # If we have an app name, try to execute action
        if app_name and len(app_name) > 1:
            log_info(f"Executing action for: {app_name} (open={is_open}, close={is_close})")
            
            if is_open:
                # Try opening as application
                result = open_application(app_name)
                if result and "couldn't find" not in result.lower():
                    return result
                
                # Try as system command
                try:
                    subprocess.Popen(app_name)
                    return f"Executing {app_name}, {jarvis.owner_name}."
                except:
                    pass
                
                # Try with .exe extension
                try:
                    subprocess.Popen(f"{app_name}.exe")
                    return f"Opening {app_name}, {jarvis.owner_name}."
                except:
                    pass
            
            elif is_close:
                # Try closing the application
                result = close_application(app_name)
                if result:
                    return result
        
        return None
        
    except Exception as e:
        log_error(f"Direct action error: {e}")
        return None

def process_command(command: str, auto_speak: bool = True):
    """Process user command and return response - DIRECT COMMAND EXECUTION MODE
    
    Args:
        command: User command string
        auto_speak: If True, automatically speak the response (default: True)
    """
    # Get JARVIS personality instance
    jarvis = get_jarvis()
    
    if not command or not isinstance(command, str):
        return "Invalid command"
    
    # Validate and sanitize input
    from python_backend.utils import sanitize_input, validate_command
    
    command = sanitize_input(command)
    if not validate_command(command):
        log_warning(f"Potentially malicious command blocked: {command}")
        return "Invalid or potentially harmful command detected"
    
    original_command = command
    command = command.lower().strip()
    
    log_info(f"Processing command: {command}")
    
    # Handle greetings with personality
    greeting_words = ['hello', 'hi', 'hey', 'namaste', 'namaskar', 'good morning', 'good afternoon', 'good evening']
    if any(word in command for word in greeting_words):
        response = jarvis.get_greeting()
        if auto_speak:
            speak(response)
        return response
    
    # 🎯 ACKNOWLEDGE COMMAND FIRST (like JARVIS does)
    # Don't acknowledge for simple queries, only for action commands
    action_keywords = ['open', 'close', 'start', 'stop', 'play', 'pause', 'shutdown', 'restart', 
                       'volume', 'brightness', 'search', 'find', 'create', 'delete', 'run',
                       'kholo', 'band', 'chalu', 'shuru', 'karo', 'बंद', 'खोलो', 'चालू']
    
    is_action_command = any(keyword in command for keyword in action_keywords)
    
    if is_action_command and auto_speak:
        # Acknowledge the command immediately
        acknowledgment = jarvis.acknowledge_command()
        speak(acknowledgment)
        log_info(f"Acknowledged: {acknowledgment}")

    try:
        # 1️⃣ WEATHER COMMAND
        if "weather" in command or "mausam" in command or "मौसम" in command:
            from python_backend.weather import get_weather_by_city, get_weather_multiple_cities
            
            # Acknowledge weather query
            if auto_speak and not is_action_command:
                ack = jarvis.get_thinking_response()
                speak(ack)
            
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
            if auto_speak:
                speak(response)
            log_info(f"Weather response: {response}")
            return response
        
        # 2️⃣ SYSTEM COMMAND - Enhanced execution
        system_response = handle_system_command(command)
        if system_response:
            # System response already has action, just return it
            # (acknowledgment was already spoken above if it's an action command)
            if auto_speak:
                speak(system_response)
            log_info(f"System response: {system_response}")
            return system_response
        
        # 2.5️⃣ DIRECT ACTION COMMANDS - If no system response, try to execute as action
        # This handles commands like "chrome kholo", "notepad open karo", etc.
        if is_action_command:
            # Try to extract and execute the command
            action_response = execute_direct_action(command)
            if action_response:
                if auto_speak:
                    speak(action_response)
                log_info(f"Direct action executed: {action_response}")
                return action_response

        # 3️⃣ LOCAL AI RESPONSE - NO CHATGPT DEPENDENCY
        # Always use local AI for questions and queries
        response = local_ai_response(command)
        log_info("Using local AI (no ChatGPT required)")
        
        # Add personality touch to local AI response
        if response and not response.startswith(jarvis.owner_name):
            response = f"{jarvis.owner_name}, {response}"
        
        if auto_speak:
            speak(response)
        return response
        
    except Exception as e:
        log_error(f"Error processing command: {e}")
        error_msg = "Sorry, I encountered an error processing your command."
        if auto_speak:
            speak(error_msg)
        return error_msg
