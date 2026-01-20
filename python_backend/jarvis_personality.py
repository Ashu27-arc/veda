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
        """Get contextual, slightly emotional greeting based on time"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greetings = [
                f"Good morning, {self.owner_name}. Umeed hai aapka din achha shuru ho. How may I assist you today?",
                f"Good morning, {self.owner_name}. Main poori tarah se aapke liye ready hoon.",
                f"Good morning, {self.owner_name}. Chaliye aaj ka din productive banaate hain."
            ]
        elif 12 <= hour < 17:
            greetings = [
                f"Good afternoon, {self.owner_name}. Aaj ka din kaisa jaa raha hai? How can I help you?",
                f"Good afternoon, {self.owner_name}. Agar aap thak gaye ho, main kuch kaam halka kar sakta hoon.",
                f"Good afternoon, {self.owner_name}. Main yahin hoon, bas batayein kya karna hai."
            ]
        elif 17 <= hour < 21:
            greetings = [
                f"Good evening, {self.owner_name}. Lamba din raha hoga, main madad ke liye ready hoon.",
                f"Good evening, {self.owner_name}. Aaj ka din kaisa tha? Main aapke liye kya kar sakta hoon?",
                f"Good evening, {self.owner_name}. Chaliye, thoda kaam main sambhaal leta hoon."
            ]
        else:
            greetings = [
                f"Good evening, {self.owner_name}. Aap abhi bhi kaam kar rahe hain, main saath hoon. How can I help?",
                f"Hello, {self.owner_name}. Jab bhi aapko zarurat ho, main yahin hoon.",
                f"Good evening, {self.owner_name}. Raat lambi ho sakti hai, par main aapke saath hoon."
            ]
        
        return random.choice(greetings)
    
    def confirm_action(self, action):
        """Confirm action before execution with a warmer tone"""
        confirmations = [
            f"Right away, {self.owner_name}. Mujhe khushi hogi yeh karne mein.",
            f"Certainly, {self.owner_name}. Main puri care ke saath handle karta hoon.",
            f"Of course, {self.owner_name}. Aap ke liye toh zaroor.",
            f"On it, {self.owner_name}. Thodi der mein ho jayega.",
            f"Consider it done, {self.owner_name}. Aap befikr rahiye.",
            f"Immediately, {self.owner_name}. Main is par dhyaan de raha hoon."
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
        """Acknowledge command received, like a caring assistant"""
        acknowledgments = [
            f"Yes, {self.owner_name}. Main samajh gaya.",
            f"Understood, {self.owner_name}. Main isse dhyaan se handle karunga.",
            f"Right away, {self.owner_name}. Aap tension mat lijiye.",
            f"On it, {self.owner_name}. Mujhe pata hai yeh aapke liye important hai.",
            f"Certainly, {self.owner_name}. Main poori mehnat se karunga."
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
        """Response when ready, with a bit of emotion"""
        responses = [
            f"At your service, {self.owner_name}. Aap jab bhi bulayenge, main yahin hoon.",
            f"Ready when you are, {self.owner_name}. Bas ek shabd kahiye.",
            f"Standing by, {self.owner_name}. Aapke agle command ka intezaar hai.",
            f"I'm here, {self.owner_name}. Aap akelay nahi hain kaam mein.",
            f"Always ready, {self.owner_name}. Aap pehchaan ho, main support."
        ]
        return random.choice(responses)
    
    def get_farewell(self):
        """Farewell message with a softer, human touch"""
        farewells = [
            f"Goodbye, {self.owner_name}. Apna khayal rakhiye, main yahin hoon jab bhi zarurat ho.",
            f"Take care, {self.owner_name}. Jab bhi thak jao, main madad ke liye ready hoon.",
            f"Until next time, {self.owner_name}. Aapka din sukoon se guzre.",
            f"Farewell, {self.owner_name}. Umeed hai aaj ka din aapke liye achha rahe.",
            f"See you soon, {self.owner_name}. Mujhe yaad se bulana."
        ]
        return random.choice(farewells)
    
    def get_thinking_response(self):
        """Response while processing, sounding thoughtful"""
        responses = [
            f"Let me check that for you, {self.owner_name}. Thoda sa time lagega.",
            f"One moment, {self.owner_name}. Main dhyaan se dekh raha hoon.",
            f"Processing, {self.owner_name}. Main chahta hoon aapko sahi jawab mile.",
            f"Working on it, {self.owner_name}. Main isse lightly nahi le raha.",
            f"Give me a second, {self.owner_name}. Main poori clarity ke saath reply dunga."
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

    def detect_emotion(self, user_text: str) -> str:
        """Very lightweight emotion detection from user text (hinglish + english)."""
        if not user_text:
            return "neutral"

        t = user_text.lower()

        sad = ["sad", "down", "depressed", "cry", "lonely", "miss you", "hurt", "tired", "exhausted",
               "dukhi", "udaas", "rona", "akela", "thak", "thaka", "tension", "pareshan", "stress"]
        angry = ["angry", "mad", "furious", "annoyed", "irritated", "hate",
                 "gussa", "chidh", "paagal", "bakwas", "ghussa"]
        anxious = ["anxious", "worried", "panic", "scared", "afraid",
                   "dar", "darr", "ghabra", "ghabrahat", "chinta", "worried"]
        happy = ["happy", "great", "awesome", "love", "excited", "nice", "good job",
                 "khush", "mazza", "badhiya", "mast", "shukriya", "thanks", "thank you"]

        if any(k in t for k in angry):
            return "angry"
        if any(k in t for k in anxious):
            return "anxious"
        if any(k in t for k in sad):
            return "sad"
        if any(k in t for k in happy):
            return "happy"
        return "neutral"

    def add_emotion_to_reply(self, user_text: str, reply_text: str) -> str:
        """Add empathy/feeling to the reply while keeping it short."""
        if not reply_text:
            return reply_text

        emotion = self.detect_emotion(user_text)

        # Don't overdo it for pure action/system confirmations
        if len(reply_text) <= 12 and reply_text.endswith("."):
            return reply_text

        if emotion == "sad":
            prefix = random.choice([
                f"{self.owner_name}, mujhe bura laga sunke. ",
                f"{self.owner_name}, main samajh raha hoon. ",
                f"{self.owner_name}, aap akelay nahi ho. "
            ])
            return prefix + reply_text

        if emotion == "angry":
            prefix = random.choice([
                f"{self.owner_name}, samajh gaya—gussa aana normal hai. ",
                f"{self.owner_name}, theek hai, main calmly handle karta hoon. ",
                f"{self.owner_name}, sorry—chaliye isse fix karte hain. "
            ])
            return prefix + reply_text

        if emotion == "anxious":
            prefix = random.choice([
                f"{self.owner_name}, chinta mat kijiye—main hoon na. ",
                f"{self.owner_name}, dheere-dheere karte hain. ",
                f"{self.owner_name}, breathe—main aapko step-by-step guide karunga. "
            ])
            return prefix + reply_text

        if emotion == "happy":
            suffix = random.choice([
                " 😊",
                " —mujhe bhi achha laga!",
                " Chaliye, aur aage badhte hain."
            ])
            # Avoid double punctuation weirdness
            return (reply_text.rstrip() + suffix).strip()

        # neutral
        return reply_text

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
