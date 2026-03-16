from anthropic import Anthropic

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.prompt_engineering.prompt_evaluator import (
    PromptEvaluator,
)
from c1_building_with_claude_api.utils.utils import (
    get_haiku_model,
    add_user_message,
    chat,
)


def run_prompt(prompt_inputs: dict):
    client: Anthropic = get_client()
    model: str = get_haiku_model()

    prompt = f"""
    Generate one-day meal plan for an athletes that meets their goal and dietary restrictions.
    
    - Height: {prompt_inputs["height"]}
    - Weight: {prompt_inputs["weight"]}
    - Goal: {prompt_inputs["goal"]}
    - Dietary restrictions: {prompt_inputs["restrictions"]}
    """

    messages = []
    add_user_message(messages, prompt)
    return chat(client, model, messages)


if __name__ == "__main__":
    client: Anthropic = get_client()
    model: str = get_haiku_model()
    evaluator: PromptEvaluator = PromptEvaluator(client, model)
    dataset_path: str = "meal_dataset.json"

    evaluator_extra_criteria: str = """
    Make sure that output should include:
    * daily caloric total, 
    * macro nutrients breakdown, 
    * meals with exact food, portions and timing
    """

    results: list = evaluator.run_evaluation(
        run_prompt, dataset_file=dataset_path, extra_criteria=evaluator_extra_criteria
    )
