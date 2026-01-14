import subprocess
import threading
import webbrowser
import time
import sys

def start_wake():
    """Start wake word detection in background"""
    try:
        import sys
        import os
        # Add project root to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from python_backend.wake_word import start_wake_word
        start_wake_word()
    except Exception as e:
        print(f"Wake word detection failed: {e}")

def start_backend():
    """Start FastAPI backend server"""
    subprocess.Popen([
        sys.executable,
        "-m", "uvicorn",
        "python_backend.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ])

def open_ui():
    """Open UI in browser after delay"""
    time.sleep(3)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    # Start backend server
    threading.Thread(target=start_backend, daemon=True).start()
    
    # Start wake word detection (optional)
    threading.Thread(target=start_wake, daemon=True).start()
    
    # Open UI
    open_ui()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down VEDA AI...")