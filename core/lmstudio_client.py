import requests

class LMStudioClient:
    """
    Handles communication with a local LM Studio server (mockable).
    """

    def __init__(self, base_url="http://localhost:1234/v1/chat/completions"):
        self.base_url = base_url

    def send_message(self, messages, model="lmstudio-community/phi-3-mini-4k"):
        """
        Sends chat messages to LM Studio.
        Returns the assistant's reply as plain text.
        """
        try:
            payload = {"model": model, "messages": messages}
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except (requests.RequestException, KeyError, IndexError, ValueError):
            return None
