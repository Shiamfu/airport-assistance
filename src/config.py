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

DATA_PATH: Path = Path("data/terminals.json")

