
import requests
import os
from dotenv import load_dotenv
from langdetect import detect

load_dotenv()

token = os.getenv("SECRET")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

question_input = input("Įveskite savo klausimą: ")

# Patikrinimas ar klausimas lietuviškai
def is_lithuanian(text):
    try:
        lang = detect(text)
        return lang == "lt"
    except:
        return False

if is_lithuanian(question_input):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Atsakinėk tik lietuviškai."},
            {"role": "user", "content": question_input}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print("\nAI atsakymas:")
        print(result["choices"][0]["message"]["content"])
    else:
        print("Klaida:", response.text)
else:
    print("Atsiprašome, bet atsakome tik į lietuviškus klausimus.")
    