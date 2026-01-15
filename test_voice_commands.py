"""
Test Voice Command Execution
Tests the enhanced voice command processing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from python_backend.ai_engine import process_command, execute_direct_action
from python_backend.system_control import handle_system_command, open_application, close_application

def test_command_processing():
    """Test various voice commands"""
    
    print("=" * 60)
    print("VEDA AI - Voice Command Testing")
    print("=" * 60)
    
    test_commands = [
        # Hindi/Hinglish commands
        ("chrome kholo", "Open Chrome"),
        ("calculator chalu karo", "Start Calculator"),
        ("notepad band karo", "Close Notepad"),
        ("volume badhao", "Increase Volume"),
        
        # English commands
        ("open firefox", "Open Firefox"),
        ("start calculator", "Start Calculator"),
        ("close chrome", "Close Chrome"),
        ("volume up", "Volume Up"),
        
        # System commands
        ("downloads kholo", "Open Downloads"),
        ("screenshot lo", "Take Screenshot"),
        ("task manager kholo", "Open Task Manager"),
    ]
    
    print("\n🧪 Testing Command Processing:\n")
    
    for command, description in test_commands:
        print(f"📝 Test: {description}")
        print(f"   Command: '{command}'")
        
        try:
            # Test system control first
            result = handle_system_command(command)
            
            if result:
                print(f"   ✅ System Control: {result[:50]}...")
            else:
                # Test direct action
                result = execute_direct_action(command)
                if result:
                    print(f"   ✅ Direct Action: {result[:50]}...")
                else:
                    print(f"   ⚠️  No handler found (will use AI)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 60)
    print("✅ Testing Complete!")
    print("=" * 60)
    print("\n📚 For full command list, see: VOICE_COMMANDS_GUIDE.md")
    print("🚀 To run VEDA AI: python run_veda_ai.py")

if __name__ == "__main__":
    test_command_processing()
