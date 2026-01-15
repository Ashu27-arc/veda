# 🎮 VEDA AI - Complete System Control Guide

## 🚀 Features

VEDA AI ab aapke laptop ko **PURA CONTROL** kar sakta hai! Koi bhi app, koi bhi command - bas bolo aur VEDA execute karega.

---

## 📱 App Opening (Koi Bhi App!)

### English Commands:
- `open chrome`
- `open notepad`
- `open calculator`
- `open spotify`
- `open vscode`
- `open word`
- `open excel`
- `open powerpoint`
- `open photoshop`
- `open any app name`

### Hindi/Hinglish Commands:
- `chrome kholo`
- `notepad kholo`
- `calculator kholo`
- `spotify kholo`
- `vscode kholo`
- `word kholo`
- `excel kholo`
- `koi bhi app kholo`

### Smart Detection:
VEDA automatically searches for apps in:
- ✅ Program Files
- ✅ Program Files (x86)
- ✅ AppData/Local/Programs
- ✅ Windows Registry
- ✅ System PATH
- ✅ Common installation directories

---

## 🌐 Website Opening

### Supported Websites:
- `open youtube` / `youtube kholo`
- `open google` / `google kholo`
- `open gmail` / `gmail kholo`
- `open facebook` / `facebook kholo`
- `open instagram` / `instagram kholo`
- `open twitter` / `twitter kholo`
- `open whatsapp` / `whatsapp kholo`
- `open spotify` / `spotify kholo`
- `open netflix` / `netflix kholo`
- `open amazon` / `amazon kholo`
- `open linkedin` / `linkedin kholo`
- `open github` / `github kholo`
- `open stackoverflow` / `stackoverflow kholo`
- `open reddit` / `reddit kholo`

---

## 🔊 Volume Control

### English:
- `volume up` - Increase volume
- `volume down` - Decrease volume
- `mute volume` - Mute sound
- `unmute volume` - Unmute sound

### Hindi/Hinglish:
- `volume badha` / `volume badhao` - Volume badhao
- `volume kam kar` / `volume kamao` - Volume kam karo
- `volume mute kar` / `chup kar` - Mute karo
- `volume chalu kar` - Unmute karo

---

## 📁 Folder Opening

### English:
- `open downloads`
- `open documents`
- `open pictures` / `open photos`
- `open music`
- `open videos`
- `open desktop`

### Hindi/Hinglish:
- `downloads kholo`
- `documents kholo`
- `pictures kholo` / `photos kholo`
- `music kholo`
- `videos kholo`
- `desktop kholo`

---

## 🖥️ System Commands

### File Management:
- `open file explorer` / `explorer kholo`
- `open this pc` / `computer kholo`
- `open task manager` / `task manager kholo`
- `open control panel` / `control panel kholo`
- `open settings` / `settings kholo`

### Screenshot:
- `take screenshot` / `screenshot lo`
- Screenshot automatically saves to Pictures folder

### Battery Status:
- `battery status` / `battery kitni hai`
- Shows battery percentage and charging status

### WiFi Control:
- `wifi on` / `wifi chalu kar`
- `wifi off` / `wifi band kar`

### System Power:
- `lock system` / `system lock kar`
- `restart system` / `system restart kar`
- `shutdown system` / `system band kar`

---

## 🎯 How It Works

### 1. Smart App Detection
```
User: "open chrome"
↓
VEDA searches:
  → System PATH
  → Program Files
  → Registry
  → Common locations
↓
Found: C:\Program Files\Google\Chrome\Application\chrome.exe
↓
Opens Chrome ✅
```

### 2. Flexible Command Recognition
VEDA understands multiple ways to say the same thing:
- "open chrome" = "chrome kholo" = "start chrome" = "chrome chalu karo"

### 3. Fallback System
If app not found:
- Tries direct command execution
- Searches Windows Registry
- Provides helpful error message

---

## 💡 Examples

### Opening Apps:
```
You: "open chrome"
VEDA: "Opening Chrome, Sir."

You: "spotify kholo"
VEDA: "Spotify khol raha hoon, Sir."

You: "open photoshop"
VEDA: "Opening Photoshop, Sir."
```

### Volume Control:
```
You: "volume up"
VEDA: "Volume increased, Sir."

You: "volume badha"
VEDA: "Volume increased, Sir."
```

### System Commands:
```
You: "take screenshot"
VEDA: "Screenshot captured and saved, Sir."

You: "battery kitni hai"
VEDA: "Sir, battery 85 percent hai aur charging."
```

---

## 🔧 Technical Details

### App Search Algorithm:
1. Check common app mappings (Chrome, Firefox, etc.)
2. Search in Program Files directories
3. Search in AppData/Local/Programs
4. Query Windows Registry
5. Try direct command execution
6. Return path if found, None otherwise

### Supported Locations:
- `C:\Program Files\`
- `C:\Program Files (x86)\`
- `%LOCALAPPDATA%\Programs\`
- `%APPDATA%\Local\Programs\`
- `C:\Windows\System32\`
- Windows Registry App Paths

---

## 🚨 Troubleshooting

### App Not Opening?
1. Check if app is installed
2. Try full app name: "open google chrome" instead of "open chrome"
3. Check logs: `logs/veda_ai.log`

### Permission Errors?
Some commands need admin rights:
- WiFi control
- System shutdown/restart
- Run VEDA AI as Administrator

### App Not Found?
VEDA will tell you:
- "Sir, I couldn't find [app name] on your system."
- Install the app or try different name

---

## 🎉 Pro Tips

1. **Natural Language**: Speak naturally! VEDA understands both English and Hindi.
2. **Shortcuts**: Use short names like "chrome" instead of "google chrome"
3. **Voice Commands**: Works perfectly with voice input!
4. **Batch Commands**: Coming soon - multiple commands at once!

---

## 📝 Logs

All commands are logged in: `logs/veda_ai.log`

Check logs to see:
- What commands were executed
- Which apps were found/not found
- Any errors that occurred

---

## 🔮 Future Features

- [ ] Close apps by name
- [ ] Switch between apps
- [ ] Minimize/Maximize windows
- [ ] Multiple monitor control
- [ ] Custom app shortcuts
- [ ] Batch command execution

---

**Made with ❤️ for complete laptop control!**
