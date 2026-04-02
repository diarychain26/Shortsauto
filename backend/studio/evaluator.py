from statistics import mean

FORBIDDEN = [
    "확실히",
    "무조건",
    "반드시 오른다",
    "반드시 떨어진다",
    "혐오",
    "욕설",
]


def _len_ok(line: str, max_chars: int = 22) -> bool:
    return len(line.strip()) <= max_chars


def evaluate(script: dict, channel: dict, template: dict) -> dict:
    scenes = script["scenes"]
    persona = channel.get("persona", "")

    violations = []
    for s in scenes:
        lines = s["on_screen_text"]
        if len(lines) != 3:
            violations.append(f"Scene{s['idx']}: 3줄 구조 위반")
        for ln in lines:
            if not _len_ok(ln):
                violations.append(f"Scene{s['idx']}: 줄 길이 초과 -> {ln}")
            for f in FORBIDDEN:
                if f in ln:
                    violations.append(f"Scene{s['idx']}: 금칙어 포함({f})")

        if "참고" not in lines[-1] and "주의" not in lines[-1]:
            violations.append(f"Scene{s['idx']}: 마지막 줄 CTA/주의 약함")

    Hook = 90 if ("시" in scenes[0]["on_screen_text"][0] or "시간" in scenes[0]["on_screen_text"][0]) else 82
    Flow = 88 if len(scenes) >= 5 else 75
    VisualFit = 92
    SubtitleReadability = 95 if len(violations) == 0 else max(60, 95 - len(violations) * 5)
    Pacing = 90
    CTA = 90 if ("참고" in scenes[-1]["on_screen_text"][-1] or "주의" in scenes[-1]["on_screen_text"][-1]) else 80
    Persona = 88 if persona else 80
    Originality = 60

    scores = {
        "Hook": Hook,
        "Flow": Flow,
        "VisualFit": VisualFit,
        "SubtitleReadability": SubtitleReadability,
        "Pacing": Pacing,
        "CTA": CTA,
        "Persona": Persona,
        "Originality": Originality,
    }

    avg = mean(scores.values())

    pass_fail = "PASS"
    reasons = []
    fixes = []

    if violations:
        pass_fail = "FAIL"
        reasons.append("룰 위반/가독성 문제 존재")
        fixes.extend(violations[:8])

    if avg < 85 or scores["Persona"] < 80:
        pass_fail = "FAIL"
        reasons.append("점수 기준 미달")
        fixes.append("Hook/Persona 강화: 첫 줄에 시간/긴급성/숫자 포함 + 말투 통일")

    return {
        "pass_fail": pass_fail,
        "scores": scores,
        "reasons": reasons,
        "fix_suggestions": fixes,
    }
