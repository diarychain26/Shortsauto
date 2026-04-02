import os
from .utils import run, which


def render_scene(image_png: str, audio_path: str, out_mp4: str):
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    if not which("ffmpeg"):
        raise RuntimeError("ffmpeg가 설치되어 있어야 합니다.")

    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        image_png,
        "-i",
        audio_path,
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        out_mp4,
    ]
    run(cmd)
    return out_mp4


def concat_scenes(scene_mp4s: list[str], out_mp4: str):
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    list_txt = os.path.join(os.path.dirname(out_mp4), "concat.txt")
    with open(list_txt, "w", encoding="utf-8") as f:
        for p in scene_mp4s:
            f.write(f"file '{p.replace("'", "\\'")}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_txt, "-c", "copy", out_mp4]
    run(cmd)
    return out_mp4
