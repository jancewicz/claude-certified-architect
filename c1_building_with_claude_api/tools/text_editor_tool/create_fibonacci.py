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
        Create directory fibonacci_agent and create fibonacci.py file. Next inside this file create a function called 
        fibonacci which will find n-th element of fibonacci sequence.
        Then in the same directory create test_fibonacci.py which will provide unit tests for that function. 
        """,
    )
    run_conversation(client, model, messages, tool_runner)
