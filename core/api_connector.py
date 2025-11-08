import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="./data/config.env")

API_URL = os.getenv("API_URL")
MODEL = os.getenv("MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))


def send_message(messages):
    """Send chat messages to LM Studio and return assistant's reply."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        else:
            return "[Error] No valid response from model."

    except requests.exceptions.RequestException as e:
        return f"[Connection Error] {e}"
