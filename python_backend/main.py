from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import sys
import os
import asyncio
import time
from collections import defaultdict
from typing import Dict, List
import hashlib
import secrets

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python_backend.ai_engine import process_command
from python_backend.voice import listen_command
from python_backend.gesture_control import start_gesture_control
from python_backend.logger import log_info, log_error, log_warning
from python_backend.settings_manager import load_settings, get_owner_name
from python_backend.jarvis_personality import get_jarvis
from python_backend.automation_engine import get_automation_engine, start_automation, get_automation_status
from python_backend.proactive_assistant import get_proactive_assistant
from python_backend.context_awareness import get_context_awareness
from python_backend.task_scheduler import get_task_scheduler
import threading

# Load settings on startup
settings = load_settings()
log_info(f"VEDA AI initializing for {get_owner_name()}")

# Start automation engine
try:
    start_automation()
    log_info("Automation engine started")
except Exception as e:
    log_error(f"Failed to start automation engine: {e}")

app = FastAPI(title="VEDA AI", version="5.0.0")

# ========== RATE LIMITING ==========
class RateLimiter:
    """Simple in-memory rate limiter"""
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make request"""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] 
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = time.time()
        window_start = now - self.window_seconds
        current_requests = len([
            req_time for req_time in self.requests[client_id] 
            if req_time > window_start
        ])
        return max(0, self.max_requests - current_requests)

# Rate limiters for different endpoints
api_rate_limiter = RateLimiter(max_requests=60, window_seconds=60)  # 60 req/min for API
ws_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)   # 30 msg/min for WebSocket
voice_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)  # 10 req/min for voice

def get_client_id(request: Request = None, websocket: WebSocket = None) -> str:
    """Get client identifier from request or websocket"""
    if request:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    elif websocket:
        return websocket.client.host if websocket.client else "unknown"
    return "unknown"

# ========== API KEY AUTHENTICATION (Optional) ==========
# Generate a session token on startup (for local use)
SESSION_TOKEN = secrets.token_hex(32)
API_KEY_ENABLED = os.getenv("VEDA_API_KEY_ENABLED", "false").lower() == "true"
API_KEY = os.getenv("VEDA_API_KEY", SESSION_TOKEN)

def verify_api_key(request: Request) -> bool:
    """Verify API key if authentication is enabled"""
    if not API_KEY_ENABLED:
        return True
    
    # Check header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        return secrets.compare_digest(token, API_KEY)
    
    # Check query parameter (for browser access)
    api_key = request.query_params.get("api_key")
    if api_key:
        return secrets.compare_digest(api_key, API_KEY)
    
    return False

# Secure CORS configuration - only allow local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",  # For development
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Active WebSocket connections with metadata
active_connections: List[Dict] = []
MAX_CONNECTIONS = 10  # Limit concurrent WebSocket connections

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    client_id = get_client_id(websocket=ws)
    
    # Check connection limit
    if len(active_connections) >= MAX_CONNECTIONS:
        await ws.close(code=1013, reason="Too many connections")
        log_warning(f"Connection rejected: too many connections from {client_id}")
        return
    
    await ws.accept()
    connection_info = {"ws": ws, "client_id": client_id, "connected_at": time.time()}
    active_connections.append(connection_info)
    log_info(f"WebSocket connection established from {client_id}")
    
    # Send greeting when connection is established
    jarvis = get_jarvis()
    greeting = jarvis.get_greeting()
    await ws.send_json({"response": greeting, "command": "system_greeting", "type": "greeting"})
    
    try:
        while True:
            # Rate limiting for WebSocket messages
            if not ws_rate_limiter.is_allowed(client_id):
                await ws.send_json({
                    "error": "Rate limit exceeded. Please wait before sending more commands.",
                    "retry_after": 60
                })
                await asyncio.sleep(1)  # Small delay to prevent spam
                continue
            
            command = await ws.receive_text()
            
            # Enhanced input validation
            if not command or len(command.strip()) == 0:
                await ws.send_json({"error": "Empty command"})
                continue
                
            if len(command) > 500:
                await ws.send_json({"error": "Command too long (max 500 characters)"})
                continue
            
            # Sanitize input
            from python_backend.utils import sanitize_input, validate_command
            command = sanitize_input(command)
            
            if not validate_command(command):
                await ws.send_json({"error": "Invalid or potentially malicious command"})
                log_warning(f"Blocked potentially malicious command from {client_id}: {command[:50]}")
                continue
            
            log_info(f"WebSocket command from {client_id}: {command}")
            response = process_command(command.strip())
            await ws.send_json({"response": response, "command": command})
            
    except WebSocketDisconnect:
        log_info(f"WebSocket disconnected: {client_id}")
    except Exception as e:
        log_error(f"WebSocket error for {client_id}: {e}")
        try:
            await ws.send_json({"error": "An error occurred processing your request"})
        except:
            pass
    finally:
        # Clean up connection
        active_connections[:] = [
            conn for conn in active_connections 
            if conn.get("ws") != ws
        ]

@app.get("/voice")
def voice_command(request: Request):
    """Handle voice command request with advanced recognition"""
    client_id = get_client_id(request)
    
    # Rate limiting for voice commands (more restrictive)
    if not voice_rate_limiter.is_allowed(client_id):
        remaining = voice_rate_limiter.get_remaining(client_id)
        log_warning(f"Voice rate limit exceeded for {client_id}")
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many voice requests. Please wait before trying again.",
                "status": "rate_limited",
                "retry_after": 60,
                "remaining_requests": remaining
            }
        )
    
    try:
        log_info(f"Voice command requested from {client_id}")
        
        # Use advanced voice recognition
        from python_backend.voice_advanced import listen_command_advanced, test_microphone_access
        
        # Quick microphone test
        if not test_microphone_access():
            log_error("Microphone not accessible")
            return {
                "error": "Microphone not accessible. Please check your microphone connection and permissions in Windows Settings > Privacy > Microphone.",
                "status": "error",
                "tips": [
                    "Check if microphone is connected",
                    "Enable microphone in Windows Settings",
                    "Close other apps using microphone"
                ]
            }
        
        # Get voice command
        command = listen_command_advanced()
        
        if not command or command.strip() == "":
            log_warning("No voice detected")
            return {
                "error": "No voice detected or could not understand speech.",
                "status": "no_speech",
                "tips": [
                    "Speak more clearly and loudly",
                    "Reduce background noise",
                    "Check internet connection (required for speech recognition)",
                    "Try speaking in Hindi, Hinglish, or English"
                ]
            }
        
        if len(command) > 500:
            return {"error": "Command too long", "status": "error"}
        
        # Validate command for security
        from python_backend.utils import sanitize_input, validate_command
        command = sanitize_input(command)
        
        if not validate_command(command):
            log_warning(f"Blocked potentially malicious voice command from {client_id}")
            return {"error": "Invalid command detected", "status": "error"}
            
        response = process_command(command)
        log_info(f"Voice command processed from {client_id}: {command}")
        return {"command": command, "response": response, "status": "success"}
        
    except OSError as e:
        log_error(f"Microphone access error: {e}")
        return {
            "error": "Microphone access error. Please check Windows Settings > Privacy > Microphone",
            "status": "error"
        }
    except Exception as e:
        log_error(f"Voice command error: {e}")
        return {
            "error": f"Voice recognition failed: {str(e)}",
            "status": "error"
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

@app.get("/voice/reset")
def voice_reset():
    """Reset voice settings to defaults - use if voice is not working"""
    try:
        from python_backend.voice_advanced import reset_voice_settings, get_voice_stats
        success = reset_voice_settings()
        
        if success:
            stats = get_voice_stats()
            return {
                "status": "success", 
                "message": "Voice settings reset to defaults. Try speaking again.",
                "new_settings": stats
            }
        else:
            return {"status": "error", "message": "Failed to reset voice settings"}
            
    except Exception as e:
        log_error(f"Voice reset error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/health")
def health_check(request: Request):
    """Health check endpoint"""
    client_id = get_client_id(request)
    jarvis = get_jarvis()
    return {
        "status": "healthy", 
        "service": "VEDA AI",
        "owner": jarvis.owner_name,
        "version": "5.0.0",
        "ai_mode": "self_training",
        "rate_limit": {
            "api_remaining": api_rate_limiter.get_remaining(client_id),
            "ws_remaining": ws_rate_limiter.get_remaining(client_id),
            "voice_remaining": voice_rate_limiter.get_remaining(client_id)
        },
        "connections": len(active_connections),
        "max_connections": MAX_CONNECTIONS
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

# ========== AUTOMATION ENDPOINTS ==========

@app.get("/automation/status")
def automation_status():
    """Get automation engine status"""
    try:
        return get_automation_status()
    except Exception as e:
        log_error(f"Error getting automation status: {e}")
        return {"error": str(e)}

@app.get("/automation/suggestions")
def get_suggestions():
    """Get proactive suggestions"""
    try:
        assistant = get_proactive_assistant()
        suggestions = assistant.get_all_suggestions()
        return {"suggestions": suggestions, "count": len(suggestions)}
    except Exception as e:
        log_error(f"Error getting suggestions: {e}")
        return {"error": str(e)}

@app.post("/automation/execute-suggestion")
async def execute_suggestion(data: dict):
    """Execute a suggested action"""
    try:
        action = data.get("action")
        if not action:
            return {"error": "Action not specified"}
        
        assistant = get_proactive_assistant()
        result = assistant.execute_suggestion_action(action)
        return {"status": "success", "result": result}
    except Exception as e:
        log_error(f"Error executing suggestion: {e}")
        return {"error": str(e)}

@app.get("/automation/context")
def get_context():
    """Get current context information"""
    try:
        context = get_context_awareness()
        return {
            "current_context": context.get_current_context(),
            "prediction": context.predict_next_action(),
            "frequent_tasks": context.get_frequent_tasks(limit=10)
        }
    except Exception as e:
        log_error(f"Error getting context: {e}")
        return {"error": str(e)}

@app.post("/automation/shortcut")
async def create_shortcut(data: dict):
    """Create a command shortcut"""
    try:
        name = data.get("name")
        command = data.get("command")
        
        if not name or not command:
            return {"error": "Name and command required"}
        
        context = get_context_awareness()
        context.create_shortcut(name, command)
        return {"status": "success", "message": f"Shortcut '{name}' created"}
    except Exception as e:
        log_error(f"Error creating shortcut: {e}")
        return {"error": str(e)}

# ========== TASK SCHEDULER ENDPOINTS ==========

@app.get("/tasks")
def get_tasks():
    """Get all scheduled tasks"""
    try:
        scheduler = get_task_scheduler()
        return {"tasks": scheduler.get_all_tasks()}
    except Exception as e:
        log_error(f"Error getting tasks: {e}")
        return {"error": str(e)}

@app.post("/tasks")
async def add_task(data: dict):
    """Add a new scheduled task"""
    try:
        scheduler = get_task_scheduler()
        task = scheduler.add_task(
            name=data.get("name"),
            command=data.get("command"),
            schedule_type=data.get("schedule_type"),
            schedule_value=data.get("schedule_value"),
            enabled=data.get("enabled", True),
            conditions=data.get("conditions")
        )
        return {"status": "success", "task": task}
    except Exception as e:
        log_error(f"Error adding task: {e}")
        return {"error": str(e)}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a scheduled task"""
    try:
        scheduler = get_task_scheduler()
        scheduler.delete_task(task_id)
        return {"status": "success", "message": f"Task {task_id} deleted"}
    except Exception as e:
        log_error(f"Error deleting task: {e}")
        return {"error": str(e)}

@app.post("/tasks/{task_id}/enable")
async def enable_task(task_id: int):
    """Enable a task"""
    try:
        scheduler = get_task_scheduler()
        scheduler.enable_task(task_id)
        return {"status": "success", "message": f"Task {task_id} enabled"}
    except Exception as e:
        log_error(f"Error enabling task: {e}")
        return {"error": str(e)}

@app.post("/tasks/{task_id}/disable")
async def disable_task(task_id: int):
    """Disable a task"""
    try:
        scheduler = get_task_scheduler()
        scheduler.disable_task(task_id)
        return {"status": "success", "message": f"Task {task_id} disabled"}
    except Exception as e:
        log_error(f"Error disabling task: {e}")
        return {"error": str(e)}

@app.get("/")
async def read_root():
    """Serve main UI"""
    return FileResponse("python_frontend/index.html")

@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    """Serve static files with security checks"""
    # Security: Prevent path traversal attacks
    if ".." in file_path or file_path.startswith("/") or file_path.startswith("\\"):
        log_warning(f"Blocked path traversal attempt: {file_path}")
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Normalize path and check for allowed extensions
    allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.ppn', '.txt'}
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext and ext not in allowed_extensions:
        log_warning(f"Blocked file access with disallowed extension: {file_path}")
        raise HTTPException(status_code=403, detail="File type not allowed")
    
    file_location = os.path.join("python_frontend", file_path)
    
    # Ensure file is within python_frontend directory (prevent symlink attacks)
    abs_file = os.path.abspath(file_location)
    abs_frontend = os.path.abspath("python_frontend")
    
    if not abs_file.startswith(abs_frontend):
        log_warning(f"Blocked access outside frontend directory: {file_path}")
        raise HTTPException(status_code=403, detail="Access denied")
    
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
