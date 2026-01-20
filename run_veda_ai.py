import subprocess
import threading
import webbrowser
import time
import sys
import os
import requests
import socket

# Fix encoding for Windows console (emoji support)
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass  # Older Python versions

def safe_print(text):
    """Print with fallback for encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remove emojis and try again
        import re
        clean_text = re.sub(r'[^\x00-\x7F]+', '', text)
        print(clean_text)

def start_wake():
    """Start wake word detection in background"""
    try:
        # Add project root to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from python_backend.wake_word import start_wake_word
        start_wake_word()
    except Exception as e:
        safe_print(f"Wake word detection failed: {e}")

def start_backend():
    """Start FastAPI backend server"""
    # Avoid starting a second server if port is already in use
    if is_port_in_use("127.0.0.1", 8000):
        safe_print("[i] Port 8000 is already in use. Skipping backend start.")
        return

    # NOTE: --reload spawns an extra reloader process and can cause port conflicts on Windows.
    # Keep it off by default; you can enable with VEDA_DEV_RELOAD=true.
    args = [
        sys.executable,
        "-m", "uvicorn",
        "python_backend.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
    ]
    if os.getenv("VEDA_DEV_RELOAD", "false").lower() == "true":
        args.append("--reload")

    try:
        subprocess.Popen(args)
    except OSError as e:
        # WinError 10048/10013: port in use / forbidden
        safe_print(f"[!] Backend start failed: {e}")
        safe_print("[i] If you already have VEDA running, just open: http://localhost:8000")
        return


def is_port_in_use(host: str, port: int) -> bool:
    """Return True if host:port is already bound/listening."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex((host, port)) == 0
    except Exception:
        # If we can't determine, assume not in use to avoid breaking startup
        return False

def wait_for_server():
    """Wait for server to be fully ready"""
    max_attempts = 60  # Increased timeout: 60 attempts × 1 second = 60 seconds
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                safe_print("[OK] Server is ready!")
                return True
        except requests.exceptions.ConnectionError:
            # Server not yet accepting connections - this is expected during startup
            pass
        except requests.exceptions.Timeout:
            # Server is responding but slow - keep waiting
            pass
        except Exception:
            # Other errors - log but continue waiting
            pass
        
        # Show progress every 5 seconds
        if (i + 1) % 5 == 0:
            safe_print(f"[...] Still waiting for server... ({i + 1}s)")
        time.sleep(1)
    return False

def open_ui():
    """Open UI in browser after server is ready"""
    safe_print("[...] Waiting for server to be ready (this may take up to 60 seconds)...")
    
    if not wait_for_server():
        safe_print("[!] Server took longer than expected to start.")
        safe_print("[i] The server might still be initializing. Try opening: http://localhost:8000")
        safe_print("[?] If it doesn't work, check the console for errors above.")
        return
    
    safe_print("[>] Opening VEDA AI in browser...")
    
    # Try multiple methods to open browser
    browser_opened = False
    
    # Method 1: Windows start command (most reliable on Windows)
    try:
        os.system("start http://localhost:8000")
        safe_print("[OK] Browser opened using Windows command!")
        browser_opened = True
    except Exception as e:
        safe_print(f"[!] Windows start failed: {e}")
    
    # Method 2: Python webbrowser module
    if not browser_opened:
        try:
            webbrowser.open("http://localhost:8000", new=2)  # new=2 opens in new tab
            safe_print("[OK] Browser opened using webbrowser module!")
            browser_opened = True
        except Exception as e:
            safe_print(f"[!] Webbrowser module failed: {e}")
    
    # Method 3: Direct browser executable
    if not browser_opened:
        try:
            # Try Chrome first
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    subprocess.Popen([chrome_path, "http://localhost:8000"])
                    safe_print("[OK] Browser opened using Chrome!")
                    browser_opened = True
                    break
        except Exception as e:
            safe_print(f"[!] Direct Chrome launch failed: {e}")
    
    if not browser_opened:
        safe_print("[!] Could not automatically open browser")
        safe_print("[i] Please manually open: http://localhost:8000")

if __name__ == "__main__":
    safe_print("=" * 50)
    safe_print("VEDA AI - Starting...")
    safe_print("=" * 50)
    safe_print("[...] Please wait while the server initializes...")
    
    # Start backend server (only if port is free)
    threading.Thread(target=start_backend, daemon=True).start()
    
    # Start wake word detection (optional)
    threading.Thread(target=start_wake, daemon=True).start()
    
    # Open UI
    open_ui()
    
    safe_print("=" * 50)
    safe_print("[OK] VEDA AI is running!")
    safe_print("[>] Browser should open automatically at http://localhost:8000")
    safe_print("[i] If browser doesn't open, manually visit: http://localhost:8000")
    safe_print("[X] Press Ctrl+C to stop")
    safe_print("=" * 50)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        safe_print("\n[...] Shutting down VEDA AI...")