import os
import subprocess
import psutil
import pyautogui
import ctypes
import winreg
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities
from python_backend.logger import log_info, log_error, log_warning
from python_backend.jarvis_personality import get_jarvis

# =========================
# APP FINDER - SMART APP DETECTION
# =========================
def find_application(app_name):
    """
    Smart application finder - searches multiple locations
    Returns path if found, None otherwise
    """
    app_name_lower = app_name.lower().strip()
    
    # Common app mappings
    app_mappings = {
        'chrome': ['chrome.exe', 'Google\\Chrome\\Application\\chrome.exe'],
        'firefox': ['firefox.exe', 'Mozilla Firefox\\firefox.exe'],
        'edge': ['msedge.exe', 'Microsoft\\Edge\\Application\\msedge.exe'],
        'brave': ['brave.exe', 'BraveSoftware\\Brave-Browser\\Application\\brave.exe'],
        'notepad': ['notepad.exe'],
        'calculator': ['calc.exe', 'CalculatorApp.exe'],
        'paint': ['mspaint.exe'],
        'word': ['winword.exe', 'Microsoft Office\\root\\Office16\\WINWORD.EXE'],
        'excel': ['excel.exe', 'Microsoft Office\\root\\Office16\\EXCEL.EXE'],
        'powerpoint': ['powerpnt.exe', 'Microsoft Office\\root\\Office16\\POWERPNT.EXE'],
        'outlook': ['outlook.exe', 'Microsoft Office\\root\\Office16\\OUTLOOK.EXE'],
        'onenote': ['onenote.exe', 'Microsoft Office\\root\\Office16\\ONENOTE.EXE'],
        'teams': ['Teams.exe', 'Microsoft\\Teams\\current\\Teams.exe'],
        'zoom': ['Zoom.exe', 'Zoom\\bin\\Zoom.exe'],
        'discord': ['Discord.exe', 'Discord\\app-*\\Discord.exe'],
        'spotify': ['Spotify.exe', 'Spotify\\Spotify.exe'],
        'vlc': ['vlc.exe', 'VideoLAN\\VLC\\vlc.exe'],
        'vscode': ['Code.exe', 'Microsoft VS Code\\Code.exe'],
        'pycharm': ['pycharm64.exe', 'JetBrains\\PyCharm*\\bin\\pycharm64.exe'],
        'photoshop': ['Photoshop.exe', 'Adobe\\Adobe Photoshop*\\Photoshop.exe'],
        'illustrator': ['Illustrator.exe', 'Adobe\\Adobe Illustrator*\\Support Files\\Contents\\Windows\\Illustrator.exe'],
        'premiere': ['Adobe Premiere Pro.exe', 'Adobe\\Adobe Premiere Pro*\\Adobe Premiere Pro.exe'],
        'obs': ['obs64.exe', 'obs-studio\\bin\\64bit\\obs64.exe'],
        'steam': ['steam.exe', 'Steam\\steam.exe'],
        'epic': ['EpicGamesLauncher.exe', 'Epic Games\\Launcher\\Portal\\Binaries\\Win64\\EpicGamesLauncher.exe'],
    }
    
    # Get possible filenames
    possible_names = app_mappings.get(app_name_lower, [f'{app_name}.exe'])
    
    # Search locations
    search_paths = [
        os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
        os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs'),
        os.path.join(os.environ.get('APPDATA', ''), 'Local\\Programs'),
        'C:\\Windows\\System32',
        'C:\\Windows',
    ]
    
    # Try each possible name in each location
    for name in possible_names:
        # Try direct execution first (for system apps)
        try:
            result = subprocess.run(['where', name.split('\\')[-1]], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0 and result.stdout.strip():
                path = result.stdout.strip().split('\n')[0]
                if os.path.exists(path):
                    log_info(f"Found {app_name} at: {path}")
                    return path
        except:
            pass
        
        # Search in common directories
        for base_path in search_paths:
            if not os.path.exists(base_path):
                continue
                
            # Direct path
            full_path = os.path.join(base_path, name)
            if os.path.exists(full_path):
                log_info(f"Found {app_name} at: {full_path}")
                return full_path
            
            # Search subdirectories (one level deep)
            try:
                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)
                    if os.path.isdir(item_path):
                        sub_path = os.path.join(item_path, name.split('\\')[-1])
                        if os.path.exists(sub_path):
                            log_info(f"Found {app_name} at: {sub_path}")
                            return sub_path
            except (PermissionError, OSError):
                continue
    
    # Try Windows Registry for installed apps
    try:
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"
        ]
        
        for reg_path in registry_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        if app_name_lower in subkey_name.lower():
                            subkey = winreg.OpenKey(key, subkey_name)
                            path, _ = winreg.QueryValueEx(subkey, "")
                            if os.path.exists(path):
                                log_info(f"Found {app_name} in registry: {path}")
                                return path
                    except:
                        continue
            except:
                continue
    except:
        pass
    
    log_warning(f"Could not find application: {app_name}")
    return None


def open_application(app_name):
    """
    Open any application by name
    """
    jarvis = get_jarvis()
    
    # Find the application
    app_path = find_application(app_name)
    
    if app_path:
        try:
            subprocess.Popen(app_path)
            log_info(f"Successfully opened: {app_name}")
            return f"Opening {app_name}, {jarvis.owner_name}."
        except Exception as e:
            log_error(f"Failed to open {app_name}: {e}")
            return f"{jarvis.owner_name}, I found {app_name} but couldn't open it."
    else:
        # Try as direct command (might be in PATH)
        try:
            subprocess.Popen(app_name)
            log_info(f"Opened {app_name} as direct command")
            return f"Opening {app_name}, {jarvis.owner_name}."
        except:
            log_error(f"Application not found: {app_name}")
            return f"{jarvis.owner_name}, I couldn't find {app_name} on your system."


def close_application(app_name):
    """
    Close/kill an application by name
    """
    jarvis = get_jarvis()
    
    try:
        # Get the process name
        process_name = app_name.lower().strip()
        
        # Add .exe if not present
        if not process_name.endswith('.exe'):
            process_name = f"{process_name}.exe"
        
        # Try to kill the process
        killed = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == process_name:
                    proc.kill()
                    killed = True
                    log_info(f"Killed process: {process_name}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if killed:
            return f"Closed {app_name}, {jarvis.owner_name}."
        else:
            # Try using taskkill command
            result = subprocess.run(['taskkill', '/F', '/IM', process_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                log_info(f"Closed {app_name} using taskkill")
                return f"Closed {app_name}, {jarvis.owner_name}."
            else:
                log_warning(f"Could not find running process: {app_name}")
                return f"{jarvis.owner_name}, {app_name} is not running."
                
    except Exception as e:
        log_error(f"Error closing {app_name}: {e}")
        return f"{jarvis.owner_name}, I couldn't close {app_name}."


# =========================
# VOLUME CONTROL
# =========================
def set_volume(action):
    """Control system volume"""
    try:
        jarvis = get_jarvis()
        
        # Get all audio devices - returns AudioDevice object
        devices = AudioUtilities.GetSpeakers()
        
        # Get volume interface directly from AudioDevice
        volume = devices.EndpointVolume
        
        # Get current volume level
        current = volume.GetMasterVolumeLevelScalar()

        if action == "up":
            new_volume = min(current + 0.1, 1.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            log_info(f"Volume increased to {int(new_volume * 100)}%")
            return f"Volume increased, {jarvis.owner_name}."

        if action == "down":
            new_volume = max(current - 0.1, 0.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            log_info(f"Volume decreased to {int(new_volume * 100)}%")
            return f"Volume decreased, {jarvis.owner_name}."

        if action == "mute":
            volume.SetMute(1, None)
            log_info("Volume muted")
            return f"Volume muted, {jarvis.owner_name}."
            
        if action == "unmute":
            volume.SetMute(0, None)
            log_info("Volume unmuted")
            return f"Volume unmuted, {jarvis.owner_name}."
            
    except AttributeError as e:
        # Fallback to keyboard shortcuts if pycaw doesn't work
        log_warning(f"Volume control via pycaw failed: {e}, using keyboard shortcuts")
        try:
            if action == "up":
                pyautogui.press('volumeup')
                return f"Volume increased, {jarvis.owner_name}."
            elif action == "down":
                pyautogui.press('volumedown')
                return f"Volume decreased, {jarvis.owner_name}."
            elif action == "mute":
                pyautogui.press('volumemute')
                return f"Volume muted, {jarvis.owner_name}."
            elif action == "unmute":
                pyautogui.press('volumemute')
                return f"Volume unmuted, {jarvis.owner_name}."
        except Exception as fallback_error:
            log_error(f"Keyboard fallback also failed: {fallback_error}")
            jarvis = get_jarvis()
            return f"I apologize, {jarvis.owner_name}, but I couldn't control the volume."
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
        original_command = command
        command = command.lower().strip()
        
        log_info(f"System control checking command: {command}")
        
        # ---- ENHANCED COMMAND DETECTION ----
        # Detect if this is an action command (open/close/start/stop)
        is_open_command = any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'launch', 'run', 'shuru'])
        is_close_command = any(word in command for word in ['close', 'band', 'stop', 'exit', 'quit'])
        
        # ---- WEBSITES ----
        if any(site in command for site in ['youtube', 'google', 'gmail', 'facebook', 'instagram', 
                                              'twitter', 'whatsapp', 'spotify', 'netflix', 'amazon',
                                              'linkedin', 'github', 'stackoverflow', 'reddit']):
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'browse', 'search']):
                import webbrowser
                
                site_urls = {
                    'youtube': 'https://www.youtube.com',
                    'google': 'https://www.google.com',
                    'gmail': 'https://mail.google.com',
                    'facebook': 'https://www.facebook.com',
                    'instagram': 'https://www.instagram.com',
                    'twitter': 'https://www.twitter.com',
                    'whatsapp': 'https://web.whatsapp.com',
                    'spotify': 'https://open.spotify.com',
                    'netflix': 'https://www.netflix.com',
                    'amazon': 'https://www.amazon.in',
                    'linkedin': 'https://www.linkedin.com',
                    'github': 'https://www.github.com',
                    'stackoverflow': 'https://stackoverflow.com',
                    'reddit': 'https://www.reddit.com',
                }
                
                for site, url in site_urls.items():
                    if site in command:
                        try:
                            webbrowser.open(url)
                            log_info(f"Opening {site}")
                            return f"Opening {site.title()}, {jarvis.owner_name}." if "open" in command else f"{site.title()} khol raha hoon, {jarvis.owner_name}."
                        except Exception as e:
                            log_error(f"{site} error: {e}")
                            return f"{jarvis.owner_name}, I couldn't open {site.title()}."

        # ---- VOLUME CONTROL ----
        if "volume" in command or "sound" in command or "audio" in command:
            if any(word in command for word in ['up', 'increase', 'badha', 'badhao', 'high', 'zyada']):
                return set_volume("up")
            elif any(word in command for word in ['down', 'decrease', 'kam', 'kamao', 'low', 'kum']):
                return set_volume("down")
            elif any(word in command for word in ['mute', 'silent', 'chup', 'band']):
                return set_volume("mute")
            elif any(word in command for word in ['unmute', 'chalu', 'on']):
                return set_volume("unmute")

        # ---- FOLDERS ----
        folder_commands = {
            'downloads': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'documents': os.path.join(os.path.expanduser('~'), 'Documents'),
            'pictures': os.path.join(os.path.expanduser('~'), 'Pictures'),
            'photos': os.path.join(os.path.expanduser('~'), 'Pictures'),
            'music': os.path.join(os.path.expanduser('~'), 'Music'),
            'videos': os.path.join(os.path.expanduser('~'), 'Videos'),
            'desktop': os.path.join(os.path.expanduser('~'), 'Desktop'),
        }
        
        for folder_name, folder_path in folder_commands.items():
            if folder_name in command and any(word in command for word in ['open', 'kholo', 'show']):
                try:
                    # Create folder if it doesn't exist
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path, exist_ok=True)
                        log_info(f"Created missing folder: {folder_path}")
                    
                    os.startfile(folder_path)
                    log_info(f"Opening {folder_name} folder")
                    return f"Opening {folder_name.title()} folder, {jarvis.owner_name}." if "open" in command else f"{folder_name.title()} folder khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Folder error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open {folder_name} folder."

        # ---- SYSTEM COMMANDS (HIGH PRIORITY - CHECK FIRST) ----
        # These need to be checked BEFORE generic app opener
        
        # Task Manager
        if "task manager" in command or "taskmanager" in command or "taskmgr" in command:
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("taskmgr.exe")
                    log_info("Opening Task Manager")
                    return f"Opening Task Manager, {jarvis.owner_name}." if "open" in command else f"Task Manager khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Task Manager error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open Task Manager."
        
        # This PC / My Computer
        if ("this pc" in command or "my computer" in command or "mycomputer" in command or 
            ("computer" in command and any(word in command for word in ['open', 'kholo', 'show']))):
            # Make sure it's not "lock computer" or "restart computer"
            if not any(word in command for word in ['lock', 'restart', 'shutdown', 'band']):
                try:
                    subprocess.Popen("explorer.exe shell:MyComputerFolder")
                    log_info("Opening This PC")
                    return f"Opening This PC, {jarvis.owner_name}." if "open" in command else f"This PC khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"This PC error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open This PC."
        
        # File Explorer
        if ("file explorer" in command or "fileexplorer" in command or 
            ("explorer" in command and not "internet explorer" in command)):
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("explorer.exe")
                    log_info("Opening File Explorer")
                    return f"Opening File Explorer, {jarvis.owner_name}." if "open" in command else f"File Explorer khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"File Explorer error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open File Explorer."

        # Control Panel
        if "control panel" in command or "controlpanel" in command:
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("control.exe")
                    log_info("Opening Control Panel")
                    return f"Opening Control Panel, {jarvis.owner_name}." if "open" in command else f"Control Panel khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Control Panel error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open Control Panel."

        # Windows Settings
        if ("settings" in command or "setting" in command) and not "control panel" in command:
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("start ms-settings:", shell=True)
                    log_info("Opening Settings")
                    return f"Opening Windows Settings, {jarvis.owner_name}." if "open" in command else f"Settings khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Settings error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open Settings."
        
        # Command Prompt
        if "command prompt" in command or "cmd" in command or "terminal" in command:
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("cmd.exe")
                    log_info("Opening Command Prompt")
                    return f"Opening Command Prompt, {jarvis.owner_name}." if "open" in command else f"Command Prompt khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Command Prompt error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open Command Prompt."
        
        # PowerShell
        if "powershell" in command or "power shell" in command:
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("powershell.exe")
                    log_info("Opening PowerShell")
                    return f"Opening PowerShell, {jarvis.owner_name}." if "open" in command else f"PowerShell khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"PowerShell error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open PowerShell."
        
        # Recycle Bin
        if "recycle bin" in command or "recyclebin" in command or "trash" in command:
            if any(word in command for word in ['open', 'kholo', 'start', 'chalu', 'show']):
                try:
                    subprocess.Popen("explorer.exe shell:RecycleBinFolder")
                    log_info("Opening Recycle Bin")
                    return f"Opening Recycle Bin, {jarvis.owner_name}." if "open" in command else f"Recycle Bin khol raha hoon, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Recycle Bin error: {e}")
                    return f"{jarvis.owner_name}, I couldn't open Recycle Bin."

        # ---- SCREENSHOT ----
        if "screenshot" in command or "screen capture" in command:
            if any(word in command for word in ['take', 'capture', 'le', 'lo', 'lena']):
                try:
                    # Create Pictures folder if it doesn't exist
                    pictures_folder = os.path.join(os.path.expanduser("~"), "Pictures")
                    if not os.path.exists(pictures_folder):
                        os.makedirs(pictures_folder, exist_ok=True)
                        log_info(f"Created Pictures folder: {pictures_folder}")
                    
                    # Generate unique filename with timestamp
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(pictures_folder, f"screenshot_{timestamp}.png")
                    
                    pyautogui.screenshot(screenshot_path)
                    log_info(f"Screenshot saved to {screenshot_path}")
                    return f"Screenshot captured and saved, {jarvis.owner_name}." if "take" in command else f"Screenshot le liya, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"Screenshot error: {e}")
                    return f"{jarvis.owner_name}, I couldn't take a screenshot."

        # ---- BATTERY ----
        if "battery" in command:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    plugged = battery.power_plugged
                    status = "charging" if plugged else "on battery"
                    
                    if "kitni" in command or "how much" in command:
                        return f"{jarvis.owner_name}, battery {percent} percent hai aur {status}."
                    return f"{jarvis.owner_name}, battery is at {percent} percent and {status}."
                return f"I apologize, {jarvis.owner_name}, battery information is not available."
            except Exception as e:
                log_error(f"Battery error: {e}")
                return f"{jarvis.owner_name}, I couldn't check battery status."

        # ---- WIFI ----
        if "wifi" in command or "wi-fi" in command:
            if any(word in command for word in ['off', 'disable', 'band', 'close']):
                try:
                    os.system("netsh interface set interface Wi-Fi disable")
                    log_info("WiFi turned off")
                    return f"WiFi turned off, {jarvis.owner_name}." if "off" in command else f"WiFi band kar diya, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"WiFi off error: {e}")
                    return f"{jarvis.owner_name}, I couldn't turn off WiFi."
            elif any(word in command for word in ['on', 'enable', 'chalu', 'start']):
                try:
                    os.system("netsh interface set interface Wi-Fi enable")
                    log_info("WiFi turned on")
                    return f"WiFi turned on, {jarvis.owner_name}." if "on" in command else f"WiFi chalu kar diya, {jarvis.owner_name}."
                except Exception as e:
                    log_error(f"WiFi on error: {e}")
                    return f"{jarvis.owner_name}, I couldn't turn on WiFi."

        # ---- SYSTEM POWER ----
        if "lock" in command and any(word in command for word in ['system', 'computer', 'pc', 'laptop']):
            try:
                ctypes.windll.user32.LockWorkStation()
                log_info("Locking system")
                return f"Locking system, {jarvis.owner_name}." if "lock" in command else f"System lock kar raha hoon, {jarvis.owner_name}."
            except Exception as e:
                log_error(f"Lock error: {e}")
                return f"{jarvis.owner_name}, I couldn't lock the system."

        if "restart" in command and any(word in command for word in ['system', 'computer', 'pc', 'laptop']):
            try:
                os.system("shutdown /r /t 5")
                log_info("Restarting system")
                return f"Restarting system in 5 seconds, {jarvis.owner_name}." if "restart" in command else f"5 seconds mein system restart ho jayega, {jarvis.owner_name}."
            except Exception as e:
                log_error(f"Restart error: {e}")
                return f"{jarvis.owner_name}, I couldn't restart the system."

        if "shutdown" in command or ("band" in command and any(word in command for word in ['system', 'computer', 'pc', 'laptop'])):
            try:
                os.system("shutdown /s /t 5")
                log_info("Shutting down system")
                return f"Shutting down system in 5 seconds, {jarvis.owner_name}." if "shutdown" in command else f"5 seconds mein system band ho jayega, {jarvis.owner_name}."
            except Exception as e:
                log_error(f"Shutdown error: {e}")
                return f"{jarvis.owner_name}, I couldn't shutdown the system."

        # ---- GENERIC APP OPENER (MOST POWERFUL) ----
        # This will handle ANY app request
        if is_open_command or is_close_command:
            # Extract app name
            app_name = command
            
            # Remove trigger words
            for word in ['open', 'kholo', 'start', 'chalu', 'launch', 'run', 'karo', 'kar', 'do', 
                        'close', 'band', 'stop', 'exit', 'quit', 'please', 'kripya', 'karo', 'dijiye']:
                app_name = app_name.replace(word, '')
            
            app_name = app_name.strip()
            
            # Skip if it's a website, folder, or system command (already handled above)
            skip_words = ['youtube', 'google', 'gmail', 'facebook', 'instagram', 'twitter',
                         'downloads', 'documents', 'pictures', 'music', 'videos', 'desktop',
                         'explorer', 'computer', 'settings', 'control panel', 'task manager',
                         'this pc', 'my computer', 'recycle bin', 'command prompt', 'powershell',
                         'wifi', 'volume', 'screenshot', 'battery', 'lock', 'restart', 'shutdown',
                         'weather', 'mausam', 'time', 'date']
            
            if app_name and len(app_name) > 1 and not any(skip in app_name for skip in skip_words):
                log_info(f"Attempting to open/close application: {app_name}")
                
                if is_open_command:
                    result = open_application(app_name)
                    if result:
                        return result
                elif is_close_command:
                    # Try to close the application
                    result = close_application(app_name)
                    if result:
                        return result

    except Exception as e:
        log_error(f"System command error: {e}")
        jarvis = get_jarvis()
        return f"I apologize, {jarvis.owner_name}, but I encountered an error executing that command."

    return None
