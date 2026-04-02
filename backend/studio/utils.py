import re
import subprocess
from shutil import which as _which


def run(cmd: list[str]):
    subprocess.check_call(cmd)


def safe_filename(s: str):
    s = re.sub(r"[^a-zA-Z0-9\-_\.]+", "_", s)
    return s[:80]


def which(exe: str) -> bool:
    return _which(exe) is not None
