"""
Advanced Automation Engine for VEDA AI
Automatically handles tasks, schedules, and proactive actions
"""
import json
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Callable
import schedule
from python_backend.logger import log_info, log_error, log_warning
from python_backend.ai_engine import process_command

AUTOMATION_CONFIG_FILE = "data/automation_config.json"
TASK_QUEUE_FILE = "data/task_queue.json"

class AutomationEngine:
    """Handles all automation tasks for VEDA AI"""
    
    def __init__(self):
        self.running = False
        self.scheduled_tasks = []
        self.task_queue = []
        self.automation_thread = None
        self.ensure_data_files()
        self.load_automation_config()
        
    def ensure_data_files(self):
        """Create automation data files if they don't exist"""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(AUTOMATION_CONFIG_FILE):
            default_config = {
                "enabled": True,
                "proactive_mode": True,
                "auto_tasks": {
                    "morning_briefing": {
                        "enabled": True,
                        "time": "08:00",
                        "actions": ["weather", "news", "calendar"]
                    },
                    "system_health_check": {
                        "enabled": True,
                        "interval": "1h",
                        "actions": ["check_disk", "check_memory", "check_updates"]
                    },
                    "auto_cleanup": {
                        "enabled": True,
                        "time": "23:00",
                        "actions": ["clear_temp", "organize_downloads"]
                    }
                },
                "smart_suggestions": {
                    "enabled": True,
                    "learn_patterns": True,
                    "suggest_shortcuts": True
                },
                "context_awareness": {
                    "enabled": True,
                    "track_usage": True,
                    "predict_needs": True
                }
            }
            with open(AUTOMATION_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
        
        if not os.path.exists(TASK_QUEUE_FILE):
            with open(TASK_QUEUE_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def load_automation_config(self):
        """Load automation configuration"""
        try:
            with open(AUTOMATION_CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            log_info("Automation config loaded")
        except Exception as e:
            log_error(f"Error loading automation config: {e}")
            self.config = {"enabled": False}
    
    def save_automation_config(self):
        """Save automation configuration"""
        try:
            with open(AUTOMATION_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            log_info("Automation config saved")
        except Exception as e:
            log_error(f"Error saving automation config: {e}")
    
    def add_scheduled_task(self, name: str, time_str: str, action: Callable, repeat: str = "daily"):
        """
        Add a scheduled task
        
        Args:
            name: Task name
            time_str: Time in HH:MM format
            action: Function to execute
            repeat: 'daily', 'hourly', 'weekly'
        """
        try:
            if repeat == "daily":
                schedule.every().day.at(time_str).do(action).tag(name)
            elif repeat == "hourly":
                schedule.every().hour.do(action).tag(name)
            elif repeat == "weekly":
                schedule.every().week.do(action).tag(name)
            
            self.scheduled_tasks.append({
                "name": name,
                "time": time_str,
                "repeat": repeat,
                "next_run": schedule.get_jobs(name)[0].next_run if schedule.get_jobs(name) else None
            })
            
            log_info(f"Scheduled task added: {name} at {time_str} ({repeat})")
        except Exception as e:
            log_error(f"Error adding scheduled task: {e}")
    
    def add_to_queue(self, task: Dict):
        """Add task to execution queue"""
        try:
            self.task_queue.append({
                **task,
                "added_at": datetime.now().isoformat(),
                "status": "pending"
            })
            self.save_task_queue()
            log_info(f"Task added to queue: {task.get('name', 'unnamed')}")
        except Exception as e:
            log_error(f"Error adding task to queue: {e}")
    
    def save_task_queue(self):
        """Save task queue to file"""
        try:
            with open(TASK_QUEUE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.task_queue, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Error saving task queue: {e}")
    
    def load_task_queue(self):
        """Load task queue from file"""
        try:
            with open(TASK_QUEUE_FILE, 'r', encoding='utf-8') as f:
                self.task_queue = json.load(f)
        except Exception as e:
            log_error(f"Error loading task queue: {e}")
            self.task_queue = []
    
    def execute_task(self, task: Dict):
        """Execute a single task"""
        try:
            task_type = task.get("type")
            task_data = task.get("data", {})
            
            log_info(f"Executing task: {task.get('name')} (type: {task_type})")
            
            if task_type == "command":
                # Execute AI command
                command = task_data.get("command")
                result = process_command(command, auto_speak=False)
                task["result"] = result
                task["status"] = "completed"
                
            elif task_type == "system":
                # Execute system action
                action = task_data.get("action")
                self.execute_system_action(action)
                task["status"] = "completed"
                
            elif task_type == "scheduled":
                # Execute scheduled action
                actions = task_data.get("actions", [])
                for action in actions:
                    self.execute_automated_action(action)
                task["status"] = "completed"
            
            task["completed_at"] = datetime.now().isoformat()
            log_info(f"Task completed: {task.get('name')}")
            
        except Exception as e:
            log_error(f"Error executing task: {e}")
            task["status"] = "failed"
            task["error"] = str(e)
    
    def execute_system_action(self, action: str):
        """Execute system-level actions"""
        try:
            if action == "check_disk":
                import psutil
                disk = psutil.disk_usage('/')
                log_info(f"Disk usage: {disk.percent}%")
                
            elif action == "check_memory":
                import psutil
                memory = psutil.virtual_memory()
                log_info(f"Memory usage: {memory.percent}%")
                
            elif action == "check_updates":
                log_info("Checking for system updates...")
                
            elif action == "clear_temp":
                log_info("Clearing temporary files...")
                
            elif action == "organize_downloads":
                log_info("Organizing downloads folder...")
                
        except Exception as e:
            log_error(f"Error executing system action {action}: {e}")
    
    def execute_automated_action(self, action: str):
        """Execute automated actions"""
        try:
            if action == "weather":
                process_command("what's the weather", auto_speak=False)
            elif action == "news":
                process_command("latest news", auto_speak=False)
            elif action == "calendar":
                process_command("show my calendar", auto_speak=False)
        except Exception as e:
            log_error(f"Error executing automated action {action}: {e}")
    
    def process_queue(self):
        """Process all pending tasks in queue"""
        self.load_task_queue()
        
        pending_tasks = [t for t in self.task_queue if t.get("status") == "pending"]
        
        for task in pending_tasks:
            self.execute_task(task)
        
        self.save_task_queue()
    
    def setup_default_schedules(self):
        """Setup default scheduled tasks"""
        if not self.config.get("enabled"):
            return
        
        auto_tasks = self.config.get("auto_tasks", {})
        
        # Morning briefing
        if auto_tasks.get("morning_briefing", {}).get("enabled"):
            time_str = auto_tasks["morning_briefing"].get("time", "08:00")
            self.add_scheduled_task(
                "morning_briefing",
                time_str,
                lambda: self.add_to_queue({
                    "name": "Morning Briefing",
                    "type": "scheduled",
                    "data": {"actions": auto_tasks["morning_briefing"].get("actions", [])}
                })
            )
        
        # System health check
        if auto_tasks.get("system_health_check", {}).get("enabled"):
            self.add_scheduled_task(
                "system_health_check",
                "09:00",
                lambda: self.add_to_queue({
                    "name": "System Health Check",
                    "type": "scheduled",
                    "data": {"actions": auto_tasks["system_health_check"].get("actions", [])}
                }),
                repeat="hourly"
            )
        
        # Auto cleanup
        if auto_tasks.get("auto_cleanup", {}).get("enabled"):
            time_str = auto_tasks["auto_cleanup"].get("time", "23:00")
            self.add_scheduled_task(
                "auto_cleanup",
                time_str,
                lambda: self.add_to_queue({
                    "name": "Auto Cleanup",
                    "type": "scheduled",
                    "data": {"actions": auto_tasks["auto_cleanup"].get("actions", [])}
                })
            )
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        log_info("Automation scheduler started")
        
        while self.running:
            try:
                schedule.run_pending()
                self.process_queue()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                log_error(f"Scheduler error: {e}")
                time.sleep(60)
    
    def start(self):
        """Start the automation engine"""
        if self.running:
            log_warning("Automation engine already running")
            return
        
        if not self.config.get("enabled"):
            log_info("Automation engine disabled in config")
            return
        
        self.running = True
        self.setup_default_schedules()
        
        self.automation_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.automation_thread.start()
        
        log_info("Automation engine started successfully")
    
    def stop(self):
        """Stop the automation engine"""
        self.running = False
        schedule.clear()
        log_info("Automation engine stopped")
    
    def get_status(self):
        """Get automation engine status"""
        return {
            "running": self.running,
            "enabled": self.config.get("enabled", False),
            "scheduled_tasks": len(self.scheduled_tasks),
            "pending_tasks": len([t for t in self.task_queue if t.get("status") == "pending"]),
            "completed_tasks": len([t for t in self.task_queue if t.get("status") == "completed"]),
            "next_tasks": self.scheduled_tasks[:5]
        }

# Global automation engine instance
_automation_engine = None

def get_automation_engine():
    """Get or create automation engine instance"""
    global _automation_engine
    if _automation_engine is None:
        _automation_engine = AutomationEngine()
    return _automation_engine

def start_automation():
    """Start automation engine"""
    engine = get_automation_engine()
    engine.start()

def stop_automation():
    """Stop automation engine"""
    engine = get_automation_engine()
    engine.stop()

def get_automation_status():
    """Get automation status"""
    engine = get_automation_engine()
    return engine.get_status()
