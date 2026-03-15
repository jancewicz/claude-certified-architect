from anthropic import Anthropic

from c1_building_with_claude_api.chat_bot.chat_bot import ChatBot
from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.utils.utils import get_haiku_model

client: Anthropic = get_client()
model: str = get_haiku_model()


if __name__ == "__main__":
    chat_bot = ChatBot(client=client, model=model)
    chat_bot.run()
