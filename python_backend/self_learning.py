"""
Self-Learning System - VEDA AI learns from conversations
Automatically saves and learns from user interactions
"""
import json
import os
from datetime import datetime
from python_backend.logger import log_info, log_error

LEARNING_DATA_FILE = "data/learning_data.json"
CONVERSATION_HISTORY_FILE = "data/conversation_history.json"

def ensure_data_files():
    """Create data files if they don't exist"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(LEARNING_DATA_FILE):
        with open(LEARNING_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    if not os.path.exists(CONVERSATION_HISTORY_FILE):
        with open(CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def save_conversation(user_input, ai_response, feedback=None):
    """
    Save conversation for learning
    
    Args:
        user_input: What user said
        ai_response: What AI responded
        feedback: Optional user feedback (positive/negative)
    """
    ensure_data_files()
    
    try:
        # Load existing conversations
        with open(CONVERSATION_HISTORY_FILE, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        # Add new conversation
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "feedback": feedback
        }
        
        conversations.append(conversation)
        
        # Keep only last 1000 conversations
        if len(conversations) > 1000:
            conversations = conversations[-1000:]
        
        # Save
        with open(CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
        
        log_info(f"Conversation saved: {user_input[:50]}...")
        
        # If positive feedback, add to learning data
        if feedback == "positive":
            add_to_learning_data(user_input, ai_response)
        
    except Exception as e:
        log_error(f"Error saving conversation: {e}")

def add_to_learning_data(user_input, ai_response):
    """Add successful interaction to learning data"""
    ensure_data_files()
    
    try:
        # Load learning data
        with open(LEARNING_DATA_FILE, 'r', encoding='utf-8') as f:
            learning_data = json.load(f)
        
        # Check if similar entry exists
        exists = any(
            item.get("prompt", "").lower() == user_input.lower() 
            for item in learning_data
        )
        
        if not exists:
            learning_data.append({
                "prompt": user_input,
                "response": ai_response,
                "learned_at": datetime.now().isoformat()
            })
            
            # Save
            with open(LEARNING_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
            
            log_info(f"Added to learning data: {user_input[:50]}...")
    
    except Exception as e:
        log_error(f"Error adding to learning data: {e}")

def get_learned_response(user_input):
    """Check if we have a learned response for this input"""
    ensure_data_files()
    
    try:
        with open(LEARNING_DATA_FILE, 'r', encoding='utf-8') as f:
            learning_data = json.load(f)
        
        # Exact match
        for item in learning_data:
            if item.get("prompt", "").lower() == user_input.lower():
                log_info(f"Using learned response for: {user_input[:50]}...")
                return item.get("response")
        
        # Partial match (contains)
        user_lower = user_input.lower()
        for item in learning_data:
            prompt_lower = item.get("prompt", "").lower()
            if prompt_lower in user_lower or user_lower in prompt_lower:
                log_info(f"Using similar learned response for: {user_input[:50]}...")
                return item.get("response")
        
        return None
    
    except Exception as e:
        log_error(f"Error getting learned response: {e}")
        return None

def get_conversation_stats():
    """Get statistics about conversations"""
    ensure_data_files()
    
    try:
        with open(CONVERSATION_HISTORY_FILE, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        with open(LEARNING_DATA_FILE, 'r', encoding='utf-8') as f:
            learning_data = json.load(f)
        
        return {
            "total_conversations": len(conversations),
            "learned_responses": len(learning_data),
            "positive_feedback": sum(1 for c in conversations if c.get("feedback") == "positive"),
            "negative_feedback": sum(1 for c in conversations if c.get("feedback") == "negative")
        }
    
    except Exception as e:
        log_error(f"Error getting stats: {e}")
        return {}

def export_training_data(output_file="training_data_export.json"):
    """Export learning data for model training"""
    ensure_data_files()
    
    try:
        with open(LEARNING_DATA_FILE, 'r', encoding='utf-8') as f:
            learning_data = json.load(f)
        
        # Format for training
        training_data = [
            {
                "prompt": item["prompt"],
                "response": item["response"]
            }
            for item in learning_data
        ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        log_info(f"Training data exported to: {output_file}")
        return f"Exported {len(training_data)} training examples to {output_file}"
    
    except Exception as e:
        log_error(f"Error exporting training data: {e}")
        return f"Error: {e}"

def clear_learning_data():
    """Clear all learning data (use with caution!)"""
    ensure_data_files()
    
    try:
        with open(LEARNING_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        log_info("Learning data cleared")
        return "Learning data cleared successfully"
    
    except Exception as e:
        log_error(f"Error clearing learning data: {e}")
        return f"Error: {e}"
