import pystray
from PIL import Image
import os
import sys

def quit_app(icon, item):
    icon.stop()
    os._exit(0)

image = Image.new("RGB", (64, 64), color="cyan")

icon = pystray.Icon(
    "VEDA AI",
    image,
    "VEDA AI",
    menu=pystray.Menu(
        pystray.MenuItem("Exit", quit_app)
    )
)

icon.run()
