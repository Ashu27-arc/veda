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
    time.sleep(5)  # Increased delay to ensure server is fully ready
    print("🌐 Opening VEDA AI in browser...")
    
    # Try multiple methods to open browser
    try:
        # Method 1: Default browser
        webbrowser.open("http://localhost:8000")
    except Exception as e:
        print(f"⚠️ Default browser failed: {e}")
        try:
            # Method 2: Windows specific
            import os
            os.system("start http://localhost:8000")
        except Exception as e2:
            print(f"⚠️ Windows start failed: {e2}")
            print("📝 Please manually open: http://localhost:8000")

if __name__ == "__main__":
    print("🚀 Starting VEDA AI...")
    print("⏳ Please wait while the server initializes...")
    
    # Start backend server
    threading.Thread(target=start_backend, daemon=True).start()
    
    # Start wake word detection (optional)
    threading.Thread(target=start_wake, daemon=True).start()
    
    # Open UI
    open_ui()
    
    print("✅ VEDA AI is running!")
    print("🌐 Browser should open automatically at http://localhost:8000")
    print("📝 If browser doesn't open, manually visit: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down VEDA AI...")