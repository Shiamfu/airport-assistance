import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPENROUTER_API")

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

if not OPEN_ROUTER_API_KEY:
    raise ValueError("OpenRouter API key not found")

_DATA_FILE = Path.cwd() / "data" / "terminals.json"
DATA_PATH = _DATA_FILE if _DATA_FILE.is_file() else None

