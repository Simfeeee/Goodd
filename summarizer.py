import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_and_analyze(text):
    prompt = f"Проанализируй и кратко резюмируй эту новость на русском: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — политический аналитик."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"].strip()

def get_emotional_reaction(text):
    prompt = f"Определи эмоциональный тон новости: {text}\nОтветь одним из: 😡 — напряжённо, 😐 — нейтрально, 🙂 — положительно. Напиши оценку и пояснение на русском."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — политический аналитик."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"].strip()