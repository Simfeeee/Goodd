import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def translate_to_russian(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Переведи следующий текст на русский язык:"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message["content"].strip()