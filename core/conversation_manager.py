from core.api_connector import send_message


class ConversationManager:
    def __init__(self, system_prompt=""):
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def get_context(self):
        return self.messages

    def chat(self, user_input):
        self.add_user_message(user_input)
        reply = send_message(self.get_context())
        self.add_assistant_message(reply)
        return reply
