import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge")

TYPECAST_API_KEY = os.getenv("TYPECAST_API_KEY", "")
TYPECAST_VOICE_ID = os.getenv("TYPECAST_VOICE_ID", "")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
OUTPUT_DIR = os.path.join(STORAGE_DIR, "outputs")
RULES_DIR = os.path.join(STORAGE_DIR, "rules")
CHANNELS_DIR = os.path.join(STORAGE_DIR, "channels")
TEMPLATES_DIR = os.path.join(STORAGE_DIR, "templates")
