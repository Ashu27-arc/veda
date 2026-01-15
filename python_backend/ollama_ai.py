"""
Ollama-based Local AI - Self-training without OpenAI
Install: https://ollama.ai/download
Models: llama2, mistral, codellama, etc.
"""
import requests
import json
from python_backend.logger import log_error, log_info

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama2"  # You can change to mistral, codellama, etc.

def ollama_response(prompt, model=DEFAULT_MODEL):
    """Get response from local Ollama model"""
    try:
        # Detect language
        is_hindi = any(word in prompt.lower() for word in ['kya', 'kaise', 'kaun', 'kab', 'kahan', 'mujhe', 'aap', 'tum', 'hai', 'ho'])
        
        system_prompt = """You are VEDA AI, a friendly AI assistant. 
        - Keep responses short (2-3 sentences)
        - Be conversational and helpful
        - If user speaks Hindi/Hinglish, respond in Hinglish
        """
        
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nVEDA:"
        
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 150
            }
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            log_error(f"Ollama API error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        log_error("Ollama not running. Start with: ollama serve")
        return None
    except Exception as e:
        log_error(f"Ollama error: {e}")
        return None

def train_ollama_model(training_data_file, model_name="veda-custom"):
    """
    Train custom Ollama model with your data
    
    Args:
        training_data_file: Path to your training data (text file)
        model_name: Name for your custom model
    
    Returns:
        Success message or error
    """
    try:
        # Read training data
        with open(training_data_file, 'r', encoding='utf-8') as f:
            training_data = f.read()
        
        # Create system prompt with training examples (single line for Ollama)
        # Replace newlines with spaces to make it single line
        training_data_clean = training_data.replace('\n', ' ').replace('\r', ' ')
        system_prompt = f"You are VEDA AI, a friendly AI assistant. Training Examples: {training_data_clean} Instructions: Keep responses short (2-3 sentences). Be conversational and helpful. If user speaks Hindi/Hinglish, respond in Hinglish. Use the training examples above as reference for your responses."
        
        # Create Modelfile for custom training (proper Ollama syntax - each command on single line)
        modelfile_content = f"""FROM {DEFAULT_MODEL}
SYSTEM {system_prompt}
PARAMETER temperature 0.7
PARAMETER num_predict 150
PARAMETER top_p 0.9
"""
        
        # Save Modelfile
        modelfile_path = "Modelfile"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        log_info(f"Modelfile created. Run: ollama create {model_name} -f {modelfile_path}")
        return f"Training setup ready! Run in terminal: ollama create {model_name} -f {modelfile_path}"
        
    except Exception as e:
        log_error(f"Training setup error: {e}")
        return f"Error: {e}"

def list_ollama_models():
    """List all available Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return []
    except:
        return []
