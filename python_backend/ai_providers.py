"""
VEDA AI - Multi-Provider AI Integration
Supports: OpenAI, Claude, Groq, Local Models
"""

import os
import json
from typing import Optional, List, Dict
from python_backend.logger import log_info, log_error, log_warning
from python_backend.ml_config import (
    AI_PROVIDER, SYSTEM_PROMPT,
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS, OPENAI_TEMPERATURE,
    CLAUDE_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS,
    GROQ_API_KEY, GROQ_MODEL,
    LM_STUDIO_URL, LM_STUDIO_MODEL
)

# ========================================
# OPENAI PROVIDER
# ========================================

def get_openai_response(
    prompt: str,
    conversation_history: Optional[List[Dict]] = None,
    system_prompt: str = SYSTEM_PROMPT
) -> Optional[str]:
    """Get response from OpenAI GPT models"""
    
    if not OPENAI_API_KEY:
        log_warning("OpenAI API key not configured")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 turns
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=OPENAI_MAX_TOKENS,
            temperature=OPENAI_TEMPERATURE
        )
        
        result = response.choices[0].message.content
        log_info(f"OpenAI response generated (model: {OPENAI_MODEL})")
        return result
        
    except ImportError:
        log_error("OpenAI library not installed. Run: pip install openai")
        return None
    except Exception as e:
        log_error(f"OpenAI API error: {e}")
        return None


# ========================================
# CLAUDE (ANTHROPIC) PROVIDER
# ========================================

def get_claude_response(
    prompt: str,
    conversation_history: Optional[List[Dict]] = None,
    system_prompt: str = SYSTEM_PROMPT
) -> Optional[str]:
    """Get response from Anthropic Claude models"""
    
    if not CLAUDE_API_KEY:
        log_warning("Claude API key not configured")
        return None
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=CLAUDE_API_KEY)
        
        messages = []
        
        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            system=system_prompt,
            messages=messages
        )
        
        result = response.content[0].text
        log_info(f"Claude response generated (model: {CLAUDE_MODEL})")
        return result
        
    except ImportError:
        log_error("Anthropic library not installed. Run: pip install anthropic")
        return None
    except Exception as e:
        log_error(f"Claude API error: {e}")
        return None


# ========================================
# GROQ PROVIDER (Fast Inference)
# ========================================

def get_groq_response(
    prompt: str,
    conversation_history: Optional[List[Dict]] = None,
    system_prompt: str = SYSTEM_PROMPT
) -> Optional[str]:
    """Get response from Groq (fast LLM inference)"""
    
    if not GROQ_API_KEY:
        log_warning("Groq API key not configured")
        return None
    
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        log_info(f"Groq response generated (model: {GROQ_MODEL})")
        return result
        
    except ImportError:
        log_error("Groq library not installed. Run: pip install groq")
        return None
    except Exception as e:
        log_error(f"Groq API error: {e}")
        return None


# ========================================
# LM STUDIO (LOCAL) PROVIDER
# ========================================

def get_lm_studio_response(
    prompt: str,
    conversation_history: Optional[List[Dict]] = None,
    system_prompt: str = SYSTEM_PROMPT
) -> Optional[str]:
    """Get response from LM Studio local server"""
    
    try:
        import requests
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{LM_STUDIO_URL}/chat/completions",
            json={
                "model": LM_STUDIO_MODEL,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            log_info(f"LM Studio response generated")
            return result
        else:
            log_error(f"LM Studio error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        log_warning("LM Studio not running. Start LM Studio and load a model.")
        return None
    except Exception as e:
        log_error(f"LM Studio error: {e}")
        return None


# ========================================
# UNIFIED AI INTERFACE
# ========================================

def get_ai_response(
    prompt: str,
    conversation_history: Optional[List[Dict]] = None,
    provider: Optional[str] = None
) -> Optional[str]:
    """
    Get AI response from configured provider with automatic fallback
    
    Priority: Specified provider -> Configured provider -> Local fallback
    """
    
    provider = provider or AI_PROVIDER
    
    providers = {
        "openai": get_openai_response,
        "claude": get_claude_response,
        "groq": get_groq_response,
        "lm_studio": get_lm_studio_response,
    }
    
    # Try specified provider first
    if provider in providers:
        response = providers[provider](prompt, conversation_history)
        if response:
            return response
    
    # Fallback chain: Groq -> OpenAI -> Claude -> LM Studio
    fallback_order = ["groq", "openai", "claude", "lm_studio"]
    
    for fallback in fallback_order:
        if fallback != provider and fallback in providers:
            log_info(f"Trying fallback provider: {fallback}")
            response = providers[fallback](prompt, conversation_history)
            if response:
                return response
    
    log_warning("All AI providers failed")
    return None


# ========================================
# PROVIDER STATUS CHECK
# ========================================

def check_provider_status() -> Dict[str, bool]:
    """Check which AI providers are configured and available"""
    
    status = {
        "openai": bool(OPENAI_API_KEY),
        "claude": bool(CLAUDE_API_KEY),
        "groq": bool(GROQ_API_KEY),
        "lm_studio": False,
        "local": True  # Local AI is always available
    }
    
    # Check LM Studio connectivity
    try:
        import requests
        response = requests.get(f"{LM_STUDIO_URL}/models", timeout=2)
        status["lm_studio"] = response.status_code == 200
    except:
        pass
    
    return status


def get_available_providers() -> List[str]:
    """Get list of available AI providers"""
    status = check_provider_status()
    return [provider for provider, available in status.items() if available]
