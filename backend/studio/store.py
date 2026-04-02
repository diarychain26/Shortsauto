import os, json, time, uuid
from .config import OUTPUT_DIR, RULES_DIR, CHANNELS_DIR, TEMPLATES_DIR


def ensure_dirs():
    for d in [OUTPUT_DIR, RULES_DIR, CHANNELS_DIR, TEMPLATES_DIR]:
        os.makedirs(d, exist_ok=True)


def new_job_id():
    return time.strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:10]


def job_dir(job_id: str):
    return os.path.join(OUTPUT_DIR, job_id)


def write_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_channel(channel_id: str):
    path = os.path.join(CHANNELS_DIR, f"{channel_id}.json")
    if not os.path.exists(path):
        return {
            "id": channel_id,
            "name": "channel-a",
            "persona": "깔끔하고 단정한 뉴스 브리핑. 과장 금지. 숫자/시간 명확히.",
            "rules": [
                "카드뉴스는 3줄 구조를 유지: (1)이벤트 (2)영향 (3)행동/주의",
                "마지막 줄은 반드시 업무 참고/주의/CTA로 마무리",
                "한 줄 18자 내외, 너무 길면 줄바꿈",
                "정치 선동/혐오/욕설 금지, 과한 단정 금지",
            ],
        }
    return read_json(path)


def load_template(template_id: str):
    path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    if not os.path.exists(path):
        return {
            "id": template_id,
            "name": "card3",
            "resolution": [1080, 1920],
            "scene_seconds": 6.4,
            "scene_count": 7,
            "topbar_title": "아이반",
            "layout": "card3",
        }
    return read_json(path)


def ruleset_path(channel_id: str):
    return os.path.join(RULES_DIR, f"{channel_id}.md")


def load_rules_markdown(channel_id: str, fallback_rules: list[str]):
    p = ruleset_path(channel_id)
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write("# Rules\n")
            for r in fallback_rules:
                f.write(f"- {r}\n")
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def append_rule(channel_id: str, line: str):
    p = ruleset_path(channel_id)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"\n- {line.strip()}\n")
