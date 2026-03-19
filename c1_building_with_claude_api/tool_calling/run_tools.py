import json

from anthropic.types import Message, ToolParam

from c1_building_with_claude_api.tool_calling.tools_and_schemas import (
    get_current_datetime,
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
    set_reminder,
    add_duration_to_datetime,
)


class ToolRunner:
    TOOL_USE: str = "tool_use"
    tools: list[ToolParam] = [
        get_current_datetime_schema,
        add_duration_to_datetime_schema,
        set_reminder_schema,
    ]

    @staticmethod
    def run_tool(tool_name: str, tool_input):
        match tool_name:
            case "get_current_datetime":
                return get_current_datetime(**tool_input)
            case "add_duration_to_datetime":
                return add_duration_to_datetime(**tool_input)
            case "set_reminder":
                return set_reminder(**tool_input)
        return None

    def run_tools(self, message: Message):
        tool_requests = [
            block for block in message.content if block.type == self.TOOL_USE
        ]
        tool_result_blocks = []

        for tool_request in tool_requests:
            try:
                tool_output = self.run_tool(tool_request.name, tool_request.input)
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_request.id,
                    "content": json.dumps(tool_output),
                    "is_error": False,
                }
            except Exception as e:
                tool_result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_request.id,
                    "content": f"Error: {e}",
                    "is_error": True,
                }
            tool_result_blocks.append(tool_result_block)
        return tool_result_blocks
