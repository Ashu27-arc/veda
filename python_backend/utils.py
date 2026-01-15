"""
Utility functions for VEDA AI
Includes security, validation, and helper functions
"""
import socket

def is_online():
    """Check if internet connection is available"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = [';', '&', '|', '`', '$', '<', '>', '"', "'", '\\', '\n', '\r', '\t']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Limit length
    max_length = 500
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def validate_command(command):
    """Validate command for security - prevents malicious commands"""
    if not command or not isinstance(command, str):
        return False
    
    # Check length
    if len(command) > 500:
        return False
    
    # Check for malicious patterns
    malicious_patterns = [
        'rm -rf', 'del /f', 'format', 'mkfs',
        'dd if=', ':(){ :|:& };:', 'fork bomb',
        'sudo', 'chmod 777', 'wget', 'curl http',
        'powershell -enc', 'cmd /c', 'eval(',
        'exec(', '__import__', 'os.system', 'subprocess.call',
        'rmdir /s', 'deltree', 'fdisk'
    ]
    
    command_lower = command.lower()
    for pattern in malicious_patterns:
        if pattern in command_lower:
            return False
    
    return True

def truncate_text(text, max_length=500):
    """Truncate text to maximum length"""
    if not text:
        return ""
    
    if len(text) > max_length:
        return text[:max_length] + "..."
    
    return text

def format_response(text, max_length=1000):
    """Format response text for display"""
    if not text:
        return "No response"
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def is_valid_url(url):
    """Check if URL is valid and safe"""
    if not url or not isinstance(url, str):
        return False
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Block potentially dangerous URLs
    dangerous_domains = ['localhost', '127.0.0.1', '0.0.0.0', 'file://']
    for domain in dangerous_domains:
        if domain in url.lower():
            return False
    
    return True

def clean_filename(filename):
    """Clean filename to prevent path traversal"""
    if not filename:
        return ""
    
    # Remove path separators
    filename = filename.replace('/', '').replace('\\', '')
    
    # Remove dangerous characters
    dangerous_chars = ['..', '<', '>', ':', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    
    return filename.strip()
