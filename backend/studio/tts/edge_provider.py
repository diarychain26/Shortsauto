import os
import subprocess
from .base import TTSProvider


class EdgeTTSProvider(TTSProvider):
    def __init__(self, voice: str = "ko-KR-SunHiNeural"):
        self.voice = voice

    def synth(self, text: str, out_path: str) -> str:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        cmd = ["edge-tts", "--voice", self.voice, "--text", text, "--write-media", out_path]
        subprocess.check_call(cmd)
        return out_path
