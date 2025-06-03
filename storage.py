
import json
import os

STORAGE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"published": []}

def save_state(state):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def is_duplicate(news_id: str) -> bool:
    state = load_state()
    return news_id in state["published"]

def mark_as_published(news_id: str):
    state = load_state()
    if news_id not in state["published"]:
        state["published"].append(news_id)
        save_state(state)
