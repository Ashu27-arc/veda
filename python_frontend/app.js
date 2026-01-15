// =======================
// GLOBAL VARIABLES
// =======================
let ws;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
let isListening = false;

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

    if (!output) return;

    if (isListening) {
        output.innerText = "⚠️ Already listening...";
        output.style.color = "#ff9800";
        return;
    }

    isListening = true;
    output.innerText = "🎤 Listening... Speak now!";
    output.style.color = "#00e5ff";

    // Add visual feedback
    if (wave) wave.classList.add("speaking");
    if (core) core.classList.add("speaking");

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