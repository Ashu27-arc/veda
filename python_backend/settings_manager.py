"""
Settings Manager for VEDA AI
Manages user preferences and JARVIS personality settings
"""

import json
import os
from python_backend.logger import log_info, log_error
from python_backend.jarvis_personality import set_owner_name

SETTINGS_FILE = "data/settings.json"

DEFAULT_SETTINGS = {
    "owner_name": "Sir",
    "personality": "jarvis",
    "language_preference": "hinglish",
    "voice_speed": 175,
    "proactive_suggestions": True,
    "confirmation_required": {
        "system_shutdown": True,
        "system_restart": True,
        "file_deletion": True
    },
    "startup_greeting": True,
    "theme": "dark"
}

def load_settings():
    """Load settings from file"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                
            # Set owner name in JARVIS personality
            owner_name = settings.get("owner_name", "Sir")
            set_owner_name(owner_name)
            
            log_info(f"Settings loaded successfully. Owner: {owner_name}")
            return settings
        else:
            # Create default settings file
            save_settings(DEFAULT_SETTINGS)
            log_info("Created default settings file")
            return DEFAULT_SETTINGS
            
    except Exception as e:
        log_error(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS

def save_settings(settings):
    """Save settings to file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        
        # Update owner name in JARVIS personality
        owner_name = settings.get("owner_name", "Sir")
        set_owner_name(owner_name)
        
        log_info(f"Settings saved successfully. Owner: {owner_name}")
        return True
        
    except Exception as e:
        log_error(f"Error saving settings: {e}")
        return False

def get_setting(key, default=None):
    """Get a specific setting"""
    settings = load_settings()
    return settings.get(key, default)

def update_setting(key, value):
    """Update a specific setting"""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)

def update_owner_name(name):
    """Update owner's name"""
    return update_setting("owner_name", name)

def get_owner_name():
    """Get owner's name"""
    return get_setting("owner_name", "Sir")

# Load settings on module import
_settings = load_settings()
