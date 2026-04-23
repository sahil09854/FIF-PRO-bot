import logging
from keep_alive import keep_alive
from bot import start_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    keep_alive()  # Keeps Replit alive 24/7
    start_bot()
