from ..config import TTS_PROVIDER
from .edge_provider import EdgeTTSProvider
from .typecast_provider import TypecastTTSProvider


def get_tts_provider():
    if TTS_PROVIDER == "typecast":
        return TypecastTTSProvider()
    return EdgeTTSProvider()
