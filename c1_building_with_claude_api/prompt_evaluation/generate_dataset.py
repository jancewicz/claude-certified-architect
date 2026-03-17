import json

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.utils.utils import (
    add_user_message,
    add_assistant_message,
    chat,
    get_haiku_model,
    text_from_message,
)


def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts 
that generate Python, JSON, or Regex specifically for AWS-related tasks. 
Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
    "format": "python", "regex" or "json",
    "criteria": "Explain what critical criteria should the task fulfill"
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, message="```json")
    message = chat(
        client=get_client(),
        model=get_haiku_model(),
        messages=messages,
        stop_sequences=["```"],
    )
    text = text_from_message(message)
    return json.loads(text.strip())


if __name__ == "__main__":
    dataset = generate_dataset()

    with open("test_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
