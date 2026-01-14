"""
VEDA AI Speaking Demo
Demonstrates that VEDA speaks for all commands
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from python_backend.ai_engine import process_command
from python_backend.jarvis_personality import set_owner_name

def demo_speaking():
    """Demo VEDA speaking for different commands"""
    
    print("=" * 70)
    print("🔊 VEDA AI - Speaking Demo")
    print("=" * 70)
    print("\n⚠️  WARNING: This will use your speakers/headphones!")
    print("Make sure your volume is at a comfortable level.\n")
    
    input("Press ENTER to start the demo (or Ctrl+C to cancel)...")
    
    # Set owner name
    set_owner_name("Sir")
    
    demos = [
        ("hello", "Greeting"),
        ("what is 2 plus 2", "Simple Query"),
        ("tell me a joke", "AI Query"),
    ]
    
    for i, (command, desc) in enumerate(demos, 1):
        print(f"\n{'=' * 70}")
        print(f"Demo {i}/{len(demos)}: {desc}")
        print(f"{'=' * 70}")
        print(f"Command: '{command}'")
        print("\n🔊 Listen to VEDA speak...")
        print("-" * 70)
        
        # Process with speaking enabled
        response = process_command(command, auto_speak=True)
        
        print(f"\n✅ VEDA spoke the response!")
        print(f"Response text: {response[:100]}...")
        
        if i < len(demos):
            input("\nPress ENTER for next demo...")
    
    print(f"\n{'=' * 70}")
    print("✅ Demo Complete!")
    print(f"{'=' * 70}")
    print("\n🎯 VEDA spoke for ALL commands!")
    print("\n💡 In the full app (python run_veda_ai.py):")
    print("   • VEDA speaks for EVERY command")
    print("   • Acknowledgments for actions")
    print("   • Thinking responses for queries")
    print("   • Natural JARVIS-like conversation")
    print("\n🚀 Start VEDA: python run_veda_ai.py")

if __name__ == "__main__":
    try:
        demo_speaking()
    except KeyboardInterrupt:
        print("\n\n❌ Demo cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Make sure your audio system is working properly")
