import os
import time
import requests
from .base import TTSProvider
from ..config import TYPECAST_API_KEY, TYPECAST_VOICE_ID


class TypecastTTSProvider(TTSProvider):
    def __init__(self):
        if not TYPECAST_API_KEY:
            raise RuntimeError("TYPECAST_API_KEY가 비어있음")
        if not TYPECAST_VOICE_ID:
            raise RuntimeError("TYPECAST_VOICE_ID가 비어있음")

        self.api_key = TYPECAST_API_KEY
        self.voice_id = TYPECAST_VOICE_ID
        self.base_url = "https://api.typecast.ai"  # 예시

    def synth(self, text: str, out_path: str) -> str:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        job_id = self._create_job(text)
        audio_url = self._wait_for_audio(job_id)
        r = requests.get(audio_url, timeout=60)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(r.content)
        return out_path

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _create_job(self, text: str) -> str:
        url = f"{self.base_url}/v1/tts/jobs"  # 예시
        payload = {"voice_id": self.voice_id, "text": text, "format": "mp3"}
        r = requests.post(url, json=payload, headers=self._headers(), timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["job_id"]

    def _wait_for_audio(self, job_id: str) -> str:
        url = f"{self.base_url}/v1/tts/jobs/{job_id}"  # 예시
        for _ in range(60):
            r = requests.get(url, headers=self._headers(), timeout=30)
            r.raise_for_status()
            data = r.json()
            st = data.get("status")
            if st in ("done", "completed", "success"):
                return data["audio_url"]
            if st in ("failed", "error"):
                raise RuntimeError(f"Typecast TTS failed: {data}")
            time.sleep(1.0)
        raise TimeoutError("Typecast TTS timeout")
