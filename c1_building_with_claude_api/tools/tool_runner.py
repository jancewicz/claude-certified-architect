import json

from anthropic.types import Message, ToolParam

from c1_building_with_claude_api.tools.text_editor_tool.text_editor_tool import (
    TextEditorTool,
)
from c1_building_with_claude_api.tools.basic_tools_usage.tools_and_schemas import (
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
            case "str_replace_editor":
                return handle_text_editor_tool(**tool_input)
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


def handle_text_editor_tool(tool_input):
    text_editor_tool: TextEditorTool = TextEditorTool()

    command = tool_input["command"]
    if command == "view":
        return text_editor_tool.view(tool_input["path"], tool_input.get("view_range"))
    elif command == "str_replace":
        return text_editor_tool.str_replace(
            tool_input["path"], tool_input["old_str"], tool_input["new_str"]
        )
    elif command == "create":
        return text_editor_tool.create(tool_input["path"], tool_input["file_text"])
    elif command == "insert":
        return text_editor_tool.insert(
            tool_input["path"],
            tool_input["insert_line"],
            tool_input["new_str"],
        )
    elif command == "undo_edit":
        return text_editor_tool.undo_edit(tool_input["path"])
    else:
        raise Exception(f"Unknown text editor command: {command}")
