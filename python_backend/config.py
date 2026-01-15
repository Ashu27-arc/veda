import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI REMOVED - Using self-training AI
# OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Self-training AI Configuration
AI_MODE = os.getenv("AI_MODE", "self_training")  # ollama, huggingface, or local
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

