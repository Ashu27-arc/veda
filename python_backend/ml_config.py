"""
VEDA AI - Machine Learning Configuration
Supports multiple AI providers: OpenAI, Claude, Groq, Local Models
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ========================================
# AI PROVIDER CONFIGURATION
# ========================================

# Primary AI Provider: "openai", "claude", "groq", "local", "lm_studio"
AI_PROVIDER = os.getenv("AI_PROVIDER", "local")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # gpt-4o, gpt-4o-mini, gpt-3.5-turbo
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Claude (Anthropic) Configuration
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")  # claude-3-opus, claude-3-sonnet, claude-3-haiku
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "500"))

# Groq Configuration (Fast inference)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # mixtral-8x7b, llama-3.1-70b

# LM Studio Configuration (Local)
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "local-model")

# ========================================
# INTENT CLASSIFICATION
# ========================================

# Intent categories for command classification
INTENT_CATEGORIES = {
    "system_control": [
        "open", "close", "start", "stop", "launch", "run", "exit", "quit",
        "kholo", "band", "chalu", "shuru", "karo"
    ],
    "volume_control": [
        "volume", "sound", "audio", "mute", "unmute", "louder", "quieter",
        "awaaz", "volume badha", "volume kam"
    ],
    "weather": [
        "weather", "temperature", "forecast", "mausam", "barish", "garmi", "thandi"
    ],
    "time_date": [
        "time", "date", "day", "today", "samay", "tarikh", "aaj", "kal"
    ],
    "greeting": [
        "hello", "hi", "hey", "namaste", "namaskar", "good morning", "good evening"
    ],
    "question": [
        "what", "how", "why", "when", "where", "who", "which",
        "kya", "kaise", "kyun", "kab", "kahan", "kaun", "konsa"
    ],
    "task_management": [
        "remind", "reminder", "schedule", "task", "todo", "yaad dilana", "kaam"
    ],
    "search": [
        "search", "find", "google", "look up", "khojo", "dhundho"
    ],
    "media_control": [
        "play", "pause", "next", "previous", "stop", "music", "video",
        "chalao", "roko", "agla", "pichla"
    ],
    "conversation": [
        "chat", "talk", "tell me", "batao", "baat karo"
    ]
}

# ========================================
# CONVERSATION MEMORY
# ========================================

# Enable conversation memory for multi-turn context
ENABLE_CONVERSATION_MEMORY = os.getenv("ENABLE_CONVERSATION_MEMORY", "true").lower() == "true"

# Maximum conversation turns to remember
MAX_CONVERSATION_TURNS = int(os.getenv("MAX_CONVERSATION_TURNS", "10"))

# Memory storage: "memory" (RAM), "file", "redis"
MEMORY_STORAGE = os.getenv("MEMORY_STORAGE", "file")

# ========================================
# SEMANTIC SIMILARITY
# ========================================

# Enable semantic similarity for better response matching
ENABLE_SEMANTIC_SIMILARITY = os.getenv("ENABLE_SEMANTIC_SIMILARITY", "true").lower() == "true"

# Similarity threshold (0.0 to 1.0)
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))

# Embedding model for semantic search
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# ========================================
# SENTIMENT ANALYSIS
# ========================================

# Enable sentiment analysis for user mood detection
ENABLE_SENTIMENT_ANALYSIS = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "true").lower() == "true"

# ========================================
# RESPONSE GENERATION
# ========================================

# System prompt for AI
SYSTEM_PROMPT = """You are VEDA, a JARVIS-like AI assistant. You are helpful, intelligent, and speak in a professional yet friendly manner.

Key traits:
- Address the user respectfully (use their name if known, otherwise "Sir")
- Be concise but informative
- Support both English and Hinglish (Hindi-English mix)
- Be proactive in offering help
- Show personality but stay professional

Current capabilities:
- System control (open/close apps, volume, etc.)
- Weather information
- Time and date queries
- General conversation
- Task scheduling
- Web searches
"""

# Hindi/Hinglish system prompt
SYSTEM_PROMPT_HINDI = """Aap VEDA hain, ek JARVIS jaisa AI assistant. Aap helpful, intelligent, aur professional lekin friendly tarike se baat karte hain.

Key traits:
- User ko respect se address karein (unka naam use karein agar pata ho, warna "Sir")
- Concise lekin informative rahein
- English aur Hinglish dono support karein
- Proactive rahein madad offer karne mein
- Personality dikhayein lekin professional rahein
"""

# ========================================
# FEATURE FLAGS
# ========================================

FEATURES = {
    "intent_classification": True,
    "conversation_memory": ENABLE_CONVERSATION_MEMORY,
    "semantic_similarity": ENABLE_SEMANTIC_SIMILARITY,
    "sentiment_analysis": ENABLE_SENTIMENT_ANALYSIS,
    "multilingual": True,
    "voice_emotion": False,  # Future: detect emotion from voice
    "face_recognition": False,  # Future: identify users by face
}

# ========================================
# LOGGING
# ========================================

ML_LOG_LEVEL = os.getenv("ML_LOG_LEVEL", "INFO")
LOG_AI_RESPONSES = os.getenv("LOG_AI_RESPONSES", "true").lower() == "true"
