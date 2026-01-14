from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_backend.ai_engine import process_command
from python_backend.voice import listen_command
from python_backend.gesture_control import start_gesture_control
from python_backend.logger import log_info, log_error, log_warning
from python_backend.settings_manager import load_settings, get_owner_name
from python_backend.jarvis_personality import get_jarvis
import threading

# Load settings on startup
settings = load_settings()
log_info(f"VEDA AI initializing for {get_owner_name()}")

app = FastAPI(title="VEDA AI", version="2.0.0")

# More secure CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Active WebSocket connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    log_info("WebSocket connection established")
    
    # Send greeting when connection is established
    jarvis = get_jarvis()
    greeting = jarvis.get_greeting()
    await ws.send_json({"response": greeting, "command": "system_greeting", "type": "greeting"})
    
    try:
        while True:
            command = await ws.receive_text()
            
            # Input validation
            if not command or len(command.strip()) == 0:
                await ws.send_json({"error": "Empty command"})
                continue
                
            if len(command) > 500:
                await ws.send_json({"error": "Command too long"})
                continue
            
            log_info(f"WebSocket command received: {command}")
            response = process_command(command.strip())
            await ws.send_json({"response": response, "command": command})
            
    except WebSocketDisconnect:
        log_info("WebSocket disconnected")
        active_connections.remove(ws)
    except Exception as e:
        log_error(f"WebSocket error: {e}")
        try:
            await ws.send_json({"error": "An error occurred processing your request"})
        except:
            pass
        if ws in active_connections:
            active_connections.remove(ws)

@app.get("/voice")
def voice_command():
    """Handle voice command request with advanced recognition"""
    try:
        log_info("Voice command requested (advanced mode)")
        
        # Use advanced voice recognition
        from python_backend.voice_advanced import listen_command_advanced, test_microphone_access
        
        # First test microphone
        if not test_microphone_access():
            return {
                "error": "❌ Microphone Not Accessible",
                "details": "Please check:\n" +
                          "1. Microphone is connected properly\n" +
                          "2. Windows Settings > Privacy > Microphone permissions enabled\n" +
                          "3. No other app is using the microphone\n" +
                          "4. Try unplugging and reconnecting your microphone",
                "troubleshooting": {
                    "step1": "Check microphone connection",
                    "step2": "Enable microphone permissions in Windows Settings",
                    "step3": "Close other apps using microphone (Zoom, Teams, etc.)",
                    "step4": "Click 'Calibrate Voice' button",
                    "step5": "Restart VEDA AI"
                }
            }
        
        # Try to get voice command
        command = listen_command_advanced()
        
        if not command:
            log_warning("No voice detected or recognition failed")
            return {
                "error": "❌ Voice Recognition Error",
                "message": "No voice detected. Please check:",
                "tips": [
                    "1. Microphone is connected and working",
                    "2. Microphone permissions are enabled",
                    "3. Speak clearly and loudly",
                    "4. Internet connection is active",
                    "5. Try running: python -m python_backend.voice_advanced"
                ],
                "troubleshooting": "💡 Troubleshooting:\n" +
                                 "• Click '🎯 Calibrate Voice' button\n" +
                                 "• Check microphone in Windows Settings\n" +
                                 "• Ensure internet connection is active\n" +
                                 "• Try speaking louder and clearer\n" +
                                 "• Reduce background noise"
            }
        
        if len(command) > 500:
            return {"error": "Command too long"}
            
        response = process_command(command)
        log_info(f"Voice command processed: {command}")
        return {"command": command, "response": response, "status": "success"}
        
    except OSError as e:
        log_error(f"Microphone access error: {e}")
        return {
            "error": "❌ Microphone Access Error",
            "details": str(e),
            "solution": "Please enable microphone permissions in Windows Settings > Privacy > Microphone"
        }
    except Exception as e:
        log_error(f"Voice command error: {e}")
        return {
            "error": "❌ Voice Recognition Failed",
            "details": str(e),
            "message": "Please check your microphone and internet connection.",
            "help": "Try clicking the 'Calibrate Voice' button"
        }

@app.get("/voice/calibrate")
def calibrate_voice():
    """Calibrate microphone for better accuracy"""
    try:
        from python_backend.voice_advanced import calibrate_microphone
        success = calibrate_microphone(duration=3)
        
        if success:
            return {"status": "success", "message": "Microphone calibrated successfully"}
        else:
            return {"status": "error", "message": "Calibration failed"}
            
    except Exception as e:
        log_error(f"Calibration error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/voice/stats")
def voice_stats():
    """Get voice recognition statistics"""
    try:
        from python_backend.voice_advanced import get_voice_stats
        stats = get_voice_stats()
        return stats
    except Exception as e:
        log_error(f"Stats error: {e}")
        return {"error": str(e)}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    jarvis = get_jarvis()
    return {
        "status": "healthy", 
        "service": "VEDA AI",
        "owner": jarvis.owner_name,
        "version": "2.0.0"
    }

@app.get("/settings")
def get_settings():
    """Get current settings"""
    from python_backend.settings_manager import load_settings
    return load_settings()

@app.post("/settings/owner")
async def update_owner(data: dict):
    """Update owner name"""
    try:
        from python_backend.settings_manager import update_owner_name
        name = data.get("name", "Sir")
        
        if update_owner_name(name):
            jarvis = get_jarvis()
            return {
                "status": "success",
                "message": f"Owner name updated to {name}",
                "greeting": jarvis.get_greeting()
            }
        else:
            return {"status": "error", "message": "Failed to update owner name"}
            
    except Exception as e:
        log_error(f"Error updating owner name: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def read_root():
    """Serve main UI"""
    return FileResponse("python_frontend/index.html")

@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    """Serve static files"""
    file_location = os.path.join("python_frontend", file_path)
    
    if os.path.exists(file_location) and os.path.isfile(file_location):
        return FileResponse(file_location)
    
    # Return 404 for missing files (except favicon)
    if file_path == "favicon.ico":
        # Return empty response for favicon
        return FileResponse("python_frontend/index.html", status_code=204)
    
    raise HTTPException(status_code=404, detail="File not found")

# Start gesture control in background (with error handling)
def start_gesture_safely():
    try:
        start_gesture_control()
    except Exception as e:
        log_error(f"Gesture control failed to start: {e}")

threading.Thread(target=start_gesture_safely, daemon=True).start()
log_info("VEDA AI backend initialized")
