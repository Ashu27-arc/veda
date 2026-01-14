import os
import subprocess
import psutil
import pyautogui
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from python_backend.logger import log_info, log_error
from python_backend.jarvis_personality import get_jarvis

# =========================
# VOLUME CONTROL
# =========================
def set_volume(action):
    """Control system volume"""
    try:
        jarvis = get_jarvis()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()

        if action == "up":
            volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
            return f"Volume increased, {jarvis.owner_name}."

        if action == "down":
            volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
            return f"Volume decreased, {jarvis.owner_name}."

        if action == "mute":
            volume.SetMute(1, None)
            return f"Volume muted, {jarvis.owner_name}."
    except Exception as e:
        log_error(f"Volume control error: {e}")
        jarvis = get_jarvis()
        return f"I apologize, {jarvis.owner_name}, but I couldn't control the volume."


# =========================
# MAIN HANDLER
# =========================
def handle_system_command(command):
    """Handle system-level commands with JARVIS personality"""
    try:
        jarvis = get_jarvis()
        
        # ---- APPS & SOFTWARE ----
        if "open chrome" in command or "chrome kholo" in command:
            subprocess.Popen("chrome")
            log_info("Opening Chrome")
            return f"Opening Chrome, {jarvis.owner_name}." if "open" in command else f"Chrome khol raha hoon, {jarvis.owner_name}."

        if "open notepad" in command or "notepad kholo" in command:
            subprocess.Popen("notepad")
            log_info("Opening Notepad")
            return f"Opening Notepad, {jarvis.owner_name}." if "open" in command else f"Notepad khol raha hoon, {jarvis.owner_name}."
        
        if "open youtube" in command or "youtube kholo" in command:
            import webbrowser
            webbrowser.open("https://www.youtube.com")
            log_info("Opening YouTube")
            return f"Opening YouTube, {jarvis.owner_name}." if "open" in command else f"YouTube khol raha hoon, {jarvis.owner_name}."
        
        if "open google" in command or "google kholo" in command:
            import webbrowser
            webbrowser.open("https://www.google.com")
            log_info("Opening Google")
            return f"Opening Google, {jarvis.owner_name}." if "open" in command else f"Google khol raha hoon, {jarvis.owner_name}."
        
        if "open whatsapp" in command or "whatsapp kholo" in command:
            import webbrowser
            webbrowser.open("https://web.whatsapp.com")
            log_info("Opening WhatsApp")
            return f"Opening WhatsApp Web, {jarvis.owner_name}." if "open" in command else f"WhatsApp khol raha hoon, {jarvis.owner_name}."
        
        if "open gmail" in command or "gmail kholo" in command:
            import webbrowser
            webbrowser.open("https://mail.google.com")
            log_info("Opening Gmail")
            return f"Opening Gmail, {jarvis.owner_name}." if "open" in command else f"Gmail khol raha hoon, {jarvis.owner_name}."
        
        if "open facebook" in command or "facebook kholo" in command:
            import webbrowser
            webbrowser.open("https://www.facebook.com")
            log_info("Opening Facebook")
            return f"Opening Facebook, {jarvis.owner_name}." if "open" in command else f"Facebook khol raha hoon, {jarvis.owner_name}."
        
        if "open instagram" in command or "instagram kholo" in command:
            import webbrowser
            webbrowser.open("https://www.instagram.com")
            log_info("Opening Instagram")
            return f"Opening Instagram, {jarvis.owner_name}." if "open" in command else f"Instagram khol raha hoon, {jarvis.owner_name}."
        
        if "open twitter" in command or "twitter kholo" in command or "open x" in command:
            import webbrowser
            webbrowser.open("https://www.twitter.com")
            log_info("Opening Twitter/X")
            return f"Opening Twitter, {jarvis.owner_name}." if "open" in command else f"Twitter khol raha hoon, {jarvis.owner_name}."
        
        if "open spotify" in command or "spotify kholo" in command:
            import webbrowser
            webbrowser.open("https://open.spotify.com")
            log_info("Opening Spotify")
            return f"Opening Spotify, {jarvis.owner_name}." if "open" in command else f"Spotify khol raha hoon, {jarvis.owner_name}."
        
        if "open calculator" in command or "calculator kholo" in command:
            subprocess.Popen("calc")
            log_info("Opening Calculator")
            return f"Opening Calculator, {jarvis.owner_name}." if "open" in command else f"Calculator khol raha hoon, {jarvis.owner_name}."
        
        if "open paint" in command or "paint kholo" in command:
            subprocess.Popen("mspaint")
            log_info("Opening Paint")
            return f"Opening Paint, {jarvis.owner_name}." if "open" in command else f"Paint khol raha hoon, {jarvis.owner_name}."
        
        if "open word" in command or "word kholo" in command:
            subprocess.Popen("winword")
            log_info("Opening Word")
            return f"Opening Microsoft Word, {jarvis.owner_name}." if "open" in command else f"Word khol raha hoon, {jarvis.owner_name}."
        
        if "open excel" in command or "excel kholo" in command:
            subprocess.Popen("excel")
            log_info("Opening Excel")
            return f"Opening Microsoft Excel, {jarvis.owner_name}." if "open" in command else f"Excel khol raha hoon, {jarvis.owner_name}."
        
        if "open powerpoint" in command or "powerpoint kholo" in command:
            subprocess.Popen("powerpnt")
            log_info("Opening PowerPoint")
            return f"Opening PowerPoint, {jarvis.owner_name}." if "open" in command else f"PowerPoint khol raha hoon, {jarvis.owner_name}."
        
        if "open file explorer" in command or "explorer kholo" in command or "files kholo" in command:
            subprocess.Popen("explorer")
            log_info("Opening File Explorer")
            return f"Opening File Explorer, {jarvis.owner_name}." if "open" in command else f"File Explorer khol raha hoon, {jarvis.owner_name}."
        
        # THIS PC / MY COMPUTER
        if "open this pc" in command or "open my computer" in command or "this pc kholo" in command or "my computer kholo" in command or "computer kholo" in command:
            subprocess.Popen("explorer.exe shell:MyComputerFolder")
            log_info("Opening This PC")
            return f"Opening This PC, {jarvis.owner_name}." if "open" in command else f"This PC khol raha hoon, {jarvis.owner_name}."
        
        if "open task manager" in command or "task manager kholo" in command:
            subprocess.Popen("taskmgr")
            log_info("Opening Task Manager")
            return f"Opening Task Manager, {jarvis.owner_name}." if "open" in command else f"Task Manager khol raha hoon, {jarvis.owner_name}."
        
        if "open control panel" in command or "control panel kholo" in command:
            subprocess.Popen("control")
            log_info("Opening Control Panel")
            return f"Opening Control Panel, {jarvis.owner_name}." if "open" in command else f"Control Panel khol raha hoon, {jarvis.owner_name}."
        
        if "open settings" in command or "settings kholo" in command:
            subprocess.Popen("ms-settings:")
            log_info("Opening Settings")
            return f"Opening Windows Settings, {jarvis.owner_name}." if "open" in command else f"Settings khol raha hoon, {jarvis.owner_name}."

        # ---- VOLUME ----
        if "volume up" in command or "volume badha" in command or "volume badhao" in command:
            return set_volume("up")

        if "volume down" in command or "volume kam kar" in command or "volume kamao" in command:
            return set_volume("down")

        if "mute volume" in command or "volume mute kar" in command or "chup kar" in command:
            return set_volume("mute")

        # ---- FILE / FOLDER ----
        if "open downloads" in command or "downloads kholo" in command:
            os.startfile(os.path.expanduser("~/Downloads"))
            return f"Opening Downloads folder, {jarvis.owner_name}." if "open" in command else f"Downloads folder khol raha hoon, {jarvis.owner_name}."

        if "open documents" in command or "documents kholo" in command:
            os.startfile(os.path.expanduser("~/Documents"))
            return f"Opening Documents folder, {jarvis.owner_name}." if "open" in command else f"Documents folder khol raha hoon, {jarvis.owner_name}."
        
        if "open pictures" in command or "pictures kholo" in command or "photos kholo" in command:
            os.startfile(os.path.expanduser("~/Pictures"))
            return f"Opening Pictures folder, {jarvis.owner_name}." if "open" in command else f"Pictures folder khol raha hoon, {jarvis.owner_name}."
        
        if "open music" in command or "music kholo" in command:
            os.startfile(os.path.expanduser("~/Music"))
            return f"Opening Music folder, {jarvis.owner_name}." if "open" in command else f"Music folder khol raha hoon, {jarvis.owner_name}."
        
        if "open videos" in command or "videos kholo" in command:
            os.startfile(os.path.expanduser("~/Videos"))
            return f"Opening Videos folder, {jarvis.owner_name}." if "open" in command else f"Videos folder khol raha hoon, {jarvis.owner_name}."

        # ---- SCREENSHOT ----
        if "take screenshot" in command or "screenshot le" in command or "screenshot lo" in command:
            pyautogui.screenshot("screenshot.png")
            return f"Screenshot captured, {jarvis.owner_name}." if "take" in command else f"Screenshot le liya, {jarvis.owner_name}."

        # ---- BATTERY ----
        if "battery status" in command or "battery check kar" in command or "battery kitni hai" in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                if "battery" in command and "kitni" in command:
                    return f"{jarvis.owner_name}, battery {percent} percent hai."
                return f"{jarvis.owner_name}, battery is at {percent} percent."
            return f"I apologize, {jarvis.owner_name}, battery information is not available." if "status" in command else f"{jarvis.owner_name}, battery ki information nahi mil rahi."

        # ---- WIFI ----
        if "wifi off" in command or "wifi band kar" in command:
            os.system("netsh interface set interface Wi-Fi disable")
            return f"WiFi turned off, {jarvis.owner_name}." if "off" in command else f"WiFi band kar diya, {jarvis.owner_name}."

        if "wifi on" in command or "wifi chalu kar" in command:
            os.system("netsh interface set interface Wi-Fi enable")
            return f"WiFi turned on, {jarvis.owner_name}." if "on" in command else f"WiFi chalu kar diya, {jarvis.owner_name}."

        # ---- SYSTEM ----
        if "lock system" in command or "system lock kar" in command or "computer lock kar" in command:
            ctypes.windll.user32.LockWorkStation()
            return f"Locking system, {jarvis.owner_name}." if "lock system" in command else f"System lock kar raha hoon, {jarvis.owner_name}."

        if "restart system" in command or "system restart kar" in command or "computer restart kar" in command:
            os.system("shutdown /r /t 5")
            return f"Restarting system in 5 seconds, {jarvis.owner_name}." if "restart system" in command else f"5 seconds mein system restart ho jayega, {jarvis.owner_name}."

        if "shutdown system" in command or "system band kar" in command or "computer band kar" in command or "shutdown kar" in command:
            os.system("shutdown /s /t 5")
            return f"Shutting down system in 5 seconds, {jarvis.owner_name}." if "shutdown system" in command else f"5 seconds mein system band ho jayega, {jarvis.owner_name}."
        
        # ---- GENERIC APP OPENER ----
        # Try to open any application by name
        if "open" in command or "kholo" in command:
            # Extract app name
            app_name = command.replace("open", "").replace("kholo", "").strip()
            
            if app_name and len(app_name) > 2:
                try:
                    # Try to open as executable
                    subprocess.Popen(app_name)
                    log_info(f"Attempting to open: {app_name}")
                    return f"Opening {app_name}, {jarvis.owner_name}." if "open" in command else f"{app_name} khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Could not open {app_name}: {e}")
                    # Don't return error, let AI handle it
                    return None

    except Exception as e:
        log_error(f"System command error: {e}")
        jarvis = get_jarvis()
        return f"I apologize, {jarvis.owner_name}, but I encountered an error executing that command."

    return None
