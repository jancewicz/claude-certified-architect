import json

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.utils.utils import (
    get_haiku_model,
    add_user_message,
    chat,
    add_assistant_message,
    text_from_message,
)

if __name__ == "__main__":
    """
    The way to ensure json markdown formatting can be easily cut from response is to append ```json to assistant message
    so Claude can see that json markdown has already started. Then using triple backticks ``` as a stop sequence can
    ensure that LLM stops generating new tokens when this sequence happens.
    """

    client = get_client()
    model = get_haiku_model()

    messages = []
    text = "Generate a very short event bridge rule as json"
    add_user_message(messages, text)
    # Add ```json -> simulate start of JSON Markdown formatting
    add_assistant_message(messages, message="```json")
    # End when ``` occurs
    message = chat(client, model, messages, stop_sequences=["```"])
    chat_response = text_from_message(message)

    # Parse JSON
    formatted_json_response = json.loads(chat_response.strip())
