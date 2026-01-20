"""
VEDA AI - Conversation Memory System
Maintains context across multiple conversation turns
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import deque
from python_backend.logger import log_info, log_error
from python_backend.ml_config import MAX_CONVERSATION_TURNS, MEMORY_STORAGE

# ========================================
# CONVERSATION MEMORY CLASS
# ========================================

class ConversationMemory:
    """
    Manages conversation history for context-aware responses
    """
    
    def __init__(self, max_turns: int = MAX_CONVERSATION_TURNS):
        self.max_turns = max_turns
        self.conversations: Dict[str, deque] = {}  # session_id -> conversation
        self.context: Dict[str, Dict] = {}  # session_id -> context variables
        self.storage_path = "data/conversation_memory.json"
        
        # Load previous conversations if using file storage
        if MEMORY_STORAGE == "file":
            self._load_from_file()
    
    def _get_session_id(self, session_id: Optional[str] = None) -> str:
        """Get or create session ID"""
        return session_id or "default"
    
    def add_turn(
        self,
        user_message: str,
        assistant_message: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Add a conversation turn to memory"""
        sid = self._get_session_id(session_id)
        
        if sid not in self.conversations:
            self.conversations[sid] = deque(maxlen=self.max_turns)
        
        turn = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": assistant_message,
            "metadata": metadata or {}
        }
        
        self.conversations[sid].append(turn)
        log_info(f"Added conversation turn (session: {sid}, total: {len(self.conversations[sid])})")
        
        # Extract and store context
        self._extract_context(user_message, assistant_message, sid)
        
        # Save to file if using file storage
        if MEMORY_STORAGE == "file":
            self._save_to_file()
    
    def get_history(
        self,
        session_id: Optional[str] = None,
        format: str = "messages"
    ) -> List:
        """
        Get conversation history
        
        Args:
            session_id: Session to get history for
            format: "messages" for OpenAI format, "turns" for raw turns
        """
        sid = self._get_session_id(session_id)
        
        if sid not in self.conversations:
            return []
        
        turns = list(self.conversations[sid])
        
        if format == "messages":
            # Convert to OpenAI message format
            messages = []
            for turn in turns:
                messages.append({"role": "user", "content": turn["user"]})
                messages.append({"role": "assistant", "content": turn["assistant"]})
            return messages
        
        return turns
    
    def get_context(self, session_id: Optional[str] = None) -> Dict:
        """Get extracted context for session"""
        sid = self._get_session_id(session_id)
        return self.context.get(sid, {})
    
    def set_context(
        self,
        key: str,
        value: any,
        session_id: Optional[str] = None
    ):
        """Set a context variable"""
        sid = self._get_session_id(session_id)
        
        if sid not in self.context:
            self.context[sid] = {}
        
        self.context[sid][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        
        log_info(f"Context set: {key} = {value} (session: {sid})")
    
    def get_context_value(
        self,
        key: str,
        session_id: Optional[str] = None,
        default: any = None
    ) -> any:
        """Get a specific context value"""
        sid = self._get_session_id(session_id)
        ctx = self.context.get(sid, {})
        
        if key in ctx:
            return ctx[key]["value"]
        return default
    
    def _extract_context(self, user_msg: str, assistant_msg: str, session_id: str):
        """Extract relevant context from conversation"""
        # Extract mentioned names
        import re
        
        # Look for "my name is X" patterns
        name_patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"call me (\w+)",
            r"mera naam (\w+)",
            r"main (\w+) hoon"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, user_msg.lower())
            if match:
                self.set_context("user_name", match.group(1).title(), session_id)
                break
        
        # Extract location mentions
        location_patterns = [
            r"(?:in|at|from|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
            r"([A-Z][a-z]+)\s+(?:mein|me|ka|ki|ke)"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, user_msg)
            if match:
                self.set_context("last_location", match.group(1), session_id)
                break
        
        # Track topics
        topics = self.get_context_value("topics", session_id, [])
        words = user_msg.lower().split()
        topic_keywords = ["weather", "music", "news", "time", "date", "app", "file"]
        for keyword in topic_keywords:
            if keyword in words and keyword not in topics:
                topics.append(keyword)
        
        if topics:
            self.set_context("topics", topics[-5:], session_id)  # Keep last 5 topics
    
    def get_summary(self, session_id: Optional[str] = None) -> str:
        """Get a summary of the conversation for context"""
        sid = self._get_session_id(session_id)
        history = self.get_history(sid, format="turns")
        
        if not history:
            return "No previous conversation."
        
        # Create brief summary
        summary_parts = []
        
        # Add context
        ctx = self.get_context(sid)
        if ctx.get("user_name"):
            summary_parts.append(f"User's name: {ctx['user_name']['value']}")
        if ctx.get("last_location"):
            summary_parts.append(f"Last mentioned location: {ctx['last_location']['value']}")
        if ctx.get("topics"):
            summary_parts.append(f"Topics discussed: {', '.join(ctx['topics']['value'])}")
        
        # Add recent turns summary
        recent = history[-3:]  # Last 3 turns
        for turn in recent:
            summary_parts.append(f"User asked about: {turn['user'][:50]}...")
        
        return "\n".join(summary_parts)
    
    def clear(self, session_id: Optional[str] = None):
        """Clear conversation history"""
        sid = self._get_session_id(session_id)
        
        if sid in self.conversations:
            del self.conversations[sid]
        if sid in self.context:
            del self.context[sid]
        
        log_info(f"Conversation cleared (session: {sid})")
        
        if MEMORY_STORAGE == "file":
            self._save_to_file()
    
    def _save_to_file(self):
        """Save conversations to file"""
        try:
            os.makedirs("data", exist_ok=True)
            
            data = {
                "conversations": {
                    sid: list(conv) for sid, conv in self.conversations.items()
                },
                "context": self.context,
                "saved_at": datetime.now().isoformat()
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            log_error(f"Failed to save conversation memory: {e}")
    
    def _load_from_file(self):
        """Load conversations from file"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load conversations
                for sid, conv in data.get("conversations", {}).items():
                    self.conversations[sid] = deque(conv, maxlen=self.max_turns)
                
                # Load context
                self.context = data.get("context", {})
                
                log_info(f"Loaded conversation memory: {len(self.conversations)} sessions")
                
        except Exception as e:
            log_error(f"Failed to load conversation memory: {e}")


# ========================================
# GLOBAL MEMORY INSTANCE
# ========================================

_memory = None

def get_conversation_memory() -> ConversationMemory:
    """Get or create global conversation memory instance"""
    global _memory
    if _memory is None:
        _memory = ConversationMemory()
    return _memory


def add_to_memory(user_msg: str, assistant_msg: str, session_id: str = None):
    """Convenience function to add conversation turn"""
    get_conversation_memory().add_turn(user_msg, assistant_msg, session_id)


def get_memory_history(session_id: str = None, format: str = "messages") -> List:
    """Convenience function to get history"""
    return get_conversation_memory().get_history(session_id, format)


def get_memory_context(session_id: str = None) -> Dict:
    """Convenience function to get context"""
    return get_conversation_memory().get_context(session_id)


def get_memory_summary(session_id: str = None) -> str:
    """Convenience function to get summary"""
    return get_conversation_memory().get_summary(session_id)
