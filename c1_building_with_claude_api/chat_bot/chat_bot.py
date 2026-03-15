from anthropic import Anthropic

from c1_building_with_claude_api.utils.utils import (
    add_user_message,
    add_assistant_message,
    chat,
)


class ChatBot:
    def __init__(self, client: Anthropic, model: str):
        self.client: Anthropic = client
        self.model: str = model
        self.messages = []
        self.system_prompt: str | None = None

    def create_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def run(self):
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "exit":
                break

            add_user_message(messages=self.messages, text=user_input)
            chat_response = chat(
                client=self.client,
                model=self.model,
                messages=self.messages,
                system_prompt=self.system_prompt,
            )
            print(f"> {chat_response}")
            add_assistant_message(messages=self.messages, text=chat_response)
