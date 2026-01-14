"""
JARVIS Personality System
- Professional yet friendly tone
- Respectful to owner
- Proactive and intelligent
- Confirms actions before execution
"""

import random
from datetime import datetime
from python_backend.logger import log_info

class JarvisPersonality:
    """JARVIS-like personality for VEDA AI"""
    
    def __init__(self, owner_name="Sir"):
        self.owner_name = owner_name
        self.conversation_context = []
        self.last_greeting_time = None
        
    def get_greeting(self):
        """Get contextual greeting based on time"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greetings = [
                f"Good morning, {self.owner_name}. How may I assist you today?",
                f"Good morning, {self.owner_name}. I'm at your service.",
                f"Good morning, {self.owner_name}. Ready to help you with anything you need."
            ]
        elif 12 <= hour < 17:
            greetings = [
                f"Good afternoon, {self.owner_name}. How can I help you?",
                f"Good afternoon, {self.owner_name}. What can I do for you?",
                f"Good afternoon, {self.owner_name}. I'm here to assist."
            ]
        elif 17 <= hour < 21:
            greetings = [
                f"Good evening, {self.owner_name}. How may I be of service?",
                f"Good evening, {self.owner_name}. What do you need?",
                f"Good evening, {self.owner_name}. Ready to assist you."
            ]
        else:
            greetings = [
                f"Good evening, {self.owner_name}. Working late, I see. How can I help?",
                f"Hello, {self.owner_name}. I'm here whenever you need me.",
                f"Good evening, {self.owner_name}. What can I do for you?"
            ]
        
        return random.choice(greetings)
    
    def confirm_action(self, action):
        """Confirm action before execution"""
        confirmations = [
            f"Right away, {self.owner_name}.",
            f"Certainly, {self.owner_name}.",
            f"Of course, {self.owner_name}.",
            f"On it, {self.owner_name}.",
            f"Consider it done, {self.owner_name}.",
            f"Immediately, {self.owner_name}."
        ]
        return random.choice(confirmations)
    
    def action_completed(self, action):
        """Confirm action completion"""
        completions = [
            f"{action}, {self.owner_name}.",
            f"{action}. Anything else?",
            f"{action}. Is there anything else you need?",
            f"Done, {self.owner_name}. {action}.",
            f"{action}. What else can I do for you?"
        ]
        return random.choice(completions)
    
    def acknowledge_command(self):
        """Acknowledge command received"""
        acknowledgments = [
            f"Yes, {self.owner_name}.",
            f"Understood, {self.owner_name}.",
            f"Right away, {self.owner_name}.",
            f"On it, {self.owner_name}.",
            f"Certainly, {self.owner_name}."
        ]
        return random.choice(acknowledgments)
    
    def report_status(self, status):
        """Report system status"""
        return f"{self.owner_name}, {status}"
    
    def handle_error(self, error_type="general"):
        """Handle errors gracefully"""
        if error_type == "not_found":
            return f"I apologize, {self.owner_name}, but I couldn't find that."
        elif error_type == "permission":
            return f"I'm sorry, {self.owner_name}, but I don't have permission to do that."
        elif error_type == "offline":
            return f"{self.owner_name}, I'm currently in offline mode. Some features may be limited."
        else:
            return f"I apologize, {self.owner_name}, but I encountered an issue. Let me try another approach."
    
    def get_ready_response(self):
        """Response when ready"""
        responses = [
            f"At your service, {self.owner_name}.",
            f"Ready when you are, {self.owner_name}.",
            f"Standing by, {self.owner_name}.",
            f"I'm here, {self.owner_name}.",
            f"Always ready, {self.owner_name}."
        ]
        return random.choice(responses)
    
    def get_farewell(self):
        """Farewell message"""
        farewells = [
            f"Goodbye, {self.owner_name}. Call me if you need anything.",
            f"Take care, {self.owner_name}. I'll be here when you need me.",
            f"Until next time, {self.owner_name}.",
            f"Farewell, {self.owner_name}. Have a great day.",
            f"See you soon, {self.owner_name}."
        ]
        return random.choice(farewells)
    
    def get_thinking_response(self):
        """Response while processing"""
        responses = [
            f"Let me check that for you, {self.owner_name}.",
            f"One moment, {self.owner_name}.",
            f"Processing, {self.owner_name}.",
            f"Working on it, {self.owner_name}.",
            f"Give me a second, {self.owner_name}."
        ]
        return random.choice(responses)
    
    def get_proactive_suggestion(self, context):
        """Proactive suggestions based on context"""
        suggestions = {
            "morning": f"{self.owner_name}, would you like me to check your schedule for today?",
            "evening": f"{self.owner_name}, shall I prepare a summary of today's activities?",
            "battery_low": f"{self.owner_name}, your battery is running low. Should I enable power saving mode?",
            "idle": f"{self.owner_name}, is there anything I can help you with?"
        }
        return suggestions.get(context, "")
    
    def format_response(self, response, action_type="info"):
        """Format response with JARVIS personality"""
        if action_type == "action":
            return f"{self.confirm_action(response)}"
        elif action_type == "completion":
            return f"{self.action_completed(response)}"
        elif action_type == "error":
            return self.handle_error(response)
        else:
            return response

# Global JARVIS instance
jarvis = JarvisPersonality(owner_name="Sir")

def set_owner_name(name):
    """Set owner's name"""
    global jarvis
    jarvis.owner_name = name
    log_info(f"Owner name set to: {name}")

def get_jarvis():
    """Get JARVIS instance"""
    return jarvis
