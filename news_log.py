import json
import os

LOG_FILE = "sent_news.json"

def load_sent_links():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_sent_links(links):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(list(links), f, ensure_ascii=False, indent=2)