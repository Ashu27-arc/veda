"""
LM Studio-based Local AI - Self-training without OpenAI
Install: https://lmstudio.ai/
Models: Any GGUF models (Llama, Mistral, Phi, etc.)
LM Studio provides OpenAI-compatible API
"""
import requests
import json
from python_backend.logger import log_error, log_info, log_warning
from python_backend.config import LM_STUDIO_API_URL as CONFIG_LM_URL, LM_STUDIO_MODEL, LM_STUDIO_TIMEOUT, LM_STUDIO_MAX_RETRIES

LM_STUDIO_API_URL = CONFIG_LM_URL + "/v1/chat/completions"
DEFAULT_MODEL = LM_STUDIO_MODEL
MAX_RETRIES = LM_STUDIO_MAX_RETRIES

def lm_studio_response(prompt, model=DEFAULT_MODEL):
    """Get response from local LM Studio model with retry logic
    
    LM Studio provides OpenAI-compatible API, making it easy to use
    """
    # Detect language
    is_hindi = any(word in prompt.lower() for word in ['kya', 'kaise', 'kaun', 'kab', 'kahan', 'mujhe', 'aap', 'tum', 'hai', 'ho'])
    
    system_prompt = """You are VEDA AI, a friendly AI assistant. 
    - Keep responses short (2-3 sentences)
    - Be conversational and helpful
    - If user speaks Hindi/Hinglish, respond in Hinglish
    """
    
    # OpenAI-compatible format (LM Studio uses this)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": False
    }
    
    # Retry logic for timeout errors
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(LM_STUDIO_API_URL, json=payload, timeout=LM_STUDIO_TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                # Extract response from OpenAI-compatible format
                if "choices" in result and len(result["choices"]) > 0:
                    message = result["choices"][0].get("message", {})
                    return message.get("content", "").strip()
                return None
            else:
                log_error(f"LM Studio API error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                log_warning(f"LM Studio timeout (attempt {attempt + 1}/{MAX_RETRIES + 1}), retrying...")
                continue
            else:
                log_error(f"LM Studio timeout after {MAX_RETRIES + 1} attempts. Consider using a faster model or increasing timeout.")
                return None
                
        except requests.exceptions.ConnectionError:
            log_error("LM Studio not running. Please start LM Studio and load a model, then enable the local server.")
            return None
            
        except Exception as e:
            log_error(f"LM Studio error: {e}")
            return None
    
    return None

# Backward compatibility alias
def ollama_response(prompt, model=DEFAULT_MODEL):
    """Backward compatibility - redirects to LM Studio"""
    return lm_studio_response(prompt, model)

def get_lm_studio_system_prompt(training_data_file=None):
    """
    Create system prompt for LM Studio with optional training data
    
    Args:
        training_data_file: Optional path to training data file
    
    Returns:
        System prompt string
    """
    base_prompt = """You are VEDA AI, a friendly AI assistant.
- Keep responses short (2-3 sentences)
- Be conversational and helpful
- If user speaks Hindi/Hinglish, respond in Hinglish
"""
    
    if training_data_file:
        try:
            with open(training_data_file, 'r', encoding='utf-8') as f:
                training_data = f.read()
            
            # Add training examples to system prompt
            base_prompt += f"\n\nTraining Examples:\n{training_data}\n\nUse these examples as reference for your responses."
            log_info(f"Loaded training data from {training_data_file}")
        except Exception as e:
            log_error(f"Error loading training data: {e}")
    
    return base_prompt

def list_lm_studio_models():
    """List all available LM Studio models"""
    try:
        # LM Studio uses OpenAI-compatible API
        models_url = CONFIG_LM_URL + "/v1/models"
        response = requests.get(models_url, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if "data" in result:
                return [model["id"] for model in result["data"]]
        return []
    except Exception as e:
        log_error(f"Error listing LM Studio models: {e}")
        return []

# Backward compatibility aliases
def train_ollama_model(training_data_file, model_name="veda-custom"):
    """Backward compatibility - LM Studio doesn't need training, just load models"""
    log_info("LM Studio uses pre-trained models. Download models from LM Studio app.")
    return "LM Studio uses pre-trained GGUF models. Download models from the LM Studio app, then load them in the local server."

def list_ollama_models():
    """Backward compatibility - redirects to LM Studio"""
    return list_lm_studio_models()
