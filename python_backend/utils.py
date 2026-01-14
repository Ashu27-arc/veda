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
    dangerous_chars = [';', '&', '|', '`', '$', '\n', '\r']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def truncate_text(text, max_length=500):
    """Truncate text to maximum length"""
    if not text:
        return ""
    
    if len(text) > max_length:
        return text[:max_length] + "..."
    
    return text
