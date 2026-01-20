"""
Utility functions for VEDA AI
Includes security, validation, and helper functions
"""
import socket
import re
import html
from typing import Optional

def is_online(timeout: float = 2.0) -> bool:
    """Check if internet connection is available"""
    # Try multiple endpoints for reliability
    endpoints = [
        ("8.8.8.8", 53),      # Google DNS
        ("1.1.1.1", 53),      # Cloudflare DNS
        ("208.67.222.222", 53)  # OpenDNS
    ]
    
    for host, port in endpoints:
        try:
            socket.create_connection((host, port), timeout=timeout)
            return True
        except OSError:
            continue
    
    return False

def sanitize_input(text: Optional[str]) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove null bytes (can bypass some filters)
    text = text.replace('\x00', '')
    
    # Remove potentially dangerous shell characters
    dangerous_chars = [';', '&', '|', '`', '$', '<', '>', '\\', '\n', '\r', '\t', '\0']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Remove Unicode direction override characters (can be used to hide malicious content)
    text = re.sub(r'[\u202A-\u202E\u2066-\u2069\u200E\u200F]', '', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Limit length
    max_length = 500
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def sanitize_for_html(text: Optional[str]) -> str:
    """Sanitize text for safe HTML display"""
    if not text:
        return ""
    return html.escape(str(text))

def validate_command(command: Optional[str]) -> bool:
    """Validate command for security - prevents malicious commands"""
    if not command or not isinstance(command, str):
        return False
    
    # Check length
    if len(command) > 500:
        return False
    
    # Check minimum length (avoid empty/trivial commands)
    if len(command.strip()) < 1:
        return False
    
    command_lower = command.lower()
    
    # Check for malicious patterns - expanded list
    malicious_patterns = [
        # Unix/Linux dangerous commands
        'rm -rf', 'rm -fr', 'rm -r', 'rmdir',
        ':(){ :|:& };:', 'fork bomb',
        'dd if=', 'mkfs', 'fdisk',
        'chmod 777', 'chown', 'sudo',
        'wget ', 'curl http', 'curl -o',
        
        # Windows dangerous commands
        'del /f', 'del /s', 'del /q',
        'format c:', 'format d:', 'format e:',
        'rd /s', 'rmdir /s', 'deltree',
        'diskpart', 'bcdedit', 'sfc /scannow',
        
        # Code injection attempts
        'eval(', 'exec(', 'compile(',
        '__import__', '__builtins__',
        'os.system', 'os.popen', 'os.exec',
        'subprocess.call', 'subprocess.run', 'subprocess.popen',
        'system(', 'shell_exec', 'passthru',
        
        # PowerShell/CMD injection
        'powershell -enc', 'powershell -e ', 'powershell -w hidden',
        'cmd /c', 'cmd.exe /c', 'cmd /k',
        'wscript', 'cscript', 'mshta',
        
        # Registry manipulation
        'reg add', 'reg delete', 'regedit',
        
        # Network attacks
        'netcat', 'nc -e', 'ncat',
        'certutil -urlcache',
        'bitsadmin /transfer',
        
        # Base64 encoded commands (common evasion)
        'base64 -d', 'base64 --decode',
        
        # SQL injection patterns (if command is used in DB)
        "'; drop", '"; drop', "' or 1=1", '" or 1=1',
        'union select', 'union all select',
    ]
    
    for pattern in malicious_patterns:
        if pattern in command_lower:
            return False
    
    # Check for suspicious character combinations
    suspicious_patterns = [
        r'\$\(.*\)',  # Command substitution
        r'`.*`',      # Backtick command substitution
        r'\|.*\|',    # Pipe chains
        r'>\s*/dev/', # Redirect to device
        r'<\s*/dev/', # Read from device
        r'&&\s*&&',   # Multiple AND operators
        r'\|\|\s*\|\|', # Multiple OR operators
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, command_lower):
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
