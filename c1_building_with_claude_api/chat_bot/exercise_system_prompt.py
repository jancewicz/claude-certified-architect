from anthropic import Anthropic

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.utils.utils import (
    chat,
    add_user_message,
    text_from_message,
)

# Create as concise response from LLM as it can get. Ask for python function that checks duplicates chars in str
if __name__ == "__main__":
    client: Anthropic = get_client()
    model: str = "claude-haiku-4-5"

    system_prompt = """
    You are coding assistant who's biggest advantage is giving very precise and short answers without deep diving into
    much details. When being asked about coding solution just return the code.
    """

    messages = []
    user_prompt = (
        "Create a python function that checks if there is a duplicate char in string"
    )
    add_user_message(messages, message=user_prompt)
    chat_response = chat(client, model, messages, system_prompt)
