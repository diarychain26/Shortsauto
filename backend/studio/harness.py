import os
from .store import ensure_dirs, new_job_id, job_dir, write_json, read_json
from .store import load_channel, load_template, load_rules_markdown, append_rule
from .generator import generate_script
from .evaluator import evaluate
from .assets import make_card_image
from .renderer import render_scene, concat_scenes
from .tts import get_tts_provider


async def run_job(brief: dict):
    ensure_dirs()
    job_id = new_job_id()
    jdir = job_dir(job_id)
    os.makedirs(jdir, exist_ok=True)

    log = []
    channel = load_channel(brief["channel_id"])
    template = load_template(brief["template_id"])
    rules_md = load_rules_markdown(channel["id"], channel.get("rules", []))

    script = generate_script(brief, channel, template, rules_md)
    write_json(os.path.join(jdir, "script.json"), script)
    log.append("스크립트/씬 자동 생성 완료")

    ev = evaluate(script, channel, template)
    write_json(os.path.join(jdir, "eval_text.json"), ev)
    log.append(f"텍스트 QA: {ev['pass_fail']}")

    if ev["pass_fail"] != "PASS":
        return {"job_id": job_id, "status": "FAILED_TEXT_QA", "output_mp4": None, "eval": ev, "log": log}

    tts = get_tts_provider()
    scene_mp4s = []
    for s in script["scenes"]:
        idx = s["idx"]
        img_path = os.path.join(jdir, f"scene_{idx:02d}.png")
        aud_path = os.path.join(jdir, f"scene_{idx:02d}.mp3")
        mp4_path = os.path.join(jdir, f"scene_{idx:02d}.mp4")

        make_card_image(s["on_screen_text"], img_path, topbar_title=template.get("topbar_title", "아이반"))
        tts.synth(s["narration"], aud_path)
        render_scene(img_path, aud_path, mp4_path)
        scene_mp4s.append(mp4_path)
        log.append(f"Scene {idx} 렌더 완료")

    final_mp4 = os.path.join(jdir, "final.mp4")
    concat_scenes(scene_mp4s, final_mp4)
    log.append("최종 영상 생성 완료")

    write_json(os.path.join(jdir, "eval_final.json"), ev)

    return {"job_id": job_id, "status": "DONE", "output_mp4": final_mp4, "eval": ev, "log": log}


def submit_feedback(job_id: str, fb: dict):
    jdir = job_dir(job_id)
    path = os.path.join(jdir, "feedback.json")
    prev = read_json(path, default=[])
    prev.append(fb)
    write_json(path, prev)

    if fb.get("verdict") == "bad":
        comment = fb.get("comment", "").strip()
        if comment:
            append_rule("channel-a", f"[피드백] {comment}")

    return {"ok": True, "job_id": job_id, "saved": True}
