from anthropic import Anthropic

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.tool_calling.run_conversation import run_conversation
from c1_building_with_claude_api.tool_calling.run_tools import ToolRunner
from c1_building_with_claude_api.utils.utils import get_haiku_model, add_user_message

if __name__ == "__main__":
    client: Anthropic = get_client()
    model: str = get_haiku_model()
    tool_runner: ToolRunner = ToolRunner()

    messages = []
    add_user_message(
        messages,
        message="What is the current time in HH:MM format? Also, what is the current time in SS format?",
    )
    run_conversation(client, model, messages, tool_runner)
