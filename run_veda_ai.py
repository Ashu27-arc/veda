import subprocess
import threading
import webbrowser
import time
import sys
import requests

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

def wait_for_server():
    """Wait for server to be fully ready"""
    import requests
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def open_ui():
    """Open UI in browser after server is ready"""
    print("⏳ Waiting for server to be ready...")
    
    if not wait_for_server():
        print("⚠️ Server took too long to start. Please manually open: http://localhost:8000")
        return
    
    print("🌐 Opening VEDA AI in browser...")
    
    # Try multiple methods to open browser
    browser_opened = False
    
    # Method 1: Windows start command (most reliable on Windows)
    try:
        import os
        os.system("start http://localhost:8000")
        print("✅ Browser opened using Windows command!")
        browser_opened = True
    except Exception as e:
        print(f"⚠️ Windows start failed: {e}")
    
    # Method 2: Python webbrowser module
    if not browser_opened:
        try:
            webbrowser.open("http://localhost:8000", new=2)  # new=2 opens in new tab
            print("✅ Browser opened using webbrowser module!")
            browser_opened = True
        except Exception as e:
            print(f"⚠️ Webbrowser module failed: {e}")
    
    # Method 3: Direct browser executable
    if not browser_opened:
        try:
            import subprocess
            # Try Chrome first
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    subprocess.Popen([chrome_path, "http://localhost:8000"])
                    print("✅ Browser opened using Chrome!")
                    browser_opened = True
                    break
        except Exception as e:
            print(f"⚠️ Direct Chrome launch failed: {e}")
    
    if not browser_opened:
        print("⚠️ Could not automatically open browser")
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