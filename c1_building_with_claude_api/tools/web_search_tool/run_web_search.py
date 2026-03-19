from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.tools.run_conversation import run_conversation
from c1_building_with_claude_api.tools.tool_runner import ToolRunner
from c1_building_with_claude_api.utils.utils import get_haiku_model, add_user_message

if __name__ == "__main__":
    client = get_client()
    model = get_haiku_model()
    tool_runner = ToolRunner()
    messages = []

    add_user_message(
        messages,
        message="""
    Can you search the web about the best exercise for gaining muscles?
    """,
    )
    run_conversation(client, model, messages, tool_runner)
