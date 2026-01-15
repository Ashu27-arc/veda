"""
Task Scheduler - Schedule and manage automated tasks
Supports one-time, recurring, and conditional tasks
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from python_backend.logger import log_info, log_error

SCHEDULED_TASKS_FILE = "data/scheduled_tasks.json"

class TaskScheduler:
    """Manages scheduled tasks"""
    
    def __init__(self):
        self.tasks = []
        self.ensure_data_file()
        self.load_tasks()
    
    def ensure_data_file(self):
        """Create scheduled tasks file"""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(SCHEDULED_TASKS_FILE):
            with open(SCHEDULED_TASKS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def load_tasks(self):
        """Load scheduled tasks"""
        try:
            with open(SCHEDULED_TASKS_FILE, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
            log_info(f"Loaded {len(self.tasks)} scheduled tasks")
        except Exception as e:
            log_error(f"Error loading scheduled tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save scheduled tasks"""
        try:
            with open(SCHEDULED_TASKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            log_info("Scheduled tasks saved")
        except Exception as e:
            log_error(f"Error saving scheduled tasks: {e}")
    
    def add_task(self, name: str, command: str, schedule_type: str, 
                 schedule_value: str, enabled: bool = True, 
                 conditions: Optional[Dict] = None):
        """
        Add a new scheduled task
        
        Args:
            name: Task name
            command: Command to execute
            schedule_type: 'once', 'daily', 'weekly', 'interval', 'conditional'
            schedule_value: Time/interval value (e.g., '08:00', '1h', 'monday')
            enabled: Whether task is enabled
            conditions: Optional conditions for execution
        """
        task = {
            "id": len(self.tasks) + 1,
            "name": name,
            "command": command,
            "schedule_type": schedule_type,
            "schedule_value": schedule_value,
            "enabled": enabled,
            "conditions": conditions or {},
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self.calculate_next_run(schedule_type, schedule_value),
            "run_count": 0
        }
        
        self.tasks.append(task)
        self.save_tasks()
        log_info(f"Task added: {name}")
        
        return task
    
    def calculate_next_run(self, schedule_type: str, schedule_value: str):
        """Calculate next run time for a task"""
        now = datetime.now()
        
        try:
            if schedule_type == "once":
                # Parse datetime string
                return schedule_value
            
            elif schedule_type == "daily":
                # Parse time (HH:MM)
                hour, minute = map(int, schedule_value.split(':'))
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if next_run <= now:
                    next_run += timedelta(days=1)
                
                return next_run.isoformat()
            
            elif schedule_type == "weekly":
                # Parse day and time
                return schedule_value
            
            elif schedule_type == "interval":
                # Parse interval (e.g., '1h', '30m')
                if schedule_value.endswith('h'):
                    hours = int(schedule_value[:-1])
                    next_run = now + timedelta(hours=hours)
                elif schedule_value.endswith('m'):
                    minutes = int(schedule_value[:-1])
                    next_run = now + timedelta(minutes=minutes)
                else:
                    next_run = now + timedelta(hours=1)
                
                return next_run.isoformat()
            
            elif schedule_type == "conditional":
                # Conditional tasks don't have fixed next run
                return None
        
        except Exception as e:
            log_error(f"Error calculating next run: {e}")
            return None
    
    def get_pending_tasks(self):
        """Get tasks that are due to run"""
        now = datetime.now()
        pending = []
        
        for task in self.tasks:
            if not task.get("enabled"):
                continue
            
            next_run_str = task.get("next_run")
            if not next_run_str:
                continue
            
            try:
                next_run = datetime.fromisoformat(next_run_str)
                if next_run <= now:
                    pending.append(task)
            except Exception as e:
                log_error(f"Error parsing next_run for task {task.get('name')}: {e}")
        
        return pending
    
    def mark_task_executed(self, task_id: int):
        """Mark a task as executed and update next run"""
        for task in self.tasks:
            if task.get("id") == task_id:
                task["last_run"] = datetime.now().isoformat()
                task["run_count"] = task.get("run_count", 0) + 1
                
                # Calculate next run
                if task["schedule_type"] != "once":
                    task["next_run"] = self.calculate_next_run(
                        task["schedule_type"],
                        task["schedule_value"]
                    )
                else:
                    # One-time task, disable it
                    task["enabled"] = False
                
                self.save_tasks()
                log_info(f"Task executed: {task['name']}")
                break
    
    def enable_task(self, task_id: int):
        """Enable a task"""
        for task in self.tasks:
            if task.get("id") == task_id:
                task["enabled"] = True
                self.save_tasks()
                log_info(f"Task enabled: {task['name']}")
                break
    
    def disable_task(self, task_id: int):
        """Disable a task"""
        for task in self.tasks:
            if task.get("id") == task_id:
                task["enabled"] = False
                self.save_tasks()
                log_info(f"Task disabled: {task['name']}")
                break
    
    def delete_task(self, task_id: int):
        """Delete a task"""
        self.tasks = [t for t in self.tasks if t.get("id") != task_id]
        self.save_tasks()
        log_info(f"Task deleted: {task_id}")
    
    def get_all_tasks(self):
        """Get all tasks"""
        return self.tasks
    
    def get_task_by_id(self, task_id: int):
        """Get a specific task"""
        for task in self.tasks:
            if task.get("id") == task_id:
                return task
        return None

# Global instance
_task_scheduler = None

def get_task_scheduler():
    """Get or create task scheduler instance"""
    global _task_scheduler
    if _task_scheduler is None:
        _task_scheduler = TaskScheduler()
    return _task_scheduler
