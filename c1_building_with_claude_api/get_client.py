from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def get_client() -> Anthropic:
    return Anthropic()


