import json
from statistics import mean

from anthropic import Anthropic

from c1_building_with_claude_api.utils.utils import (
    add_user_message,
    add_assistant_message,
    chat,
)


class ModelGrader:
    def __init__(self, client: Anthropic, model: str):
        self.client = client
        self.model = model

    def grade_by_model(self, test_case: dict[str, str], output: dict) -> dict:
        # Create evaluation prompt
        eval_prompt = f"""
        You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        Solution to Evaluate:
        <solution>
        {output}
        </solution>
        
        Criteria the task should fulfill:
        <criteria>
        {test_case["criteria"]}
        <criteria>

        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10

        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
            """

        messages = []
        add_user_message(messages, eval_prompt)
        add_assistant_message(messages, message="```json")
        eval_text = (
            chat(self.client, self.model, messages, stop_sequences=["```"])
            .content[0]
            .text
        )
        return json.loads(eval_text)

    @staticmethod
    def calc_mean_scores(eval_results) -> list[int]:
        return mean([result["score"] for result in eval_results])
