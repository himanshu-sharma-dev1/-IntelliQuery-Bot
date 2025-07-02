import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
COMMAND_PREFIX = "!"

# File paths
FAQ_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FAQ.md"))

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "discord_bot.log"

# API Keys
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
