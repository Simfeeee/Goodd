def get_topic_emojis(text):
    text = text.lower()
    emojis = []
    if "украина" in text or "ukraine" in text:
        emojis.append("🇺🇦")
    if "сша" in text or "usa" in text or "байден" in text or "biden" in text:
        emojis.append("🇺🇸")
    if "россия" in text or "russia" in text or "путин" in text:
        emojis.append("🇷🇺")
    if "китай" in text or "china" in text or "си цзиньпин" in text:
        emojis.append("🇨🇳")
    if "выборы" in text or "election" in text:
        emojis.append("🗳")
    if "экономик" in text or "economy" in text:
        emojis.append("💰")
    if "война" in text or "war" in text or "конфликт" in text:
        emojis.append("⚔️")
    if "санкции" in text or "санкция" in text:
        emojis.append("🚫")
    if "переговоры" in text or "мир" in text:
        emojis.append("🤝")
    return " ".join(emojis) if emojis else "🌍"