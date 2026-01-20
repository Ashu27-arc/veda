// =======================
// GLOBAL VARIABLES
// =======================
let ws;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
let isListening = false;
let cameraStream = null;

// =======================
// STARFIELD ANIMATION
// =======================
function initStarfield() {
    const canvas = document.getElementById('stars');
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Could not get canvas context');
        return;
    }

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const stars = [];
    const numStars = 200;

    // Create stars
    for (let i = 0; i < numStars; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2,
            opacity: Math.random(),
            twinkleSpeed: Math.random() * 0.02 + 0.01
        });
    }

    // Animate stars
    function animateStars() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        stars.forEach(star => {
            // Twinkle effect
            star.opacity += star.twinkleSpeed;
            if (star.opacity > 1 || star.opacity < 0) {
                star.twinkleSpeed = -star.twinkleSpeed;
            }

            // Draw star
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(0, 229, 255, ${star.opacity})`;
            ctx.shadowBlur = 10;
            ctx.shadowColor = 'rgba(0, 229, 255, 0.8)';
            ctx.fill();
        });

        requestAnimationFrame(animateStars);
    }

    animateStars();

    // Resize handler
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// Initialize starfield when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStarfield);
} else {
    initStarfield();
}

// =======================
// WEBSOCKET CONNECTION
// =======================
function connectWebSocket() {
    try {
        ws = new WebSocket("ws://localhost:8000/ws");

        ws.onopen = () => {
            console.log("✅ Connected to VEDA AI");
            const output = document.getElementById("output");
            if (output) {
                output.innerText = "✅ Connecting to VEDA...";
                output.style.color = "#00ff00";
            }
            reconnectAttempts = 0;
        };

        ws.onerror = (error) => {
            console.error("❌ WebSocket error:", error);
            const output = document.getElementById("output");
            if (output) {
                output.innerText = "❌ Connection error. Trying to reconnect...";
                output.style.color = "#ff4444";
            }
        };

        ws.onclose = () => {
            console.log("⚠️ Disconnected from VEDA AI");
            const output = document.getElementById("output");
            if (output) {
                output.innerText = "⚠️ Disconnected. Reconnecting...";
                output.style.color = "#ff9800";
            }

            // Try to reconnect
            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                setTimeout(connectWebSocket, 2000);
            } else {
                if (output) {
                    output.innerText = "❌ Connection lost. Please refresh the page or restart VEDA AI server.";
                    output.style.color = "#ff4444";
                }
            }
        };

        ws.onmessage = (event) => {
            const output = document.getElementById("output");
            if (!output) return;

            try {
                const data = JSON.parse(event.data);

                if (data.error) {
                    output.innerText = "❌ Error: " + data.error;
                    output.style.color = "#ff4444";
                } else if (data.type === "greeting") {
                    // Handle initial greeting from VEDA
                    output.innerText = "🤖 VEDA: " + data.response + "\n\n✅ Ready for commands!";
                    output.style.color = "#00e5ff";
                } else if (data.response) {
                    // Show command and response
                    if (data.command === "system_greeting") {
                        output.innerText = "🤖 VEDA: " + data.response;
                    } else {
                        output.innerText = "You: " + data.command + "\n\n🤖 VEDA: " + data.response;
                    }
                    output.style.color = "#00e5ff";
                } else {
                    output.innerText = event.data;
                    output.style.color = "#00e5ff";
                }
            } catch (e) {
                // Fallback for plain text messages
                output.innerText = event.data;
                output.style.color = "#00e5ff";
            }
        };
    } catch (error) {
        console.error("❌ Failed to create WebSocket:", error);
        const output = document.getElementById("output");
        if (output) {
            output.innerText = "❌ Failed to connect. Please ensure VEDA AI server is running.\n\nRun: python run_veda_ai.py";
            output.style.color = "#ff4444";
        }
    }
}

// Initialize WebSocket connection when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', connectWebSocket);
} else {
    connectWebSocket();
}

// =======================
// TEXT COMMAND
// =======================
function sendCommand() {
    const commandInput = document.getElementById("command");
    const output = document.getElementById("output");

    if (!commandInput || !output) return;

    const command = commandInput.value.trim();

    if (!command) {
        output.innerText = "⚠️ Please enter a command";
        output.style.color = "#ff9800";
        return;
    }

    if (command.length > 500) {
        output.innerText = "⚠️ Command too long (max 500 characters)";
        output.style.color = "#ff9800";
        return;
    }

    // Check if WebSocket is connected
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        output.innerText = "❌ Not connected. Reconnecting...";
        output.style.color = "#ff4444";
        connectWebSocket();
        return;
    }

    output.innerText = "⏳ Processing...";
    output.style.color = "#00e5ff";

    try {
        ws.send(command);
        commandInput.value = "";
    } catch (error) {
        console.error("❌ Send error:", error);
        output.innerText = "❌ Failed to send command. Please try again.";
        output.style.color = "#ff4444";
    }
}

// Allow Enter key to send command
document.addEventListener('DOMContentLoaded', () => {
    const commandInput = document.getElementById("command");
    if (commandInput) {
        commandInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                sendCommand();
            }
        });
    }
});

// =======================
// VOICE TRIGGER
// =======================
function startVoice() {
    const output = document.getElementById("output");
    const wave = document.getElementById("wave");
    const core = document.querySelector(".veda-core");
    const rightSection = document.querySelector(".right-section");

    if (!output) return;

    if (isListening) {
        output.innerText = "⚠️ Already listening...";
        output.style.color = "#ff9800";
        return;
    }

    isListening = true;
    output.innerText = "🎤 Listening... Speak now!";
    output.style.color = "#00e5ff";

    // Add visual feedback to both sides
    if (wave) wave.classList.add("speaking");
    if (core) core.classList.add("speaking");
    if (rightSection) rightSection.classList.add("speaking");

    fetch("http://localhost:8000/voice")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            isListening = false;
            if (wave) wave.classList.remove("speaking");
            if (core) core.classList.remove("speaking");
            if (rightSection) rightSection.classList.remove("speaking");

            if (data.status === "success" && data.response) {
                // Success - show command and response
                output.innerText = "You: " + data.command + "\n\n🤖 VEDA: " + data.response;
                output.style.color = "#00e5ff";
            } else if (data.status === "no_speech") {
                // No speech detected - simple message
                output.innerText = "⚠️ No speech detected. Please try again and speak clearly.";
                output.style.color = "#ff9800";
            } else if (data.error) {
                // Error occurred
                output.innerText = "❌ " + data.error;
                output.style.color = "#ff4444";
            } else {
                output.innerText = "⚠️ No response received";
                output.style.color = "#ff9800";
            }
        })
        .catch(error => {
            isListening = false;
            if (wave) wave.classList.remove("speaking");
            if (core) core.classList.remove("speaking");
            if (rightSection) rightSection.classList.remove("speaking");

            console.error("❌ Voice error:", error);
            output.innerText = "❌ Connection Error\n\nPlease ensure VEDA AI server is running.";
            output.style.color = "#ff4444";
        });
}

// =======================
// VOICE CALIBRATION
// =======================
function calibrateMic() {
    const output = document.getElementById("output");
    if (!output) return;

    output.innerText = "🎯 Starting voice calibration...\n\n" +
        "Please remain SILENT for 3 seconds.\n" +
        "This will help VEDA AI understand your environment better.";
    output.style.color = "#ff9800";

    fetch("http://localhost:8000/voice/calibrate")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            if (data.status === "success") {
                output.innerText = "✅ Calibration Successful!\n\n" +
                    data.message + "\n\n" +
                    "Your voice recognition is now optimized.\n" +
                    "Try speaking a command now!";
                output.style.color = "#00ff00";
            } else {
                output.innerText = "❌ Calibration Failed\n\n" + data.message;
                output.style.color = "#ff4444";
            }
        })
        .catch(error => {
            console.error("❌ Calibration error:", error);
            output.innerText = "❌ Calibration Error\n\n" +
                "Could not calibrate microphone.\n" +
                "Please ensure VEDA AI server is running.";
            output.style.color = "#ff4444";
        });
}

// =======================
// UTILITY FUNCTIONS
// =======================

// Check server health
function checkServerHealth() {
    fetch("http://localhost:8000/health")
        .then(res => res.json())
        .then(data => {
            console.log("✅ Server health:", data);
        })
        .catch(error => {
            console.error("❌ Server health check failed:", error);
        });
}

// Check health on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkServerHealth);
} else {
    checkServerHealth();
}

// Prevent page unload if listening
window.addEventListener('beforeunload', (e) => {
    if (isListening) {
        e.preventDefault();
        // Modern browsers ignore custom messages, just prevent default
        return '';
    }
});

console.log("🤖 VEDA AI Frontend Initialized");
console.log("Version: 2.0.0 (Cosmic Edition)");

// =======================
// AUTOMATION FUNCTIONS
// =======================

// Toggle automation panel
function toggleAutomationPanel() {
    const modal = document.getElementById('automation-modal');
    if (modal) {
        modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';
        if (modal.style.display === 'flex') {
            loadTasks();
            loadContext();
        }
    }
}

// Show specific tab
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Activate button
    event.target.classList.add('active');

    // Load data for the tab
    if (tabName === 'tasks') {
        loadTasks();
    } else if (tabName === 'context') {
        loadContext();
    } else if (tabName === 'shortcuts') {
        loadShortcuts();
    }
}

// Load suggestions
function loadSuggestions() {
    const panel = document.getElementById('suggestions-panel');
    const list = document.getElementById('suggestions-list');

    if (!panel || !list) return;

    panel.style.display = 'block';
    list.innerHTML = '<div class="loading">Loading suggestions...</div>';

    fetch('http://localhost:8000/automation/suggestions')
        .then(res => res.json())
        .then(data => {
            if (data.suggestions && data.suggestions.length > 0) {
                list.innerHTML = '';
                data.suggestions.forEach(suggestion => {
                    const item = document.createElement('div');
                    item.className = `suggestion-item priority-${suggestion.priority}`;
                    item.innerHTML = `
                        <div class="suggestion-icon">${getSuggestionIcon(suggestion.type)}</div>
                        <div class="suggestion-content">
                            <div class="suggestion-message">${suggestion.message}</div>
                            <button class="btn-execute-suggestion" onclick="executeSuggestion('${suggestion.action}')">
                                Execute
                            </button>
                        </div>
                    `;
                    list.appendChild(item);
                });
            } else {
                list.innerHTML = '<div class="no-suggestions">No suggestions at the moment. Everything looks good! ✅</div>';
            }
        })
        .catch(error => {
            console.error('Error loading suggestions:', error);
            list.innerHTML = '<div class="error">Failed to load suggestions</div>';
        });
}

// Get icon for suggestion type
function getSuggestionIcon(type) {
    const icons = {
        'warning': '⚠️',
        'info': 'ℹ️',
        'suggestion': '💡',
        'optimization': '⚡'
    };
    return icons[type] || '💡';
}

// Execute suggestion
function executeSuggestion(action) {
    const output = document.getElementById('output');
    if (output) {
        output.innerText = '⏳ Executing suggestion...';
    }

    fetch('http://localhost:8000/automation/execute-suggestion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: action
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success' && output) {
                output.innerText = '✅ ' + data.result;
                output.style.color = '#00ff00';
            }
            loadSuggestions(); // Refresh suggestions
        })
        .catch(error => {
            console.error('Error executing suggestion:', error);
            if (output) {
                output.innerText = '❌ Failed to execute suggestion';
                output.style.color = '#ff4444';
            }
        });
}

// Close suggestions panel
function closeSuggestions() {
    const panel = document.getElementById('suggestions-panel');
    if (panel) {
        panel.style.display = 'none';
    }
}

// Load scheduled tasks
function loadTasks() {
    const list = document.getElementById('tasks-list');
    if (!list) return;

    list.innerHTML = '<div class="loading">Loading tasks...</div>';

    fetch('http://localhost:8000/tasks')
        .then(res => res.json())
        .then(data => {
            if (data.tasks && data.tasks.length > 0) {
                list.innerHTML = '<h3>Scheduled Tasks</h3>';
                data.tasks.forEach(task => {
                    const item = document.createElement('div');
                    item.className = `task-item ${task.enabled ? 'enabled' : 'disabled'}`;
                    item.innerHTML = `
                        <div class="task-info">
                            <div class="task-name">${task.name}</div>
                            <div class="task-details">
                                ${task.command} | ${task.schedule_type}: ${task.schedule_value}
                            </div>
                            <div class="task-stats">
                                Runs: ${task.run_count} | Last: ${task.last_run ? new Date(task.last_run).toLocaleString() : 'Never'}
                            </div>
                        </div>
                        <div class="task-actions">
                            <button onclick="toggleTask(${task.id}, ${task.enabled})">${task.enabled ? 'Disable' : 'Enable'}</button>
                            <button onclick="deleteTask(${task.id})">Delete</button>
                        </div>
                    `;
                    list.appendChild(item);
                });
            } else {
                list.innerHTML = '<div class="no-tasks">No scheduled tasks yet. Add one above!</div>';
            }
        })
        .catch(error => {
            console.error('Error loading tasks:', error);
            list.innerHTML = '<div class="error">Failed to load tasks</div>';
        });
}

// Add scheduled task
function addScheduledTask() {
    const name = document.getElementById('task-name').value;
    const command = document.getElementById('task-command').value;
    const scheduleType = document.getElementById('task-schedule-type').value;
    const scheduleValue = document.getElementById('task-schedule-value').value;

    if (!name || !command || !scheduleValue) {
        alert('Please fill all fields');
        return;
    }

    fetch('http://localhost:8000/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                command: command,
                schedule_type: scheduleType,
                schedule_value: scheduleValue,
                enabled: true
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Task added successfully!');
                document.getElementById('task-name').value = '';
                document.getElementById('task-command').value = '';
                document.getElementById('task-schedule-value').value = '';
                loadTasks();
            }
        })
        .catch(error => {
            console.error('Error adding task:', error);
            alert('Failed to add task');
        });
}

// Toggle task enabled/disabled
function toggleTask(taskId, currentlyEnabled) {
    const action = currentlyEnabled ? 'disable' : 'enable';

    fetch(`http://localhost:8000/tasks/${taskId}/${action}`, {
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                loadTasks();
            }
        })
        .catch(error => {
            console.error('Error toggling task:', error);
        });
}

// Delete task
function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: 'DELETE'
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                loadTasks();
            }
        })
        .catch(error => {
            console.error('Error deleting task:', error);
        });
}

// Load context information
function loadContext() {
    const info = document.getElementById('context-info');
    if (!info) return;

    info.innerHTML = '<div class="loading">Loading context...</div>';

    fetch('http://localhost:8000/automation/context')
        .then(res => res.json())
        .then(data => {
            let html = '<h3>Current Context</h3>';

            if (data.current_context) {
                html += `
                    <div class="context-section">
                        <h4>Time Context</h4>
                        <p>Time of Day: ${data.current_context.time_of_day}</p>
                        <p>Day: ${data.current_context.day_of_week}</p>
                    </div>
                `;
            }

            if (data.prediction && data.prediction.likely_apps) {
                html += `
                    <div class="context-section">
                        <h4>Predicted Apps (based on usage patterns)</h4>
                        <ul>
                `;
                data.prediction.likely_apps.forEach(app => {
                    html += `<li>${app.app} (frequency: ${app.frequency})</li>`;
                });
                html += '</ul></div>';
            }

            if (data.frequent_tasks) {
                html += `
                    <div class="context-section">
                        <h4>Most Frequent Commands</h4>
                        <ul>
                `;
                data.frequent_tasks.forEach(task => {
                    html += `<li>${task.command} (${task.count} times)</li>`;
                });
                html += '</ul></div>';
            }

            info.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading context:', error);
            info.innerHTML = '<div class="error">Failed to load context</div>';
        });
}

// Create shortcut
function createShortcut() {
    const name = document.getElementById('shortcut-name').value;
    const command = document.getElementById('shortcut-command').value;

    if (!name || !command) {
        alert('Please fill all fields');
        return;
    }

    fetch('http://localhost:8000/automation/shortcut', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                command: command
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Shortcut created successfully!');
                document.getElementById('shortcut-name').value = '';
                document.getElementById('shortcut-command').value = '';
            }
        })
        .catch(error => {
            console.error('Error creating shortcut:', error);
            alert('Failed to create shortcut');
        });
}

// Load shortcuts
function loadShortcuts() {
    // Placeholder - implement if needed
    const list = document.getElementById('shortcuts-list');
    if (list) {
        list.innerHTML = '<div class="info">Shortcuts are saved and can be used in commands</div>';
    }
}

// Auto-load suggestions every 5 minutes
setInterval(() => {
    const panel = document.getElementById('suggestions-panel');
    if (panel && panel.style.display === 'block') {
        loadSuggestions();
    }
}, 300000); // 5 minutes

console.log("🤖 VEDA AI Automation Features Loaded");

// =======================
// CAMERA (WEB UI)
// =======================

async function toggleCamera() {
    const video = document.getElementById('camera');
    const output = document.getElementById('output');

    if (!video) {
        console.warn('Camera element not found');
        return;
    }

    // If already running → stop it
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        video.srcObject = null;
        if (output) {
            output.innerText = "📷 Camera stopped.";
            output.style.color = "#ff9800";
        }
        return;
    }

    // Start camera
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 640 }, height: { ideal: 480 } },
            audio: false
        });
        cameraStream = stream;
        video.srcObject = stream;
        if (output) {
            output.innerText = "📷 Camera started. Gesture control (backend) can also use your webcam.";
            output.style.color = "#00e5ff";
        }
    } catch (err) {
        console.error("Camera error:", err);
        if (output) {
            output.innerText = "❌ Could not access camera. Please allow camera permission in your browser.";
            output.style.color = "#ff4444";
        }
    }
}