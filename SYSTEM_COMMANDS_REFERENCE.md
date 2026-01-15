# 🎮 VEDA AI - System Commands Reference

## ✅ ALL WORKING COMMANDS

### 🖥️ System Tools

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `open task manager` | `task manager kholo` | Opens Task Manager |
| `open this pc` | `this pc kholo` | Opens This PC |
| `open my computer` | `computer kholo` | Opens This PC |
| `open file explorer` | `explorer kholo` | Opens File Explorer |
| `open control panel` | `control panel kholo` | Opens Control Panel |
| `open settings` | `settings kholo` | Opens Windows Settings |
| `open command prompt` | `cmd kholo` | Opens Command Prompt |
| `open powershell` | `powershell kholo` | Opens PowerShell |
| `open recycle bin` | `recycle bin kholo` | Opens Recycle Bin |

### 📱 Applications

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `open notepad` | `notepad kholo` | Opens Notepad |
| `open calculator` | `calculator kholo` | Opens Calculator |
| `open paint` | `paint kholo` | Opens Paint |
| `open chrome` | `chrome kholo` | Opens Chrome |
| `open firefox` | `firefox kholo` | Opens Firefox |
| `open edge` | `edge kholo` | Opens Edge |
| `open word` | `word kholo` | Opens MS Word |
| `open excel` | `excel kholo` | Opens MS Excel |
| `open powerpoint` | `powerpoint kholo` | Opens PowerPoint |
| `open spotify` | `spotify kholo` | Opens Spotify |
| `open vscode` | `vscode kholo` | Opens VS Code |
| `open [any app]` | `[koi bhi app] kholo` | Opens any installed app |

### 📁 Folders

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `open downloads` | `downloads kholo` | Opens Downloads folder |
| `open documents` | `documents kholo` | Opens Documents folder |
| `open pictures` | `pictures kholo` | Opens Pictures folder |
| `open photos` | `photos kholo` | Opens Pictures folder |
| `open music` | `music kholo` | Opens Music folder |
| `open videos` | `videos kholo` | Opens Videos folder |
| `open desktop` | `desktop kholo` | Opens Desktop folder |

### 🌐 Websites

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `open youtube` | `youtube kholo` | Opens YouTube |
| `open google` | `google kholo` | Opens Google |
| `open gmail` | `gmail kholo` | Opens Gmail |
| `open facebook` | `facebook kholo` | Opens Facebook |
| `open instagram` | `instagram kholo` | Opens Instagram |
| `open twitter` | `twitter kholo` | Opens Twitter |
| `open whatsapp` | `whatsapp kholo` | Opens WhatsApp Web |
| `open spotify` | `spotify kholo` | Opens Spotify Web |
| `open netflix` | `netflix kholo` | Opens Netflix |
| `open amazon` | `amazon kholo` | Opens Amazon |
| `open linkedin` | `linkedin kholo` | Opens LinkedIn |
| `open github` | `github kholo` | Opens GitHub |
| `open stackoverflow` | `stackoverflow kholo` | Opens Stack Overflow |
| `open reddit` | `reddit kholo` | Opens Reddit |

### 🔊 Volume Control

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `volume up` | `volume badha` | Increases volume by 10% |
| `volume down` | `volume kam kar` | Decreases volume by 10% |
| `mute volume` | `volume mute kar` | Mutes volume |
| `unmute volume` | `volume chalu kar` | Unmutes volume |

### 📸 Screenshot

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `take screenshot` | `screenshot lo` | Takes screenshot |
| `capture screen` | `screen capture karo` | Takes screenshot |

### 🔋 Battery

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `battery status` | `battery kitni hai` | Shows battery percentage |
| `check battery` | `battery check kar` | Shows battery status |

### 📡 WiFi

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `wifi on` | `wifi chalu kar` | Turns WiFi on |
| `wifi off` | `wifi band kar` | Turns WiFi off |

### ⚡ System Power

| Command (English) | Command (Hindi) | Action |
|-------------------|-----------------|--------|
| `lock system` | `system lock kar` | Locks the computer |
| `restart system` | `system restart kar` | Restarts in 5 seconds |
| `shutdown system` | `system band kar` | Shuts down in 5 seconds |

---

## 🎯 Command Variations

VEDA understands multiple ways to say the same thing:

### Opening Apps:
- `open chrome` ✅
- `chrome kholo` ✅
- `start chrome` ✅
- `chrome chalu karo` ✅
- `launch chrome` ✅
- `run chrome` ✅

### Volume Control:
- `volume up` ✅
- `volume badha` ✅
- `volume badhao` ✅
- `increase volume` ✅
- `volume zyada kar` ✅

---

## 🔧 Technical Details

### Priority Order:
1. **System Tools** (Task Manager, This PC, etc.) - Highest priority
2. **Websites** (YouTube, Google, etc.)
3. **Volume Control**
4. **Folders** (Downloads, Documents, etc.)
5. **Screenshot & Battery**
6. **WiFi & Power**
7. **Generic App Opener** - Lowest priority (catches everything else)

### Why This Order?
- System commands are checked first to avoid conflicts
- Example: "open computer" should open "This PC", not search for an app called "computer"
- Generic app opener is last to catch any app not explicitly defined

---

## 🚨 Troubleshooting

### Command Not Working?

**1. Check Spelling:**
- ✅ `open task manager`
- ❌ `open taskmanager` (no space)

**2. Use Full Name:**
- ✅ `open task manager`
- ✅ `open this pc`
- ✅ `open control panel`

**3. Check Logs:**
```bash
type logs\veda_ai.log
```

**4. Try Alternative:**
- If "open chrome" doesn't work, try "chrome kholo"
- If "task manager" doesn't work, try "taskmgr"

### App Not Found?
- Make sure the app is installed
- Try full app name: "google chrome" instead of "chrome"
- Check if app is in Program Files

### Permission Denied?
Some commands need admin rights:
- WiFi control
- System shutdown/restart
- Run VEDA AI as Administrator

---

## 💡 Pro Tips

1. **Natural Language**: Speak naturally! VEDA understands context.
2. **Mix Languages**: Use Hinglish freely - "chrome kholo" works!
3. **Shortcuts**: Use short names - "calc" instead of "calculator"
4. **Voice Commands**: All commands work perfectly with voice!
5. **Multiple Commands**: Execute commands rapidly without waiting!

---

## 🧪 Testing

Run the test script to verify all commands:
```bash
python test_system_commands_complete.py
```

This will test:
- ✅ All system tools
- ✅ All applications
- ✅ All folders
- ✅ All websites
- ✅ Volume control
- ✅ Screenshots & battery
- ✅ Both English and Hindi commands

---

## 📝 Examples

### Opening Multiple Apps:
```
You: "open chrome"
VEDA: "Opening Chrome, Sir." ✅

You: "open calculator"
VEDA: "Opening Calculator, Sir." ✅

You: "open task manager"
VEDA: "Opening Task Manager, Sir." ✅
```

### System Control:
```
You: "open this pc"
VEDA: "Opening This PC, Sir." ✅

You: "open control panel"
VEDA: "Opening Control Panel, Sir." ✅

You: "open settings"
VEDA: "Opening Windows Settings, Sir." ✅
```

### Mixed Commands:
```
You: "chrome kholo"
VEDA: "Chrome khol raha hoon, Sir." ✅

You: "volume badha"
VEDA: "Volume increased, Sir." ✅

You: "screenshot lo"
VEDA: "Screenshot le liya, Sir." ✅
```

---

**Last Updated:** January 15, 2026  
**Status:** ✅ All Commands Working  
**Total Commands:** 50+ system commands + unlimited app support
