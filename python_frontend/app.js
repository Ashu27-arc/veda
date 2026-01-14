// =======================
// GLOBAL VARIABLES
// =======================
let ws;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
let isListening = false;

// Get DOM elements
const wave = document.getElementById("wave");
const core = document.querySelector(".veda-core");
const output = document.getElementById("output");
const commandInput = document.getElementById("command");

// =======================
// WEBSOCKET CONNECTION
// =======================
function connectWebSocket() {
    try {
        ws = new WebSocket("ws://localhost:8000/ws");

        ws.onopen = () => {
            console.log("✅ Connected to VEDA AI");
            output.innerText = "✅ Connecting to VEDA...";
            output.style.color = "#00ff00";
            reconnectAttempts = 0;
        };

        ws.onerror = (error) => {
            console.error("❌ WebSocket error:", error);
            output.innerText = "❌ Connection error. Trying to reconnect...";
            output.style.color = "#ff4444";
        };

        ws.onclose = () => {
            console.log("⚠️ Disconnected from VEDA AI");
            output.innerText = "⚠️ Disconnected. Reconnecting...";
            output.style.color = "#ff9800";

            // Try to reconnect
            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                setTimeout(connectWebSocket, 2000);
            } else {
                output.innerText = "❌ Connection lost. Please refresh the page or restart VEDA AI server.";
                output.style.color = "#ff4444";
            }
        };

        ws.onmessage = (event) => {
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
        output.innerText = "❌ Failed to connect. Please ensure VEDA AI server is running.\n\nRun: python run_veda_ai.py";
        output.style.color = "#ff4444";
    }
}

// Initialize WebSocket connection
connectWebSocket();

// =======================
// TEXT COMMAND
// =======================
function sendCommand() {
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
commandInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendCommand();
    }
});

// =======================
// VOICE TRIGGER
// =======================
function startVoice() {
    if (isListening) {
        output.innerText = "⚠️ Already listening...";
        output.style.color = "#ff9800";
        return;
    }

    isListening = true;
    output.innerText = "🎤 Initializing microphone...\n\nPlease allow microphone access if prompted.\nThen speak clearly when you see 'Listening...'";
    output.style.color = "#00e5ff";

    // Add visual feedback
    wave.classList.add("speaking");
    core.classList.add("speaking");

    fetch("http://localhost:8000/voice")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            isListening = false;
            wave.classList.remove("speaking");
            core.classList.remove("speaking");

            if (data.error) {
                output.innerText = "❌ Voice Recognition Error\n\n" + data.error;
                output.style.color = "#ff4444";

                // Show troubleshooting tips after a delay
                setTimeout(() => {
                    output.innerText += "\n\n💡 Troubleshooting:\n" +
                        "• Click '🎯 Calibrate Voice' button\n" +
                        "• Check microphone in Windows Settings\n" +
                        "• Ensure internet connection is active\n" +
                        "• Try speaking louder and clearer\n" +
                        "• Reduce background noise";
                }, 1000);
            } else if (data.response) {
                output.innerText = "You: " + data.command + "\n\n🤖 VEDA: " + data.response;
                output.style.color = "#00e5ff";
            } else {
                output.innerText = "⚠️ No response received";
                output.style.color = "#ff9800";
            }
        })
        .catch(error => {
            isListening = false;
            wave.classList.remove("speaking");
            core.classList.remove("speaking");

            console.error("❌ Voice error:", error);
            output.innerText = "❌ Connection Error\n\n" +
                "Could not connect to voice recognition service.\n\n" +
                "Please ensure:\n" +
                "• VEDA AI server is running (python run_veda_ai.py)\n" +
                "• Internet connection is active\n" +
                "• Microphone is connected and working";
            output.style.color = "#ff4444";
        });
}

// =======================
// VOICE CALIBRATION
// =======================
function calibrateMic() {
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
// SOUND REACTIVE SYSTEM (DISABLED TO PREVENT BLINKING)
// =======================
// Audio visualization removed to prevent constant blinking
// Visual feedback is now only shown during active voice commands

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
checkServerHealth();

// Prevent page unload if listening
window.addEventListener('beforeunload', (e) => {
    if (isListening) {
        e.preventDefault();
        e.returnValue = '';
    }
});

console.log("🤖 VEDA AI Frontend Initialized");
console.log("Version: 2.0.0 (JARVIS Personality Edition)");