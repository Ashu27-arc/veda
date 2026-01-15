from python_backend.jarvis_personality import get_jarvis

def local_ai_response(command):
    """Offline AI responses with JARVIS personality and Hinglish support - NO CHATGPT REQUIRED"""
    
    jarvis = get_jarvis()
    
    # ⚡ PRIORITY CHECKS - Time/Date (check FIRST before dictionary matching)
    # Time queries (both languages)
    if any(word in command for word in ["time", "samay", "kitne baje", "baje"]):
        from datetime import datetime
        time_str = datetime.now().strftime('%I:%M %p')
        if any(word in command for word in ["samay", "kitne baje", "baje", "batao"]):
            return f"{jarvis.owner_name}, abhi {time_str} baj rahe hain."
        return f"{jarvis.owner_name}, it's {time_str} right now."

    # Date queries (both languages)
    if any(word in command for word in ["date", "today", "tarikh", "aaj ki date"]):
        from datetime import datetime
        date_str = datetime.now().strftime('%A, %B %d, %Y')
        if any(word in command for word in ["tarikh", "aaj ki date", "aaj"]):
            return f"{jarvis.owner_name}, aaj {date_str} hai."
        return f"{jarvis.owner_name}, today is {date_str}."
    
    # English responses - JARVIS style
    qa_english = {
        "who are you": f"I am VEDA, your personal AI assistant, {jarvis.owner_name}. I'm here to help you with anything you need - from system control to information retrieval.",
        "what is your name": f"My name is VEDA, {jarvis.owner_name}. At your service.",
        "who made you": f"I was created to serve as your personal assistant, {jarvis.owner_name}. My purpose is to make your life easier and more efficient.",
        "what can you do": f"I have extensive capabilities, {jarvis.owner_name}. I can control your system, manage applications, check weather, answer questions, and much more. What would you like me to do?",
        "hello": jarvis.get_greeting(),
        "hi": jarvis.get_greeting(),
        "hey": jarvis.get_greeting(),
        "how are you": f"All systems operational, {jarvis.owner_name}. How may I assist you today?",
        "thank you": f"You're most welcome, {jarvis.owner_name}. Always happy to help.",
        "thanks": f"My pleasure, {jarvis.owner_name}. That's what I'm here for.",
        "bye": jarvis.get_farewell(),
        "goodbye": jarvis.get_farewell(),
        "good morning": f"Good morning, {jarvis.owner_name}. I trust you slept well. How may I assist you today?",
        "good night": f"Good night, {jarvis.owner_name}. Rest well. I'll be here if you need me.",
        "help": f"Of course, {jarvis.owner_name}. I can control your system, open applications, manage volume, check weather, answer questions, and assist with various tasks. What do you need?",
        "tell me a joke": f"Certainly, {jarvis.owner_name}. Why did the AI go to school? To improve its learning algorithms! Shall I find you a better one?",
        "are you there": jarvis.get_ready_response(),
        "veda": f"Yes, {jarvis.owner_name}. How can I help?",
        "status": f"All systems operational, {jarvis.owner_name}. Ready to assist.",
        "ready": jarvis.get_ready_response(),
    }
    
    # Hinglish responses - JARVIS style with Hindi (REMOVED generic "batao", "kya hai" to avoid conflicts)
    qa_hinglish = {
        "tum kaun ho": f"Main VEDA hoon, aapka personal AI assistant, {jarvis.owner_name}. Aapki har zarurat ke liye main yahaan hoon.",
        "tumhara naam kya hai": f"Mera naam VEDA hai, {jarvis.owner_name}. Aapki seva mein hazir hoon.",
        "tumhe kisne banaya": f"Mujhe aapki personal assistant banaya gaya hai, {jarvis.owner_name}. Mera maksad aapki zindagi ko aasan aur behtar banana hai.",
        "tum kya kar sakti ho": f"Mere paas bahut capabilities hain, {jarvis.owner_name}. Main system control kar sakti hoon, applications manage kar sakti hoon, weather check kar sakti hoon, aur bahut kuch. Aap kya chahte hain?",
        "namaste": f"Namaste, {jarvis.owner_name}. Aaj main aapki kaise madad kar sakti hoon?",
        "kaise ho": f"Sab systems operational hain, {jarvis.owner_name}. Aapki kya seva kar sakti hoon?",
        "shukriya": f"Aapka swagat hai, {jarvis.owner_name}. Madad karna mera kaam hai.",
        "dhanyavaad": f"Koi baat nahi, {jarvis.owner_name}. Yahi toh mera maksad hai.",
        "alvida": f"Alvida, {jarvis.owner_name}. Zarurat ho toh bulana.",
        "good morning": f"Good morning, {jarvis.owner_name}. Umeed hai aapne achhi neend li. Aaj kya kaam hai?",
        "good night": f"Good night, {jarvis.owner_name}. Achhi neend aaye. Main yahaan hoon agar zarurat ho.",
        "madad": f"Zaroor, {jarvis.owner_name}. Main system control, applications, volume, weather, aur bahut kuch kar sakti hoon. Kya chahiye?",
        "joke sunao": f"Bilkul, {jarvis.owner_name}. AI school kyun gaya? Apne algorithms improve karne! Koi aur sunau?",
        "kya haal hai": f"Sab theek hai, {jarvis.owner_name}. Systems ready hain. Aapko kya chahiye?",
        "kya chal raha hai": f"Sab kuch smooth chal raha hai, {jarvis.owner_name}. Aapke liye kya kar sakti hoon?",
        "taiyar ho": f"Hamesha taiyar hoon, {jarvis.owner_name}.",
        "veda": f"Ji {jarvis.owner_name}, kya kaam hai?",
        "status": f"Sab systems operational hain, {jarvis.owner_name}. Ready to assist.",
        "kaise kare": f"Main madad kar sakti hoon {jarvis.owner_name}. Aur detail mein bataiye kya karna hai.",
    }
    
    # Check Hinglish first
    for q in qa_hinglish:
        if q in command:
            return qa_hinglish[q]
    
    # Check English
    for q in qa_english:
        if q in command:
            return qa_english[q]
    
    # Weather queries - redirect to weather command
    if "weather" in command or "mausam" in command:
        if "mausam" in command:
            return f"{jarvis.owner_name}, weather check karne ke liye 'weather' command use karein. Example: 'Delhi ka weather batao'"
        return f"{jarvis.owner_name}, to check weather, use the weather command. Example: 'weather in Delhi'"
    
    # Conversational responses
    if any(word in command for word in ["love you", "pyar", "like you"]):
        if "love" in command:
            return f"That's very kind of you, {jarvis.owner_name}. I'm always here to serve you."
        return f"Bahut achha laga sunkar, {jarvis.owner_name}. Main hamesha aapke saath hoon."
    
    if any(word in command for word in ["smart", "intelligent", "clever", "genius", "achha", "badhiya"]):
        if any(w in command for w in ["smart", "intelligent", "clever", "genius"]):
            return f"Thank you, {jarvis.owner_name}. I strive to serve you better every day."
        return f"Shukriya, {jarvis.owner_name}. Main hamesha behtar hone ki koshish karta hoon."
    
    # System info queries
    if "system" in command or "computer" in command or "pc" in command:
        if any(w in command for w in ["info", "information", "details", "specs"]):
            import platform
            return f"{jarvis.owner_name}, you're running {platform.system()} {platform.release()} on {platform.machine()} architecture."
    
    # Default responses based on language - MORE HELPFUL
    if any(word in command for word in ["kya", "kaise", "kab", "kahan", "kaun", "kyun"]):
        return f"Samajh gaya {jarvis.owner_name}. Main aapki madad karne ke liye yahaan hoon. Kya aap thoda aur detail mein bata sakte hain?"
    
    if any(word in command for word in ["what", "how", "when", "where", "who", "why"]):
        return f"I understand, {jarvis.owner_name}. I'm here to help. Could you provide more details about what you need?"
    
    # Generic helpful response
    return f"I'm listening, {jarvis.owner_name}. I can help you with system control, opening applications, checking time/date, and more. What would you like me to do?"
