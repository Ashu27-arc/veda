import subprocess
import threading
import webbrowser
import time
import sys
import os
import requests
import socket

def safe_print(msg):
    try:
        print(msg)
    except:
        print(msg.encode("ascii", "ignore").decode())

def is_port_open(host="127.0.0.1", port=8000):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except:
        return False

def start_backend():
    if is_port_open():
        safe_print("[i] Backend already running")
        return

    args = [
        sys.executable,
        "-m", "uvicorn",
        "python_backend.main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]
    subprocess.Popen(args)

def wait_for_server():
    for _ in range(30):
        try:
            r = requests.get("http://127.0.0.1:8000/health", timeout=1)
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def open_browser():
    url = "http://127.0.0.1:8000"
    try:
        webbrowser.open(url)
    except:
        pass

def start_gesture():
    try:
        from python_backend.gesture_control import start_gesture_control
        start_gesture_control()
    except Exception as e:
        safe_print(f"Gesture error: {e}")

if __name__ == "__main__":
    safe_print("=================================")
    safe_print("VEDA AI - LOCAL MODE")
    safe_print("=================================")

    threading.Thread(target=start_backend, daemon=True).start()
    threading.Thread(target=start_gesture, daemon=True).start()

    if wait_for_server():
        open_browser()
        safe_print("[OK] VEDA AI running at http://localhost:8000")
    else:
        safe_print("[!] Server startup timeout")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        safe_print("Shutting down VEDA AI...")
