"""
Context Awareness System - VEDA AI understands user patterns and context
Tracks usage, predicts needs, and provides proactive suggestions
"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from python_backend.logger import log_info, log_error

CONTEXT_DATA_FILE = "data/context_data.json"
USER_PATTERNS_FILE = "data/user_patterns.json"

class ContextAwareness:
    """Tracks and analyzes user behavior patterns"""
    
    def __init__(self):
        self.context_data = {}
        self.user_patterns = {}
        self.ensure_data_files()
        self.load_context_data()
    
    def ensure_data_files(self):
        """Create context data files"""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(CONTEXT_DATA_FILE):
            with open(CONTEXT_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    "app_usage": {},
                    "command_frequency": {},
                    "time_patterns": {},
                    "location_context": {}
                }, f, indent=2)
        
        if not os.path.exists(USER_PATTERNS_FILE):
            with open(USER_PATTERNS_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    "daily_routine": [],
                    "frequent_tasks": [],
                    "preferences": {},
                    "shortcuts": {}
                }, f, indent=2)
    
    def load_context_data(self):
        """Load context data"""
        try:
            with open(CONTEXT_DATA_FILE, 'r', encoding='utf-8') as f:
                self.context_data = json.load(f)
            
            with open(USER_PATTERNS_FILE, 'r', encoding='utf-8') as f:
                self.user_patterns = json.load(f)
            
            log_info("Context data loaded")
        except Exception as e:
            log_error(f"Error loading context data: {e}")
    
    def save_context_data(self):
        """Save context data"""
        try:
            with open(CONTEXT_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.context_data, f, indent=2, ensure_ascii=False)
            
            with open(USER_PATTERNS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_patterns, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Error saving context data: {e}")
    
    def track_app_usage(self, app_name: str):
        """Track application usage"""
        app_usage = self.context_data.get("app_usage", {})
        
        if app_name not in app_usage:
            app_usage[app_name] = {
                "count": 0,
                "last_used": None,
                "usage_times": []
            }
        
        app_usage[app_name]["count"] += 1
        app_usage[app_name]["last_used"] = datetime.now().isoformat()
        app_usage[app_name]["usage_times"].append(datetime.now().hour)
        
        self.context_data["app_usage"] = app_usage
        self.save_context_data()
    
    def track_command(self, command: str):
        """Track command frequency"""
        cmd_freq = self.context_data.get("command_frequency", {})
        
        cmd_lower = command.lower()
        if cmd_lower not in cmd_freq:
            cmd_freq[cmd_lower] = {
                "count": 0,
                "last_used": None
            }
        
        cmd_freq[cmd_lower]["count"] += 1
        cmd_freq[cmd_lower]["last_used"] = datetime.now().isoformat()
        
        self.context_data["command_frequency"] = cmd_freq
        self.save_context_data()
    
    def get_current_context(self):
        """Get current context information"""
        now = datetime.now()
        hour = now.hour
        
        # Determine time of day
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        return {
            "time_of_day": time_of_day,
            "hour": hour,
            "day_of_week": now.strftime("%A"),
            "date": now.strftime("%Y-%m-%d")
        }
    
    def predict_next_action(self):
        """Predict what user might want to do next"""
        context = self.get_current_context()
        hour = context["hour"]
        
        # Get apps used at this time
        app_usage = self.context_data.get("app_usage", {})
        likely_apps = []
        
        for app, data in app_usage.items():
            usage_times = data.get("usage_times", [])
            if hour in usage_times:
                likely_apps.append({
                    "app": app,
                    "frequency": usage_times.count(hour)
                })
        
        # Sort by frequency
        likely_apps.sort(key=lambda x: x["frequency"], reverse=True)
        
        return {
            "context": context,
            "likely_apps": likely_apps[:3],
            "suggestions": self.generate_suggestions(context)
        }
    
    def generate_suggestions(self, context):
        """Generate proactive suggestions based on context"""
        suggestions = []
        hour = context["hour"]
        time_of_day = context["time_of_day"]
        
        # Morning suggestions
        if time_of_day == "morning":
            suggestions.extend([
                "Check weather for today",
                "Review your calendar",
                "Check emails"
            ])
        
        # Afternoon suggestions
        elif time_of_day == "afternoon":
            suggestions.extend([
                "Take a break reminder",
                "Check pending tasks"
            ])
        
        # Evening suggestions
        elif time_of_day == "evening":
            suggestions.extend([
                "Review today's accomplishments",
                "Plan for tomorrow"
            ])
        
        # Night suggestions
        elif time_of_day == "night":
            suggestions.extend([
                "System cleanup",
                "Backup important files"
            ])
        
        return suggestions
    
    def learn_pattern(self, action: str, context: dict):
        """Learn user patterns"""
        daily_routine = self.user_patterns.get("daily_routine", [])
        
        pattern = {
            "action": action,
            "time": context.get("hour"),
            "day": context.get("day_of_week"),
            "timestamp": datetime.now().isoformat()
        }
        
        daily_routine.append(pattern)
        
        # Keep only last 100 patterns
        if len(daily_routine) > 100:
            daily_routine = daily_routine[-100:]
        
        self.user_patterns["daily_routine"] = daily_routine
        self.save_context_data()
    
    def get_frequent_tasks(self, limit=10):
        """Get most frequent tasks"""
        cmd_freq = self.context_data.get("command_frequency", {})
        
        # Sort by count
        sorted_cmds = sorted(
            cmd_freq.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )
        
        return [
            {
                "command": cmd,
                "count": data["count"],
                "last_used": data["last_used"]
            }
            for cmd, data in sorted_cmds[:limit]
        ]
    
    def create_shortcut(self, name: str, command: str):
        """Create a shortcut for frequent commands"""
        shortcuts = self.user_patterns.get("shortcuts", {})
        shortcuts[name.lower()] = command
        self.user_patterns["shortcuts"] = shortcuts
        self.save_context_data()
        log_info(f"Shortcut created: {name} -> {command}")
    
    def get_shortcut(self, name: str):
        """Get shortcut command"""
        shortcuts = self.user_patterns.get("shortcuts", {})
        return shortcuts.get(name.lower())

# Global instance
_context_awareness = None

def get_context_awareness():
    """Get or create context awareness instance"""
    global _context_awareness
    if _context_awareness is None:
        _context_awareness = ContextAwareness()
    return _context_awareness
