"""
VEDA AI - Enhanced AI Engine with ML Features
Integrates: Intent Classification, Conversation Memory, Semantic Search, Sentiment Analysis
"""

from typing import Optional, Dict
from python_backend.logger import log_info, log_error, log_warning
from python_backend.jarvis_personality import get_jarvis
from python_backend.ml_config import FEATURES, SYSTEM_PROMPT, ENABLE_CONVERSATION_MEMORY

# Import ML components
from python_backend.intent_classifier import classify_intent, get_intent
from python_backend.conversation_memory import (
    get_conversation_memory, add_to_memory, get_memory_history, get_memory_summary
)
from python_backend.semantic_search import get_semantic_response, learn_response
from python_backend.sentiment_analyzer import analyze_sentiment, get_empathetic_prefix

# Import AI providers
from python_backend.ai_providers import get_ai_response, check_provider_status


class EnhancedAIEngine:
    """
    Enhanced AI Engine with full ML capabilities
    
    Features:
    - Intent Classification: Understands what user wants
    - Conversation Memory: Remembers context
    - Semantic Search: Finds similar learned responses
    - Sentiment Analysis: Detects user mood
    - Multi-provider AI: OpenAI, Claude, Groq, Local
    """
    
    def __init__(self):
        self.jarvis = get_jarvis()
        self.memory = get_conversation_memory()
        self.session_id = "default"
        
        # Check available providers
        self.providers = check_provider_status()
        log_info(f"AI Engine initialized. Available providers: {[k for k, v in self.providers.items() if v]}")
    
    def process(
        self,
        command: str,
        session_id: Optional[str] = None,
        use_memory: bool = True,
        detect_sentiment: bool = True
    ) -> Dict:
        """
        Process command with full ML pipeline
        
        Args:
            command: User's input command
            session_id: Session identifier for memory
            use_memory: Whether to use conversation memory
            detect_sentiment: Whether to analyze sentiment
        
        Returns:
            {
                "response": str,
                "intent": dict,
                "sentiment": dict,
                "context": dict,
                "provider": str
            }
        """
        self.session_id = session_id or self.session_id
        
        result = {
            "response": "",
            "intent": {},
            "sentiment": {},
            "context": {},
            "provider": "local"
        }
        
        try:
            # Step 1: Classify Intent
            log_info(f"Processing: {command[:50]}...")
            intent_result = classify_intent(command)
            result["intent"] = intent_result
            log_info(f"Intent: {intent_result['intent']} ({intent_result['confidence']:.2f})")
            
            # Step 2: Analyze Sentiment
            if detect_sentiment and FEATURES.get("sentiment_analysis"):
                sentiment_result = analyze_sentiment(command)
                result["sentiment"] = sentiment_result
                log_info(f"Sentiment: {sentiment_result['sentiment']}")
            
            # Step 3: Get Context from Memory
            if use_memory and ENABLE_CONVERSATION_MEMORY:
                result["context"] = self.memory.get_context(self.session_id)
                conversation_history = get_memory_history(self.session_id)
            else:
                conversation_history = None
            
            # Step 4: Check for semantic learned response
            if FEATURES.get("semantic_similarity"):
                semantic_response = get_semantic_response(command)
                if semantic_response:
                    log_info("Using semantic learned response")
                    result["response"] = self._enhance_response(
                        semantic_response, 
                        result.get("sentiment", {})
                    )
                    result["provider"] = "semantic"
                    
                    # Save to memory
                    if use_memory:
                        add_to_memory(command, result["response"], self.session_id)
                    
                    return result
            
            # Step 5: Route based on Intent
            response = self._route_by_intent(
                command,
                intent_result["intent"],
                conversation_history
            )
            
            if response:
                result["response"] = self._enhance_response(
                    response,
                    result.get("sentiment", {})
                )
                result["provider"] = "intent_router"
            else:
                # Step 6: Use AI Provider
                response = get_ai_response(command, conversation_history)
                
                if response:
                    result["response"] = self._enhance_response(
                        response,
                        result.get("sentiment", {})
                    )
                    result["provider"] = "ai"
                else:
                    # Fallback to local AI
                    from python_backend.local_ai import local_ai_response
                    result["response"] = local_ai_response(command)
                    result["provider"] = "local"
            
            # Step 7: Save to Memory
            if use_memory and ENABLE_CONVERSATION_MEMORY:
                add_to_memory(command, result["response"], self.session_id)
            
            # Step 8: Learn from interaction (for future semantic search)
            if FEATURES.get("semantic_similarity"):
                learn_response(command, result["response"])
            
            return result
            
        except Exception as e:
            log_error(f"AI Engine error: {e}")
            result["response"] = f"I apologize, {self.jarvis.owner_name}, I encountered an error."
            result["provider"] = "error"
            return result
    
    def _route_by_intent(
        self,
        command: str,
        intent: str,
        conversation_history: Optional[list] = None
    ) -> Optional[str]:
        """Route command based on classified intent"""
        
        # Handle specific intents locally
        if intent == "greeting":
            return self.jarvis.get_greeting()
        
        if intent == "time_date":
            from datetime import datetime
            now = datetime.now()
            
            if any(word in command.lower() for word in ["time", "samay", "baje"]):
                time_str = now.strftime('%I:%M %p')
                if any(word in command.lower() for word in ["samay", "baje"]):
                    return f"{self.jarvis.owner_name}, abhi {time_str} baj rahe hain."
                return f"{self.jarvis.owner_name}, it's {time_str}."
            
            if any(word in command.lower() for word in ["date", "tarikh", "aaj"]):
                date_str = now.strftime('%A, %B %d, %Y')
                if any(word in command.lower() for word in ["tarikh", "aaj"]):
                    return f"{self.jarvis.owner_name}, aaj {date_str} hai."
                return f"{self.jarvis.owner_name}, today is {date_str}."
        
        # System control, weather, etc. - let main ai_engine handle
        if intent in ["system_control", "volume_control", "weather"]:
            return None  # Will be handled by main system
        
        # For questions and conversations, use AI
        return None
    
    def _enhance_response(self, response: str, sentiment: Dict) -> str:
        """Enhance response based on sentiment"""
        if not sentiment:
            return response
        
        sentiment_type = sentiment.get("sentiment", "neutral")
        
        # Add empathetic prefix for negative sentiments
        if sentiment_type == "frustrated":
            prefix = "I understand your frustration. "
            if not response.startswith(prefix) and not response.startswith("I understand"):
                response = prefix + response
        
        elif sentiment_type == "confused":
            prefix = "Let me help clarify. "
            if not response.startswith(prefix) and not response.startswith("Let me"):
                response = prefix + response
        
        elif sentiment_type == "negative":
            if not any(response.startswith(p) for p in ["I'm sorry", "I apologize", "Sorry"]):
                response = "I'm here to help. " + response
        
        return response
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        return get_memory_summary(self.session_id)
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear(self.session_id)
        log_info("Conversation memory cleared")
    
    def set_context(self, key: str, value: any):
        """Set a context variable"""
        self.memory.set_context(key, value, self.session_id)
    
    def get_context(self, key: str, default: any = None) -> any:
        """Get a context variable"""
        return self.memory.get_context_value(key, self.session_id, default)
    
    def get_status(self) -> Dict:
        """Get AI engine status"""
        return {
            "providers": self.providers,
            "features": FEATURES,
            "session_id": self.session_id,
            "memory_turns": len(get_memory_history(self.session_id, format="turns")),
            "context": self.memory.get_context(self.session_id)
        }


# ========================================
# GLOBAL INSTANCE
# ========================================

_engine = None

def get_enhanced_ai_engine() -> EnhancedAIEngine:
    """Get or create global enhanced AI engine"""
    global _engine
    if _engine is None:
        _engine = EnhancedAIEngine()
    return _engine


def process_with_ml(command: str, session_id: str = None) -> Dict:
    """Process command with full ML pipeline"""
    return get_enhanced_ai_engine().process(command, session_id)


def get_ml_response(command: str, session_id: str = None) -> str:
    """Get just the response (convenience function)"""
    result = process_with_ml(command, session_id)
    return result["response"]


# ========================================
# INTEGRATION WITH EXISTING AI ENGINE
# ========================================

def enhance_ai_engine_response(command: str, original_response: str = None) -> str:
    """
    Enhance existing AI engine with ML features
    Can be called from the original ai_engine.py
    """
    engine = get_enhanced_ai_engine()
    
    # If we have an original response, just enhance it with sentiment
    if original_response:
        sentiment = analyze_sentiment(command)
        return engine._enhance_response(original_response, sentiment)
    
    # Otherwise, process fully
    result = engine.process(command)
    return result["response"]
