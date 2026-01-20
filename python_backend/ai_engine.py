from python_backend.system_control import handle_system_command, open_application, close_application
from python_backend.voice import speak
from python_backend.utils import is_online
from python_backend.local_ai import local_ai_response
from python_backend.logger import log_info, log_error, log_warning
from python_backend.jarvis_personality import get_jarvis
from python_backend.context_awareness import get_context_awareness
from python_backend.config import AI_MODE
import subprocess
import os
import webbrowser

# ========== ML FEATURES IMPORT ==========
try:
    from python_backend.intent_classifier import classify_intent, get_intent
    from python_backend.conversation_memory import add_to_memory, get_memory_history
    from python_backend.semantic_search import get_semantic_response, learn_response
    from python_backend.sentiment_analyzer import analyze_sentiment, get_empathetic_prefix
    from python_backend.ai_providers import get_ai_response as get_provider_response
    from python_backend.ml_config import FEATURES, ENABLE_CONVERSATION_MEMORY
    ML_FEATURES_AVAILABLE = True
    log_info("ML features loaded successfully")
except ImportError as e:
    ML_FEATURES_AVAILABLE = False
    log_warning(f"ML features not available: {e}")

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

def process_command(command: str, auto_speak: bool = True, session_id: str = None):
    """Process user command and return response - DIRECT COMMAND EXECUTION MODE
    
    Args:
        command: User command string
        auto_speak: If True, automatically speak the response (default: True)
        session_id: Session ID for conversation memory (optional)
        
    Returns:
        str: Response from VEDA AI
    """
    # Early validation
    if not command or not isinstance(command, str):
        return "Please provide a valid command."
    
    command = str(command).strip()
    if len(command) == 0:
        return "Empty command received. Please say something."
    
    if len(command) > 1000:
        return "Command is too long. Please keep it under 1000 characters."
    
    # Get JARVIS personality instance (with error handling)
    try:
        jarvis = get_jarvis()
    except Exception as e:
        log_error(f"Failed to get JARVIS instance: {e}")
        jarvis = None
    
    # Track command in context awareness (non-critical)
    try:
        context = get_context_awareness()
        if context:
            context.track_command(command)
    except Exception as e:
        log_warning(f"Context tracking failed (non-critical): {e}")
    
    # ========== ML FEATURES: Intent Classification & Sentiment ==========
    intent_info = None
    sentiment_info = None
    
    if ML_FEATURES_AVAILABLE:
        try:
            # Classify intent for better understanding (with timeout protection)
            intent_info = classify_intent(command)
            if intent_info:
                log_info(f"Intent: {intent_info.get('intent', 'unknown')} (confidence: {intent_info.get('confidence', 0):.2f})")
            
            # Analyze sentiment for empathetic responses
            sentiment_info = analyze_sentiment(command)
            if sentiment_info:
                log_info(f"Sentiment: {sentiment_info.get('sentiment', 'neutral')}")
        except Exception as e:
            log_warning(f"ML feature error (using fallback): {e}")
            intent_info = {"intent": "unknown", "confidence": 0}
            sentiment_info = {"sentiment": "neutral", "confidence": 0}
    
    # Validate and sanitize input
    from python_backend.utils import sanitize_input, validate_command
    
    command = sanitize_input(command)
    if not command:
        return "Could not process your command. Please try again."
        
    if not validate_command(command):
        log_warning(f"Potentially malicious command blocked: {command[:50]}...")
        return "I cannot process that command for security reasons."
    
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

        # 3️⃣ CHECK LEARNED RESPONSES (Self-learning + Semantic Search)
        from python_backend.self_learning import get_learned_response, save_conversation
        
        # Try semantic search first (ML-based)
        if ML_FEATURES_AVAILABLE and FEATURES.get("semantic_similarity"):
            try:
                semantic_response = get_semantic_response(command)
                if semantic_response:
                    log_info("Using semantic learned response")
                    # Add empathy based on sentiment
                    if sentiment_info and sentiment_info.get("sentiment") in ["frustrated", "negative"]:
                        semantic_response = get_empathetic_prefix(command) + semantic_response
                    if auto_speak:
                        speak(semantic_response)
                    return semantic_response
            except Exception as e:
                log_error(f"Semantic search error: {e}")
        
        # Fallback to exact match learning
        learned_response = get_learned_response(command)
        
        if learned_response:
            log_info("Using learned response from previous conversations")
            if auto_speak:
                speak(learned_response)
            return learned_response

        # 4️⃣ AI RESPONSE - Multiple options with ML Enhancement
        # AI_MODE comes from config: "lm_studio", "huggingface", "local", "openai", "claude", "groq"
        mode = (AI_MODE or "self_training").lower()
        response = None
        
        # Get conversation history for context (if ML features available)
        conversation_history = None
        if ML_FEATURES_AVAILABLE and ENABLE_CONVERSATION_MEMORY:
            try:
                conversation_history = get_memory_history(session_id)
            except Exception as e:
                log_error(f"Memory history error: {e}")

        # Helper to try Hugging Face then fall back to local
        def _use_huggingface_or_local(prompt: str):
            hf_response = None
            try:
                from python_backend.huggingface_ai import huggingface_response
                hf_response = huggingface_response(prompt)
                if hf_response:
                    log_info("Using Hugging Face (local AI)")
                    return hf_response
            except ImportError:
                log_info("Hugging Face not available")
            except Exception as e_inner:
                log_error(f"Hugging Face error: {e_inner}")

            # Fallback to local AI (rule-based)
            local_response = local_ai_response(prompt)
            log_info("Using local AI (rule-based, no external dependency)")
            return local_response
        
        # Try ML-based AI providers first (OpenAI, Claude, Groq)
        if ML_FEATURES_AVAILABLE and mode in ["openai", "claude", "groq"]:
            try:
                response = get_provider_response(command, conversation_history, provider=mode)
                if response:
                    log_info(f"Using {mode} AI provider")
            except Exception as e:
                log_error(f"{mode} provider error: {e}")

        if not response and mode == "lm_studio":
            # Prefer LM Studio, then Hugging Face, then local
            try:
                from python_backend.lm_studio_ai import lm_studio_response
                from python_backend.config import LM_STUDIO_MODEL
                response = lm_studio_response(command, model=LM_STUDIO_MODEL)
                if response:
                    log_info(f"Using LM Studio model: {LM_STUDIO_MODEL}")
            except ImportError:
                log_info("LM Studio not available")
            except Exception as e:
                log_error(f"LM Studio error: {e}")

            if not response:
                response = _use_huggingface_or_local(command)

        elif not response and mode == "huggingface":
            # Skip LM Studio completely, stay fully local/embedded
            response = _use_huggingface_or_local(command)

        elif not response and mode == "local":
            # Pure rule-based, no external model calls at all
            response = local_ai_response(command)
            log_info("Using local AI only (rule-based, fully offline)")

        elif not response:
            # Backward-compatible behaviour (old self_training mode):
            # Try ML providers → LM Studio → Hugging Face → local
            
            # First try ML providers if available
            if ML_FEATURES_AVAILABLE:
                try:
                    response = get_provider_response(command, conversation_history)
                    if response:
                        log_info("Using ML AI provider (auto-selected)")
                except Exception as e:
                    log_error(f"ML provider error: {e}")
            
            if not response:
                try:
                    from python_backend.lm_studio_ai import lm_studio_response
                    from python_backend.config import LM_STUDIO_MODEL
                    response = lm_studio_response(command, model=LM_STUDIO_MODEL)
                    if response:
                        log_info(f"Using LM Studio model: {LM_STUDIO_MODEL}")
                except ImportError:
                    log_info("LM Studio not available")
                except Exception as e:
                    log_error(f"LM Studio error: {e}")

            if not response:
                response = _use_huggingface_or_local(command)
        
        # Add personality touch
        if response and not response.startswith(jarvis.owner_name):
            response = f"{jarvis.owner_name}, {response}"

        # Add emotional intelligence layer (empathy / warmth)
        try:
            response = jarvis.add_emotion_to_reply(original_command, response)
        except Exception:
            # Never break core response path if emotion layer fails
            pass
        
        # ========== ML ENHANCEMENT: Sentiment-based response ==========
        if ML_FEATURES_AVAILABLE and sentiment_info:
            try:
                sentiment = sentiment_info.get("sentiment", "neutral")
                
                # Add empathetic prefix for frustrated users
                if sentiment == "frustrated" and not response.startswith("I understand"):
                    response = "I understand your frustration. " + response
                
                # Add clarification prefix for confused users
                elif sentiment == "confused" and not response.startswith("Let me"):
                    response = "Let me help clarify. " + response
                    
            except Exception as e:
                log_error(f"Sentiment enhancement error: {e}")
        
        if auto_speak:
            speak(response)
        
        # Save conversation for self-learning
        save_conversation(original_command, response)
        
        # ========== ML ENHANCEMENT: Save to conversation memory ==========
        if ML_FEATURES_AVAILABLE and ENABLE_CONVERSATION_MEMORY:
            try:
                add_to_memory(original_command, response, session_id)
            except Exception as e:
                log_error(f"Memory save error: {e}")
        
        # Learn for semantic search
        if ML_FEATURES_AVAILABLE and FEATURES.get("semantic_similarity"):
            try:
                learn_response(original_command, response)
            except Exception as e:
                log_error(f"Semantic learn error: {e}")
        
        return response
        
    except KeyboardInterrupt:
        log_warning("Command processing interrupted")
        return "Command processing was interrupted."
    except MemoryError:
        log_error("Memory error during command processing")
        return "I ran out of memory processing that command. Please try a simpler request."
    except TimeoutError:
        log_error("Timeout during command processing")
        return "The operation timed out. Please try again."
    except Exception as e:
        log_error(f"Error processing command: {type(e).__name__}: {e}")
        error_msg = f"Sorry, I encountered an error: {type(e).__name__}. Please try again."
        
        # Don't try to speak if the error might be speech-related
        if auto_speak and "speech" not in str(e).lower() and "audio" not in str(e).lower():
            try:
                speak(error_msg)
            except Exception:
                pass  # Ignore speech errors during error handling
                
        return error_msg
