from pathlib import Path

PROMPT_PATH = Path(__file__).parent / "system_prompt.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()