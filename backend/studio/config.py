import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")

# IMAGE
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "pillow")  # pillow|gemini
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

# Gemini auth mode
# - api_key(Developer API): GEMINI_API_KEY or GOOGLE_API_KEY
# - oauth/adc(Vertex AI): GOOGLE_GENAI_USE_VERTEXAI=true + GOOGLE_CLOUD_PROJECT/LOCATION + ADC
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() in ("1", "true", "yes")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# TTS
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge")

TYPECAST_API_KEY = os.getenv("TYPECAST_API_KEY", "")
TYPECAST_VOICE_ID = os.getenv("TYPECAST_VOICE_ID", "")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
OUTPUT_DIR = os.path.join(STORAGE_DIR, "outputs")
RULES_DIR = os.path.join(STORAGE_DIR, "rules")
CHANNELS_DIR = os.path.join(STORAGE_DIR, "channels")
TEMPLATES_DIR = os.path.join(STORAGE_DIR, "templates")
