
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_to_russian(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Переведи на русский: {text}"}
        ]
    )
    return response.choices[0].message.content.strip()
