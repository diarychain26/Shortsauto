def generate_script(brief: dict, channel: dict, template: dict, rules_md: str) -> dict:
    """MVP: 룰 기반 자동 생성(LLM 연결 전에도 동작)"""
    scene_count = template.get("scene_count", 7)
    scene_sec = template.get("scene_seconds", 6.4)

    topic = brief["topic"].strip()
    bullets = brief.get("bullets", [])
    while len(bullets) < scene_count:
        bullets.append("핵심 포인트를 확인하세요.")

    persona = channel.get("persona", "")

    scenes = []
    for i in range(scene_count):
        b = bullets[i] if i < len(bullets) else ""
        line1 = topic if i == 0 else f"{topic} (요약 {i+1})"
        line2 = b
        line3 = "업무 간 참고 바랍니다!"
        narration = f"{line1}. {line2}. {line3}"
        scenes.append(
            {
                "idx": i + 1,
                "duration_sec": scene_sec,
                "on_screen_text": [line1, line2, line3],
                "narration": narration,
            }
        )

    full_text = "\n".join([s["narration"] for s in scenes])
    return {
        "full_text": full_text,
        "scenes": scenes,
        "meta": {
            "persona": persona,
            "rules": rules_md,
            "target_seconds": brief.get("target_seconds", 45),
            "estimated_seconds": scene_count * scene_sec,
        },
    }
