from anthropic import Anthropic
from anthropic.types import MessageParam


def get_haiku_model() -> str:
    return "claude-haiku-4-5"


def add_user_message(messages: list[MessageParam], text: str) -> None:
    user_message: MessageParam = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages: list[MessageParam], text: str) -> None:
    assistant_message: MessageParam = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(
    client: Anthropic,
    model: str,
    messages: list[MessageParam],
    system_prompt: str | None = None,
    temperature: float = 0.0,
    stop_sequences: list[str] = [],
):
    chat_params = {
        "model": model,
        "max_tokens": 2000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if system_prompt:
        chat_params["system"] = system_prompt

    message = client.messages.create(**chat_params)
    return message.content[0].text
