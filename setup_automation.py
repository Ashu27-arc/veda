"""
VEDA AI - Automation Setup Script
Automatically sets up automation features with default configuration
"""
import json
import os
import sys

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Created directory: {path}")
    else:
        print(f"ℹ️  Directory already exists: {path}")

def create_file(path, content):
    """Create file with content if it doesn't exist"""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            if isinstance(content, dict) or isinstance(content, list):
                json.dump(content, f, indent=2, ensure_ascii=False)
            else:
                f.write(content)
        print(f"✅ Created file: {path}")
    else:
        print(f"ℹ️  File already exists: {path}")

def setup_automation():
    """Setup automation system"""
    print("🤖 VEDA AI - Automation Setup")
    print("=" * 50)
    
    # Create data directory
    create_directory("data")
    
    # Create automation config
    automation_config = {
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
    create_file("data/automation_config.json", automation_config)
    
    # Create context data
    context_data = {
        "app_usage": {},
        "command_frequency": {},
        "time_patterns": {},
        "location_context": {}
    }
    create_file("data/context_data.json", context_data)
    
    # Create user patterns
    user_patterns = {
        "daily_routine": [],
        "frequent_tasks": [],
        "preferences": {},
        "shortcuts": {}
    }
    create_file("data/user_patterns.json", user_patterns)
    
    # Create task queue
    create_file("data/task_queue.json", [])
    
    # Create scheduled tasks
    create_file("data/scheduled_tasks.json", [])
    
    # Create learning data if not exists
    if not os.path.exists("data/learning_data.json"):
        create_file("data/learning_data.json", [])
    
    # Create conversation history if not exists
    if not os.path.exists("data/conversation_history.json"):
        create_file("data/conversation_history.json", [])
    
    print("\n" + "=" * 50)
    print("✅ Automation setup complete!")
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run VEDA AI: python run_veda_ai.py")
    print("3. Open browser: http://localhost:8000")
    print("4. Click '⚙️ AUTO' button to configure automation")
    print("\n📖 Read AUTOMATION_GUIDE.md for detailed instructions")
    print("=" * 50)

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'schedule',
        'psutil',
        'pyttsx3',
        'speechrecognition'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def main():
    """Main setup function"""
    try:
        setup_automation()
        check_dependencies()
        
        print("\n🎉 Setup successful! VEDA AI is ready with automation features.")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
