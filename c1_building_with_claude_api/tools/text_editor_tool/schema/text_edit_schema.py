def get_text_schema(model: str):
    if model.startswith("claude-haiku-4-5"):
        return {
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool",
            "max_characters": 5000,
        }
    else:
        raise ValueError(f"Error: can't fetch editor schema version for the {model}")
