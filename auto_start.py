import os
import shutil

startup = os.path.join(
    os.getenv("APPDATA"),
    "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
)

exe_path = os.path.abspath("VEDA_AI.exe")
shutil.copy(exe_path, startup)
