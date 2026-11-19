import os
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPENROUTER_API")

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemini-2.5-flash"
)

if not OPEN_ROUTER_API_KEY:
    raise ValueError("OpenRouter API key not found")

