from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import sys
import time
import asyncio
from collections import defaultdict
from typing import Dict, List
import secrets
import threading

# ================= ENV DETECTION =================
IS_CLOUD = os.getenv("RENDER", "").lower() == "true"

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ================= INTERNAL IMPORTS =================
from python_backend.ai_engine import process_command
from python_backend.logger import log_info, log_error, log_warning
from python_backend.settings_manager import load_settings, get_owner_name
from python_backend.jarvis_personality import get_jarvis
from python_backend.automation_engine import (
    get_automation_engine,
    start_automation,
    get_automation_status
)
from python_backend.proactive_assistant import get_proactive_assistant
from python_backend.context_awareness import get_context_awareness
from python_backend.task_scheduler import get_task_scheduler

# ================= APP INIT =================
settings = load_settings()
log_info(f"VEDA AI starting for {get_owner_name()} | CLOUD={IS_CLOUD}")

app = FastAPI(title="VEDA AI", version="5.0.0")

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if IS_CLOUD else [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= RATE LIMITING =================
class RateLimiter:
    def __init__(self, max_requests=60, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        self.requests[client_id] = [
            t for t in self.requests[client_id] if t > window_start
        ]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True

api_rate = RateLimiter()
ws_rate = RateLimiter(30)

def get_client_id(request: Request = None, websocket: WebSocket = None):
    if request and request.client:
        return request.client.host
    if websocket and websocket.client:
        return websocket.client.host
    return "unknown"

# ================= AUTOMATION (LOCAL ONLY) =================
if not IS_CLOUD:
    try:
        start_automation()
        log_info("Automation engine started (local)")
    except Exception as e:
        log_error(f"Automation start failed: {e}")

# ================= WEBSOCKET =================
active_connections = []

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    client_id = get_client_id(websocket=ws)

    await ws.accept()
    active_connections.append(ws)

    jarvis = get_jarvis()
    await ws.send_json({"response": jarvis.get_greeting(), "type": "greeting"})

    try:
        while True:
            if not ws_rate.is_allowed(client_id):
                await ws.send_json({"error": "Rate limit exceeded"})
                await asyncio.sleep(1)
                continue

            command = await ws.receive_text()
            response = process_command(command)
            await ws.send_json({"command": command, "response": response})

    except WebSocketDisconnect:
        log_info(f"WS disconnected: {client_id}")
    except Exception as e:
        log_error(f"WS error: {e}")
    finally:
        if ws in active_connections:
            active_connections.remove(ws)

# ================= API =================
@app.get("/health")
def health(request: Request):
    client_id = get_client_id(request)
    jarvis = get_jarvis()
    return {
        "status": "healthy",
        "cloud": IS_CLOUD,
        "owner": jarvis.owner_name,
        "connections": len(active_connections),
    }

@app.get("/settings")
def settings_api():
    return load_settings()

# ================= VOICE (DISABLED ON CLOUD) =================
@app.get("/voice")
def voice_api():
    if IS_CLOUD:
        return {"status": "disabled", "reason": "Voice disabled on cloud"}

    from python_backend.voice_advanced import listen_command_advanced
    cmd = listen_command_advanced()
    return {"command": cmd, "response": process_command(cmd)}

# ================= AUTOMATION APIs =================
@app.get("/automation/status")
def automation_status():
    return get_automation_status()

@app.get("/automation/suggestions")
def automation_suggestions():
    assistant = get_proactive_assistant()
    return assistant.get_all_suggestions()

# ================= TASKS =================
@app.get("/tasks")
def tasks():
    scheduler = get_task_scheduler()
    return scheduler.get_all_tasks()

# ================= UI =================
@app.get("/")
async def index():
    return FileResponse("python_frontend/index.html")

@app.get("/{path:path}")
async def static_files(path: str):
    base = os.path.abspath("python_frontend")
    full = os.path.abspath(os.path.join(base, path))

    if not full.startswith(base):
        raise HTTPException(403)

    if os.path.exists(full):
        return FileResponse(full)

    raise HTTPException(404)

log_info("VEDA AI backend ready")
