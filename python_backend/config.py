import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI REMOVED - Using self-training AI
# OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Self-training AI Configuration
AI_MODE = os.getenv("AI_MODE", "self_training")  # lm_studio, huggingface, or local
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "local-model")  # Model loaded in LM Studio
LM_STUDIO_API_URL = os.getenv("LM_STUDIO_API_URL", "http://localhost:1234")  # LM Studio default port
LM_STUDIO_TIMEOUT = int(os.getenv("LM_STUDIO_TIMEOUT", "60"))  # Timeout in seconds
LM_STUDIO_MAX_RETRIES = int(os.getenv("LM_STUDIO_MAX_RETRIES", "2"))  # Number of retries on timeout

# Backward compatibility (for old code that uses OLLAMA variables)
OLLAMA_MODEL = LM_STUDIO_MODEL
OLLAMA_API_URL = LM_STUDIO_API_URL
OLLAMA_TIMEOUT = LM_STUDIO_TIMEOUT
OLLAMA_MAX_RETRIES = LM_STUDIO_MAX_RETRIES

