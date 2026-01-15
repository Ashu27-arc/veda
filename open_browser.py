"""
Simple script to open VEDA AI in browser
"""
import webbrowser
import os
import subprocess
import time

def check_server():
    """Check if server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def open_browser():
    """Open browser with multiple fallback methods"""
    url = "http://localhost:8000"
    
    print("🔍 Checking if VEDA AI server is running...")
    if not check_server():
        print("❌ Server is not running!")
        print("📝 Please start VEDA AI first using: start_veda.bat")
        input("\nPress Enter to exit...")
        return
    
    print("✅ Server is running!")
    print("🌐 Opening browser...\n")
    
    browser_opened = False
    
    # Method 1: Windows start command (most reliable)
    try:
        os.system(f"start {url}")
        print("✅ Browser opened successfully!")
        browser_opened = True
    except Exception as e:
        print(f"⚠️ Method 1 failed: {e}")
    
    # Method 2: Python webbrowser
    if not browser_opened:
        try:
            webbrowser.open(url, new=2)
            print("✅ Browser opened successfully!")
            browser_opened = True
        except Exception as e:
            print(f"⚠️ Method 2 failed: {e}")
    
    # Method 3: Direct Chrome
    if not browser_opened:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                try:
                    subprocess.Popen([chrome_path, url])
                    print("✅ Browser opened successfully!")
                    browser_opened = True
                    break
                except Exception as e:
                    print(f"⚠️ Chrome launch failed: {e}")
    
    if not browser_opened:
        print("❌ Could not automatically open browser")
        print(f"📝 Please manually open: {url}")
    
    time.sleep(2)

if __name__ == "__main__":
    open_browser()
