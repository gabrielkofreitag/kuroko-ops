import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Model Profiles
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "anthropic/claude-3.5-sonnet")
SMART_MODEL = os.getenv("SMART_MODEL", "anthropic/claude-3.5-sonnet")
CHEAP_MODEL = os.getenv("CHEAP_MODEL", "google/gemini-2.0-flash-001")
CODING_MODEL = os.getenv("CODING_MODEL", "anthropic/claude-3.5-sonnet")

# Global Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DOCKER_WORKSPACE = os.getenv("DOCKER_WORKSPACE", "/workspace")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/kuroko.db")

# Debug Mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
DEBUG_LEVEL = int(os.getenv("DEBUG_LEVEL", "1"))
