import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

from .config import IMAGE_PROVIDER
from .gemini_image import generate_card_with_gemini


def make_card_image(lines: list[str], out_png: str, topbar_title: str = "아이반", w: int = 1080, h: int = 1920):
    """카드 이미지 생성.

    - IMAGE_PROVIDER=pillow: Pillow로 레이아웃 고정
    - IMAGE_PROVIDER=gemini: Gemini(Nano Banana)로 카드 이미지 자체를 생성
    """

    if IMAGE_PROVIDER.lower() == "gemini":
        safe_lines = (lines + [""] * 3)[:3]
        return generate_card_with_gemini(topbar_title=topbar_title, lines=safe_lines, out_png=out_png, w=w, h=h)

    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)

    def font(size: int):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", size)
        except Exception:
            try:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
            except Exception:
                return ImageFont.load_default()

    bar_h = 120
    d.rectangle([0, 0, w, bar_h], fill=(61, 133, 247))
    d.text((w // 2, bar_h // 2), topbar_title, fill="white", font=font(44), anchor="mm")

    y = 200
    d.text((60, y), lines[0], fill="black", font=font(60))
    y += 140

    for line in lines[1:]:
        wrapped = textwrap.wrap(line, width=18)
        for wl in wrapped:
            d.text((60, y), wl, fill="black", font=font(52))
            y += 72
        y += 20

    box_w, box_h = 880, 520
    x0 = (w - box_w) // 2
    y0 = h - box_h - 220
    d.rectangle([x0, y0, x0 + box_w, y0 + box_h], outline=(200, 200, 200), width=6)

    img.save(out_png)
    return out_png
