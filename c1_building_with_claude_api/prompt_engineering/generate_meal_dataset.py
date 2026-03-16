from anthropic import Anthropic
from pydantic import BaseModel

from c1_building_with_claude_api.get_client import get_client
from c1_building_with_claude_api.prompt_engineering.prompt_evaluator import (
    PromptEvaluator,
)
from c1_building_with_claude_api.utils.utils import get_haiku_model


class MealDatasetGenerationParams(BaseModel):
    task_description: str
    prompt_inputs_spec: dict[str, str]
    output_file: str
    num_cases: int


if __name__ == "__main__":
    client: Anthropic = get_client()
    model: str = get_haiku_model()
    evaluator = PromptEvaluator(client, model)

    meal_dataset_params = MealDatasetGenerationParams(
        task_description="Write concise 1 day meal plan for the athlete",
        prompt_inputs_spec={
            "height": "Athlete's height in cm",
            "weight": "Athlete's weight in kg",
            "goal": "Goal of the athlete",
            "restrictions": "Dietary restrictions of the athlete",
        },
        output_file="meal_dataset.json",
        num_cases=3,
    )

    dataset = evaluator.generate_dataset(
        task_description=meal_dataset_params.task_description,
        prompt_inputs_spec=meal_dataset_params.prompt_inputs_spec,
        output_file=meal_dataset_params.output_file,
        num_cases=meal_dataset_params.num_cases,
    )
