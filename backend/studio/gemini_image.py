import os
from typing import List

from google import genai

from .config import GEMINI_IMAGE_MODEL


def generate_card_with_gemini(*, topbar_title: str, lines: List[str], out_png: str, w: int = 1080, h: int = 1920) -> str:
    """Gemini(Nano Banana)로 카드 이미지를 직접 생성.

    - SDK: google-genai (Client는 환경변수 GEMINI_API_KEY를 자동 인식)
    - 모델 기본값: gemini-2.5-flash-image
    """

    os.makedirs(os.path.dirname(out_png), exist_ok=True)

    prompt = f"""
Create a clean vertical 9:16 card news image (exactly {w}x{h}).
Design rules:
- White background, minimal and modern.
- Top bar height about 120px, solid blue (#3d85f7). Center the title text '{topbar_title}' in white.
- Place three Korean text lines under the top bar, left aligned with generous margins.
- The three lines must match EXACTLY (keep Korean punctuation):
  1) {lines[0]}
  2) {lines[1]}
  3) {lines[2]}
- Use a bold headline style for line 1, and slightly smaller but readable font for line 2 and 3.
- Do NOT add extra text, watermarks, logos, or icons.
- Keep it readable like a YouTube Shorts alert card.
""".strip()

    client = genai.Client()  # picks up GEMINI_API_KEY env var
    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[prompt],
    )

    for part in getattr(response, "parts", []) or []:
        if getattr(part, "inline_data", None) is not None:
            img = part.as_image()
            img.save(out_png)
            return out_png

    for cand in getattr(response, "candidates", []) or []:
        content = getattr(cand, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            if getattr(part, "inline_data", None) is not None:
                img = part.as_image()
                img.save(out_png)
                return out_png

    raise RuntimeError("Gemini image generation returned no image data.")
