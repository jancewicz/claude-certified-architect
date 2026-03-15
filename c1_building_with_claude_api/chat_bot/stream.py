from anthropic import Anthropic

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.utils.utils import (
    add_user_message,
    chat,
    get_haiku_model,
)

if __name__ == "__main__":
    client: Anthropic = get_client()

    messages = []
    user_message = "Tell me a brief history of siamese neural network"
    add_user_message(messages=messages, text=user_message)

    with client.messages.stream(
        model=get_haiku_model(), max_tokens=500, messages=messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="")

    # Get final message together after stream finishes
    stream.get_final_message()
