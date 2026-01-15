"""
Proactive Assistant - VEDA AI takes initiative and suggests actions
Monitors system, predicts needs, and provides intelligent suggestions
"""
import psutil
import os
from datetime import datetime
from python_backend.logger import log_info, log_error
from python_backend.context_awareness import get_context_awareness
from python_backend.jarvis_personality import get_jarvis

class ProactiveAssistant:
    """Proactively monitors and suggests actions"""
    
    def __init__(self):
        self.context = get_context_awareness()
        self.jarvis = get_jarvis()
        self.last_suggestions = []
    
    def check_system_health(self):
        """Check system health and provide warnings"""
        suggestions = []
        
        try:
            # Check disk space
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                suggestions.append({
                    "type": "warning",
                    "priority": "high",
                    "message": f"{self.jarvis.owner_name}, disk space is critically low ({disk.percent}%). Consider cleaning up files.",
                    "action": "cleanup_disk"
                })
            elif disk.percent > 80:
                suggestions.append({
                    "type": "info",
                    "priority": "medium",
                    "message": f"Disk space is getting low ({disk.percent}%). You might want to free up some space.",
                    "action": "cleanup_disk"
                })
            
            # Check memory
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                suggestions.append({
                    "type": "warning",
                    "priority": "high",
                    "message": f"Memory usage is very high ({memory.percent}%). Consider closing some applications.",
                    "action": "close_apps"
                })
            
            # Check CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                suggestions.append({
                    "type": "warning",
                    "priority": "medium",
                    "message": f"CPU usage is high ({cpu_percent}%). System might be slow.",
                    "action": "check_processes"
                })
            
            # Check battery (if laptop)
            battery = psutil.sensors_battery()
            if battery:
                if battery.percent < 20 and not battery.power_plugged:
                    suggestions.append({
                        "type": "warning",
                        "priority": "high",
                        "message": f"Battery is low ({battery.percent}%). Please connect charger.",
                        "action": "battery_saver"
                    })
            
        except Exception as e:
            log_error(f"Error checking system health: {e}")
        
        return suggestions
    
    def suggest_based_on_time(self):
        """Suggest actions based on time of day"""
        suggestions = []
        context = self.context.get_current_context()
        time_of_day = context["time_of_day"]
        hour = context["hour"]
        
        # Morning suggestions (5 AM - 12 PM)
        if time_of_day == "morning":
            if hour == 8:
                suggestions.append({
                    "type": "suggestion",
                    "priority": "low",
                    "message": f"Good morning, {self.jarvis.owner_name}! Would you like to check today's weather?",
                    "action": "weather"
                })
            
            if hour == 9:
                suggestions.append({
                    "type": "suggestion",
                    "priority": "low",
                    "message": "Time to start your day! Need help opening your work applications?",
                    "action": "open_work_apps"
                })
        
        # Afternoon suggestions (12 PM - 5 PM)
        elif time_of_day == "afternoon":
            if hour == 14:
                suggestions.append({
                    "type": "suggestion",
                    "priority": "low",
                    "message": "It's been a while. Consider taking a short break, Sir.",
                    "action": "break_reminder"
                })
        
        # Evening suggestions (5 PM - 9 PM)
        elif time_of_day == "evening":
            if hour == 18:
                suggestions.append({
                    "type": "suggestion",
                    "priority": "low",
                    "message": "Evening, Sir. Would you like a summary of today's activities?",
                    "action": "daily_summary"
                })
        
        # Night suggestions (9 PM - 5 AM)
        elif time_of_day == "night":
            if hour == 23:
                suggestions.append({
                    "type": "suggestion",
                    "priority": "low",
                    "message": "It's getting late. Should I prepare the system for shutdown?",
                    "action": "prepare_shutdown"
                })
        
        return suggestions
    
    def suggest_based_on_patterns(self):
        """Suggest actions based on learned patterns"""
        suggestions = []
        
        try:
            # Get predicted next action
            prediction = self.context.predict_next_action()
            likely_apps = prediction.get("likely_apps", [])
            
            if likely_apps:
                top_app = likely_apps[0]
                suggestions.append({
                    "type": "suggestion",
                    "priority": "low",
                    "message": f"You usually open {top_app['app']} around this time. Would you like me to open it?",
                    "action": f"open_{top_app['app']}"
                })
            
            # Get frequent tasks
            frequent_tasks = self.context.get_frequent_tasks(limit=5)
            if frequent_tasks:
                # Suggest creating shortcuts for frequent tasks
                for task in frequent_tasks:
                    if task["count"] > 10:  # Used more than 10 times
                        suggestions.append({
                            "type": "suggestion",
                            "priority": "low",
                            "message": f"You use '{task['command']}' frequently. Would you like to create a shortcut?",
                            "action": f"create_shortcut_{task['command']}"
                        })
        
        except Exception as e:
            log_error(f"Error suggesting based on patterns: {e}")
        
        return suggestions
    
    def suggest_optimizations(self):
        """Suggest system optimizations"""
        suggestions = []
        
        try:
            # Check for unused applications
            # Check for duplicate files
            # Check for outdated software
            
            # Placeholder suggestions
            suggestions.append({
                "type": "optimization",
                "priority": "low",
                "message": "I can help optimize your system. Would you like me to run a cleanup?",
                "action": "system_optimization"
            })
        
        except Exception as e:
            log_error(f"Error suggesting optimizations: {e}")
        
        return suggestions
    
    def get_all_suggestions(self):
        """Get all current suggestions"""
        all_suggestions = []
        
        # System health suggestions (high priority)
        all_suggestions.extend(self.check_system_health())
        
        # Time-based suggestions
        all_suggestions.extend(self.suggest_based_on_time())
        
        # Pattern-based suggestions
        all_suggestions.extend(self.suggest_based_on_patterns())
        
        # Optimization suggestions
        all_suggestions.extend(self.suggest_optimizations())
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_suggestions.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 2))
        
        # Store for reference
        self.last_suggestions = all_suggestions
        
        return all_suggestions
    
    def execute_suggestion_action(self, action: str):
        """Execute a suggested action"""
        try:
            from python_backend.ai_engine import process_command
            
            if action == "weather":
                return process_command("what's the weather today", auto_speak=False)
            
            elif action == "cleanup_disk":
                return process_command("clean up disk space", auto_speak=False)
            
            elif action == "close_apps":
                return "Please close unnecessary applications to free up memory."
            
            elif action == "battery_saver":
                return process_command("enable battery saver mode", auto_speak=False)
            
            elif action == "open_work_apps":
                return "Opening your usual work applications..."
            
            elif action == "daily_summary":
                return self.generate_daily_summary()
            
            elif action == "system_optimization":
                return "Running system optimization..."
            
            else:
                return f"Action '{action}' not implemented yet."
        
        except Exception as e:
            log_error(f"Error executing suggestion action: {e}")
            return f"Error executing action: {e}"
    
    def generate_daily_summary(self):
        """Generate a summary of today's activities"""
        try:
            # Get today's stats
            stats = self.context.get_frequent_tasks(limit=5)
            
            summary = f"Here's your daily summary, {self.jarvis.owner_name}:\n\n"
            summary += f"You executed {len(stats)} different commands today.\n"
            
            if stats:
                summary += "\nMost frequent tasks:\n"
                for i, task in enumerate(stats[:3], 1):
                    summary += f"{i}. {task['command']} ({task['count']} times)\n"
            
            return summary
        
        except Exception as e:
            log_error(f"Error generating daily summary: {e}")
            return "Unable to generate daily summary."

# Global instance
_proactive_assistant = None

def get_proactive_assistant():
    """Get or create proactive assistant instance"""
    global _proactive_assistant
    if _proactive_assistant is None:
        _proactive_assistant = ProactiveAssistant()
    return _proactive_assistant
