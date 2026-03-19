import json

from anthropic.types import Message, ToolParam

from c1_building_with_claude_api.tools.web_search_tool.web_search_schema import (
    get_web_search_schema,
)
from c1_building_with_claude_api.tools.text_editor_tool.text_edit_schema import (
    get_text_schema,
)
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
from c1_building_with_claude_api.utils.utils import get_haiku_model


class ToolRunner:
    TOOL_USE: str = "tool_use"

    def __init__(self):
        self.editor = TextEditorTool()
        self.model = get_haiku_model()
        self.tools: list[ToolParam] = [
            get_current_datetime_schema,
            add_duration_to_datetime_schema,
            set_reminder_schema,
            get_text_schema(self.model),
            get_web_search_schema(self.model),
        ]

    def run_tool(self, tool_name: str, tool_input):
        match tool_name:
            case "get_current_datetime":
                return get_current_datetime(**tool_input)
            case "add_duration_to_datetime":
                return add_duration_to_datetime(**tool_input)
            case "set_reminder":
                return set_reminder(**tool_input)
            case "str_replace_based_edit_tool":
                return self._run_editor_tool(tool_input)
            case "web_search":
                return get_web_search_schema(self.model)
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

    def _run_editor_tool(self, tool_input: dict) -> str:
        command = tool_input.get("command")
        path = tool_input.get("path", "")

        match command:
            case "view":
                return self.editor.view(path, tool_input.get("view_range"))
            case "str_replace":
                return self.editor.str_replace(
                    path, tool_input["old_str"], tool_input["new_str"]
                )
            case "create":
                return self.editor.create(path, tool_input["file_text"])
            case "insert":
                return self.editor.insert(
                    path, tool_input["insert_line"], tool_input["new_str"]
                )
            case _:
                raise ValueError(f"Unknown editor command: {command}")
