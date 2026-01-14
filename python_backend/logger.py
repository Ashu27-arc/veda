import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/veda_ai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('VEDA_AI')

def log_info(message):
    try:
        logger.info(message)
    except UnicodeEncodeError:
        # Fallback for console output issues
        logger.info(message.encode('utf-8', errors='ignore').decode('utf-8'))

def log_error(message):
    try:
        logger.error(message)
    except UnicodeEncodeError:
        logger.error(message.encode('utf-8', errors='ignore').decode('utf-8'))

def log_warning(message):
    try:
        logger.warning(message)
    except UnicodeEncodeError:
        logger.warning(message.encode('utf-8', errors='ignore').decode('utf-8'))
