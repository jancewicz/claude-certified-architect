from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.tool_calling.tools_and_schemas import (
    get_current_datetime_schema,
    get_current_datetime,
)
from c1_building_with_claude_api.utils.utils import get_haiku_model, add_user_message

if __name__ == "__main__":
    client = get_client()
    model = get_haiku_model()

    messages = []
    add_user_message(messages, message="Can you get me current time?")

    chat_response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        tools=[get_current_datetime_schema],
    )

    messages.append({"role": "assistant", "content": chat_response.content})
    tool_user_block_response = chat_response.content[0].input
    result = get_current_datetime(**tool_user_block_response)

    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": chat_response.content[0].id,
                    "content": result,
                    "is_error": False,
                }
            ],
        }
    )

    print(
        client.messages.create(
            model=model,
            max_tokens=1000,
            messages=messages,
            tools=[get_current_datetime_schema],
        )
    )
