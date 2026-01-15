"""Quick test for system commands"""
import sys
sys.path.insert(0, '.')

from python_backend.system_control import handle_system_command

print("\n🧪 Testing System Commands\n")
print("=" * 60)

# Test commands
commands = [
    "open notepad",
    "notepad kholo",
    "open calculator",
    "open youtube",
]

for cmd in commands:
    print(f"\n📝 Testing: '{cmd}'")
    result = handle_system_command(cmd)
    if result:
        print(f"✅ Result: {result}")
    else:
        print(f"❌ No match found")
    print("-" * 60)

print("\n✅ Test complete!")
