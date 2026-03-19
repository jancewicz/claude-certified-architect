def get_web_search_schema(model: str):
    if model.startswith("claude-haiku-4-5"):
        return {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5,
            "allowed_domains": ["nih.gov"],
        }
    else:
        raise ValueError(
            f"Error: can't fetch web search schema version for the {model}"
        )
