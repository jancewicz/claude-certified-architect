from anthropic import Anthropic
from anthropic.types import MessageParam

from c1_building_with_claude_api.tool_calling.run_tools import ToolRunner
from c1_building_with_claude_api.tool_calling.tools_and_schemas import (
    get_current_datetime,
)
from c1_building_with_claude_api.utils.utils import (
    chat,
    add_assistant_message,
    add_user_message,
    text_from_message,
)


def run_conversation(
    client: Anthropic, model: str, messages: list[MessageParam], tool_runner: ToolRunner
):
    while True:
        response = chat(client, model, messages, tools=tool_runner.tools)
        add_assistant_message(messages, response)
        print(text_from_message(message=response))

        if response.stop_reason != tool_runner.TOOL_USE:
            break

        tool_results = tool_runner.run_tools(response)
        add_user_message(messages, tool_results)

    return messages
